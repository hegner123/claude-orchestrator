# Source Directory Structure - LLM Quick Reference

## Project Classification Matrix

```
PROJECT              TYPE          FILES    ROLE                    REUSABILITY
================================================================================
Seed.Core            Library       145      Infrastructure          Generic/Reusable
Seed.DataTypes       Library       115      Property Editors        Generic/Reusable
Seed.Backoffice.Ext  Library       Var      Business Logic          Project-Specific
UmbracoProject       Host App      2        Runtime Container       Configuration
Seed.Web             Frontend      Var      UI/Presentation         Project-Specific
```

## Decision Tree: Where Does This Task Belong?

```
QUERY: Which project should I work in?

├─ Is it a backoffice UI control (property editor)?
│  ├─ Reusable across industries? → Seed.DataTypes/
│  └─ Project-specific? → Seed.Backoffice.Extensions/CustomPickers/
│
├─ Is it data transformation for API?
│  ├─ Standard Umbraco types (media, content)? → Seed.Core/ApiSafeConverters/
│  └─ Custom document types (boats, products)? → Seed.Backoffice.Extensions/ApiSafeConverters/
│
├─ Is it schema definition?
│  └─ UmbracoProject/umbraco/Deploy/Revision/*.uda
│
├─ Is it frontend UI component?
│  └─ Seed.Web/common/components/
│
├─ Is it TypeScript type definition?
│  └─ Seed.Web/lib/umbraco/types/
│
├─ Is it shared infrastructure (caching, services, base classes)?
│  └─ Seed.Core/
│
├─ Is it business logic (products, quotes, dealers)?
│  └─ Seed.Backoffice.Extensions/
│
├─ Is it configuration or middleware?
│  └─ UmbracoProject/Program.cs or appsettings*.json
│
└─ Is it external API integration?
   ├─ Generic (Instagram, Vimeo, Autodesk)? → Seed.DataTypes/*/Services/
   └─ Project-specific (Epicor)? → Seed.Backoffice.Extensions/Products/Services/
```

## Project Dependency Chain

```
COMPILATION DEPENDENCIES:
Seed.Core (base)
  ↓
  ├─→ Seed.DataTypes
  │     ↓
  │     └─→ Seed.Backoffice.Extensions
  │           ↓
  │           └─→ UmbracoProject (host)
  └─→ Seed.Backoffice.Extensions
        ↓
        └─→ UmbracoProject (host)

RUNTIME API COMMUNICATION:
UmbracoProject ←→ Seed.Web (HTTP/JSON)
```

## Seed.Core/ - Infrastructure Library

```
CLASSIFICATION:
├─ TYPE: .NET 8 Class Library
├─ SCOPE: Generic, reusable across any Umbraco project
├─ FILES: 145 C# files
├─ REFERENCED BY: All other C# projects
└─ PHILOSOPHY: "Could this be used in a different Umbraco project?"

KEY DIRECTORIES:
├─ ApiSafeConverters/ (18 base converters)
│  ├─ BaseApiSafeConverter.cs → Abstract base for all converters
│  ├─ IApiSafeConverter.cs → Converter interface
│  ├─ MediaApiSafeConverter.cs → Umbraco.MediaPicker3
│  ├─ PublishedContentApiSafeConverter.cs → Umbraco.ContentPicker
│  ├─ BlockGridApiSafeConverter.cs → Umbraco.BlockGrid
│  └─ BlockListApiSafeConverter.cs → Umbraco.BlockList
│
├─ Services/ (9 core services)
│  └─ DataService, EmailService, ExamineService, etc.
│
├─ Models/ (shared DTOs)
│  └─ Blog/, Dealer/, Event/, Gallery/, Image/, Search/
│
├─ Extensions/ → Extension methods for Umbraco types
├─ Membership/ → Auth and token services
├─ VirtualPages/ → Virtual routing
└─ Stringifier/ → Search indexing

KEY FILES:
├─ DataApiController.cs → Base controller for data endpoints
├─ CoreComposer.cs → DI setup
└─ SeedHelper.cs → Utility helpers

WORK HERE WHEN:
✅ Adding base converter for standard Umbraco type
✅ Creating shared models for multiple projects
✅ Implementing infrastructure services (caching, GraphQL)
✅ Adding extension methods for Umbraco types

NEVER WORK HERE FOR:
❌ Project-specific business logic (boats, products, dealers)
❌ Custom property editors
❌ Frontend components
❌ Schema definitions
```

## Seed.DataTypes/ - Custom Property Editors

```
CLASSIFICATION:
├─ TYPE: .NET 8 Class Library
├─ SCOPE: Reusable property editors
├─ FILES: 115 C# files (15 custom editors)
├─ DEPENDENCIES: Seed.Core only
└─ PHILOSOPHY: "Would a hotel/school/store use this editor?"

PROPERTY EDITOR INVENTORY (15 Total):
├─ AimbaseNewsletterPicker/ → Newsletter selection
├─ AutodeskViewer/ → CAD file viewer (Forge API)
├─ BlockPicker/ → Block selection
├─ CustomPicker/ → Extensible picker framework
├─ FlexibleLinks/ → Multi-type link picker
├─ GeocodedLocation/ → Location with geocoding
├─ IconPicker/ → Icon selection
├─ InstagramMediaPicker/ → Instagram integration
├─ PositionPicker/ → Position/alignment
├─ SeoSettings/ → SEO metadata
├─ SideSizer/ → Dimension picker
├─ SocialSettings/ → Social media settings
├─ VideoEmbedder/ → Multi-provider video embed
└─ VimeoVideoSelector/ → Vimeo integration

DIRECTORY STRUCTURE PATTERN:
{EditorName}/
├─ Core/ → Property editor implementation
├─ Models/ → Data models
├─ Services/ → External API integration (if needed)
├─ Interfaces/ → Service contracts (if needed)
├─ Providers/ → Provider implementations (if needed)
└─ wwwroot/App_Plugins/ → Backoffice JavaScript/CSS

WORK HERE WHEN:
✅ Creating new backoffice property editor
✅ Adding external API integration (Instagram, Vimeo, Autodesk)
✅ Building extensible editor framework (FlexibleLinks, CustomPicker)
✅ Implementing reusable UI controls for backoffice

NEVER WORK HERE FOR:
❌ Project-specific converters
❌ Business logic (products, quotes)
❌ Schema definitions
❌ Frontend React components
```

## Seed.Backoffice.Extensions/ - Project-Specific Logic

```
CLASSIFICATION:
├─ TYPE: .NET 8 Class Library
├─ SCOPE: Project-specific (Keystone Ridge Designs)
├─ DEPENDENCIES: Seed.Core + Seed.DataTypes
└─ PHILOSOPHY: "Unique to this website, not reusable elsewhere"

KEY DIRECTORIES:
├─ ApiSafeConverters/ (53 project-specific converters)
│  ├─ Models/ → Converter output models
│  └─ AccordionApiSafeConverter.cs, BannerApiSafeConverter.cs, etc.
│
├─ Products/ → Product catalog + Epicor integration
│  ├─ Services/ → ProductService, Epicor API
│  ├─ Models/ → Product data models
│  └─ HealthChecks/ → Product health checks
│
├─ QuoteBuilder/ → Quote generation
├─ FormExtensions/ → Umbraco Forms customizations
│  ├─ Fields/ → Custom form fields
│  ├─ Workflows/ → Form workflows
│  └─ PreValueSourceTypes/ → Dynamic dropdown sources
│
├─ Membership/ → Member management
├─ Blog/ → Blog functionality
├─ SiteSearch/ → Site search
├─ Videos/ → Video management
└─ CustomPickers/ → Project-specific pickers

KEY FILES:
├─ ExtensionComposer.cs → DI setup
└─ BoatHelper.cs → Boat-specific utilities

WORK HERE WHEN:
✅ Creating converters for custom document types (boats, products)
✅ Implementing business logic (quotes, products, dealers)
✅ Adding custom form fields/workflows
✅ Extending membership functionality
✅ Building project-specific features

NEVER WORK HERE FOR:
❌ Generic infrastructure (belongs in Seed.Core)
❌ Reusable property editors (belongs in Seed.DataTypes)
❌ Schema definitions (belongs in UmbracoProject)
❌ Frontend components (belongs in Seed.Web)
```

## UmbracoProject/ - Host Application

```
CLASSIFICATION:
├─ TYPE: ASP.NET Core Web Application (.NET 8)
├─ SCOPE: Configuration + Schema + Runtime Container
├─ C# FILES: 2 (minimal code)
├─ SCHEMA FILES: 619 UDA + 922 uSync = 1,541 total
└─ PHILOSOPHY: "Thin orchestration layer, logic in Seed.* libraries"

DIRECTORY STRUCTURE:
├─ umbraco/Deploy/Revision/ (619 UDA files)
│  ├─ data-type__*.uda → Data type schemas
│  ├─ document-type__*.uda → Document type schemas
│  └─ document-type-container__*.uda → Folders
│
├─ uSync/v9/ (922 files) → uSync schema sync
├─ Controllers/ (1 file) → AutodeskController.cs
├─ Views/ (22 files) → Razor templates
│  ├─ Partials/Forms/Emails/ → Email templates
│  ├─ Partials/blockgrid/ → Block Grid rendering
│  └─ Partials/blocklist/ → Block List rendering
│
├─ wwwroot/ → Static assets
├─ scss/ → SCSS source (compiled via Gulp)
├─ App_Plugins/cmsimport/ → CMS Import plugin
│
└─ CONFIGURATION FILES:
   ├─ Program.cs → Startup, middleware, DI
   ├─ appsettings.json → Base config
   ├─ appsettings.Development.json → Dev overrides
   ├─ appsettings.Staging.json → Staging overrides
   ├─ appsettings.Production.json → Prod overrides
   ├─ rte-style-formats.json → TinyMCE styles
   ├─ package.json → Gulp dependencies
   └─ gulpfile.js → SCSS compilation

C# CODE (2 files only):
├─ Program.cs → Startup configuration
└─ Controllers/AutodeskController.cs → Autodesk API endpoints

WORK HERE WHEN:
✅ Modifying startup/middleware (Program.cs)
✅ Creating UDA files (via backoffice, auto-generated)
✅ Adding custom API controllers
✅ Configuring environment settings (appsettings*.json)
✅ Managing Razor email templates
✅ Adding RTE styles (rte-style-formats.json)
✅ Updating backoffice SCSS (scss/*.scss)

NEVER WORK HERE FOR:
❌ Business logic (belongs in Seed.Backoffice.Extensions)
❌ Property editors (belongs in Seed.DataTypes)
❌ Infrastructure services (belongs in Seed.Core)
❌ Frontend React components (belongs in Seed.Web)
❌ Manually editing UDA files (use backoffice instead)
```

## Seed.Web/ - Next.js Frontend

```
CLASSIFICATION:
├─ TYPE: Next.js 15 / React 19 / TypeScript
├─ SCOPE: Frontend UI/UX
├─ DEPENDENCIES: None (standalone, consumes UmbracoProject API)
└─ PHILOSOPHY: "Decoupled frontend consuming Delivery API"

DIRECTORY STRUCTURE:
├─ app/ → Next.js App Router
│  ├─ [[...slug]]/ → Dynamic Umbraco page routing
│  └─ api/ → Next.js API routes (server-side)
│
├─ common/
│  ├─ components/ → Reusable React components
│  │  └─ blockGrid/blocks/ → Block Grid element components
│  ├─ types/ → Shared TypeScript types
│  └─ util/ → Utility functions
│
├─ lib/
│  ├─ umbraco/types/ → TypeScript types for API responses ⭐
│  │  ├─ imageModel.type.ts → ImageModel from MediaApiSafeConverter
│  │  ├─ umbracoNode.type.ts → UmbracoNode from PublishedContentApiSafeConverter
│  │  ├─ blockGridItem.type.ts → Block Grid items
│  │  └─ blockListItem.type.ts → Block List items
│  └─ greensock/ → GSAP setup
│
├─ modules/ → Feature modules
├─ content/ → Static assets (images, videos, fonts, icons)
├─ public/ → Public static assets
├─ styles/ → Global styles
│
└─ CONFIGURATION FILES:
   ├─ next.config.js → Next.js config
   ├─ tsconfig.json → TypeScript config
   ├─ package.json → Dependencies
   ├─ .env.development → Dev env vars
   └─ .env.production → Prod env vars

CRITICAL PATTERN:
└─ TypeScript types in lib/umbraco/types/ MUST match ApiSafeConverter output

WORK HERE WHEN:
✅ Building React components
✅ Creating pages and routes
✅ Adding TypeScript types for API responses
✅ Implementing UI/UX features
✅ Managing frontend build and deployment

NEVER WORK HERE FOR:
❌ Backend business logic (belongs in Seed.Backoffice.Extensions)
❌ Data transformation (belongs in ApiSafeConverters)
❌ Schema definitions (belongs in UmbracoProject)
❌ Property editors (belongs in Seed.DataTypes)
```

## File Modification Safety Matrix

```
PROJECT/PATH                                    SAFE    REASON
================================================================================
Seed.Core/**/*.cs                               ✅      C# code
Seed.DataTypes/**/*.cs                          ✅      C# code
Seed.Backoffice.Extensions/**/*.cs              ✅      C# code
UmbracoProject/Program.cs                       ✅      Startup config
UmbracoProject/appsettings*.json                ✅      Configuration
UmbracoProject/Views/**/*.cshtml                ✅      Razor templates
UmbracoProject/scss/*.scss                      ✅      SCSS source
UmbracoProject/rte-style-formats.json           ✅      RTE config
UmbracoProject/Controllers/*.cs                 ✅      Custom endpoints
UmbracoProject/umbraco/Deploy/Revision/*.uda    ❌      Auto-generated, edit via backoffice
UmbracoProject/uSync/v9/**/*.config             ❌      Auto-generated, edit via backoffice
UmbracoProject/wwwroot/css/*.css                ❌      Compiled from SCSS
Seed.Web/**/*.tsx, *.ts                         ✅      React/TypeScript
```

## Quick Action Patterns

### PATTERN: Add New Property to Document Type

```
STEP 1: Generate UUID
├─ ACTION: uuidgen (on macOS/Linux)
└─ RESULT: Use in property Key field

STEP 2: Add to UDA file
├─ FILE: UmbracoProject/umbraco/Deploy/Revision/document-type__*.uda
├─ LOCATION: PropertyTypes array in appropriate PropertyGroup
└─ INCLUDE: Name, Alias, Key (UUID), PropertyEditorAlias, DataType UDI

STEP 3: Update ApiSafeConverter (if needed)
├─ IF: Property uses custom converter
└─ FILE: Seed.Backoffice.Extensions/ApiSafeConverters/*ApiSafeConverter.cs

STEP 4: Update TypeScript types
├─ FIND: All components consuming this document type
├─ UPDATE: Type definitions to include new property
└─ FILE: Seed.Web/lib/umbraco/types/*.type.ts or component files

STEP 5: Validate
├─ ACTION: cd src/Seed.Web && npx tsc --noEmit
└─ MUST: Zero TypeScript errors
```

### PATTERN: Add New ApiSafeConverter

```
DECISION: Which project?
├─ Standard Umbraco type? → Seed.Core/ApiSafeConverters/
└─ Custom document type? → Seed.Backoffice.Extensions/ApiSafeConverters/

STEP 1: Create converter file
├─ NAME: {ComponentName}ApiSafeConverter.cs
├─ INHERIT: BaseApiSafeConverter OR BaseContentTypeApiSafeConverter
└─ SET: EditorAlias or ContentTypes property

STEP 2: Implement conversion
├─ METHOD: ConvertToApiSafeValue OR ConvertElement
└─ RETURN: Simple, JSON-serializable object

STEP 3: Create output model (if complex)
├─ LOCATION: Seed.Backoffice.Extensions/ApiSafeConverters/Models/
└─ NAME: {ComponentName}Model.cs

STEP 4: Update TypeScript types
├─ LOCATION: Seed.Web/lib/umbraco/types/
├─ CREATE: {componentName}Model.type.ts
└─ EXPORT: Interface matching C# model

STEP 5: No registration needed
└─ Auto-discovered via EditorAlias/ContentTypes
```

### PATTERN: Add Custom Property Editor

```
DECISION: Reusable or project-specific?
├─ Reusable across industries? → Seed.DataTypes/
└─ Project-specific? → Seed.Backoffice.Extensions/CustomPickers/

IF Seed.DataTypes:
├─ CREATE: Seed.DataTypes/{EditorName}/
├─ STRUCTURE:
│  ├─ Core/ → Property editor implementation
│  ├─ Models/ → Data models
│  ├─ Services/ → External API (if needed)
│  └─ wwwroot/App_Plugins/{editorName}/ → Backoffice JS/CSS
└─ REFERENCE: Seed.DataTypes from UmbracoProject

IF Seed.Backoffice.Extensions:
└─ CREATE: Seed.Backoffice.Extensions/CustomPickers/{EditorName}/
```

## Project Size Reference

```
PROJECT                     C# FILES    SCHEMA FILES    TOTAL COMPLEXITY
===========================================================================
Seed.Core                   145         0               High (infrastructure)
Seed.DataTypes              115         0               Medium (15 editors)
Seed.Backoffice.Extensions  Variable    0               High (business logic)
UmbracoProject              2           1,541           Low code, high schema
Seed.Web                    Variable    0               High (frontend)
```

## Lookup Table: Common Tasks

```
TASK                                    PRIMARY LOCATION                           SECONDARY LOCATIONS
=========================================================================================================
Create property editor                  Seed.DataTypes/{Name}/                     -
Create base converter                   Seed.Core/ApiSafeConverters/               -
Create custom converter                 Seed.Backoffice.Extensions/ApiSafeConverters/ -
Define schema                           UmbracoProject/umbraco/Deploy/Revision/    -
Add property to doc type                UmbracoProject/umbraco/Deploy/Revision/    TypeScript types
Create React component                  Seed.Web/common/components/                -
Add TypeScript type                     Seed.Web/lib/umbraco/types/                Component files
Configure middleware                    UmbracoProject/Program.cs                  -
Configure environment                   UmbracoProject/appsettings.*.json          -
Add API endpoint                        UmbracoProject/Controllers/                Seed.Web/app/api/
Implement business logic                Seed.Backoffice.Extensions/                -
Add shared service                      Seed.Core/Services/                        -
Add external API integration            Seed.DataTypes/{Name}/Services/            -
Create email template                   UmbracoProject/Views/Partials/Forms/Emails/ -
Add RTE style                           UmbracoProject/rte-style-formats.json      scss/rte.scss
Update backoffice styles                UmbracoProject/scss/*.scss                 -
```

## File Naming Conventions Lookup

```
FILE TYPE                   PATTERN                                     LOCATION
============================================================================================
ApiSafeConverter            {Name}ApiSafeConverter.cs                   */ApiSafeConverters/
UDA Data Type               data-type__{uuid-with-dashes}.uda           UmbracoProject/umbraco/Deploy/Revision/
UDA Document Type           document-type__{uuid-with-dashes}.uda       UmbracoProject/umbraco/Deploy/Revision/
UDA Container               document-type-container__{uuid}.uda         UmbracoProject/umbraco/Deploy/Revision/
TypeScript Type             {name}.type.ts                              Seed.Web/lib/umbraco/types/
React Component             {ComponentName}.tsx (PascalCase)            Seed.Web/common/components/
Composer                    {Name}Composer.cs                           */
Service                     {Name}Service.cs                            */Services/
Model                       {Name}Model.cs                              */Models/
```
