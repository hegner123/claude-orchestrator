# Seed.DataTypes - Component Reference

## Project Identification

```
PROJECT: Seed.DataTypes
TYPE: .NET 8 Razor Class Library
LOCATION: src/Seed.DataTypes/
FILES: 115 C# files
PURPOSE: Reusable custom property editors
DEPENDENCIES: Seed.Core, Umbraco.Cms.Core
REFERENCED BY: Seed.Backoffice.Extensions, UmbracoProject
```

## Editor Inventory (15 Total)

```
EXTENSIBLE FRAMEWORKS (3):
├─ FlexibleLinks → Multi-type link system (6 built-in types)
├─ VideoEmbedder → Multi-provider video embed (3 providers)
└─ CustomPicker → Extensible content picker framework

EXTERNAL API INTEGRATIONS (4):
├─ AutodeskViewer → Autodesk Forge CAD viewer
├─ VimeoVideoSelector → Vimeo API integration
├─ InstagramMediaPicker → Instagram API integration
└─ AimbaseNewsletterPicker → Newsletter platform integration

SPECIALIZED INPUTS (8):
├─ SeoSettings → SEO metadata (title, description, OG, Twitter)
├─ SocialSettings → Social media account links
├─ GeocodedLocation → Google Maps location picker
├─ IconPicker → Icon selection UI
├─ PositionPicker → Positioning/alignment selector
├─ SideSizer → Column width configurator
├─ BlockPicker → Block element selector
└─ (Various utility pickers)
```

## Component Lookup

### LOOKUP: FlexibleLinks

```
LOCATION: FlexibleLinks/
TYPE: Extensible link system
EXTENSION POINT: IFlexibleLinkType interface

FILE STRUCTURE:
├─ Core/
│  ├─ FlexibleLinksPropertyEditor.cs
│  ├─ FlexibleLinksConfiguration.cs
│  └─ FlexibleLinksValueConverter.cs
├─ Types/
│  ├─ ExternalLinkType.cs (https:// links)
│  ├─ InternalLinkType.cs (internal content picker)
│  ├─ EmailLinkType.cs (mailto: links)
│  ├─ PhoneLinkType.cs (tel: links)
│  ├─ DownloadLinkType.cs (media file download)
│  └─ AnchorLinkType.cs (page anchors)
└─ Models/
   └─ FlexibleLink.cs (base model)

EXTENSION PATTERN:
public class {TypeName}LinkType : IFlexibleLinkType
{
    public string Name => "Display Name";
    public string Alias => "alias";
    public string Icon => "icon-link";

    public object GetModel(FlexibleLink link)
    {
        return new { Url, Title, Target, Custom Properties };
    }
}

COLLECTION BUILDER: Auto-discovers all IFlexibleLinkType implementations
BACKOFFICE UI: App_Plugins/FlexibleLinks/
```

### LOOKUP: VideoEmbedder

```
LOCATION: VideoEmbedder/
TYPE: Multi-provider video embed
EXTENSION POINT: IVideoProvider interface

FILE STRUCTURE:
├─ Core/
│  ├─ VideoEmbedderPropertyEditor.cs
│  └─ VideoEmbedderValueConverter.cs
├─ Providers/
│  ├─ YouTubeProvider.cs (YouTube video parsing)
│  ├─ VimeoProvider.cs (Vimeo video parsing)
│  └─ WistiaProvider.cs (Wistia video parsing)
├─ Models/
│  └─ VideoEmbed.cs
└─ Services/
   └─ VideoService.cs

PROVIDER PATTERN:
public class {Platform}Provider : IVideoProvider
{
    public string Name => "Platform Name";
    public bool CanHandle(string url) { }
    public VideoEmbed GetEmbed(string url) { }
}

COLLECTION BUILDER: Auto-discovers all IVideoProvider implementations
BACKOFFICE UI: App_Plugins/VideoEmbedder/
```

### LOOKUP: AutodeskViewer

```
LOCATION: AutodeskViewer/
TYPE: CAD file viewer integration
API: Autodesk Forge

FILE STRUCTURE:
├─ Core/
│  ├─ AutodeskViewerPropertyEditor.cs
│  └─ AutodeskViewerValueConverter.cs
├─ Services/
│  ├─ IAutodeskViewerService.cs
│  └─ AutodeskViewerService.cs (213 lines)
└─ Models/
   └─ AutodeskModel.cs

KEY SERVICE: AutodeskViewerService.cs
├─ GetModelsAsync() → List<AutodeskModel>
├─ GetModelByIdAsync(string id) → AutodeskModel
├─ GetAccessTokenAsync() → OAuth2 token with caching
└─ API BASE: https://developer.api.autodesk.com

CONFIGURATION (appsettings.json in UmbracoProject):
{
  "Autodesk": {
    "ClientId": "...",
    "ClientSecret": "...",
    "BucketKey": "krd_products"
  }
}

CONTROLLER: UmbracoProject/Controllers/AutodeskController.cs
├─ GET /api/autodesk/models
└─ GET /api/autodesk/models/{id}

BACKOFFICE UI: App_Plugins/AutodeskViewer/
```

### LOOKUP: VimeoVideoSelector

```
LOCATION: VimeoVideoSelector/
TYPE: Vimeo API integration
API: Vimeo API v3

FILE STRUCTURE:
├─ Core/
│  ├─ VimeoVideoSelectorPropertyEditor.cs
│  └─ VimeoVideoSelectorValueConverter.cs
├─ Services/
│  ├─ IVimeoService.cs
│  └─ VimeoService.cs
└─ Models/
   ├─ VimeoVideo.cs
   └─ VimeoFolder.cs

KEY SERVICE: VimeoService.cs
├─ GetVideosAsync() → List<VimeoVideo>
├─ GetFoldersAsync() → List<VimeoFolder>
└─ API BASE: https://api.vimeo.com/

CONFIGURATION (appsettings.json):
{
  "Video": {
    "BaseUrl": "https://api.vimeo.com/",
    "AccessToken": "..."
  }
}

BACKOFFICE UI: App_Plugins/VimeoVideoSelector/
```

### LOOKUP: InstagramMediaPicker

```
LOCATION: InstagramMediaPicker/
TYPE: Instagram API integration
API: Instagram Graph API

FILE STRUCTURE:
├─ Core/
│  ├─ InstagramMediaPickerPropertyEditor.cs
│  └─ InstagramMediaPickerValueConverter.cs
├─ Services/
│  ├─ IInstagramService.cs
│  └─ InstagramService.cs
└─ Models/
   └─ InstagramMedia.cs

KEY SERVICE: InstagramService.cs
├─ GetMediaAsync() → List<InstagramMedia>
├─ Uses Skybrud.Social.Instagram library
└─ OAuth2 authentication

DEPENDENCIES: Skybrud.Social.Instagram (1.0.0-beta008)
BACKOFFICE UI: App_Plugins/InstagramMediaPicker/
```

### LOOKUP: SeoSettings

```
LOCATION: SeoSettings/
TYPE: SEO metadata editor
SCOPE: Title, description, OG, Twitter cards, canonical

FILE STRUCTURE:
├─ Core/
│  ├─ SeoSettingsPropertyEditor.cs
│  ├─ SeoSettingsConfiguration.cs
│  └─ SeoSettingsValueConverter.cs
└─ Models/
   └─ SeoSettings.cs

MODEL PROPERTIES:
├─ MetaTitle
├─ MetaDescription
├─ OgTitle, OgDescription, OgImage
├─ TwitterTitle, TwitterDescription, TwitterImage
├─ CanonicalUrl
└─ NoIndex, NoFollow

BACKOFFICE UI: App_Plugins/SeoSettings/
└─ Tabs: General, OpenGraph, Twitter, Advanced
```

### LOOKUP: GeocodedLocation

```
LOCATION: GeocodedLocation/
TYPE: Google Maps location picker
FEATURES: Map click, geocoding, reverse geocoding

FILE STRUCTURE:
├─ Core/
│  ├─ GeocodedLocationPropertyEditor.cs
│  └─ GeocodedLocationValueConverter.cs
└─ Models/
   └─ GeocodedLocation.cs

MODEL PROPERTIES:
├─ Latitude (double)
├─ Longitude (double)
├─ Address (string)
└─ Zoom (int)

BACKOFFICE UI: App_Plugins/GeocodedLocation/
└─ Interactive Google Maps widget
```

### LOOKUP: CustomPicker

```
LOCATION: CustomPicker/
TYPE: Extensible content picker framework
PURPOSE: Base for creating specialized pickers

FILE STRUCTURE:
├─ Core/
│  ├─ CustomPickerPropertyEditor.cs
│  └─ CustomPickerValueConverter.cs
├─ Models/
│  └─ CustomPickerItem.cs
└─ Extensions/
   └─ CustomPickerExtensions.cs

USAGE: Extend for specialized content selection
BACKOFFICE UI: App_Plugins/CustomPicker/
```

### LOOKUP: AimbaseNewsletterPicker

```
LOCATION: AimbaseNewsletterPicker/
TYPE: Newsletter platform integration
FEATURES: Newsletter selection, Forms field, workflow

FILE STRUCTURE:
├─ Core/
│  ├─ AimbaseNewsletterPickerPropertyEditor.cs
│  └─ AimbaseNewsletterPickerValueConverter.cs
├─ FieldTypes/
│  └─ AimbaseNewsletterField.cs (Umbraco Forms field)
├─ Workflows/
│  └─ SubscribeToNewsletterWorkflow.cs
└─ Models/
   └─ AimbaseNewsletter.cs

INTEGRATION POINTS:
├─ Property Editor → Backoffice newsletter selection
├─ Forms Field → Frontend newsletter signup
└─ Workflow → Auto-subscribe on form submission

BACKOFFICE UI: App_Plugins/AimbaseNewsletterPicker/
```

### LOOKUP: SocialSettings

```
LOCATION: SocialSettings/
TYPE: Social media account links
PLATFORMS: Facebook, Twitter, Instagram, LinkedIn, YouTube

FILE STRUCTURE:
├─ Core/
│  ├─ SocialSettingsPropertyEditor.cs
│  └─ SocialSettingsValueConverter.cs
└─ Models/
   └─ SocialSettings.cs

MODEL PROPERTIES:
├─ FacebookUrl
├─ TwitterUrl
├─ InstagramUrl
├─ LinkedInUrl
├─ YouTubeUrl
└─ PinterestUrl

BACKOFFICE UI: App_Plugins/SocialSettings/
```

### LOOKUP: IconPicker, PositionPicker, SideSizer, BlockPicker

```
LOCATION: {EditorName}/
TYPE: Specialized UI controls
PURPOSE: Simple value selection

IconPicker:
├─ Icon selection from predefined set
└─ Returns icon class name

PositionPicker:
├─ Position/alignment selection
└─ Returns position value (left, center, right, etc.)

SideSizer:
├─ Column width configuration
└─ Returns size value

BlockPicker:
├─ Block element selection
└─ Returns block identifier

PATTERN (all similar):
├─ Core/{EditorName}PropertyEditor.cs
├─ Core/{EditorName}ValueConverter.cs
└─ wwwroot/App_Plugins/{editorName}/
```

## Collection Builder Pattern

```
MECHANISM: Auto-discovery of implementations

INTERFACE: IFlexibleLinkType
├─ Scan assembly for all implementations
├─ Register each as transient service
└─ Available in FlexibleLinks dropdown

INTERFACE: IVideoProvider
├─ Scan assembly for all implementations
├─ Register each as transient service
└─ Used by VideoEmbedder to parse URLs

REGISTRATION: SeedDataTypesComposer.cs
public class SeedDataTypesComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        builder.FlexibleLinks()
               .Add<ExternalLinkType>()
               .Add<InternalLinkType>()
               // Auto-discovered implementations
    }
}

BENEFIT: Add new type by creating class, no manual registration
```

## Backoffice Assets

```
LOCATION: wwwroot/App_Plugins/

STRUCTURE PER EDITOR:
{editorAlias}/
├─ package.manifest (Umbraco registration)
├─ {editor}.controller.js (Angular controller)
├─ {editor}.html (Angular template)
└─ {editor}.css (Editor styles)

EXAMPLES:
├─ FlexibleLinks/
├─ VideoEmbedder/
├─ AutodeskViewer/
├─ SeoSettings/
└─ [... 15 editors total]

FRAMEWORK: AngularJS (Umbraco backoffice standard)
```

## Service Integration Points

```
SERVICES WITH EXTERNAL APIS:

AutodeskViewerService:
├─ FILE: Services/AutodeskViewerService.cs (213 lines)
├─ INTERFACE: IAutodeskViewerService
├─ REGISTRATION: Singleton (token caching)
└─ CONSUMED BY: AutodeskController (UmbracoProject)

VimeoService:
├─ FILE: Services/VimeoService.cs
├─ INTERFACE: IVimeoService
├─ REGISTRATION: Transient
└─ CONSUMED BY: VimeoVideoSelector property editor

InstagramService:
├─ FILE: Services/InstagramService.cs
├─ INTERFACE: IInstagramService
├─ REGISTRATION: Transient
└─ CONSUMED BY: InstagramMediaPicker property editor

VIDEO SERVICE PATTERN:
├─ OAuth2 token management
├─ HTTP client for API calls
├─ Response parsing to models
├─ Error handling
└─ Token caching (if applicable)
```

## Configuration Requirements

```
FILE: appsettings.json (in UmbracoProject)

Autodesk:
{
  "Autodesk": {
    "ClientId": "...",
    "ClientSecret": "...",
    "BucketKey": "krd_products"
  }
}

Vimeo:
{
  "Video": {
    "BaseUrl": "https://api.vimeo.com/",
    "AccessToken": "..."
  }
}

Instagram:
{
  "Instagram": {
    "ClientId": "...",
    "ClientSecret": "..."
  }
}

PATTERN: External API credentials stored in UmbracoProject, not Seed.DataTypes
└─ Keeps library reusable, config environment-specific
```

## Extension Points

```
ADD NEW FLEXIBLE LINK TYPE:
├─ CREATE: FlexibleLinks/Types/{TypeName}LinkType.cs
├─ IMPLEMENT: IFlexibleLinkType
├─ DEFINE: Name, Alias, Icon, GetModel()
└─ AUTO-DISCOVERED: Collection builder finds it

ADD NEW VIDEO PROVIDER:
├─ CREATE: VideoEmbedder/Providers/{Platform}Provider.cs
├─ IMPLEMENT: IVideoProvider
├─ DEFINE: Name, CanHandle(), GetEmbed()
└─ AUTO-DISCOVERED: Collection builder finds it

ADD NEW PROPERTY EDITOR:
├─ CREATE: {EditorName}/Core/{EditorName}PropertyEditor.cs
├─ CREATE: {EditorName}/Core/{EditorName}ValueConverter.cs
├─ CREATE: {EditorName}/Models/{EditorName}.cs
├─ CREATE: wwwroot/App_Plugins/{editorAlias}/
│  ├─ package.manifest
│  ├─ {editor}.controller.js
│  ├─ {editor}.html
│  └─ {editor}.css
└─ REGISTER: In composer if needed
```

## File Count by Category

```
TOTAL: 115 C# files

BY EDITOR (approximate):
├─ FlexibleLinks: 12 files (6 types + core)
├─ VideoEmbedder: 8 files (3 providers + core)
├─ AutodeskViewer: 6 files (service + models + core)
├─ VimeoVideoSelector: 6 files
├─ InstagramMediaPicker: 6 files
├─ AimbaseNewsletterPicker: 8 files (field + workflow)
├─ CustomPicker: 8 files
├─ SeoSettings: 4 files
├─ GeocodedLocation: 4 files
├─ SocialSettings: 4 files
└─ Others (6 editors): ~45 files

PLUS: Shared utilities, extensions, base classes
```

## Dependencies

```
NUGET PACKAGES:
├─ Umbraco.Cms.Core (13.12.0)
├─ Skybrud.Social.Facebook (1.0.0-beta006)
└─ Skybrud.Social.Instagram (1.0.0-beta008)

PROJECT REFERENCES:
└─ Seed.Core (base library)

REFERENCED BY:
├─ Seed.Backoffice.Extensions
└─ UmbracoProject
```

## Quick Lookup

```
QUERY: Find editor for X

Link management → FlexibleLinks
Video embedding → VideoEmbedder
CAD files → AutodeskViewer
Vimeo videos → VimeoVideoSelector
Instagram media → InstagramMediaPicker
Newsletter → AimbaseNewsletterPicker
SEO metadata → SeoSettings
Location → GeocodedLocation
Social links → SocialSettings
Icons → IconPicker
Positioning → PositionPicker
Column widths → SideSizer
Block selection → BlockPicker
Custom picker → CustomPicker (extend this)

QUERY: Find file for X

Property editor implementation:
└─ {EditorName}/Core/{EditorName}PropertyEditor.cs

Value converter:
└─ {EditorName}/Core/{EditorName}ValueConverter.cs

Model:
└─ {EditorName}/Models/{EditorName}.cs

Service:
└─ {EditorName}/Services/{ServiceName}Service.cs

Backoffice UI:
└─ wwwroot/App_Plugins/{editorAlias}/

FlexibleLinks type:
└─ FlexibleLinks/Types/{TypeName}LinkType.cs

Video provider:
└─ VideoEmbedder/Providers/{Platform}Provider.cs
```

## Key Interfaces

```
INTERFACE: IFlexibleLinkType
├─ LOCATION: FlexibleLinks/
├─ PURPOSE: Define new link types
├─ METHODS:
│  ├─ string Name { get; }
│  ├─ string Alias { get; }
│  ├─ string Icon { get; }
│  └─ object GetModel(FlexibleLink link)
└─ IMPLEMENTATIONS: 6 built-in (External, Internal, Email, Phone, Download, Anchor)

INTERFACE: IVideoProvider
├─ LOCATION: VideoEmbedder/
├─ PURPOSE: Define video platform support
├─ METHODS:
│  ├─ string Name { get; }
│  ├─ bool CanHandle(string url)
│  └─ VideoEmbed GetEmbed(string url)
└─ IMPLEMENTATIONS: 3 built-in (YouTube, Vimeo, Wistia)

INTERFACE: IAutodeskViewerService
├─ LOCATION: AutodeskViewer/Services/
├─ PURPOSE: Autodesk Forge API access
├─ METHODS:
│  ├─ Task<List<AutodeskModel>> GetModelsAsync()
│  ├─ Task<AutodeskModel> GetModelByIdAsync(string id)
│  └─ Task<string> GetAccessTokenAsync()
└─ IMPLEMENTATION: AutodeskViewerService (213 lines)

INTERFACE: IVimeoService
├─ LOCATION: VimeoVideoSelector/Services/
├─ PURPOSE: Vimeo API access
└─ METHODS: GetVideosAsync(), GetFoldersAsync()

INTERFACE: IInstagramService
├─ LOCATION: InstagramMediaPicker/Services/
├─ PURPOSE: Instagram API access
└─ METHODS: GetMediaAsync()
```
