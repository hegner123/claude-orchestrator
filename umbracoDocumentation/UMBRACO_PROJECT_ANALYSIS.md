# UmbracoProject - Component Reference

## Project Classification

```
TYPE: Host Application (Deployment Container)
LOCATION: src/UmbracoProject/
C# FILES: 2 (minimal code)
SCHEMA FILES: 619 UDA + 922 uSync = 1,541 total
ROLE: Configuration + Schema Storage + Runtime Host
PHILOSOPHY: Thin orchestration layer (logic in Seed.* libraries)
```

## Directory Structure Map

```
src/UmbracoProject/
├─ Controllers/                    (1 file - project-specific API endpoints)
├─ Views/                          (22 files - Razor templates)
├─ umbraco/Deploy/Revision/        (619 UDA files - schema definitions)
├─ uSync/v9/                       (922 files - schema sync)
├─ wwwroot/                        (static assets)
├─ App_Plugins/                    (backoffice packages)
├─ scss/                           (SCSS source)
├─ appsettings*.json               (4 config files - env-specific)
├─ Program.cs                      (startup)
├─ package.json                    (Gulp dependencies)
└─ gulpfile.js                     (SCSS build)
```

## C# Code Inventory

```
TOTAL: 2 C# files

FILE: Program.cs
├─ ROLE: ASP.NET Core startup
├─ CONTAINS: Umbraco service registration, middleware pipeline
└─ MODIFY WHEN: Adding middleware, health checks, CORS policies

FILE: Controllers/AutodeskController.cs (50 lines)
├─ ROLE: API endpoint for Autodesk Forge CAD viewer
├─ ENDPOINTS:
│  ├─ GET /api/autodesk/models
│  └─ GET /api/autodesk/models/{id}
├─ DEPENDENCIES: IAutodeskViewerService (Seed.DataTypes)
└─ PATTERN: Thin controller delegates to service
```

## Schema Files (UDA)

```
LOCATION: umbraco/Deploy/Revision/
COUNT: 619 files
FORMAT: JSON (.uda extension)
NAMING: {type}__{GUID}.uda
AUTO-GENERATED: Yes (on save in backoffice)
MANUAL EDIT: ❌ Never

FILE TYPES:
├─ document-type__*.uda       (content type schemas)
├─ data-type__*.uda            (field configurations)
├─ template__*.uda             (rendering templates)
├─ media-type__*.uda           (media schemas)
├─ document-type-container__*.uda  (folders)
└─ data-type-container__*.uda      (folders)

USAGE:
├─ Version control of content schema
├─ Deployment across environments
└─ Source of truth for production

WORKFLOW:
├─ Edit schema in backoffice → UDA auto-created
├─ Commit to Git → Deploy to other environments
└─ On startup → UDA files auto-applied to database
```

## Configuration Files

```
FILE: appsettings.json (base config)
FILE: appsettings.Development.json (local dev overrides)
FILE: appsettings.Staging.json (staging overrides)
FILE: appsettings.Production.json (production overrides)

KEY SECTIONS:
├─ Umbraco:CMS:DeliveryApi
│  ├─ Enabled: true
│  ├─ ApiKey: c0234bf6-81e6-409e-8b04-0911c64f86e4
│  └─ MemberAuthorization: enabled
├─ Umbraco:CMS:Global:Smtp
│  ├─ Host: mail.keystoneridgedesigns.com
│  └─ Port: 2564
├─ Umbraco:Storage:AzureBlob
│  ├─ ConnectionString: [Azure connection]
│  └─ ContainerName: krd-media
├─ Autodesk (Forge API)
│  ├─ ClientId, ClientSecret
│  └─ BucketKey: krd_products
├─ Video (Vimeo API)
│  ├─ BaseUrl: https://api.vimeo.com/
│  └─ AccessToken: [token]
├─ Jwt (Member auth)
│  ├─ Key, Issuer, Audience
│  └─ Frontend: https://localhost:3000
└─ Seed
   ├─ ApiKey: [delivery API key]
   └─ PreviewKey: [preview mode key]
```

## Razor View Templates

```
LOCATION: Views/
COUNT: 22 .cshtml files
PURPOSE: Server-side rendering (emails, legacy features)

MAIN VIEW:
└─ Views/home.cshtml → Status page ("CMS Running")

FORM EMAIL TEMPLATES: Views/Partials/Forms/Emails/
├─ BasicEmail.cshtml (273 lines)
│  ├─ Styled HTML email with KRD branding
│  ├─ Responsive layout, inline CSS
│  └─ Dynamic field rendering by type
├─ SubmitQuote.cshtml
└─ RegisterQuote.cshtml

BLOCK GRID RENDERING: Views/Partials/blockgrid/
├─ default.cshtml → Main wrapper
├─ area.cshtml, areas.cshtml → Grid structure
├─ items.cshtml → Block iterator
└─ Components/
   ├─ oneColumn.cshtml
   ├─ twoColumn.cshtml
   ├─ richtext.cshtml
   └─ gridImage.cshtml

BLOCK LIST RENDERING: Views/Partials/blocklist/
└─ default.cshtml

LEGACY GRID: Views/Partials/grid/
├─ bootstrap3.cshtml, bootstrap3-fluid.cshtml
└─ editors/ → rte, media, embed, macro, textstring
```

## Frontend Build System

```
TOOL: Gulp 5.0
PURPOSE: Compile SCSS for backoffice styles
SOURCE: scss/rte.scss
OUTPUT: wwwroot/css/rte.css
FRAMEWORK: Foundation Sites 6.8

FILE: package.json
├─ gulp: 5.0.0
├─ gulp-sass: 5.1.0
├─ sass: 1.77.5
└─ foundation-sites: 6.8.1

FILE: gulpfile.js
├─ TASK: scss:watch → Auto-compile on change
├─ INPUT: scss/**/*.{scss,sass}
├─ OUTPUT: wwwroot/css/
└─ BINDING: Auto-runs on project open (Visual Studio)

WORKFLOW:
├─ Edit: scss/rte.scss
├─ Gulp auto-compiles → wwwroot/css/rte.css
├─ Refresh backoffice to see changes
└─ Commit both: SCSS source + compiled CSS
```

## Static Resources

```
LOCATION: wwwroot/
PUBLIC URL: https://domain.com/{path}

wwwroot/
├─ app_plugins/global/     (backoffice JavaScript/CSS)
├─ css/                    (compiled from SCSS)
└─ fonts/                  (web fonts)

USAGE:
├─ Backoffice customization
├─ RTE styles
└─ Custom admin scripts
```

## Backoffice Plugins

```
LOCATION: App_Plugins/

PLUGIN: cmsimport/
├─ PURPOSE: Data import tool (CSV, Excel, XML, SQL)
├─ USE CASE: Bulk import products/boats from Epicor
└─ STRUCTURE:
   ├─ backoffice/ → Admin UI
   ├─ config/ → Plugin settings
   ├─ dialogs/ → Modal windows
   └─ fields/ → Field mapping UI
```

## RTE Style Formats

```
FILE: rte-style-formats.json (240 lines)
PURPOSE: TinyMCE editor style options for content editors

CATEGORIES:
├─ Headings (h1-h6, p)
├─ Margins (no margin, small/medium/large top/bottom)
├─ Buttons (5 button styles: Button, Button Blue, Button Outline, etc.)
├─ Images (float left/right)
├─ Text (small/large, colors, underlines, PDF icon)
├─ Font Weights (100-900)
└─ Width Caps (max-width constraints)

FORMAT:
{
  "title": "Button Blue",
  "selector": "a",
  "classes": "buttonBlue"
}

IMPLEMENTATION: CSS classes in scss/rte.scss
```

## Project Dependencies

```
FILE: UmbracoProject.csproj

PROJECT REFERENCES:
├─ Seed.Core
├─ Seed.DataTypes
└─ Seed.Backoffice.Extensions

DEPENDENCY CHAIN:
UmbracoProject
├─→ Seed.Backoffice.Extensions
│   ├─→ Seed.DataTypes
│   │   └─→ Seed.Core
│   └─→ Seed.Core
└─→ Seed.Core (direct reference)

NUGET PACKAGES:
├─ Umbraco.Cms (13.x)
├─ Umbraco.Forms
├─ Umbraco.Deploy.Cloud
└─ Umbraco.Storage.AzureBlob
```

## Integration Points

```
WITH SEED.CORE:
├─ Uses: Base ApiSafeConverters, ExamineService, DataService, EmailService
├─ Exposes: DataApiController at /umbraco/api/data/*
└─ Runtime: Collection builder auto-registers converters

WITH SEED.DATATYPES:
├─ Loads: 15 custom property editors into backoffice
├─ Uses: IAutodeskViewerService in AutodeskController
└─ Backoffice: Renders FlexibleLinks, VideoEmbedder, CustomPicker, etc.

WITH SEED.BACKOFFICE.EXTENSIONS:
├─ Loads: 53 project-specific ApiSafeConverters
├─ Registers: ProductService, FormWorkflows, MembershipService
└─ Exposes: Project-specific API endpoints

WITH SEED.WEB (Next.js):
├─ API: Umbraco Delivery API at /umbraco/delivery/api/v1/*
├─ CORS: Configured for https://localhost:3000
├─ Auth: JWT tokens for member authentication
└─ Preview: PreviewKey enables draft content viewing
```

## Key Patterns

```
PATTERN: Separation of Concerns
├─ CODE → Seed.* libraries (reusable, testable)
├─ CONFIGURATION → UmbracoProject (environment-specific)
└─ SCHEMA → UDA/uSync files (version controlled)

PATTERN: Multi-Environment Configuration
├─ Base: appsettings.json
├─ Override: appsettings.{Environment}.json
└─ Selection: ASPNETCORE_ENVIRONMENT variable

PATTERN: Schema-Driven Development
├─ Edit in backoffice → UDA auto-generated
├─ Commit to Git → Track schema changes
├─ Deploy to other environments → UDA auto-applied
└─ No manual database migrations

PATTERN: Minimal Custom Code
├─ Only 2 C# files in entire project
├─ Business logic → Seed.Backoffice.Extensions
├─ Infrastructure → Seed.Core
└─ Host app → Configuration only
```

## Component Lookup

```
QUERY: Where to find X?

Custom API endpoints:
└─ Controllers/*.cs

Email templates:
└─ Views/Partials/Forms/Emails/*.cshtml

Block Grid components:
└─ Views/Partials/blockgrid/Components/*.cshtml

Document type schemas:
└─ umbraco/Deploy/Revision/document-type__*.uda

Data type schemas:
└─ umbraco/Deploy/Revision/data-type__*.uda

Environment config:
└─ appsettings.{Environment}.json

RTE style options:
└─ rte-style-formats.json

Backoffice styles:
└─ scss/*.scss → wwwroot/css/*.css

Static assets:
└─ wwwroot/

Umbraco packages:
└─ App_Plugins/
```

## File Modification Rules

```
SAFE TO EDIT:
✅ appsettings*.json → Configuration changes
✅ Views/**/*.cshtml → Template modifications
✅ scss/*.scss → Style changes
✅ rte-style-formats.json → RTE options
✅ Controllers/*.cs → Custom endpoints
✅ Program.cs → Startup configuration
✅ gulpfile.js → Build tasks

NEVER EDIT:
❌ umbraco/Deploy/Revision/*.uda → Auto-generated, edit via backoffice
❌ uSync/v9/**/*.config → Auto-generated, edit via backoffice
❌ wwwroot/css/*.css → Compiled from SCSS, edit source instead

CAREFUL:
⚠️ web.config → Only for IIS-specific settings
⚠️ package.json → Changing versions may break build
```

## Common File Operations

```
OPERATION: Add new API endpoint
├─ CREATE: Controllers/{Name}Controller.cs
├─ PATTERN: Thin controller, delegate to service (Seed.* library)
├─ INJECT: Service via constructor
└─ COMMIT: Single .cs file

OPERATION: Add email template
├─ CREATE: Views/Partials/Forms/Emails/{Name}.cshtml
├─ INHERIT: Umbraco.Cms.Web.Common.Views.UmbracoViewPage<FormsHtmlModel>
├─ USE: @Model.Fields, @Model.HeaderHtml, @Model.BodyHtml
└─ COMMIT: Single .cshtml file

OPERATION: Add Block Grid component
├─ CREATE: Views/Partials/blockgrid/Components/{name}.cshtml
├─ CONFIGURE: Block to use this view in backoffice
└─ COMMIT: Single .cshtml file

OPERATION: Add RTE style
├─ EDIT: rte-style-formats.json → Add style definition
├─ EDIT: scss/rte.scss → Implement CSS for class
├─ WAIT: Gulp auto-compiles to wwwroot/css/rte.css
└─ COMMIT: JSON + SCSS + CSS

OPERATION: Change environment setting
├─ IDENTIFY: Which environment? (Dev/Staging/Prod)
├─ EDIT: appsettings.{Environment}.json
├─ RESTART: Application to apply changes
└─ COMMIT: Modified appsettings file

OPERATION: Add Umbraco package
├─ OPTION A: dotnet add package {PackageName}
├─ OPTION B: Copy to App_Plugins/{packageName}/
├─ CONFIGURE: In appsettings.json if needed
├─ RESTART: Application
└─ CONFIGURE: In backoffice if needed
```

## Critical Paths

```
PATH: Schema change workflow
├─ Backoffice → Edit document/data type → Save
├─ UDA → umbraco/Deploy/Revision/{type}__{GUID}.uda created
├─ Git → git add + commit + push
├─ Other envs → Pull + restart → UDA auto-applied
└─ Verification → Check backoffice schema matches

PATH: Configuration change workflow
├─ Identify environment (Dev/Staging/Prod)
├─ Edit appsettings.{Environment}.json
├─ Test locally (if Dev)
├─ Commit + push
├─ Deploy to environment
├─ Restart application
└─ Verification → Check new config active

PATH: Razor view modification
├─ Edit .cshtml file in Views/
├─ Save (hot reload in development)
├─ Test in browser
├─ Commit + push
├─ Deploy
└─ No restart needed (views are dynamic)

PATH: SCSS style update
├─ Edit scss/*.scss
├─ Gulp auto-compiles (watch running)
├─ Refresh backoffice (hard refresh)
├─ Test styles
├─ Commit both SCSS + compiled CSS
└─ Deploy
```

## Size Metrics

```
C# CODE: 2 files (~100 lines total)
SCHEMA FILES: 1,541 files (619 UDA + 922 uSync)
VIEW TEMPLATES: 22 files
CONFIG FILES: 8 files
STATIC ASSETS: Variable
TOTAL PROJECT: ~1,600+ files (mostly schema)

COMPARISON TO OTHER PROJECTS:
├─ Seed.Core: 145 C# files (heavy code)
├─ Seed.DataTypes: 115 C# files (heavy code)
├─ Seed.Backoffice.Extensions: Variable C# files (heavy code)
└─ UmbracoProject: 2 C# files (minimal code, heavy config/schema)
```
