# TypeScript Types ↔ Converters ↔ UDA - LLM Quick Reference

## Three-Layer Architecture

```
LAYER 1: SCHEMA (UDA Files)
├─ LOCATION: src/UmbracoProject/umbraco/Deploy/Revision/
├─ FORMAT: JSON (.uda)
├─ PURPOSE: Define WHAT + HOW configured
└─ ROLE: Source of truth

       ↓ EditorAlias Binding

LAYER 2: TRANSFORMATION (ApiSafeConverters)
├─ LOCATION: src/Seed.Core/ApiSafeConverters/, src/Seed.Backoffice.Extensions/ApiSafeConverters/
├─ FORMAT: C# classes
├─ PURPOSE: HOW data transforms (runtime)
├─ FALLBACK: 80% automatic passthrough (no converter needed)
└─ ROLE: Umbraco objects → JSON-safe models

       ↓ JSON Serialization

LAYER 3: CONSUMPTION (TypeScript Types)
├─ LOCATION: src/Seed.Web/lib/umbraco/types/
├─ FORMAT: TypeScript interfaces/types
├─ PURPOSE: WHAT shape data has
└─ ROLE: Type-safe frontend consumption

CRITICAL: All three layers must stay synchronized
```

## Type Correspondence Matrix

```
EDITORALIAS              C# MODEL             CONVERTER                        TS TYPE             LOCATION
============================================================================================================================
Umbraco.MediaPicker3     ApiSafeImage         MediaApiSafeConverter            ImageModel          @lib/umbraco/types/imageModel.type
Umbraco.ContentPicker    JsonPublishedContent PublishedContentApiSafeConverter UmbracoNode         @lib/umbraco/types/umbracoNode.type
Umbraco.MultiNodeTreePicker JsonPublishedContent[] PublishedContentApiSafeConverter UmbracoNode[]      @lib/umbraco/types/umbracoNode.type
Umbraco.BlockGrid        BlockModel[]         BlockGridApiSafeConverter        BlockGridItem[]     @lib/umbraco/types/blockGridItem.type
Umbraco.BlockList        BlockModel[]         BlockListApiSafeConverter        BlockListItem[]     @lib/umbraco/types/blockListItem.type
Umbraco.TinyMCE          string               RichContentApiSafeConverter      string (HTML)       Inline
UmbracoForms.FormPicker  ApiSafeForm          UmbracoFormApiSafeConverter      ApiSafeForm         Custom type

SIMPLE TYPES (NO CONVERTER):
Umbraco.TextBox          string               ❌ Automatic passthrough          string              Inline
Umbraco.TextArea         string               ❌ Automatic passthrough          string              Inline
Umbraco.Integer          int                  ❌ Automatic passthrough          number              Inline
Umbraco.Decimal          decimal              ❌ Automatic passthrough          number              Inline
Umbraco.TrueFalse        bool                 ❌ Automatic passthrough          boolean             Inline
Umbraco.DateTime         DateTime             ❌ Automatic passthrough          string (ISO 8601)   Inline
Umbraco.DropDown.Flexible string               ❌ Automatic passthrough          string OR union     Inline
Umbraco.CheckBoxList     string[]             ❌ Automatic passthrough          string[]            Inline
Umbraco.Slider           decimal              ❌ Automatic passthrough          number              Inline
```

## DatabaseType → TypeScript Mapping

```
UDA DATABASETYPE         C# TYPE              JSON TYPE            TYPESCRIPT TYPE
=========================================================================================
Nvarchar                 string               string               string
Integer                  int                  number               number
Decimal                  decimal              number               number
Date                     DateTime             string (ISO 8601)    string
Ntext                    string               string               string
```

## Decision Tree: What TypeScript Type Do I Use?

```
QUERY: What TypeScript type should I use for this property?

├─ Check UDA EditorAlias in data type
│
├─ Is it a simple editor (TextBox, Integer, Toggle)?
│  ├─ TextBox/TextArea → string
│  ├─ Integer/Decimal/Slider → number
│  ├─ TrueFalse → boolean
│  ├─ DateTime → string (ISO 8601)
│  ├─ DropDown → string OR "Opt1" | "Opt2" | "Opt3" (union)
│  └─ CheckBoxList → string[]
│
├─ Is it Umbraco.MediaPicker3?
│  └─ import { ImageModel } from "@lib/umbraco/types/imageModel.type"
│
├─ Is it Umbraco.ContentPicker or MultiNodeTreePicker?
│  └─ import { UmbracoNode } from "@lib/umbraco/types/umbracoNode.type"
│     (or UmbracoNode[] for multi-picker)
│
├─ Is it Umbraco.BlockGrid?
│  └─ Component receives BlockGridItem
│     Content property typed per block alias
│
├─ Is it Umbraco.BlockList?
│  └─ Component receives BlockListItem
│     Content property typed per block alias
│
├─ Is it a custom data type?
│  └─ Check if converter exists
│     ├─ Converter exists → Use output type from converter
│     └─ No converter → Use automatic passthrough type
│
└─ Is it a custom content type with converter?
   └─ Manually define type matching converter output
```

## Complete Data Flow Example

```
EXAMPLE: Media picker with crops from UDA → Frontend

STEP 1: UDA DEFINITION
data-type__*.uda:
{
  "EditorAlias": "Umbraco.MediaPicker3",
  "Configuration": {
    "crops": [
      { "alias": "mobile", "width": 300, "height": 609 },
      { "alias": "desktop", "width": 1416, "height": 540 }
    ]
  }
}

STEP 2: C# MODEL
ApiSafeImage.cs:
public class ApiSafeImage {
    public string Name { get; set; }
    public string Url { get; set; }
    public ImageCropperValue? Crops { get; set; }  // Contains mobile/desktop crops
    public int Width { get; set; }
    public int Height { get; set; }
}

STEP 3: CONVERTER
MediaApiSafeConverter.cs:
public override object ConvertToApiSafeValue(...) {
    return new ApiSafeImage {
        Name = content.Name,
        Url = content.Url(...),
        Crops = content.LocalCrops,  // Includes UDA crops
        Width = content.Value<int>("umbracoWidth"),
        Height = content.Value<int>("umbracoHeight")
    };
}

STEP 4: JSON RESPONSE
{
  "name": "hero.jpg",
  "url": "https://cdn.example.com/media/hero.jpg",
  "crops": {
    "crops": [
      { "alias": "mobile", "width": 300, "height": 609 },
      { "alias": "desktop", "width": 1416, "height": 540 }
    ]
  },
  "width": 2832,
  "height": 1080
}

STEP 5: TYPESCRIPT TYPE
imageModel.type.ts:
export type ImageModel = {
    name: string,
    url: string,
    crops?: ImageCropModel,  // Matches JSON structure
    width: number,
    height: number
}

STEP 6: COMPONENT USAGE
Component.tsx:
import { ImageModel } from "@lib/umbraco/types/imageModel.type";

export type MyComponentModel = {
  heroImage: ImageModel  // Reuse shared type
}

const { heroImage } = content as MyComponentModel;
const mobileCrop = heroImage.crops?.crops.find(c => c.alias === "mobile");
```

## Block Grid Pattern (Special Case)

```
PATTERN: Block Grid blocks typed by alias

FLOW:
UDA defines element type "richtext" →
Converter transforms to BlockModel with alias: "richtext" →
Frontend component receives BlockGridItem →
Component casts content based on alias

UDA:
{
  "Name": "Rich Text",
  "Alias": "richtext",
  "IsElementType": true,
  "PropertyTypes": [
    { "Alias": "text", "DataType": "..." },
    { "Alias": "contentSize", "DataType": "..." }
  ]
}

C# CONVERTER OUTPUT:
{
  "alias": "richtext",
  "content": {
    "text": "<p>Hello world</p>",
    "contentSize": "Standard"
  }
}

TYPESCRIPT COMPONENT:
import BlockGridItem from "@lib/umbraco/types/blockGridItem.type";

export type TextModel = {
  text: string;
  contentSize?: "Standard" | "Narrow";
};

export default function RichText({ content }: BlockGridItem) {
  const { text, contentSize } = content as TextModel;
  // TypeScript knows text is string, contentSize is optional union
}

KEY: BlockGridItem is generic wrapper, specific type via cast
```

## Type Synchronization Checklist

```
WHEN MODIFYING SCHEMA:

□ Step 1: Update UDA file
  ├─ Add/modify property in PropertyTypes
  ├─ Set EditorAlias for data type
  └─ Configure crops/options/limits

□ Step 2: Evaluate converter requirement
  ├─ Simple editor? → Skip to Step 4 (automatic passthrough)
  ├─ Complex editor? → Check if converter exists
  └─ Custom logic needed? → Update/create converter

□ Step 3: Update C# converter (if needed)
  ├─ Modify ConvertToApiSafeValue logic
  ├─ Update C# model properties
  └─ Ensure JSON-serializable output

□ Step 4: Update TypeScript types
  ├─ Locate ALL components using this document type
  ├─ Update type definitions to match converter output OR automatic passthrough
  ├─ Add imports for complex types (ImageModel, UmbracoNode)
  └─ Match optionality (? for optional properties)

□ Step 5: Validate TypeScript compilation
  ├─ cd src/Seed.Web
  ├─ npx tsc --noEmit
  └─ MUST: Zero errors

□ Step 6: Verify component destructuring
  └─ Ensure components can destructure new property

INCOMPLETE = Property exists in CMS but not usable in frontend
COMPLETE = Property flows UDA → Converter → TypeScript → Component
```

## Optionality Rules

```
C# NULLABLE                 TYPESCRIPT OPTIONAL          MEANING
========================================================================================
public string Name          name: string                 Required, always has value
public string? Description  description?: string         Optional, may be undefined
public ImageCropModel? Crops crops?: ImageCropModel     Optional nested object

UDA MANDATORY → TYPESCRIPT REQUIRED:
{
  "Mandatory": true   → property: Type (no ?)
  "Mandatory": false  → property?: Type (with ?)
}

DEFAULT: If unsure, make optional (add ?) to prevent runtime errors
```

## Naming Conventions

```
LAYER                   CONVENTION                          EXAMPLES
================================================================================================
C# Model                ApiSafe{Entity} OR {Entity}Model    ApiSafeImage, FeedBoat
TypeScript Type         {Entity}Model OR type name          ImageModel, FeedBoat
Component Type          {Component}Model                    FeedBoatsModel, TextModel
Property Alias (UDA)    camelCase                           heroImage, showInNavigation
Property Name (UDA)     Title Case with Spaces              Hero Image, Show in Navigation

CONSISTENCY: Keep names consistent across layers for maintainability
```

## Common Patterns

### PATTERN 1: Simple Property (Automatic Passthrough)

```
UDA:
{
  "Alias": "title",
  "DataType": "umb://data-type/{textbox-uuid}"
}

CONVERTER: ❌ None (automatic passthrough)

TYPESCRIPT:
export type PageModel = {
  title: string  // Direct mapping, no converter needed
}

USAGE:
const { title } = content as PageModel;
```

### PATTERN 2: Media Picker

```
UDA:
{
  "Alias": "heroImage",
  "DataType": "umb://data-type/{media-picker-uuid}"
}
Data type EditorAlias: "Umbraco.MediaPicker3"

CONVERTER: ✅ MediaApiSafeConverter → ApiSafeImage

TYPESCRIPT:
import { ImageModel } from "@lib/umbraco/types/imageModel.type";

export type PageModel = {
  heroImage: ImageModel  // Reuse shared type
}

USAGE:
const { heroImage } = content as PageModel;
<img src={heroImage.url} alt={heroImage.name} />
```

### PATTERN 3: Content Picker

```
UDA:
{
  "Alias": "relatedPage",
  "DataType": "umb://data-type/{content-picker-uuid}"
}
Data type EditorAlias: "Umbraco.ContentPicker"

CONVERTER: ✅ PublishedContentApiSafeConverter → JsonPublishedContent

TYPESCRIPT:
import { UmbracoNode } from "@lib/umbraco/types/umbracoNode.type";

export type PageModel = {
  relatedPage: UmbracoNode
}

USAGE:
const { relatedPage } = content as PageModel;
<a href={relatedPage.url}>{relatedPage.name}</a>
```

### PATTERN 4: Dropdown with Union Type

```
UDA:
{
  "EditorAlias": "Umbraco.DropDown.Flexible",
  "Configuration": {
    "items": [
      { "value": "Standard" },
      { "value": "Narrow" }
    ]
  }
}

CONVERTER: ❌ None (automatic passthrough → string)

TYPESCRIPT:
export type ContentSize = "Standard" | "Narrow";  // Union type for type safety

export type TextModel = {
  contentSize?: ContentSize  // Type-safe dropdown
}

USAGE:
const { contentSize } = content as TextModel;
if (contentSize === "Narrow") { ... }  // TypeScript validates
```

### PATTERN 5: Custom Content Type with Business Logic

```
UDA:
{
  "Alias": "feedBoats",
  "PropertyTypes": [
    { "Alias": "buildLinkText", ... },
    { "Alias": "priceFormat", ... }
  ]
}

CONVERTER: ✅ FeedBoatsApiSafeConverter (custom logic)
Output: { boats: ApiSafeFeedBoat[], compareUrl: string }

TYPESCRIPT: (manually defined to match converter output)
import { ImageModel } from "@lib/umbraco/types/imageModel.type";

export type FeedBoat = {
  id: number;
  name: string;
  cardImage: ImageModel;
  priceText: string;  // Computed by converter
  // ...
}

export type FeedBoatsModel = {
  boats: FeedBoat[],  // Aggregated by converter
  compareUrl: string
}

USAGE:
const { boats } = content as FeedBoatsModel;
boats.map(boat => <Card key={boat.id} {...boat} />)

CRITICAL: Type must match converter OUTPUT, not UDA schema
```

## Shared Type Library

```
LOCATION: src/Seed.Web/lib/umbraco/types/

CORE TYPES (REUSE THESE):
├─ imageModel.type.ts → ImageModel (MediaPicker3)
├─ imageCropModel.type.ts → ImageCropModel (nested in ImageModel)
├─ imageCrop.type.ts → ImageCrop (individual crop)
├─ focalPoint.type.ts → FocalPoint (crop coordinates)
├─ umbracoNode.type.ts → UmbracoNode (ContentPicker)
├─ blockGridItem.type.ts → BlockGridItem (Block Grid wrapper)
└─ blockListItem.type.ts → BlockListItem (Block List wrapper)

USAGE:
import { ImageModel } from "@lib/umbraco/types/imageModel.type";
import { UmbracoNode } from "@lib/umbraco/types/umbracoNode.type";

DO NOT duplicate these types in components
```

## Troubleshooting Lookup

```
ISSUE                                   SOLUTION
================================================================================================
Property doesn't exist (TS error)       ├─ Verify property alias matches UDA exactly (case-sensitive)
                                        ├─ Check property added to type definition
                                        └─ Ensure EditorAlias correct for automatic passthrough

Type mismatch                           ├─ Check converter output type in C#
                                        ├─ Verify TypeScript type matches converter output
                                        ├─ For simple types, verify automatic passthrough mapping
                                        └─ Inspect API response to confirm structure

Unexpected undefined values             ├─ Add ? to TypeScript property (make optional)
                                        ├─ Check UDA Mandatory field
                                        ├─ Verify content has value
                                        └─ Add null checks in component

Wrong data structure                    ├─ Review converter ConvertToApiSafeValue logic
                                        ├─ Check if custom converter modifies structure
                                        ├─ Inspect API response JSON
                                        └─ Update TypeScript type to match actual response

IntelliSense not showing type           ├─ Restart TypeScript server (VS Code: Cmd+Shift+P → Restart TS Server)
                                        ├─ Verify type is exported (export type ...)
                                        ├─ Check import path correct
                                        └─ Run npx tsc --noEmit to verify

Compilation errors after UDA change     ├─ Locate ALL components using changed document type
                                        ├─ Update type definitions in each component
                                        ├─ Match new property structure
                                        └─ Run npx tsc --noEmit until zero errors
```

## Best Practices

```
PRACTICE                                GUIDELINE
================================================================================================
Use Shared Types                        ├─ Import ImageModel, UmbracoNode from @lib/umbraco/types
                                        ├─ Don't duplicate type definitions
                                        └─ Maintain centralized type library

Match Optionality                       ├─ C# nullable (?) = TypeScript optional (?)
                                        ├─ UDA Mandatory: false = TypeScript optional (?)
                                        └─ When in doubt, make optional to prevent runtime errors

Type-Safe Unions                        ├─ Dropdowns → "Opt1" | "Opt2" | "Opt3"
                                        ├─ Better than generic string
                                        └─ Enables exhaustiveness checking

Document Custom Transformations         ├─ Add JSDoc comments explaining converter logic
                                        ├─ Reference C# converter file
                                        └─ Note UDA file location

Keep Types Synchronized                 ├─ UDA change = Check converter = Update TypeScript
                                        ├─ Run npx tsc --noEmit before committing
                                        └─ All layers must stay in sync

Component-Level Type Assertions         ├─ Define type in component file
                                        ├─ Cast content: content as ComponentModel
                                        └─ TypeScript validates within component scope

Understand Automatic Passthrough        ├─ Simple types need NO TypeScript updates beyond adding property
                                        ├─ Complex types require checking converter output
                                        └─ When in doubt, inspect API response
```

## Anti-Patterns (What NOT to Do)

```
❌ NEVER: Duplicate type definitions across components
   ✅ INSTEAD: Import shared types from @lib/umbraco/types

❌ NEVER: Assume TypeScript type matches UDA schema for custom converters
   ✅ INSTEAD: Check converter output, type matches CONVERTER not UDA

❌ NEVER: Skip TypeScript compilation validation after UDA changes
   ✅ INSTEAD: Always run npx tsc --noEmit

❌ NEVER: Use 'any' to bypass type errors
   ✅ INSTEAD: Fix type definition to match actual data

❌ NEVER: Forget to import complex types (ImageModel, UmbracoNode)
   ✅ INSTEAD: Import from @lib/umbraco/types for reusability

❌ NEVER: Make all properties required without checking UDA Mandatory field
   ✅ INSTEAD: Match optionality between layers

❌ NEVER: Assume simple property editors need converters
   ✅ INSTEAD: Trust automatic passthrough for string/number/bool
```

## Workflow: Adding Property End-to-End

```
SCENARIO: Add "subtitle" property to page

STEP 1: Modify UDA
├─ Generate UUID: uuidgen
├─ Add property to document type PropertyTypes
├─ Data type: Textbox (Umbraco.TextBox)
└─ Set Mandatory: false

STEP 2: Evaluate converter
├─ EditorAlias: Umbraco.TextBox
├─ Decision: Simple type → Automatic passthrough ✅
└─ Action: No converter changes needed

STEP 3: Update TypeScript
├─ Locate component using this document type
├─ Add property to type definition
└─ Type: subtitle?: string (optional because Mandatory: false)

export type PageModel = {
  title: string,
  subtitle?: string,  // NEW - automatic passthrough from UDA
  heroImage: ImageModel
}

STEP 4: Update component
├─ Destructure new property
└─ Use in JSX

const { title, subtitle, heroImage } = content as PageModel;
return (
  <div>
    <h1>{title}</h1>
    {subtitle && <h2>{subtitle}</h2>}
  </div>
);

STEP 5: Validate
├─ npx tsc --noEmit (zero errors)
├─ Test in browser
└─ Verify API response includes subtitle

RESULT: Property works without C# converter changes (automatic passthrough)
```

## Architecture Benefits

```
BENEFIT                         IMPACT
================================================================================================
Type Safety Across Stack        ├─ UDA: Schema validation at deployment
                                ├─ C#: Compile-time checking in backend
                                ├─ TypeScript: Compile-time checking in frontend
                                └─ Runtime: JSON schema validation (implicit)

Single Source of Truth          └─ UDA files = authoritative schema

Refactoring Safety              ├─ Change property name in UDA
                                ├─ Compiler errors in C# converters
                                ├─ Compiler errors in TypeScript components
                                └─ Fix all errors before deployment

Developer Experience            ├─ IntelliSense in both C# and TypeScript
                                ├─ Self-documenting code through types
                                ├─ Reduced runtime errors
                                └─ Easier onboarding

Automatic Fallback Benefits     ├─ Add simple properties without C# changes
                                ├─ Only ~20% of properties need custom converters
                                ├─ Faster development for simple schema changes
                                └─ Graceful degradation if converter missing
```

## Cross-Reference

```
NEED                                    CONSULT
================================================================================================
UDA file syntax                         UDA_FILE_FORMAT.md
Converter decision logic                UDA_APISAFECONVERTERS_RELATIONSHIP.md
End-to-end workflows                    DATATYPE_IMPLEMENTATION_GUIDE.md
Project structure                       SRC_DIRECTORY_STRUCTURE.md
Converter implementations               src/Seed.Core/ApiSafeConverters/
TypeScript type definitions             src/Seed.Web/lib/umbraco/types/
```

## Key Takeaways

```
1. THREE LAYERS: UDA (schema) → Converter (transform) → TypeScript (consume)
2. BINDING: EditorAlias connects UDA ↔ Converter
3. CORRESPONDENCE: C# Model → JSON → TypeScript Type (manual synchronization)
4. AUTOMATIC PASSTHROUGH: Simple types (string/number/bool) need NO converter
5. COMPLEX TYPES: Media/Content/Blocks/Custom need converters
6. OPTIONALITY: C# nullable (?) = TypeScript optional (?)
7. SHARED TYPES: Reuse ImageModel, UmbracoNode from @lib/umbraco/types
8. VALIDATION: Always run npx tsc --noEmit before committing
9. BLOCK GRID: Generic BlockGridItem wrapper, cast content by alias
10. CUSTOM CONVERTERS: TypeScript type matches CONVERTER OUTPUT, not UDA schema

WORKFLOW COMPLETE = UDA modified + Converter evaluated + TypeScript updated + Compilation succeeds
```
