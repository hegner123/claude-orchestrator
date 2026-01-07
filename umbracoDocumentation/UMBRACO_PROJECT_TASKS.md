# UmbracoProject - Task Decision Guide

## Task Classification System

```
BELONGS IN UMBRACOPROJECT:
✅ Configuration (appsettings.json)
✅ Server-side templates (Razor views)
✅ Project-specific API controllers (thin HTTP adapters)
✅ RTE customization (formats, styles)
✅ Static assets (wwwroot/)
✅ Umbraco packages (App_Plugins/)
✅ Application startup (Program.cs)
✅ Web server config (web.config)
✅ Schema storage (UDA files - auto-generated only)

DOES NOT BELONG:
❌ Business logic → Seed.Backoffice.Extensions or Seed.Core
❌ ApiSafeConverters → Seed.Backoffice.Extensions or Seed.Core
❌ Property Editors → Seed.DataTypes
❌ Services → Seed.Backoffice.Extensions or Seed.Core
❌ React components → Seed.Web
❌ Reusable utilities → Seed.Core
❌ Unit testable code → Seed.* libraries
```

## Decision Tree: Where Does This Task Belong?

```
QUERY: I need to implement something...

├─ Is it C# business logic?
│  └─ YES → Seed.Backoffice.Extensions or Seed.Core (NOT UmbracoProject)
│
├─ Is it a custom property editor?
│  └─ YES → Seed.DataTypes (NOT UmbracoProject)
│
├─ Is it an ApiSafeConverter?
│  └─ YES → Seed.Backoffice.Extensions or Seed.Core (NOT UmbracoProject)
│
├─ Is it a React component?
│  └─ YES → Seed.Web (NOT UmbracoProject)
│
├─ Is it configuration (API keys, settings)?
│  └─ YES → UmbracoProject/appsettings.json ✅
│
├─ Is it a server-rendered template (email, legacy)?
│  └─ YES → UmbracoProject/Views/ ✅
│
├─ Is it a project-specific API endpoint?
│  └─ YES → UmbracoProject/Controllers/ ✅
│
├─ Is it RTE styling or formats?
│  └─ YES → UmbracoProject (rte-style-formats.json, scss/) ✅
│
├─ Is it a static file (favicon, robots.txt)?
│  └─ YES → UmbracoProject/wwwroot/ ✅
│
├─ Is it an Umbraco package?
│  └─ YES → UmbracoProject/App_Plugins/ ✅
│
└─ Is it application startup config?
   └─ YES → UmbracoProject/Program.cs ✅
```

## Task Pattern Library

### PATTERN 1: Custom API Controller

```
CONDITION: Need project-specific HTTP endpoint (not generic CRUD)

LOCATION: Controllers/{Name}Controller.cs

TEMPLATE:
using Microsoft.AspNetCore.Mvc;

[Route("api/[controller]")]
[ApiController]
public class {Name}Controller : ControllerBase
{
    private readonly I{Name}Service _service;

    public {Name}Controller(I{Name}Service service)
    {
        _service = service;
    }

    [HttpGet]
    public async Task<IActionResult> Get()
    {
        var result = await _service.GetDataAsync();
        return Ok(result);
    }
}

RULES:
├─ Keep controller thin (5-10 lines per method max)
├─ Delegate ALL logic to service (implemented in Seed.* library)
├─ No direct database access
├─ No business logic
└─ Just HTTP request/response handling

EXISTING EXAMPLE:
└─ Controllers/AutodeskController.cs (Autodesk Forge API endpoints)

WHEN TO USE:
├─ Need custom routing not available in DataApiController
├─ Project-specific endpoint (boats, quotes, KRD-specific)
└─ Not generic enough for Seed.Core

FILES MODIFIED:
└─ CREATE: Controllers/{Name}Controller.cs
```

### PATTERN 2: Razor Email Template

```
CONDITION: Need HTML email template for Umbraco Forms

LOCATION: Views/Partials/Forms/Emails/{Name}.cshtml

TEMPLATE:
@inherits Umbraco.Cms.Web.Common.Views.UmbracoViewPage<Umbraco.Forms.Core.Models.FormsHtmlModel>
@{
    var siteDomain = Context.Request.Scheme + "://" + Context.Request.Host;
}
<!DOCTYPE html>
<html>
<head>
    <style type="text/css">
        /* Inline CSS required for emails */
    </style>
</head>
<body>
    @if (!string.IsNullOrEmpty(Model.HeaderHtml?.ToString())) {
        @Model.HeaderHtml
    }

    @foreach (var field in Model.Fields) {
        <h4>@field.Name</h4>
        <p>@field.GetValue()</p>
    }
</body>
</html>

RULES:
├─ Use inline CSS (external stylesheets don't work in email)
├─ Responsive design with media queries
├─ Test in multiple email clients
└─ Company branding (logo, colors)

EXISTING EXAMPLES:
├─ BasicEmail.cshtml (273 lines - full featured)
├─ SubmitQuote.cshtml
└─ RegisterQuote.cshtml

WHEN TO USE:
├─ Custom email template for Umbraco Forms
├─ Specific formatting requirements
└─ Branded transactional emails

FILES MODIFIED:
└─ CREATE: Views/Partials/Forms/Emails/{Name}.cshtml
```

### PATTERN 3: Block Grid Component

```
CONDITION: Need new component for Umbraco Block Grid

LOCATION: Views/Partials/blockgrid/Components/{name}.cshtml

TEMPLATE:
@inherits Umbraco.Cms.Web.Common.Views.UmbracoViewPage<Umbraco.Cms.Core.Models.Blocks.BlockGridItem>
@{
    var content = Model.Content;
    var settings = Model.Settings;
}

<div class="@(settings?.Value<string>("cssClass"))">
    <h2>@content.Value("title")</h2>
    <div>@content.Value("text")</div>
</div>

RULES:
├─ Access content via Model.Content
├─ Access settings via Model.Settings
├─ Keep view logic minimal
└─ Use helper methods for complex rendering

EXISTING EXAMPLES:
├─ oneColumn.cshtml
├─ twoColumn.cshtml
├─ richtext.cshtml
└─ gridImage.cshtml

WHEN TO USE:
├─ New Block Grid component needed
├─ Custom layout requirement
└─ Server-side rendering needed (vs. frontend component)

ADDITIONAL STEPS:
├─ Create document type in backoffice (element type)
├─ Configure block to use this view
└─ Test in Block Grid

FILES MODIFIED:
└─ CREATE: Views/Partials/blockgrid/Components/{name}.cshtml
```

### PATTERN 4: Environment Configuration

```
CONDITION: Need to change API key, connection string, or feature flag

LOCATION: appsettings.{Environment}.json

DECISION: Which file to edit?
├─ All environments → appsettings.json (base)
├─ Local dev only → appsettings.Development.json
├─ Staging only → appsettings.Staging.json
└─ Production only → appsettings.Production.json

EXAMPLES:
{
  "Umbraco": {
    "CMS": {
      "DeliveryApi": {
        "ApiKey": "NEW-API-KEY-HERE"
      }
    }
  },
  "Autodesk": {
    "ClientId": "NEW-CLIENT-ID",
    "ClientSecret": "NEW-SECRET"
  },
  "Features": {
    "EnableBoatBuilder": true
  }
}

RULES:
├─ Never commit secrets to Git (use environment variables or Azure Key Vault)
├─ Require application restart for changes to take effect
├─ Document what each setting does
└─ Use hierarchical JSON structure

WHEN TO USE:
├─ External API credentials
├─ Connection strings
├─ Feature flags
├─ Performance tuning (timeouts, batch sizes)
└─ Environment-specific URLs

FILES MODIFIED:
└─ EDIT: appsettings.{Environment}.json
```

### PATTERN 5: RTE Style Format

```
CONDITION: Content editors need new style option in rich text editor

LOCATION: rte-style-formats.json

TEMPLATE:
{
  "title": "Style Display Name",
  "selector": "a",              // or "h1,h2,h3,p" or "div" etc.
  "classes": "cssClassName"     // CSS class to apply
}

OR for inline elements:
{
  "title": "Highlight Text",
  "inline": "span",
  "classes": "highlightText"
}

OR for block wrappers:
{
  "title": "Callout Box",
  "block": "div",
  "classes": "calloutBox",
  "wrapper": true
}

IMPLEMENTATION STEPS:
├─ STEP 1: Add style definition to rte-style-formats.json
├─ STEP 2: Implement CSS in scss/rte.scss
│  └─ .cssClassName { /* styles */ }
├─ STEP 3: Wait for Gulp to compile → wwwroot/css/rte.css
├─ STEP 4: Hard refresh backoffice
└─ STEP 5: Test in TinyMCE editor

EXISTING EXAMPLES:
├─ Buttons (Button, Button Blue, Button Outline)
├─ Text colors (Black Text, Blue Text, White Text)
├─ Margins (Margin Top Small/Medium/Large)
└─ Font weights (100-900)

FILES MODIFIED:
├─ EDIT: rte-style-formats.json
├─ EDIT: scss/rte.scss
└─ AUTO: wwwroot/css/rte.css (Gulp compiles)
```

### PATTERN 6: Backoffice SCSS Styling

```
CONDITION: Need to customize backoffice appearance

LOCATION: scss/rte.scss

WORKFLOW:
├─ STEP 1: Edit scss/rte.scss
│  └─ Add/modify SCSS rules
├─ STEP 2: Gulp auto-compiles (watch task running)
│  └─ Output: wwwroot/css/rte.css
├─ STEP 3: Hard refresh backoffice (Ctrl+Shift+R)
├─ STEP 4: Verify styles applied
└─ STEP 5: Commit both SCSS source + compiled CSS

FOUNDATION FRAMEWORK:
├─ Available: Foundation Sites 6.8
├─ Import: @import '~foundation-sites/scss/foundation';
└─ Use mixins and variables from Foundation

EXAMPLES:
.buttonBlue {
  background-color: #007299;
  color: white;
  padding: 0.5rem 1rem;
}

.whiteText {
  color: white !important;
}

FILES MODIFIED:
├─ EDIT: scss/rte.scss
└─ AUTO: wwwroot/css/rte.css (Gulp compiles)
```

### PATTERN 7: Static Asset

```
CONDITION: Need to add favicon, robots.txt, or public file

LOCATION: wwwroot/{path}

EXAMPLES:
├─ wwwroot/favicon.ico
├─ wwwroot/robots.txt
├─ wwwroot/apple-touch-icon.png
├─ wwwroot/.well-known/security.txt
└─ wwwroot/images/og-image.png

PUBLIC URL: https://domain.com/{path}
└─ wwwroot/favicon.ico → https://domain.com/favicon.ico

RULES:
├─ Files are publicly accessible
├─ No authentication required
├─ Served directly by web server (fast)
└─ Don't use for media (use Umbraco Media Library → Azure Blob)

WHEN TO USE:
├─ Meta files (robots.txt, sitemap.xml, security.txt)
├─ Icons (favicon, touch icons)
├─ Static JavaScript/CSS for backoffice
└─ OpenGraph images

FILES MODIFIED:
└─ CREATE: wwwroot/{path}/{filename}
```

### PATTERN 8: Umbraco Package Installation

```
CONDITION: Need to install backoffice package/plugin

OPTION A: NuGet Package
├─ COMMAND: dotnet add package {PackageName}
├─ LOCATION: Package appears in App_Plugins/ (auto)
└─ CONFIG: May need appsettings.json configuration

OPTION B: Manual Installation
├─ DOWNLOAD: Package files from vendor
├─ EXTRACT: To App_Plugins/{packageName}/
├─ VERIFY: Check package.manifest exists
└─ CONFIG: May need appsettings.json configuration

POST-INSTALL STEPS:
├─ RESTART: Application (required)
├─ VERIFY: Package appears in backoffice
├─ CONFIGURE: In backoffice if needed
└─ COMMIT: App_Plugins/ folder + .csproj (if NuGet)

EXISTING EXAMPLE:
└─ App_Plugins/cmsimport/ (CMSImport data import tool)

FILES MODIFIED:
├─ CREATE: App_Plugins/{packageName}/ (if manual)
├─ EDIT: UmbracoProject.csproj (if NuGet)
└─ OPTIONAL: appsettings.json (package config)
```

### PATTERN 9: Application Startup Middleware

```
CONDITION: Need to add middleware, health checks, or startup config

LOCATION: Program.cs

EXAMPLES:

Add CORS:
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("https://www.keystoneridgedesigns.com")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

app.UseCors("AllowFrontend");

Add Health Checks:
builder.Services.AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database")
    .AddCheck<BlobStorageHealthCheck>("blob_storage");

app.MapHealthChecks("/health");

Add Custom Middleware:
app.UseMiddleware<SecurityHeadersMiddleware>();

RULES:
├─ Order matters (middleware pipeline is sequential)
├─ Add services in builder.Services
├─ Add middleware in app.Use*
└─ Test thoroughly (can break entire application)

FILES MODIFIED:
└─ EDIT: Program.cs
```

### PATTERN 10: uSync Configuration

```
CONDITION: Need to change uSync behavior

LOCATION: appsettings.json → uSync section

CONFIGURATION:
{
  "uSync": {
    "Settings": {
      "ExportOnSave": true,              // Auto-export when saving in backoffice
      "ImportAtStartup": true,            // Auto-import on application start
      "ExportAtStartup": false,           // Don't export at startup
      "UseGuidFilenames": false,          // Use human-readable names
      "RebuildCacheOnCompletion": true
    },
    "Sets": {
      "Default": {
        "Enabled": true,
        "HandlerDefaults": [
          {
            "Handler": "ContentTypeHandler",
            "Enabled": true,
            "Actions": ["Import", "Export"]
          },
          {
            "Handler": "ContentHandler",
            "Enabled": false,            // Don't sync content
            "Actions": []
          }
        ]
      }
    }
  }
}

WHEN TO USE:
├─ Change auto-export/import behavior
├─ Enable/disable content sync
├─ Configure what gets synced
└─ Troubleshooting sync issues

FILES MODIFIED:
└─ EDIT: appsettings.json
```

## Anti-Patterns (NEVER DO THIS)

### ❌ ANTI-PATTERN 1: Business Logic in Controllers

```
BAD EXAMPLE:
[HttpPost("quote")]
public IActionResult SubmitQuote([FromBody] QuoteRequest request)
{
    // ❌ Business logic in controller
    var total = 0m;
    foreach (var item in request.Items)
    {
        total += item.Price * item.Quantity;
    }

    // ❌ Direct database access
    var quote = new Quote { Total = total };
    _context.Quotes.Add(quote);
    _context.SaveChanges();

    return Ok(quote);
}

CORRECT:
[HttpPost("quote")]
public async Task<IActionResult> SubmitQuote([FromBody] QuoteRequest request)
{
    // ✅ Delegate to service
    var quote = await _quoteService.ProcessQuoteAsync(request);
    return Ok(quote);
}

// Service implemented in Seed.Backoffice.Extensions
```

### ❌ ANTI-PATTERN 2: Manually Editing UDA Files

```
BAD:
// Manually editing: umbraco/Deploy/Revision/document-type__abc123.uda
{
  "Name": "Product Page",
  "Alias": "productPage",  // ❌ Changed manually
  // ...
}

CORRECT:
1. Open Umbraco backoffice
2. Settings → Document Types → Product Page
3. Edit alias field
4. Save
5. UDA file auto-updates
6. Commit auto-generated file
```

### ❌ ANTI-PATTERN 3: Reusable Code in UmbracoProject

```
BAD:
// UmbracoProject/Controllers/ProductController.cs
public class ProductController : ControllerBase
{
    [HttpGet("search")]
    public IActionResult Search(string query)
    {
        // ❌ Reusable search logic in controller
        var results = _examineService.Search(new PublishedContentSearchParameters
        {
            Query = query,
            DocumentTypes = new[] { "product" },
            MaxResults = 100
        });
        return Ok(results);
    }
}

CORRECT:
// Seed.Backoffice.Extensions/Services/ProductSearchService.cs
public class ProductSearchService : IProductSearchService
{
    // ✅ Reusable service in library
    public ISearchResults SearchProducts(string query) { }
}

// UmbracoProject/Controllers/ProductController.cs
public class ProductController : ControllerBase
{
    [HttpGet("search")]
    public IActionResult Search(string query)
    {
        // ✅ Controller delegates to service
        var results = _productSearchService.SearchProducts(query);
        return Ok(results);
    }
}
```

### ❌ ANTI-PATTERN 4: Secrets in appsettings.json Committed to Git

```
BAD:
{
  "ConnectionStrings": {
    "Umbraco": "Server=prod-sql;Database=UmbracoDb;User=sa;Password=SuperSecret123!;"
  }
}
// ❌ Committed to Git (security vulnerability)

CORRECT OPTION A (Token Replacement):
{
  "ConnectionStrings": {
    "Umbraco": "#{DbConnectionString}#"  // ✅ Token replaced in deployment
  }
}

CORRECT OPTION B (Environment Variables):
// appsettings.json
{
  "ConnectionStrings": {
    "Umbraco": ""  // ✅ Overridden by env var: CONNECTION_STRING__UMBRACO
  }
}

// Program.cs
builder.Configuration.AddEnvironmentVariables();
```

### ❌ ANTI-PATTERN 5: Complex Logic in Razor Views

```
BAD:
@* Views/productDetail.cshtml *@
@{
    // ❌ Business logic and queries in view
    var product = Model.Content;
    var relatedProducts = new List<IPublishedContent>();

    foreach (var cat in product.Value<IEnumerable<IPublishedContent>>("categories"))
    {
        var products = _examineService.Search(...);
        relatedProducts.AddRange(products.Results.Select(x => x.Content));
    }
}

CORRECT:
@* Views/productDetail.cshtml *@
@{
    // ✅ Use pre-computed data from ApiSafeConverter
    var product = Model.Content;
    var relatedProducts = product.Value<IEnumerable<IPublishedContent>>("relatedProducts");
}

OR BETTER:
// ✅ Don't use Razor for modern apps → Use Next.js in Seed.Web
```

## Quick Reference

### Task → Location Mapping

```
TASK: Add custom API endpoint
└─ FILE: Controllers/{Name}Controller.cs

TASK: Add email template
└─ FILE: Views/Partials/Forms/Emails/{Name}.cshtml

TASK: Add Block Grid component
└─ FILE: Views/Partials/blockgrid/Components/{name}.cshtml

TASK: Change API key/config
└─ FILE: appsettings.{Environment}.json

TASK: Add RTE style
└─ FILES: rte-style-formats.json + scss/rte.scss

TASK: Customize backoffice styles
└─ FILE: scss/rte.scss

TASK: Add static file (favicon, robots.txt)
└─ FILE: wwwroot/{path}

TASK: Install Umbraco package
└─ LOCATION: App_Plugins/{packageName}/

TASK: Add middleware/startup config
└─ FILE: Program.cs

TASK: Configure uSync
└─ FILE: appsettings.json → uSync section
```

### Validation Checklist

```
BEFORE IMPLEMENTING IN UMBRACOPROJECT:

□ Is this configuration? → YES = UmbracoProject
□ Is this a server-side template? → YES = UmbracoProject
□ Is this a project-specific API endpoint? → YES = UmbracoProject
□ Is this business logic? → NO! = Seed.* library
□ Is this reusable? → NO! = Seed.* library
□ Is this a React component? → NO! = Seed.Web
□ Am I modifying UDA files manually? → STOP! = Use backoffice
□ Does this need to be unit tested? → NO! = Should be in library
□ Could another project use this? → NO! = Should be in library
```

## Critical Rules

```
RULE 1: UmbracoProject is for orchestration, not implementation
└─ If it has logic, it belongs in Seed.* libraries

RULE 2: Never manually edit UDA or uSync files
└─ Always use backoffice to make schema changes

RULE 3: Controllers must be thin (5-10 lines per method)
└─ All logic delegates to services in Seed.* libraries

RULE 4: Razor views are for legacy/email only
└─ Modern frontend uses Next.js in Seed.Web

RULE 5: Configuration changes require restart
└─ appsettings.json changes not applied until restart

RULE 6: No secrets in version control
└─ Use environment variables or Azure Key Vault

RULE 7: Commit both SCSS source + compiled CSS
└─ Don't commit only compiled CSS

RULE 8: Schema = backoffice, Config = files, Code = libraries
└─ Clear separation of concerns
```
