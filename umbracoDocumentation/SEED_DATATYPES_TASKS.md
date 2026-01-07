# Seed.DataTypes - Task Decision Guide

## Project Classification

```
PROJECT: Seed.DataTypes
LOCATION: src/Seed.DataTypes/
PURPOSE: Custom Umbraco property editors (backoffice UI controls)
SCOPE: Reusable across industries
KEY QUESTION: "Would a real estate site, e-commerce store, or university use this editor?"
DEPENDENCIES: Seed.Core only (no circular dependencies)
```

## Decision Tree: Does Task Belong Here?

```
QUERY: Should this be implemented in Seed.DataTypes?

├─ Is it a backoffice UI control (property editor)?
│  ├─ NO → Wrong project (see other decision trees)
│  └─ YES → Continue
│
├─ Is it reusable across different industries?
│  ├─ NO → Seed.Backoffice.Extensions (project-specific)
│  ├─ UNSURE → Ask: Would [hotel/school/store] use this?
│  └─ YES → Continue
│
├─ Is it configuration of existing editor?
│  ├─ YES → UDA files (NOT code)
│  └─ NO → Continue
│
├─ Does it contain business logic?
│  ├─ YES → Service in Seed.Backoffice.Extensions (NOT property editor)
│  └─ NO → Continue
│
└─ Is it a new editor OR extension to existing extensible editor?
   ├─ New editor → Seed.DataTypes ✅
   └─ Extension to FlexibleLinks/VideoEmbedder/CustomPicker → Seed.DataTypes ✅
```

## Reusability Test

```
APPLY THIS TEST TO EVERY TASK:

QUESTION: Could these industries use this property editor?
├─ Real estate website?
├─ E-commerce store?
├─ University website?
├─ Restaurant chain?
└─ Government portal?

IF 2+ say YES → Seed.DataTypes ✅
IF only KRD/boats say YES → Seed.Backoffice.Extensions ❌
```

## Task Pattern Library

### PATTERN 1: New Custom Property Editor

```
CONDITION: Need entirely new backoffice UI control

EXAMPLES:
├─ Color Palette Picker (select from predefined colors)
├─ Date Range Picker (start/end dates)
├─ Tag Cloud Editor (visual tag selection)
├─ Timeline Editor (events on timeline)
└─ Pricing Tier Builder (tiered pricing UI)

IMPLEMENTATION STEPS:
├─ 1. CREATE: PropertyEditors/{EditorName}/
│  ├─ {EditorName}Configuration.cs (editor settings)
│  ├─ {EditorName}ConfigurationEditor.cs (settings UI)
│  └─ {EditorName}ValueConverter.cs (convert value to typed object)
├─ 2. CREATE: App_Plugins/{editorAlias}/
│  ├─ package.manifest (register editor with Umbraco)
│  ├─ {editor}.html (Angular view)
│  ├─ {editor}.controller.js (Angular controller)
│  └─ {editor}.css (editor styles)
├─ 3. CREATE: Models/{EditorName}Model.cs (C# model for value)
├─ 4. TEST: In backoffice data type creation
└─ 5. COMMIT: All files

EXISTING EXAMPLES:
├─ SeoSettings (SEO metadata editor)
├─ GeocodedLocation (Google Maps picker)
└─ IconPicker (icon selection UI)

DEPENDENCIES: Seed.Core (for base classes)

FILES CREATED:
├─ PropertyEditors/{EditorName}/*.cs (3-4 files)
├─ App_Plugins/{editorAlias}/*.{html,js,css}
└─ Models/{EditorName}Model.cs
```

### PATTERN 2: Extend Extensible Editor

```
CONDITION: Add new type to FlexibleLinks, VideoEmbedder, or CustomPicker

EXTENSIBLE EDITORS:
├─ FlexibleLinks → Link type system (uses collection builder)
├─ VideoEmbedder → Video provider system (YouTube, Vimeo, etc.)
└─ CustomPicker → Content picker variations

EXAMPLE: Add new FlexibleLinks type

IMPLEMENTATION:
├─ 1. CREATE: FlexibleLinks/Types/{TypeName}LinkType.cs
│  └─ Implement IFlexibleLinkType interface
├─ 2. DEFINE: Link properties (URL, title, icon, etc.)
├─ 3. FRONTEND: Collection builder auto-discovers type
├─ 4. TEST: Type appears in FlexibleLinks dropdown
└─ 5. COMMIT: Single .cs file

CODE TEMPLATE:
public class {TypeName}LinkType : IFlexibleLinkType
{
    public string Name => "{Display Name}";
    public string Alias => "{alias}";
    public string Icon => "{umbraco-icon}";

    public object GetModel(FlexibleLink link)
    {
        return new
        {
            Url = link.Url,
            Title = link.Title,
            // Custom properties
        };
    }
}

EXISTING EXAMPLES:
├─ FlexibleLinks: ExternalLinkType, InternalLinkType, EmailLinkType, PhoneLinkType, DownloadLinkType, AnchorLinkType (6 types)
├─ VideoEmbedder: YouTubeProvider, VimeoProvider, WistiaProvider (3 providers)
└─ CustomPicker: (framework for variations)

FILES MODIFIED:
└─ CREATE: {Category}/Types/{TypeName}.cs OR {Category}/Providers/{ProviderName}.cs
```

### PATTERN 3: External API Integration

```
CONDITION: Property editor needs third-party API data

EXAMPLES:
├─ Pinterest Board Selector (Pinterest API)
├─ Unsplash Image Picker (Unsplash API)
├─ Google Fonts Selector (Google Fonts API)
├─ Giphy GIF Picker (Giphy API)
└─ Weather Widget (Weather API)

IMPLEMENTATION STRUCTURE:
├─ 1. CREATE: Services/I{ServiceName}Service.cs (interface)
├─ 2. CREATE: Services/{ServiceName}Service.cs (implementation)
│  ├─ OAuth/API key handling
│  ├─ HTTP client for API calls
│  ├─ Caching (reduce API calls)
│  └─ Error handling
├─ 3. CREATE: PropertyEditors/{EditorName}/ (UI control)
├─ 4. CREATE: App_Plugins/{editorAlias}/ (backoffice UI)
│  └─ Calls controller endpoint → service → API
├─ 5. CONFIGURE: appsettings.json (API keys in UmbracoProject)
└─ 6. REGISTER: Service in collection builder

EXISTING EXAMPLES:
├─ AutodeskViewer/AutodeskViewerService.cs (Autodesk Forge API, 213 lines)
├─ VimeoVideoSelector/VimeoService.cs (Vimeo API)
└─ InstagramMediaPicker/InstagramService.cs (Instagram API)

PATTERN:
public class {Service}Service : I{Service}Service
{
    private readonly HttpClient _httpClient;
    private readonly IConfiguration _config;
    private string _cachedToken;

    public async Task<List<{Item}>> Get{Items}Async()
    {
        var token = await GetAccessTokenAsync();
        var response = await _httpClient.GetAsync($"{_baseUrl}/items", token);
        return ParseResponse(response);
    }

    private async Task<string> GetAccessTokenAsync()
    {
        // OAuth or API key auth
        // Cache token until expiry
    }
}

CONFIGURATION: appsettings.json (in UmbracoProject)
{
  "{ServiceName}": {
    "ClientId": "...",
    "ClientSecret": "...",
    "BaseUrl": "https://api.service.com/"
  }
}

FILES CREATED:
├─ Services/I{ServiceName}Service.cs
├─ Services/{ServiceName}Service.cs
├─ PropertyEditors/{EditorName}/*.cs
└─ App_Plugins/{editorAlias}/*
```

### PATTERN 4: Structured Data Editor

```
CONDITION: Editor for complex structured data (not simple text/number)

EXAMPLES:
├─ FAQ Editor (question/answer pairs)
├─ Business Hours Editor (day/time ranges)
├─ Pricing Tiers (tier name/price/features)
├─ Team Members (name/role/photo/bio)
└─ Social Links (platform/URL/icon mapping)

CHARACTERISTICS:
├─ Multiple fields per item
├─ Repeatable items
├─ Drag-and-drop reordering
└─ Saved as JSON

IMPLEMENTATION:
├─ 1. CREATE: Models/{EditorName}Item.cs (single item model)
├─ 2. CREATE: PropertyEditors/{EditorName}/*.cs
├─ 3. CREATE: App_Plugins/{editorAlias}/
│  └─ Repeater UI with add/remove/reorder
├─ 4. VALUE: Saved as JSON array
└─ 5. CONVERTER: Deserialize to List<{Item}>

VALUE CONVERTER:
public class {EditorName}ValueConverter : PropertyValueConverterBase
{
    public override object ConvertIntermediateToObject(
        IPublishedElement owner, IPublishedPropertyType propertyType,
        PropertyCacheLevel cacheLevel, object source, bool preview)
    {
        var json = source?.ToString();
        if (string.IsNullOrEmpty(json)) return new List<{Item}>();

        return JsonConvert.DeserializeObject<List<{Item}>>(json);
    }
}

EXISTING EXAMPLES:
├─ Would be good additions to library
└─ Currently implemented project-specifically

FILES CREATED:
├─ Models/{EditorName}Item.cs
├─ PropertyEditors/{EditorName}/*.cs
└─ App_Plugins/{editorAlias}/*
```

## Anti-Patterns

### ❌ ANTI-PATTERN 1: Project-Specific Property Editor

```
BAD: Creating editor only useful for boats/KRD

EXAMPLE:
public class BoatSpecificationsEditor  // ❌ Only boats use this

CORRECT: Create in Seed.Backoffice.Extensions OR use generic editor

GENERIC ALTERNATIVES:
├─ Use repeater with name/value pairs
├─ Use Block Grid for complex layouts
└─ Use nested content for structured data

IF editor is reusable → Seed.DataTypes ✅
IF editor is project-specific → Seed.Backoffice.Extensions ❌
```

### ❌ ANTI-PATTERN 2: Configuration via Code

```
BAD: Hardcoding configuration in property editor

public class SomeEditor
{
    private const string API_KEY = "abc123";  // ❌ Hardcoded
    private readonly string[] _allowedTypes = { "boat", "product" };  // ❌ Project-specific
}

CORRECT: Configure via UDA files and appsettings.json

// UDA file configuration (data type settings)
// appsettings.json for API keys (in UmbracoProject)
// Editor stays generic and reusable
```

### ❌ ANTI-PATTERN 3: Business Logic in Property Editor

```
BAD: Implementing business rules in editor

public class PriceEditor
{
    public object GetValue()
    {
        var price = GetInput();
        var tax = price * 0.07;  // ❌ Business logic
        var total = price + tax;
        return total;
    }
}

CORRECT: Property editor = UI control only

// Business logic → Service in Seed.Backoffice.Extensions
// Property editor → Captures input, returns value
// ApiSafeConverter → Applies business logic when converting for API
```

### ❌ ANTI-PATTERN 4: Using Code When UDA Config Works

```
BAD: Creating custom property editor when UDA config would work

// Creating "ImagePickerWithCrop" editor
// When you can configure media picker with crop in UDA:
{
  "DataType": "Umbraco.MediaPicker3",
  "Configuration": {
    "crops": [{...}],
    "filter": "Image"
  }
}

CORRECT: Only create editor if behavior can't be configured
```

### ❌ ANTI-PATTERN 5: Not Following Collection Builder Pattern

```
BAD: Manual registration

// Manually registering each type
builder.Services.AddTransient<IFlexibleLinkType, ExternalLinkType>();
builder.Services.AddTransient<IFlexibleLinkType, InternalLinkType>();
// ❌ Requires code change for each new type

CORRECT: Use collection builder (auto-discovery)

// Collection builder finds all IFlexibleLinkType implementations
// Just add new class, it's automatically discovered
// No registration code needed
```

## Decision Matrix

```
QUERY: Where does this task belong?

├─ Need backoffice UI control?
│  ├─ NO → Not a property editor task
│  └─ YES → Continue
│
├─ Reusable across industries?
│  ├─ NO → Seed.Backoffice.Extensions
│  └─ YES → Seed.DataTypes ✅
│
├─ Configuration of existing editor?
│  ├─ YES → UDA file (not code)
│  └─ NO → Seed.DataTypes ✅
│
├─ Extension to existing extensible editor?
│  ├─ FlexibleLinks type → Seed.DataTypes ✅
│  ├─ VideoEmbedder provider → Seed.DataTypes ✅
│  └─ CustomPicker variation → Seed.DataTypes ✅
│
└─ External API integration?
   ├─ Generic API (Unsplash, Google) → Seed.DataTypes ✅
   └─ Project API (Epicor, KRD-specific) → Seed.Backoffice.Extensions
```

## Validation Checklist

```
BEFORE IMPLEMENTING IN SEED.DATATYPES:

□ Is this a property editor (backoffice UI control)?
□ Could 2+ different industries use this?
□ Does it only capture/display data (no business logic)?
□ Is it NOT configurable via existing editors + UDA files?
□ If extending existing editor, is it generic (not project-specific)?
□ If API integration, is the API generic (not client-specific)?
□ Have I checked existing editors (don't duplicate)?

IF ALL YES → Seed.DataTypes ✅
IF ANY NO → Wrong project (see other decision trees)
```

## Quick Reference

```
TASK → LOCATION:

New property editor:
└─ PropertyEditors/{EditorName}/ + App_Plugins/{alias}/

FlexibleLinks type:
└─ FlexibleLinks/Types/{TypeName}LinkType.cs

VideoEmbedder provider:
└─ VideoEmbedder/Providers/{Provider}Provider.cs

External API service:
└─ Services/I{Service}Service.cs + Services/{Service}Service.cs

Property editor model:
└─ Models/{EditorName}Model.cs

Value converter:
└─ PropertyEditors/{EditorName}/{EditorName}ValueConverter.cs
```

## Critical Rules

```
RULE 1: Reusability test
└─ If only KRD/boats use it → Seed.Backoffice.Extensions

RULE 2: No business logic
└─ Property editors capture data, services process data

RULE 3: Configure via files, not code
└─ UDA files for editor config, appsettings.json for API keys

RULE 4: Use collection builder for extensibility
└─ Auto-discovery, no manual registration

RULE 5: Don't duplicate existing editors
└─ Check if UDA configuration can achieve goal

RULE 6: Generic > Specific
└─ Design for any industry, configure for specific use

RULE 7: Dependencies: Seed.Core only
└─ Don't reference Seed.Backoffice.Extensions (creates circular dependency)
```

## Existing Editor Inventory

```
CURRENT EDITORS (15 total):

EXTENSIBLE FRAMEWORKS:
├─ FlexibleLinks (6 built-in types, extensible via IFlexibleLinkType)
├─ VideoEmbedder (3 providers: YouTube, Vimeo, Wistia)
└─ CustomPicker (framework for custom content pickers)

SPECIALIZED EDITORS:
├─ AutodeskViewer (CAD file viewer with Forge API)
├─ VimeoVideoSelector (Vimeo API integration)
├─ InstagramMediaPicker (Instagram API integration)
├─ AimbaseNewsletterPicker (Newsletter platform integration)
├─ GeocodedLocation (Google Maps location picker)
├─ SeoSettings (SEO metadata: title, description, OG, Twitter)
├─ SocialSettings (Social media account links)
├─ IconPicker (Icon selection UI)
├─ PositionPicker (Positioning/alignment selector)
├─ SideSizer (Column width configurator)
└─ BlockPicker (Block selection UI)

BEFORE CREATING NEW EDITOR:
└─ Check if existing editor or UDA config can solve need
```
