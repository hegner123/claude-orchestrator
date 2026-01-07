# UDA ↔ ApiSafeConverter Relationship - LLM Quick Reference

## Core Relationship (80/20 Rule)

```
CRITICAL CONCEPT: Automatic Fallback Mechanism

├─ 80% of properties → Automatic passthrough (NO converter needed)
├─ 20% of properties → Custom converter (complex transformations)
└─ BINDING: EditorAlias field connects UDA ↔ Converter

LAYERS:
UDA Files (Schema Layer)          →    Define WHAT exists + HOW configured
ApiSafeConverters (Runtime Layer)  →    Define HOW data transforms
EditorAlias (Binding)             →    Connects the two layers
```

## Automatic Passthrough Lookup (NO Converter Needed)

```
EDITORALIAS                       VALUE TYPE    JSON OUTPUT            NEEDS CONVERTER
==================================================================================================
Umbraco.TextBox                   string        "text value"           ❌ NO - Direct passthrough
Umbraco.TextArea                  string        "multi-line\ntext"     ❌ NO - Direct passthrough
Umbraco.Integer                   int           42                     ❌ NO - Direct passthrough
Umbraco.Decimal                   decimal       99.99                  ❌ NO - Direct passthrough
Umbraco.TrueFalse                 bool          true/false             ❌ NO - Direct passthrough
Umbraco.DateTime                  DateTime      "2024-01-15T10:30:00Z" ❌ NO - Auto ISO serialize
Umbraco.DropDown.Flexible         string        "Selected Value"       ❌ NO - Direct passthrough
Umbraco.RadioButtonList           string        "Selected Option"      ❌ NO - Direct passthrough
Umbraco.CheckBoxList              string[]      ["Opt1", "Opt2"]       ❌ NO - Direct passthrough
Umbraco.Slider                    decimal       50.5                   ❌ NO - Direct passthrough
Umbraco.Label                     string        "label text"           ❌ NO - Direct passthrough
Umbraco.ColorPicker               string        "#FF0000"              ❌ NO - Direct passthrough

COVERAGE: ~80% of all property editors use automatic passthrough
```

## Custom Converter Required Lookup

```
EDITORALIAS                       RAW TYPE                  CONVERTER                        OUTPUT TYPE             WHY NEEDED
======================================================================================================================================
Umbraco.MediaPicker3              MediaWithCrops            MediaApiSafeConverter            ApiSafeImage            Crop extraction, URL resolution
Umbraco.ContentPicker             IPublishedContent         PublishedContentApiSafeConverter JsonPublishedContent    Reference resolution
Umbraco.MultiNodeTreePicker       IEnumerable<IPC>          PublishedContentApiSafeConverter JsonPublishedContent[]  Reference resolution
Umbraco.BlockGrid                 BlockGridModel            BlockGridApiSafeConverter        BlockModel[]            Recursive processing
Umbraco.BlockList                 BlockListModel            BlockListApiSafeConverter        BlockModel[]            Recursive processing
Umbraco.TinyMCE                   string (HTML)             RichContentApiSafeConverter      string (sanitized)      Optional HTML processing
UmbracoForms.FormPicker           Form                      UmbracoFormApiSafeConverter      ApiSafeForm             Form structure extraction
Custom Data Types                 Various                   Custom converters                Custom models           Business logic

COVERAGE: ~20% of property editors need custom converters
```

## Decision Tree: Does This Property Need a Converter?

```
QUERY: Does this EditorAlias need a custom converter?

├─ Is it a simple value type?
│  ├─ string, number, boolean, DateTime → NO ✅ (automatic passthrough)
│  └─ Complex object (Media, Content, Block) → Continue evaluation
│
├─ Does it return Umbraco-specific objects?
│  ├─ IPublishedContent, MediaWithCrops, BlockModel → YES ❌ (needs converter)
│  └─ Simple serializable values → NO ✅ (automatic passthrough)
│
├─ Does it need reference resolution?
│  ├─ Contains UDIs → YES ❌ (needs converter)
│  └─ Direct values → NO ✅ (automatic passthrough)
│
├─ Does it have nested structures?
│  ├─ Blocks, areas, recursive content → YES ❌ (needs converter)
│  └─ Flat values → NO ✅ (automatic passthrough)
│
└─ Does it need business logic?
   ├─ Calculations, aggregations, formatting → YES ❌ (needs custom converter)
   └─ Raw value is usable → NO ✅ (automatic passthrough)

DEFAULT: When in doubt → NO converter needed (system will use passthrough)
```

## The Binding: EditorAlias

```
UDA LAYER (Schema)                              RUNTIME LAYER (Converter)
================================                =====================================
{                                               public class MediaApiSafeConverter
  "EditorAlias": "Umbraco.MediaPicker3",   →   {
  "Configuration": {                                public override string[] EditorAlias => new[] {
    "crops": [...]                                      "Umbraco.MediaPicker3"  ← MUST MATCH
  }                                                 };
}                                                 }

CONNECTION MECHANISM:
1. System loops through properties
2. For each property, checks EditorAlias
3. Searches converter collection for matching EditorAlias
4. IF FOUND → Call ConvertToApiSafeValue()
5. IF NOT FOUND → Use automatic passthrough
```

## Fallback Mechanism (Code Pattern)

```csharp
PATTERN: Automatic Passthrough Logic

foreach (var prop in content.Properties) {
    // STEP 1: Try to find matching converter
    var converter = _apiSafeConverters.Value.FirstOrDefault(x => x.IsEditor(prop));

    // STEP 2: Get property value
    var val = content.Value(fallback, prop.Alias);

    // STEP 3: FALLBACK DECISION
    if (converter == null) {
        // NO CONVERTER FOUND → Automatic passthrough
        newVal.Add(prop.Alias, val == null ? null : val);
    }
    else {
        // CONVERTER FOUND → Transform value
        var value = converter.ConvertToApiSafeValue(val, culture, segment, ids, additionalData);
        newVal.Add(prop.Alias, value == null ? null : value);
    }
}

RESULT: ~80% of properties follow null-check branch (no converter)
```

## Practical Example: Mixed Property Types

```
SCENARIO: Product page with 5 properties

UDA SCHEMA:
├─ productName (Umbraco.TextBox)
├─ price (Umbraco.Decimal)
├─ inStock (Umbraco.TrueFalse)
├─ productImage (Umbraco.MediaPicker3)
└─ category (Umbraco.DropDown.Flexible)

PROCESSING:
┌────────────────┬─────────────┬────────────────────┬────────────────────┐
│ PROPERTY       │ CONVERTER   │ ACTION             │ OUTPUT             │
├────────────────┼─────────────┼────────────────────┼────────────────────┤
│ productName    │ Not found   │ Passthrough        │ "Widget Pro 3000"  │
│ price          │ Not found   │ Passthrough        │ 299.99             │
│ inStock        │ Not found   │ Passthrough        │ true               │
│ productImage   │ ✅ FOUND    │ Convert            │ ApiSafeImage {...} │
│ category       │ Not found   │ Passthrough        │ "Electronics"      │
└────────────────┴─────────────┴────────────────────┴────────────────────┘

RESULT: 4/5 properties (80%) used automatic passthrough
        1/5 properties (20%) used custom converter
```

## Converter Types Matrix

```
CONVERTER TYPE                      MATCHES VIA          EXAMPLE                      USE CASE
=====================================================================================================
Property Editor Converter           EditorAlias          MediaApiSafeConverter        Standard Umbraco editors
                                                         Matches: "Umbraco.MediaPicker3"

Content Type Converter              ContentTypes         FeedBoatsApiSafeConverter    Custom document types
                                                         Matches: "contentType.feedBoats"

Element Type Converter              ContentTypes         BannerStandardApiSafeConverter Block Grid/List elements
(BaseContentTypeApiSafeConverter)                        Matches: "contentType.bannerStandard"
```

## Configuration Influence

```
UDA CONFIGURATION AFFECTS CONVERTER OUTPUT:

UDA LAYER:                                      RUNTIME DATA AVAILABLE:
{                                               content.LocalCrops.Crops = [
  "Configuration": {                                { alias: "mobile", width: 300, height: 609 },
    "crops": [                                      { alias: "desktop", width: 1416, height: 540 }
      {                                         ]
        "alias": "mobile",         →
        "width": 300,
        "height": 609
      },
      {
        "alias": "desktop",
        "width": 1416,
        "height": 540
      }
    ]
  }
}

API OUTPUT:                                     FRONTEND USAGE:
{                                               const mobileCrop = image.crops.crops
  "crops": {                                        .find(c => c.alias === "mobile");
    "crops": [                    →
      { "alias": "mobile", ... },               <Image
      { "alias": "desktop", ... }                   src={mobileCrop.url}
    ]                                               width={mobileCrop.width}
  }                                                 height={mobileCrop.height}
}                                               />

FLOW: UDA config → Runtime object → Converter extracts → API response → Frontend uses
```

## When to Create Custom Converter

```
CREATE CUSTOM CONVERTER:
├─ ✅ Complex object transformation (MediaWithCrops → ApiSafeImage)
├─ ✅ Reference resolution (UDI → IPublishedContent → JSON)
├─ ✅ Data aggregation (fetch from multiple sources)
├─ ✅ Nested/recursive structures (Block Grid areas/blocks)
├─ ✅ Business logic (price formatting, calculations)
└─ ✅ Security/sanitization (HTML sanitizing, XSS prevention)

DO NOT CREATE CONVERTER:
├─ ❌ Simple value types (string, number, bool)
├─ ❌ Pre-formatted data (dropdown selections)
├─ ❌ Read-only data (labels)
└─ ❌ Already JSON-serializable values

DECISION: If value.GetType() is string/int/decimal/bool/DateTime → NO converter needed
```

## Converter Implementation Patterns

### PATTERN 1: Property Editor Converter

```csharp
WHEN: Converting standard Umbraco property editor
WHERE: Seed.Core/ApiSafeConverters/

public class MyApiSafeConverter : BaseApiSafeConverter
{
    // BINDING: EditorAlias connects to UDA
    public override string[] EditorAlias => new[] {
        "Umbraco.MediaPicker3"  // Must match UDA EditorAlias exactly
    };

    // TRANSFORMATION: Convert complex object to JSON-safe
    public override object ConvertToApiSafeValue(
        object value,
        string culture,
        string? segment,
        List<int> ids,
        Dictionary<string, object> additionalData)
    {
        if (value == null) return null;

        var mediaWithCrops = (MediaWithCrops)value;

        return new ApiSafeImage {
            Name = mediaWithCrops.Content.Name,
            Url = mediaWithCrops.Content.Url(null, UrlMode.Absolute),
            Crops = mediaWithCrops.LocalCrops,
            Width = mediaWithCrops.Content.Value<int>("umbracoWidth"),
            Height = mediaWithCrops.Content.Value<int>("umbracoHeight")
        };
    }
}

REGISTRATION: Automatic via CoreComposer reflection
```

### PATTERN 2: Content Type Converter

```csharp
WHEN: Custom logic for specific document type
WHERE: Seed.Backoffice.Extensions/ApiSafeConverters/

public class FeedBoatsApiSafeConverter : BaseContentTypeApiSafeConverter
{
    // BINDING: ContentTypes connects to document type alias
    public override string[] ContentTypes => new[] { "feedBoats" };

    // TRANSFORMATION: Custom business logic
    public override object ConvertElement(
        IPublishedElement element,
        string? culture,
        string? segment,
        List<int> ids,
        Dictionary<string, object> additionalData)
    {
        // Custom logic: fetch boats from content tree
        // Aggregate data from multiple sources
        // Apply business rules

        return new {
            boats = GetBoatsFromContentTree(),
            filters = GenerateFilters(),
            metadata = BuildMetadata()
        };
    }
}

REGISTRATION: Automatic via reflection
MATCHING: System matches "contentType.feedBoats"
```

### PATTERN 3: Nested Conversion

```csharp
WHEN: Block Grid/List with nested blocks
WHERE: Seed.Core/ApiSafeConverters/BlockGridApiSafeConverter.cs

public override object ConvertToApiSafeValue(object value, ...)
{
    var blocks = (IEnumerable<BlockGridItem>)value;

    foreach (var block in blocks) {
        // NESTED CONVERSION: Find converter for this block's content type
        var converter = _apiSafeConverters.Value
            .FirstOrDefault(x => x.IsEditor("contentType." + block.Content.ContentType.Alias));

        if (converter != null) {
            // Use custom converter for this block type
            var convertedBlock = converter.ConvertElement(...);
        }
        else {
            // Use default conversion (automatic passthrough)
            var defaultBlock = ConvertElementDefault(...);
        }
    }
}

PATTERN: Recursive converter lookup enables nested Block Grid structures
```

## Registration & Discovery

```
REGISTRATION PATTERN (CoreComposer.cs):

builder.ApiSafeConverters()
    .Add(() => builder.TypeLoader.GetTypes<IApiSafeConverter>());

DISCOVERY:
├─ Reflection scans assemblies
├─ Finds all classes implementing IApiSafeConverter
├─ Registers in ApiSafeConvertersCollection
└─ Available for lookup at runtime

COLLECTION USAGE:
// Find by property
var converter = _apiSafeConverters.Value.FirstOrDefault(x => x.IsEditor(property));

// Find by alias
var converter = _apiSafeConverters.Value.FirstOrDefault(x => x.IsEditor("Umbraco.MediaPicker3"));

// Find by content type
var converter = _apiSafeConverters.Value.FirstOrDefault(x => x.IsEditor("contentType.feedBoats"));

INJECTION: Use Lazy<ApiSafeConvertersCollection> to prevent circular dependencies
```

## Workflow: Design Time → Runtime

```
STEP 1: DESIGN TIME (Developer creates UDA)
├─ Create data type UDA file
├─ Set EditorAlias: "Umbraco.MediaPicker3"
├─ Configure crops, limits, options
└─ Add property to document type

STEP 2: DEPLOYMENT TIME
├─ UDA files deployed to Umbraco
├─ Umbraco reads schema definitions
├─ Database tables created
└─ Backoffice UI generated

STEP 3: CONTENT ENTRY TIME
├─ Editor opens backoffice
├─ Fills in property (uploads image)
├─ Sets crops based on UDA config
└─ Saves content

STEP 4: RUNTIME (API Request)
├─ Load content: IPublishedContent
├─ Identify property editor: EditorAlias
├─ Find converter: Match EditorAlias
├─ Transform data: ConvertToApiSafeValue() OR automatic passthrough
└─ Serialize to JSON: API response

STEP 5: FRONTEND CONSUMPTION
├─ Fetch API data
├─ Use transformed structure
├─ Access crops by alias from UDA config
└─ Render component
```

## Benefits of Automatic Fallback

```
BENEFIT                         IMPACT
================================================================================================
Reduced Code Complexity         ├─ Only ~20% of potential converters needed
                                ├─ Less code to maintain and test
                                └─ Smaller codebase

Extensibility                   ├─ Add simple properties to UDA without C# changes
                                ├─ No backend deployment for simple schema additions
                                └─ Graceful handling of new simple properties

Performance                     ├─ No converter overhead for simple types
                                ├─ Direct passthrough faster than method invocation
                                └─ Reduced memory allocations

Backward Compatibility          ├─ If converter removed, fallback to raw values
                                ├─ Graceful degradation instead of errors
                                └─ Useful during refactoring

Developer Experience            ├─ Don't overthink simple properties
                                ├─ Focus converter effort on complex transformations
                                └─ System "just works" for 80% of cases
```

## Anti-Patterns (What NOT to Do)

```
❌ NEVER: Create converters for simple value types
   ✅ INSTEAD: Rely on automatic passthrough for string/number/bool

❌ NEVER: Hardcode EditorAlias strings without Constants
   ✅ INSTEAD: Use Constants.PropertyEditors.Aliases when available

❌ NEVER: Inject ApiSafeConvertersCollection directly (circular dependency)
   ✅ INSTEAD: Use Lazy<ApiSafeConvertersCollection>

❌ NEVER: Return non-JSON-serializable objects from converter
   ✅ INSTEAD: Return simple types, arrays, dictionaries, POCOs

❌ NEVER: Create circular references in converted data
   ✅ INSTEAD: Use ids parameter to track visited content

❌ NEVER: Assume converter exists for all EditorAlias values
   ✅ INSTEAD: Handle null converter case (automatic passthrough)

❌ NEVER: Perform expensive operations in converters
   ✅ INSTEAD: Cache, batch, or pre-compute where possible

❌ NEVER: Throw exceptions for missing data in converters
   ✅ INSTEAD: Return null or empty structures, log warnings
```

## Troubleshooting Lookup

```
ISSUE                                   SOLUTION
================================================================================================
Converter not found                     ├─ Verify EditorAlias matches UDA exactly (case-sensitive)
                                        ├─ Check converter registered in correct project
                                        ├─ Ensure project referenced in UmbracoProject
                                        └─ Restart application to reload converters

Property returns null                   ├─ Check automatic passthrough returning null
                                        ├─ Verify content has value for property
                                        └─ Add logging to converter to debug

Wrong data structure in API             ├─ Verify converter ConvertToApiSafeValue return type
                                        ├─ Check TypeScript types match converter output
                                        └─ Inspect API response to confirm structure

Circular reference error                ├─ Use ids parameter to track visited content
                                        ├─ Check for recursive content references
                                        └─ Add id to ids list before processing

Performance issues                      ├─ Profile converter execution time
                                        ├─ Avoid N+1 queries in converters
                                        ├─ Batch load related content
                                        └─ Use caching where appropriate

UDA config not reflected in API         ├─ Verify converter uses Configuration from UDA
                                        ├─ Check crops/options extracted correctly
                                        └─ Ensure deployment completed successfully
```

## Converter Output Requirements

```
MUST RETURN:
├─ JSON-serializable types only
├─ Simple types: string, number, bool, DateTime, null
├─ Arrays: T[]
├─ Objects: POCOs with public properties
├─ Dictionaries: Dictionary<string, object>
└─ Nested structures of above

CANNOT RETURN:
├─ ❌ IPublishedContent (Umbraco object)
├─ ❌ MediaWithCrops (Umbraco object)
├─ ❌ Complex objects with circular references
├─ ❌ Types requiring custom serializers
└─ ❌ Database connections, streams, file handles

VALIDATION: If JSON.Stringify(output) throws → Bad converter output
```

## Quick Reference: UDA ↔ Converter Mapping

```
UDA FIELD                           CONVERTER PROPERTY               PURPOSE
================================================================================================
EditorAlias                         EditorAlias[]                    Binding contract for property editors
Document type Alias                 ContentTypes[]                   Binding contract for content types
Configuration.crops[]               Used in ConvertToApiSafeValue    Crop sizes available at runtime
Configuration.items[]               Used in ConvertToApiSafeValue    Dropdown options available
Dependencies[]                      N/A                              Deployment only
Name                                N/A                              Display only
DatabaseType                        N/A                              Storage only

CRITICAL: EditorAlias is the primary binding mechanism
```

## Summary Table

```
ASPECT                  UDA FILES                           APISAFECONVERTERS
================================================================================================
Layer                   Schema definition                   Runtime transformation
Format                  JSON (.uda extension)               C# classes
Purpose                 Define WHAT + HOW configured        Define HOW data transforms
When                    Design time                         Execution time
Connection              Specifies EditorAlias               Implements EditorAlias
Contains                Configuration, metadata             Conversion logic
Modified By             Developers (via backoffice/files)   Developers (C# code)
Used By                 Umbraco Deploy                      API endpoints
Affects                 Backoffice UI, database schema      API responses
Registration            Deployed via Umbraco Deploy         Auto-discovered via reflection
Coverage                100% of properties                  ~20% need custom converters
Fallback                N/A                                 Automatic passthrough for remaining 80%
```

## Cross-Reference

```
NEED                                    CONSULT
================================================================================================
UDA file syntax                         UDA_FILE_FORMAT.md
End-to-end workflows                    DATATYPE_IMPLEMENTATION_GUIDE.md
TypeScript type mapping                 TYPESCRIPT_TYPES_RELATIONSHIP.md
Project structure                       SRC_DIRECTORY_STRUCTURE.md
Converter implementations               src/Seed.Core/ApiSafeConverters/
Custom converter examples               src/Seed.Backoffice.Extensions/ApiSafeConverters/
```

## Key Takeaways

```
1. AUTOMATIC FALLBACK: ~80% of properties need NO converter
2. EDITORALIAS BINDING: Connects UDA schema ↔ Runtime converter
3. SIMPLE TYPES PASSTHROUGH: string/number/bool/DateTime auto-serialize
4. COMPLEX TYPES NEED CONVERTERS: Media/Content/Blocks need transformation
5. CONFIGURATION FLOWS: UDA config → Runtime object → Converter → API
6. LAZY INJECTION: Prevent circular dependencies with Lazy<>
7. JSON-SAFE OUTPUT: Converters must return serializable types
8. TRUST THE SYSTEM: If uncertain, skip converter (fallback handles it)
```
