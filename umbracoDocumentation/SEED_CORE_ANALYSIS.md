# Seed.Core - Component Reference (LLM-Optimized)

## Project Classification

```
TYPE: .NET 8 Class Library
SCOPE: Generic/Reusable Infrastructure
FILES: 145 C# files
REFERENCED BY: All C# projects (Seed.DataTypes, Seed.Backoffice.Extensions, UmbracoProject)
PHILOSOPHY: "Could this be used in a different Umbraco project?" = YES → Belongs here
ROLE: Foundation layer providing base converters, services, and infrastructure
```

## Component Inventory Matrix

```
COMPONENT           COUNT    ROLE                        AUTO-REGISTER    EXTENSIBLE
==========================================================================================
ApiSafeConverters   18       Data transformation         ✅ Yes           ✅ Yes
Services            9        Business logic/infra        ❌ Manual DI      ⚠️ Via DI
Models              50+      Data structures             N/A              N/A
Extensions          10+      Utility methods             N/A              ✅ Yes
Importers           6        Content migration           ✅ Yes           ✅ Yes
Stringifiers        4        Search indexing             ✅ Yes           ✅ Yes
Virtual Pages       Base     Dynamic routing             ✅ Yes           ✅ Yes
```

## ApiSafeConverters Quick Lookup (18 Total)

```
EDITOR ALIAS                      CONVERTER CLASS                    OUTPUT TYPE
================================================================================================
Umbraco.MediaPicker3              MediaApiSafeConverter              ApiSafeImage|ApiSafeVideo|ApiSafeFile
Umbraco.ContentPicker             PublishedContentApiSafeConverter   JsonPublishedContent
Umbraco.MultiNodeTreePicker       PublishedContentApiSafeConverter   JsonPublishedContent
Umbraco.BlockGrid                 BlockGridApiSafeConverter          Nested JSON structure
Umbraco.BlockList                 BlockListApiSafeConverter          Array of block elements
Umbraco.TinyMCE                   RichContentApiSafeConverter        HTML string
Umbraco.RichText                  RichContentApiSafeConverter        HTML string
Umbraco.DateTime                  DatePickerApiConverter             ISO 8601 string
UmbracoForms.FormPicker           UmbracoFormApiSafeConverter        ApiSafeForm
Umbraco.Grid (legacy)             GridApiSafeConverter               Grid structure
Umbraco.NestedContent (legacy)    NestedContentApiSafeConverter      Array of elements

INFRASTRUCTURE CONVERTERS:
├─ BaseApiSafeConverter → Abstract base for all converters
├─ BaseContentTypeApiSafeConverter → Base for Block Grid/List elements
└─ ApiSafeConvertersCollection → Collection manager
```

## Automatic Passthrough Editors (No Converter Needed)

```
EDITOR ALIAS                   OUTPUT TYPE    NOTES
=======================================================================
Umbraco.TextBox                string         Direct passthrough
Umbraco.TextArea               string         Direct passthrough
Umbraco.Integer                int            Direct passthrough
Umbraco.Decimal                decimal        Direct passthrough
Umbraco.TrueFalse              bool           Direct passthrough
Umbraco.DropDown.Flexible      string         Direct passthrough
Umbraco.CheckBoxList           string[]       Direct passthrough
Umbraco.RadioButtonList        string         Direct passthrough
Umbraco.Slider                 decimal        Direct passthrough
Umbraco.ColorPicker            string         Direct passthrough

COVERAGE: ~80% of property editors use automatic passthrough
```

## Services Inventory (9 Core Services)

```
SERVICE              INTERFACE           PURPOSE                           LIFETIME      KEY METHODS
===================================================================================================================
ExamineService       IExamineService     Lucene search wrapper             Singleton     Search(...), Complex queries
SearchService        ISearchService      High-level search abstraction     Singleton     Site-wide search, faceting
ImageService         IImageService       Image processing/manipulation     Singleton     Resize, crop, optimize
EmailService         IEmailService       Email sending via SMTP            Singleton     SendEmail(...)
TokenService         ITokenService       JWT token ops                     Singleton     Generate, validate, decode
DataService          -                   Main API data access              Singleton     GetPage, GetCollection, etc.
SeedHelper           -                   Utility helpers                   Singleton     GetVersionedPath, RenderPartial
```

## DataApiController Endpoint Map

```
METHOD   ENDPOINT                              PURPOSE                                    AUTH
=============================================================================================================
GET      /api/data/pages                       List all pages for sitemap                API Key
GET      /api/data/page?slug={slug}            Get single page by URL                    API Key
GET      /api/data/error-page?errorCode={n}    Get error page (404, 500, etc.)          API Key
GET      /api/data/modals/{guid}               Get modal content                         API Key
GET      /api/data/collection                  Get filtered/paginated collection         API Key
GET      /api/data/collectionFilters           Get available filter options              API Key
GET      /api/data/boat-build-exists?key={k}   Validate boat configuration               API Key
POST     /api/data/download-files              Batch download media as ZIP               API Key
POST     /api/data/log                         Frontend error logging                    API Key
GET      /api/data/sitemap                     XML sitemap generation                    API Key
GET      /api/data/robots                      robots.txt generation                     API Key
GET      /api/data/redirects                   All URL redirects                         API Key
GET      /api/data/redirect?url={url}          Single redirect lookup                    API Key

AUTHENTICATION:
├─ API Key: Required in Api-Key header for all requests
└─ Preview Key: Required in Preview-Key header for preview mode
```

## Model Classification

```
CATEGORY              MODELS                                      LOCATION
===========================================================================================
Core API-Safe         ApiSafeFile, ApiSafeImage, ApiSafeVideo    Models/Image/
                      JsonPublishedContent                        Models/
                      ApiSafeForm                                 Models/

Request/Response      GetCollectionRequest                        Models/
                      ResponseModel                               Models/
                      FileDownloadRequest                         Models/
                      LogData                                     Models/

Search                PublishedContentSearchParameters            Models/Search/
                      ExamineSearchModel                          Models/Search/
                      ExamineSearchFieldWeight                    Models/Search/
                      SortingDefinition                           Models/Search/

Domain-Specific       Blog models                                 Models/Blog/
                      Brochure models                             Models/Brochures/
                      Carousel models                             Models/Carousel/
                      Dealer models                               Models/Dealer/
                      Gallery models                              Models/Gallery/
                      Event models                                Models/Event/

Utility               Redirect                                    Models/
                      SitemapEntry                                Models/
                      PageCultureInfo                             Models/
                      BuildSheetData                              Models/
                      ImportSettings                              Models/
                      BlockModel                                  Models/
```

## Decision Tree: Does This Belong in Seed.Core?

```
QUERY: Should this component be in Seed.Core?

├─ Is it a converter for standard Umbraco property editor?
│  ├─ Standard editor (MediaPicker, ContentPicker, BlockGrid)? → YES, Seed.Core ✅
│  └─ Custom project editor (boats, products)? → NO, Seed.Backoffice.Extensions
│
├─ Is it infrastructure/service used across projects?
│  ├─ Generic (caching, search, email)? → YES, Seed.Core ✅
│  └─ Project-specific (product catalog, quotes)? → NO, Seed.Backoffice.Extensions
│
├─ Is it a shared data model?
│  ├─ Generic (ApiSafeImage, search params)? → YES, Seed.Core ✅
│  └─ Project-specific (boat details)? → NO, Seed.Backoffice.Extensions
│
├─ Is it an extension method for Umbraco types?
│  ├─ Generic Umbraco helpers? → YES, Seed.Core ✅
│  └─ Project-specific helpers? → NO, Seed.Backoffice.Extensions
│
└─ Is it reusable across different industries?
   ├─ Could hotel/school/store use it? → YES, Seed.Core ✅
   └─ Unique to this project? → NO, Seed.Backoffice.Extensions
```

## Converter Pattern Reference

### Pattern 1: BaseApiSafeConverter Implementation

```csharp
WHEN: Converting standard Umbraco property editor
WHERE: Seed.Core/ApiSafeConverters/

public class MyApiSafeConverter : BaseApiSafeConverter
{
    // REQUIRED: Editor alias for auto-registration
    public override string[] EditorAlias => new[] { "Umbraco.MyEditor" };

    // REQUIRED: Conversion logic
    public override object ConvertToApiSafeValue(
        object value,
        string? culture,
        string? segment,
        List<int> ids,
        Dictionary<string, object> additionalData)
    {
        // Transform value to JSON-safe structure
        return apiSafeValue;
    }
}

REGISTRATION: Automatic via reflection (no manual registration needed)
DISCOVERY: EditorAlias property used for matching
```

### Pattern 2: BaseContentTypeApiSafeConverter Implementation

```csharp
WHEN: Converting Block Grid/List element types
WHERE: Seed.Core/ApiSafeConverters/ OR Seed.Backoffice.Extensions/ApiSafeConverters/

public class MyElementConverter : BaseContentTypeApiSafeConverter
{
    // REQUIRED: Content type aliases for matching
    public override string[] ContentTypes => new[] { "myElement" };

    // REQUIRED: Element conversion logic
    public override object ConvertElement(
        IPublishedElement element,
        string? culture,
        string? segment,
        List<int> ids,
        Dictionary<string, object> additionalData)
    {
        // Transform element to JSON-safe structure
        return elementData;
    }
}

REGISTRATION: Automatic via reflection
DISCOVERY: ContentTypes property used for matching
```

### Pattern 3: Using Converters

```csharp
LOCATION: Services, Controllers, Other Converters

// INJECT: Lazy to prevent circular dependencies
private readonly Lazy<ApiSafeConvertersCollection> _converters;

public MyService(Lazy<ApiSafeConvertersCollection> converters)
{
    _converters = converters;
}

// USAGE: Find converter by property
var converter = _converters.Value.FirstOrDefault(x => x.IsEditor(property));
if (converter != null)
{
    var apiSafeValue = converter.ConvertToApiSafeValue(
        value, culture, segment, ids, additionalData
    );
}

// USAGE: Find converter by alias
var converter = _converters.Value.FirstOrDefault(
    x => x.IsEditor("Umbraco.MediaPicker3")
);
```

## Service Pattern Reference

### Pattern 1: ExamineService Search

```csharp
WHEN: Performing content search
WHERE: Any service/controller needing search

// INJECT
private readonly IExamineService _examineService;

// SIMPLE SEARCH
var results = _examineService.Search("ExternalIndex", "searchTerm");

// COMPLEX SEARCH
var results = _examineService.Search(new PublishedContentSearchParameters
{
    ExamineIndex = "ExternalIndex",
    AllowedContentTypes = ["boat", "product"],
    SortingDefinition = new SortingDefinition
    {
        SortType = Examine.Search.SortType.String,
        Alias = "nodeName",
        Direction = SortDirectionEnum.Ascending
    },
    Filters = new List<ExamineSearchModel>
    {
        new ExamineSearchModel
        {
            Keywords = ["search term"],
            Fields = new List<ExamineSearchFieldWeight>
            {
                new ExamineSearchFieldWeight
                {
                    Name = "nodeName",
                    Weight = 5,
                    Wildcard = true
                }
            }
        }
    }
});

FEATURES:
├─ Content type filtering
├─ Parent node filtering
├─ Keyword search with field weighting
├─ Wildcard support
├─ Range queries
├─ Sorting (asc/desc)
├─ AND/OR logic
└─ Performance logging
```

### Pattern 2: DataService Content Retrieval

```csharp
WHEN: Retrieving content for API responses
WHERE: DataApiController

// INJECT
private readonly DataService _dataService;

// GET SINGLE PAGE
var page = await _dataService.GetPage(slug, preview: false, culture: "en-US");

// GET ALL PAGES (sitemap)
var pages = await _dataService.GetPages(preview: false, culture: "en-US");

// GET COLLECTION (filtered/paginated)
var collection = await _dataService.GetCollection(new GetCollectionRequest
{
    ParentId = 1234,
    ContentTypes = ["boat"],
    PageSize = 20,
    PageNumber = 1,
    SortField = "name",
    SortDirection = SortDirectionEnum.Ascending
});

// GET ERROR PAGE
var errorPage = await _dataService.GetErrorPage(404, preview: false, culture: "en-US");

// GET MODAL
var modal = await _dataService.GetModal(guid, culture: "en-US", segment: null);

PATTERN: All methods return API-safe converted content
```

### Pattern 3: SeedHelper Utilities

```csharp
WHEN: Need versioned paths, partial rendering, or manual conversion
WHERE: Controllers, views, services

// INJECT
private readonly SeedHelper _seedHelper;

// CACHE BUSTING
var cssPath = _seedHelper.GetVersionedPath("/css/site.css");
// Returns: /css/site.css?v=abc123hash

// RENDER PARTIAL TO STRING (email templates)
var emailHtml = await _seedHelper.RenderPartialToString(
    "~/Views/Emails/Welcome.cshtml",
    emailModel
);

// MANUAL CONTENT CONVERSION
var jsonContent = _seedHelper.ToJson(
    umbracoContent,
    culture: "en-US",
    segment: null,
    additionalData: new Dictionary<string, object>()
);

USE CASES:
├─ cssPath → Static asset cache busting
├─ emailHtml → Email template rendering
└─ jsonContent → Manual API-safe conversion
```

## Extension Points

### Add New ApiSafeConverter

```
STEP 1: Create converter class
├─ LOCATION: Seed.Core/ApiSafeConverters/{Name}ApiSafeConverter.cs
├─ INHERIT: BaseApiSafeConverter OR BaseContentTypeApiSafeConverter
└─ IMPLEMENT: EditorAlias/ContentTypes + ConvertToApiSafeValue/ConvertElement

STEP 2: No registration needed
└─ Auto-discovered via reflection

STEP 3: Restart application
└─ Converter automatically available in collection

EXAMPLE:
public class TagsApiSafeConverter : BaseApiSafeConverter
{
    public override string[] EditorAlias => new[] { "Umbraco.Tags" };

    public override object ConvertToApiSafeValue(...)
    {
        var tags = value as IEnumerable<string>;
        return tags?.ToArray() ?? Array.Empty<string>();
    }
}
```

### Add New Service

```
STEP 1: Create interface + implementation
├─ INTERFACE: Seed.Core/Services/IMyService.cs
└─ IMPLEMENTATION: Seed.Core/Services/MyService.cs

STEP 2: Register in CoreComposer
├─ FILE: Seed.Core/CoreComposer.cs
└─ ADD: builder.Services.AddSingleton<IMyService, MyService>();

STEP 3: Inject where needed
└─ CONSTRUCTOR: public MyClass(IMyService myService) { ... }

EXAMPLE:
public interface IMyService
{
    Task<string> DoSomething(int id);
}

public class MyService : IMyService
{
    public async Task<string> DoSomething(int id)
    {
        // Implementation
    }
}
```

### Add New Importer

```
STEP 1: Create importer class
├─ LOCATION: Seed.Core/Import/{Name}Importer.cs
└─ IMPLEMENT: IImporter interface

STEP 2: Implement methods
├─ CanImport(string editorAlias) → Return true if handles this editor
└─ Import(...) → Transform old format to new format

STEP 3: No registration needed
└─ Auto-discovered via ImporterCollectionBuilder

USE CASE: Content migrations, Umbraco version upgrades

EXAMPLE:
public class MyImporter : IImporter
{
    public bool CanImport(string editorAlias)
    {
        return editorAlias == "OldEditor.Alias";
    }

    public object Import(object oldValue)
    {
        // Transform to new format
        return newValue;
    }
}
```

### Add New Stringifier

```
STEP 1: Create stringifier class
├─ LOCATION: Seed.Core/Stringifier/{Name}Stringifier.cs
└─ INHERIT: BaseStringifier OR implement IStringify

STEP 2: Implement methods
├─ CanStringify(string editorAlias) → Return true if handles this editor
└─ Stringify(object value) → Extract plain text for search indexing

STEP 3: No registration needed
└─ Auto-discovered via StringifierComposer

USE CASE: Extract searchable text from complex content for Examine indexing

EXAMPLE:
public class MyStringifier : BaseStringifier
{
    public override bool CanStringify(string editorAlias)
    {
        return editorAlias == "My.CustomEditor";
    }

    public override string Stringify(object value)
    {
        // Extract plain text
        return plainText;
    }
}
```

### Add New Virtual Page Handler

```
STEP 1: Create handler class
├─ LOCATION: Seed.Core/VirtualPages/{Name}VirtualPageHandler.cs
└─ IMPLEMENT: IVirtualPageHandler

STEP 2: Implement methods
├─ ShouldHandle(string url) → Return true if this handler processes URL
└─ HandleRequest(HttpContext context) → Generate page content

STEP 3: Register in composer
├─ FILE: Seed.Core/CoreComposer.cs (or custom composer)
└─ ADD: builder.VirtualPages().Add<MyVirtualPageHandler>();

USE CASE: Dynamic pages (search results, generated content, API-driven pages)

EXAMPLE:
public class SearchVirtualPageHandler : IVirtualPageHandler
{
    public bool ShouldHandle(string url)
    {
        return url.StartsWith("/search");
    }

    public VirtualPageModel HandleRequest(HttpContext context)
    {
        // Generate page content
        return virtualPage;
    }
}
```

## Dependency Injection Patterns

### Singleton Services

```csharp
WHEN: Stateless services, shared resources
WHERE: CoreComposer.cs

builder.Services.AddSingleton<IExamineService, ExamineService>();
builder.Services.AddSingleton<ISearchService, SearchService>();
builder.Services.AddSingleton<IImageService, ImageService>();
builder.Services.AddSingleton<IEmailService, EmailService>();
builder.Services.AddSingleton<ITokenService, TokenService>();
builder.Services.AddSingleton<SeedHelper>();
builder.Services.AddSingleton<DataService>();

LIFETIME: Single instance for application lifetime
THREAD SAFETY: Must be thread-safe
```

### Lazy Injection (Circular Dependencies)

```csharp
WHEN: Circular dependency (e.g., converter needs converter collection)
WHERE: Constructor injection

// INJECT
private readonly Lazy<ApiSafeConvertersCollection> _converters;

public MyConverter(Lazy<ApiSafeConvertersCollection> converters)
{
    _converters = converters;
}

// ACCESS
var converter = _converters.Value.FirstOrDefault(...);

PATTERN: Defers initialization until .Value accessed
PREVENTS: Circular dependency errors at DI container setup
```

## Collection Builder Pattern

```
PATTERN: Extensible collections with auto-discovery

USED FOR:
├─ ApiSafeConverters
├─ Importers
├─ Stringifiers
└─ Virtual Page Handlers

ARCHITECTURE:
├─ IExtensible → Interface implemented by items
├─ ExtensibleCollection → Collection of items
├─ ExtensibleCollectionBuilder → Builder for registration
└─ Composer → Registers builder

REGISTRATION:
builder.Extensibles().Add(() => builder.TypeLoader.GetTypes<IExtensible>());

AUTO-DISCOVERY: Yes (via reflection)
MANUAL ADDITION: Optional (builder.Extensibles().Add<MyExtensible>())
```

## Performance Patterns

### Caching Strategies

```
FILE HASH CACHING (SeedHelper.GetVersionedPath):
├─ Cache MD5 hash of file content
├─ Use FileSystemWatcher for invalidation
├─ Lifetime: Until file modified
└─ Purpose: Asset cache busting

EXAMINE QUERY CACHING (ExamineService):
├─ Optional caching at service layer
├─ Consider distributed cache for multi-server
├─ Invalidation: Content save/publish events
└─ Purpose: Reduce Lucene query overhead

CONVERTER PERFORMANCE:
├─ Called frequently (every API request)
├─ Keep conversions fast (avoid N+1 queries)
├─ Use Lazy<> for expensive lookups
└─ Batch operations where possible
```

### Examine Index Optimization

```
STRATEGY:
├─ Separate indexes for different content types
├─ Custom indexes for products, blogs, dealers
├─ Configurable field analyzers
└─ Stringifiers extract searchable text efficiently

CONFIGURATION:
├─ FILE: Seed.Core/ConfigureIndexOptions.cs
├─ DEFINE: Indexed fields
├─ SET: Analyzers (StandardAnalyzer, KeywordAnalyzer, etc.)
└─ CONFIGURE: Field types (text, number, date)

PERFORMANCE:
├─ Use field weighting for relevance
├─ Limit result sets (default 10,000)
├─ Performance logging with stopwatch
└─ Wildcard queries carefully (can be slow)
```

## Security Patterns

### API Key Validation

```
LOCATION: DataApiController
METHOD: All endpoints

// VALIDATE API KEY
var apiKey = Request.Headers["Api-Key"].FirstOrDefault();
if (apiKey != _configuration["Seed:ApiKey"])
{
    return Unauthorized();
}

// VALIDATE PREVIEW KEY (for preview mode)
var previewKey = Request.Headers["Preview-Key"].FirstOrDefault();
if (preview && previewKey != _configuration["Seed:PreviewKey"])
{
    return Unauthorized();
}

CONFIGURATION:
├─ appsettings.json → Seed:ApiKey, Seed:PreviewKey
├─ Environment variables → Override per environment
└─ NEVER commit keys to source control

ROTATION: Periodically update keys in all environments
```

### JWT Token Management

```
SERVICE: TokenService (Membership/TokenService.cs)

GENERATION:
var token = _tokenService.GenerateToken(user, claims);

VALIDATION:
var isValid = _tokenService.ValidateToken(token);

DECODING:
var decodedToken = _tokenService.DecodeToken(token);

BEST PRACTICES:
├─ Secure signing key (store in environment variable)
├─ Appropriate expiration (15-60 minutes for access token)
├─ Refresh token rotation
├─ Claims validation (issuer, audience, expiration)
└─ HTTPS only for token transmission
```

## Troubleshooting Lookup

```
ISSUE                                       SOLUTION
=================================================================================================
ApiSafeConverter not found                  ├─ Verify EditorAlias matches exactly
                                            ├─ Check converter in Seed.Core or referenced project
                                            └─ Ensure project reference in UmbracoProject

Examine query returns no results            ├─ Check index exists: _examineManager.TryGetIndex(...)
                                            ├─ Verify content is indexed (Examine dashboard)
                                            ├─ Check field names are correct
                                            └─ Test with simple query first

Circular dependency with converters         ├─ Use Lazy<ApiSafeConvertersCollection> injection
                                            └─ Never inject collection directly in converters

Preview mode not working                    ├─ Check both Api-Key and Preview-Key headers
                                            ├─ Verify keys match configuration
                                            └─ Ensure preview parameter is true

Converter not auto-registering              ├─ Verify EditorAlias property is set correctly
                                            ├─ Ensure class inherits BaseApiSafeConverter
                                            ├─ Check project is referenced in UmbracoProject
                                            └─ Restart application

Service not injecting                       ├─ Verify registration in CoreComposer
                                            ├─ Check interface matches implementation
                                            └─ Ensure correct lifetime (Singleton, Scoped, Transient)
```

## Component File Map

```
COMPONENT                      FILE PATH                                    KEY CLASSES
=================================================================================================
ApiSafeConverters              ApiSafeConverters/                           18 converter classes
├─ Base Infrastructure         BaseApiSafeConverter.cs                      BaseApiSafeConverter
                               IApiSafeConverter.cs                          IApiSafeConverter
                               BaseContentTypeApiSafeConverter.cs           BaseContentTypeApiSafeConverter
                               ApiSafeConvertersCollection.cs                ApiSafeConvertersCollection
├─ Media Converters            MediaApiSafeConverter.cs                     MediaApiSafeConverter
├─ Content Converters          PublishedContentApiSafeConverter.cs          PublishedContentApiSafeConverter
├─ Block Converters            BlockGridApiSafeConverter.cs                 BlockGridApiSafeConverter
                               BlockListApiSafeConverter.cs                  BlockListApiSafeConverter
└─ Legacy Converters           GridApiSafeConverter.cs                      GridApiSafeConverter
                               NestedContentApiSafeConverter.cs              NestedContentApiSafeConverter

Services                       Services/                                     9 service classes
├─ ExamineService              ExamineService.cs                            IExamineService, ExamineService
├─ SearchService               SearchService.cs                             ISearchService, SearchService
├─ ImageService                ImageService.cs                              IImageService, ImageService
├─ EmailService                EmailService.cs                              IEmailService, EmailService
└─ TokenService                Membership/TokenService.cs                   ITokenService, TokenService

Controllers                    /                                             2 controller classes
├─ DataApiController           DataApiController.cs                         DataApiController
└─ MembershipApiController     Membership/MembershipApiController.cs        MembershipApiController

Core Utilities                 /                                             Utility classes
├─ DataService                 DataService.cs                               DataService
├─ SeedHelper                  SeedHelper.cs                                SeedHelper
└─ CoreComposer                CoreComposer.cs                              CoreComposer

Models                         Models/                                       50+ model classes
├─ Core API-Safe               Image/ApiSafeImage.cs                        ApiSafeImage, ApiSafeVideo, ApiSafeFile
                               JsonPublishedContent.cs                       JsonPublishedContent
├─ Search Models               Search/                                      Search parameter models
└─ Domain Models               Blog/, Dealer/, Event/, Gallery/, etc.       Domain-specific DTOs

Extensions                     Extensions/                                   Extension method classes
├─ IPublishedContentExtensions IPublishedContentExtensions.cs               Navigation, property helpers
├─ StringExtensions            StringExtensions.cs                          String manipulation
└─ WebCompositionExtensions    WebCompositionExtensions.cs                  DI helpers

Import                         Import/                                       6 importer classes
├─ Base Infrastructure         IImporter.cs, ImporterBase.cs                Import interfaces
└─ Specific Importers          GridImporter.cs, MediaPickerImporter.cs      Content migration tools

Stringifier                    Stringifier/                                  4 stringifier classes
├─ Base Infrastructure         IStringify.cs, BaseStringifier.cs            Stringifier interfaces
└─ Specific Stringifiers       RTEStringifier.cs, GridStringifier.cs        Text extraction for indexing

VirtualPages                   VirtualPages/                                 Virtual page infrastructure
├─ Base Infrastructure         IVirtualPageHandler.cs                       Handler interface
└─ Collection                  VirtualPageCollection.cs                     Handler collection

GraphQL                        GraphQL/                                      GraphQL support structures
Caching                        Caching/Core/                                 Caching infrastructure
ContentTemplateApplicator      ContentTemplateApplicator/                    Template application
Enums                          Enums/                                        Shared enumerations
```

## NuGet Dependencies Reference

```
PACKAGE                                VERSION      PURPOSE
=================================================================================================
Umbraco.Cms.Core                       13.12.0      Core Umbraco CMS functionality
Umbraco.Cms.Imaging.ImageSharp         13.12.0      Image processing
Umbraco.Cms.Web.BackOffice             13.12.0      Backoffice integration
Umbraco.Forms.Core                     13.7.0       Forms functionality
Umbraco.Forms.Core.Providers           13.7.0       Forms providers
Umbraco.Forms.Web                      13.7.0       Forms web integration
UrlTracker.Core                        13.1.0       URL tracking/redirects
UrlTracker.Web                         13.1.0       URL tracker web integration
Skybrud.Social.Facebook                1.0.0-beta   Facebook API integration
Skybrud.Social.Instagram               1.0.0-beta   Instagram API integration
MediaInfo.Wrapper.Core                 21.9.3       Video metadata extraction
Microsoft.AspNetCore.Authentication    8.0.16       JWT Bearer auth
.JwtBearer
```

## Anti-Patterns (What NOT to Do)

```
❌ NEVER: Put project-specific logic in Seed.Core
   ✅ INSTEAD: Use Seed.Backoffice.Extensions for project-specific code

❌ NEVER: Inject ApiSafeConvertersCollection directly in converters
   ✅ INSTEAD: Use Lazy<ApiSafeConvertersCollection>

❌ NEVER: Manually register ApiSafeConverters
   ✅ INSTEAD: Set EditorAlias/ContentTypes, auto-discovery handles registration

❌ NEVER: Perform N+1 queries in converters
   ✅ INSTEAD: Batch load related content, cache lookups

❌ NEVER: Return IPublishedContent directly from DataService
   ✅ INSTEAD: Always convert to API-safe models via converters

❌ NEVER: Hard-code API keys in source
   ✅ INSTEAD: Store in environment variables/configuration

❌ NEVER: Throw exceptions in converters for missing data
   ✅ INSTEAD: Return null or empty structures, log warnings

❌ NEVER: Block async calls with .Result or .Wait()
   ✅ INSTEAD: Use async/await throughout call chain
```

## Quick Action Patterns

### PATTERN: Add Property to Existing Model

```
WHEN: Need to extend ApiSafeImage, JsonPublishedContent, etc.
WHERE: Seed.Core/Models/

STEP 1: Add property to C# model
├─ FILE: Models/Image/ApiSafeImage.cs (or relevant model)
└─ ADD: public string MyNewProperty { get; set; }

STEP 2: Update converter to populate property
├─ FILE: ApiSafeConverters/MediaApiSafeConverter.cs (or relevant converter)
└─ SET: MyNewProperty = ...

STEP 3: Update TypeScript types in frontend
├─ FILE: Seed.Web/lib/umbraco/types/imageModel.type.ts
└─ ADD: myNewProperty: string

STEP 4: Validate TypeScript compilation
└─ RUN: cd src/Seed.Web && npx tsc --noEmit
```

### PATTERN: Add New Endpoint to DataApiController

```
WHEN: Need new API endpoint
WHERE: Seed.Core/DataApiController.cs

STEP 1: Add method to DataService
├─ FILE: Seed.Core/DataService.cs
└─ ADD: public async Task<MyResult> GetMyData(...) { ... }

STEP 2: Add controller action
├─ FILE: Seed.Core/DataApiController.cs
└─ ADD:
    [HttpGet("my-data")]
    public async Task<IActionResult> GetMyData([FromQuery] string param)
    {
        // Validate API key
        // Call DataService
        // Return result
    }

STEP 3: Test endpoint
└─ URL: https://localhost/api/data/my-data?param=value
    HEADER: Api-Key: {key}
```

### PATTERN: Extend ExamineService Search

```
WHEN: Need custom search logic
WHERE: Seed.Core/Services/ExamineService.cs

STEP 1: Add method to IExamineService interface
├─ FILE: Seed.Core/Services/IExamineService.cs
└─ ADD: ISearchResults MyCustomSearch(MySearchParams params);

STEP 2: Implement in ExamineService
├─ FILE: Seed.Core/Services/ExamineService.cs
└─ ADD: Method implementation with Lucene query building

STEP 3: Use in DataService or controllers
└─ INJECT: IExamineService
    CALL: _examineService.MyCustomSearch(params)
```
