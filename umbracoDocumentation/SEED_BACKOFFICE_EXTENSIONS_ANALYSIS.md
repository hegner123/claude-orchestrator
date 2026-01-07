# Seed.Backoffice.Extensions In-Depth Analysis

This document provides a comprehensive analysis of the `Seed.Backoffice.Extensions` project, which contains project-specific Umbraco CMS extensions and business logic for the Keystone Ridge Designs website.

## Project Overview

**Type:** .NET 8 Razor Class Library
**Purpose:** Project-specific business logic, ApiSafeConverters, and custom Umbraco backoffice functionality
**Dependencies:**
- Seed.Core (base library)
- Seed.DataTypes (custom property editors)
- Umbraco.Cms.Core (13.12.0)
- Umbraco.Cms.Web.BackOffice (13.12.0)
- Umbraco.Forms.Core (13.7.0)
- EpicorRESTAPICore (2.2.0.2) - ERP integration
- uSync.Core (13.2.0)

**Referenced By:** UmbracoProject (main application)

---

## Directory Structure

```
Seed.Backoffice.Extensions/
├── ApiSafeConverters/        # 53 custom converters for content transformation
│   └── Models/               # Supporting data models for converters
├── Blog/                     # Blog functionality and custom indexing
├── ContentExport/            # Content export utilities for backoffice
├── CookiePro/                # Cookie consent integration
├── CustomPickers/            # Project-specific picker controls
├── FlexibleLinks/            # Custom link types
├── FormExtensions/           # Umbraco Forms customizations
│   ├── Fields/               # Custom form fields
│   ├── Models/               # Form data models
│   ├── PreValueSourceTypes/  # Custom dropdown data sources
│   └── Workflows/            # Form submission workflows
├── Membership/               # Member management and authentication
│   ├── Fields/               # Membership-specific form fields
│   ├── Models/               # Member data models
│   └── Workflows/            # Member-related workflows
├── Products/                 # Product catalog and Epicor integration
│   ├── HealthChecks/         # Product data validation checks
│   ├── Models/               # Product data models
│   └── Services/             # Product business logic
├── QuoteBuilder/             # Quote generation system
│   └── Models/               # Quote data models
├── SiteSearch/               # Site search functionality
│   └── Models/               # Search data models
├── Tagging/                  # Content tagging system
├── ValueMappers/             # Custom value transformation
├── Videos/                   # Video management
│   └── Models/               # Video data models
└── wwwroot/                  # Frontend assets for backoffice
    └── App_Plugins/          # Backoffice JavaScript/CSS/HTML
```

---

## Core Components

### 1. ApiSafeConverters/ (53 Converters)

**Purpose:** Transform complex Umbraco content structures into JSON-safe data for the Delivery API.

**Architecture Pattern:** Each converter inherits from `BaseContentTypeApiSafeConverter` and targets specific content type aliases.

#### Complete List of Converters

**Banner & Hero Components:**
- `BannerBreadcrumbApiSafeConverter` - Breadcrumb navigation banners
- `BannerVideoApiSafeConverter` - Video background banners

**Call-to-Action (CTA) Components:**
- `CtaBasicApiSafeConverter` - Basic call-to-action blocks
- `CtaBoatWizardApiSafeConverter` - Boat builder wizard CTAs
- `CtaImageScrollRevealApiSafeConverter` - Scroll-triggered image reveal CTAs
- `CtaRotatingImageApiSafeConverter` - Rotating image CTAs
- `CtaVideoApiSafeConverter` - Video-based CTAs

**Carousel Components:**
- `CarouselBlogApiSafeConverter` - Blog post carousels
- `CarouselBoatApiSafeConverter` - Boat showcase carousels
- `CarouselCategoriesApiSafeConverter` - Category carousels
- `CarouselProductsApiSafeConverter` - Product carousels
- `CarouselTestimonialsApiSafeConverter` - Customer testimonial carousels

**Feed/Listing Components:**
- `FeedBlogApiSafeConverter` - Blog feed listings
- `FeedBoatsApiSafeConverter` - Boat catalog feeds
- `FeedCollectionsApiSafeConverter` - Product collection feeds
- `FeedCompareBoatsApiSafeConverter` - Boat comparison feeds
- `FeedGalleryApiSafeConverter` - Image gallery feeds
- `FeedProductCategoryApiSafeConverter` - Product category feeds
- `FeedProductsApiSafeConverter` - Product listing feeds
- `FeedResourcesApiSafeConverter` - Resource library feeds

**Navigation & Structure:**
- `BreadcrumbApiSafeConverter` - Breadcrumb navigation
- `BoatNavigationStandardApiSafeConverter` - Boat-specific navigation
- `FilterNavigationApiSafeConverter` - Filterable navigation
- `FooterLinksApiSafeConverter` - Footer link groups
- `MainLinkApiSafeConverter` - Primary navigation links
- `PageLinksApiSafeConverter` - Page-level link collections
- `ColumnLinksApiSafeConverter` - Multi-column link layouts

**Content Display:**
- `AccordionApiSafeConverter` - Accordion/collapsible content
- `GridTabItemApiSafeConverter` - Grid-based tabbed content
- `TabItemApiSafeConverter` - Tab navigation items
- `ScrollingGalleryApiSafeConverter` - Scrolling image galleries
- `HotspotsHorizontalApiSafeConverter` - Interactive hotspot images
- `BrochuresApiSafeConverter` - Downloadable brochure listings

**Boat-Specific:**
- `BoatDetailsMetricApiSafeConverter` - Boat specifications and metrics
- `BoatOptionsApiSafeConverter` - Boat configuration options
- `BoatQuickSpecsApiSafeConverter` - Quick specification displays
- `BoatSelectorApiSafeConverter` - Boat selection interfaces

**Product-Specific:**
- `ProductIntroApiSafeConverter` - Product introduction sections
- `ProductOptionsApiSafeConverter` - Product configuration options
- `ProductFilesApiSafeConverter` - Product-related file downloads

**Dealer & Location:**
- `DealerSearchApiSafeConverter` - Dealer locator search
- `DealerStandardApiSafeConverter` - Standard dealer listings

**Blog & Content:**
- `BlogDetailsApiSafeConverter` - Blog post details
- `BlogFeedApiSafeConverter` - Blog feed (alternative implementation)
- `AuthorProfileStandardApiSafeConverter` - Author profile displays

**Statistics & Data:**
- `StatsSummaryApiSafeConverter` - Statistical summary displays
- `StatsWithHighlightsApiSafeConverter` - Highlighted statistics

**Sliders:**
- `SliderCommunityApiSafeConverter` - Community content sliders

**Search & SEO:**
- `SearchApiSafeConverter` - Search result formatting
- `SeoSettingsApiConverter` - SEO metadata transformation

**Mapping:**
- `SitemapLayerApiSafeConverter` - Sitemap layer data

**Authentication:**
- `LoginFormApiSafeConverter` - Login form configuration

**Side Navigation:**
- `SideNavigationData` - Side navigation structure

#### Converter Pattern Example

```csharp
public class AccordionApiSafeConverter : BaseContentTypeApiSafeConverter
{
    public override string[] ContentTypes => ["accordion"];

    public override object ConvertElement(
        IPublishedElement element,
        string? culture,
        string? segment,
        List<int> ids,
        Dictionary<string, object>? additionalData = null)
    {
        // Transform complex Umbraco structure into simple JSON
        return new {
            Intro = element.Value<string>("intro"),
            Items = transformedItems,
            Categories = categories
        };
    }
}
```

**Key Features:**
- **Automatic Registration:** Converters are discovered via `ContentTypes` property
- **Nested Conversion:** Converters can call other converters (e.g., BlockGrid within Accordion)
- **Circular Reference Prevention:** Uses `ids` list to track processed nodes
- **Culture Support:** Handles multi-language content via `culture` parameter

#### ApiSafeConverters/Models/

Supporting data models for converter output:

- **`AccordionFilter`** - Accordion category filters
- **`ApiSafeMainLink`** - Main navigation link structure
- **`BoatGroup`** - Boat grouping data
- **`BoatTileModel`** - Boat tile display model
- **`BreadcrumbData`** - Breadcrumb navigation structure
- **`BreadcrumbItem`** - Individual breadcrumb item
- **`ColumnLink`** - Multi-column link item
- **`FeedBoatGroup`** - Boat feed grouping
- **`FilterBucket`** - Filter container
- **`FilterGroup`** - Filter group structure
- **`FilterOption`** - Individual filter option
- **`IFilter`** - Filter interface
- **`LinkWithChildren`** - Hierarchical link structure
- **`LinkWithChildrenPlusToggle`** - Expandable link structure
- **`ModifiedFooterLinks`** - Footer link transformation
- **`NestableLink`** - Nested navigation links
- **`PageLink`** - Page reference link
- **`ProductOptions`** - Product option structure
- **`SideNavigationData`** - Side navigation structure

**Pattern:** These models represent the "API-safe" output that the frontend TypeScript types mirror.

---

### 2. Blog/

**Purpose:** Custom blog functionality with specialized indexing for search and filtering.

**Files:**
- **`BlogComposer.cs`** - Dependency injection setup for blog services
- **`BlogIndex.cs`** - Custom Examine index definition for blog content
- **`BlogIndexingComponent.cs`** - Blog content indexing logic

**Functionality:**
- Custom Examine index for fast blog post searching
- Specialized indexing of blog metadata (tags, categories, authors, dates)
- Optimized for blog-specific queries (by author, by tag, by date range)

**Integration Point:** Works with `BlogDetailsApiSafeConverter` and `BlogFeedApiSafeConverter` to deliver blog content to frontend.

---

### 3. Products/

**Purpose:** Comprehensive product catalog management with Epicor ERP integration.

**Architecture:** This is one of the most complex subsystems in the project.

#### Key Services

**`ProductService.cs`** (715 lines)

Core business logic for product management:

**Methods:**

1. **`List(IEnumerable<string> ids, string contentType)`**
   - Retrieves products by IDs
   - Uses custom "productIndex" Examine index
   - Returns `PickerOption` for backoffice pickers
   - Supports both product groups and individual products

2. **`List(string contentType, string searchTerm)`**
   - Searches products by name or description
   - Weighted search (name=5, description=1)
   - Wildcard matching enabled
   - Sorted alphabetically

3. **`GetQuoteData(int id)`**
   - Retrieves product quote configuration
   - Finds all quotable variants for a product
   - Builds option groups based on category settings
   - Returns `ProductQuoteData` with variants and options

4. **`GetCategories()`**
   - Retrieves product category hierarchy
   - Includes subcategories
   - Returns structured `ProductCategory` objects

5. **`GetProductGroups(string id)`**
   - Gets product groups for Forms dropdown
   - Used in Umbraco Forms for product selection

6. **`GetProductConfiguration(int id)`**
   - Retrieves full product configuration for builder
   - Includes option groups, pricing, and dependencies
   - Returns `ProductConfigurationData`

7. **`GetOptionCaption(string category, string value)`**
   - Translates option IDs to display names
   - Used for quote/order display

8. **`GetProductDescription(string sku)`**
   - Retrieves product description by SKU

9. **`Import(bool replace)`**
   - **CRITICAL:** Imports products from Epicor ERP
   - Creates/updates products, collections, and categories
   - Uses blueprints for consistent structure
   - Updates assets and relationships
   - Transaction-safe (rolls back on error)
   - Returns count of imported products

**Import Process:**
1. Reads Epicor data from "productIndex" Examine index
2. Creates collections based on product codes
3. Creates categories and subcategories
4. Creates or updates product nodes
5. Links products to collections and categories
6. Updates Block Grid feeds to reference new content

#### Indexing Components

**`ProductIndex.cs`**
- Custom Examine index definition for products
- Indexes product variants with searchable fields

**`ProductIndexValueSetBuilder.cs`**
- Defines which fields are indexed
- Configures field weights and analyzers

**`ProductIndexPopulator.cs`**
- Populates product index from Epicor data source
- Handles bulk indexing operations

#### Pickers

**`ProductGroupPicker.cs`**
- Custom backoffice picker for product groups
- Uses ProductService for search

**`ProductCategoryPicker.cs`**
- Custom picker for product categories

#### Controllers

**`AutodeskApiController.cs`**
- API endpoints for Autodesk Forge integration
- CAD file translation and viewing

#### Health Checks

Located in `Products/HealthChecks/`:

**`ProductEpicorCheck.cs`**
- Validates Epicor data integration
- Checks for missing or invalid product data

**`AssetsCheck.cs`**
- Validates product asset completeness
- Ensures required media files exist

**`DescriptionCheck.cs`**
- Checks for missing product descriptions
- Quality assurance for content

**`AutodeskUploadCheck.cs`**
- Validates Autodesk file uploads
- Checks CAD file processing status

#### File Handlers

**`File3dSavingHandler.cs`**
- Handles 3D file uploads (DWG, IGS, SKP)
- Triggers Autodesk translation workflow

#### Models

Located in `Products/Models/`:

**Data Transfer Objects:**
- **`FullProduct`** - Complete product data structure
- **`ProductListng`** - Product listing view model (note: typo in original)
- **`ProductCategory`** - Category hierarchy
- **`ProductSubCategory`** - Subcategory reference
- **`ProductConfigurationData`** - Product builder configuration
- **`ProductQuoteData`** - Quote generation data
- **`ProductOptionGroup`** - Option group structure
- **`ProductGroup`** - Product group data
- **`OptionDependency`** - Option dependencies (conditional options)

**API Integration:**
- **`AutodeskTranslateResponse`** - Autodesk API response
- **`AutodeskTranslateStatus`** - Translation status tracking

**Supporting:**
- **`NodeReference`** - Umbraco node reference
- **`BlockList`** - Block list data structure

**Integration Points:**
- Uses `ApiSafeConverters` for product data transformation
- Integrates with `QuoteBuilder` for quote generation
- Provides data to `FeedProductsApiSafeConverter` and `ProductIntroApiSafeConverter`
- Uses Epicor ERP as data source (via Examine index)

---

### 4. FormExtensions/

**Purpose:** Extensive Umbraco Forms customizations for complex form scenarios.

#### Custom Fields (`Fields/`)

**`BoatBuilderImage`**
- Image selector for boat configuration
- Stores builder preset images

**`LongHiddenField`**
- Hidden field with extended value length
- Stores complex JSON data from boat builder

**`SubmitEventTracker`**
- Tracks form submission events
- Analytics integration

**Additional Fields:**
- Custom text fields with API validation
- Date pickers with default values
- Dependent dropdowns (cascading selections)
- Session validation fields
- Multi-column checkbox lists
- Radio buttons with horizontal layout

#### PreValue Source Types (`PreValueSourceTypes/`)

**`ManualPreValueSourceType.cs`**
- Custom dropdown data source
- Allows manual entry of options with multi-culture support

#### Workflows (`Workflows/`)

**`BoatBuildSheetRedirect.cs`**
- Redirects to boat build sheet after form submission
- Passes configuration data to builder

#### Models (`Models/`)

**`BuilderImageModel`**
- Image data for boat builder
- Includes crop coordinates and display options

**`MultiCulturePreValue`**
- Multi-language form option values

#### Frontend Assets (`wwwroot/App_Plugins/FormExtensions/`)

**Controllers (JavaScript):**
- `api-mapper.controller.js` - Maps form fields to API endpoints
- `database-column-selector.controller.js` - Selects database columns for mapping
- `dependent-prevalues.controller.js` - Manages dependent dropdown options
- `field-picker.controller.js` - Picks form fields
- `multi-field-picker.controller.js` - Multi-field selection
- `multi-values.controller.js` - Multiple value entry
- `paired-column-picker.controller.js` - Paired column selection
- `table-mapper.controller.js` - Maps form data to table columns

**Styles:**
- `dependentPrevalues.css`
- `tableMapper.css`

**HTML Templates (`wwwroot/App_Plugins/UmbracoForms/backoffice/Common/`):**

Field Types:
- `apiValidatedTextfield.html`
- `boatbuilderimage.html`
- `datepickerWithDefault.html`
- `dependentDropdown.html`
- `sessionCheck.html`
- `longhiddenfield.html`
- `multiColumnCheckboxList.html`
- `radioButtonsWithHorizontal.html`

Setting Types:
- `apiMapper.html`
- `databaseColumnSelector.html`
- `dependentPrevalues.html`
- `fieldpicker.html`
- `multiFieldPicker.html`
- `multivalues.html`
- `pairedColumnPicker.html`
- `tableMapper.html`

**Key Feature:** Complex boat builder form that captures configuration and generates quotes.

---

### 5. Membership/

**Purpose:** Custom member management and profile functionality.

#### Core Interface

**`IProfileManager`**
- Contract for profile management operations

**`ProfileManager`**
- Implementation of profile management
- Handles member data CRUD operations

#### API Controller

**`CustomMembershipApiController.cs`**
- Custom API endpoints for member operations
- Authentication and authorization logic

#### Composer

**`MembershipComposer.cs`**
- Registers profile manager and services

#### Fields (`Fields/`)

Custom form fields for member registration and profile updates.

#### Workflows (`Workflows/`)

Form workflows for member-related operations:
- Registration workflows
- Profile update workflows
- Password reset workflows

#### Models (`Models/`)

Member data transfer objects and view models.

**Integration:** Registered in `ExtensionComposer.cs` as singleton `IProfileManager`.

---

### 6. QuoteBuilder/

**Purpose:** Generate product quotes based on user selections.

#### Components

**`QuoteApiController.cs`**
- API endpoints for quote generation
- Calculates pricing based on product options
- Returns quote data for display or PDF generation

**`QuoteBuilderLinkCheck.cs`**
- Validates quote builder links
- Ensures quote data integrity

**`QuoteBuilderLinkType.cs`**
- Custom link type for quote builder
- Used in FlexibleLinks system

#### Models (`Models/`)

Quote data structures:
- Quote line items
- Pricing calculations
- Product selections
- Customer information

**Integration:** Works with `ProductService.GetQuoteData()` to retrieve product configuration.

---

### 7. SiteSearch/

**Purpose:** Site-wide search functionality.

#### Models (`Models/`)

Search-related data models:
- Search query parameters
- Search result models
- Facet/filter data

**Integration:** Uses Examine indexes (ExternalIndex, ProductIndex, BlogIndex) for fast searching.

---

### 8. Tagging/

**Purpose:** Content tagging system for categorization and filtering.

**Functionality:**
- Tag management
- Content-to-tag relationships
- Tag-based filtering in feeds

---

### 9. Videos/

**Purpose:** Video content management.

#### Models (`Models/`)

Video data models:
- Video metadata
- Embed configurations
- Thumbnail data

**Integration:** Works with `Seed.DataTypes.VideoEmbedder` and `Seed.DataTypes.VimeoVideoSelector`.

---

### 10. ValueMappers/

**Purpose:** Custom value transformation for property editors.

**Functionality:**
- Transforms property values during save/retrieve
- Custom serialization/deserialization
- Data migration support

---

### 11. ContentExport/

**Purpose:** Export content from Umbraco for backup or migration.

#### Components

**`ContentExportService.cs`**
- Core export logic
- Serializes content to JSON/XML

**`ContentExportApiController.cs`**
- API endpoints for export operations

**`ContentExportComposer.cs`**
- Dependency injection setup

**`ExportData.cs`**
- Export data structure

**`MenuHandler.cs`**
- Adds export menu items to backoffice

**Frontend Assets (`wwwroot/App_Plugins/ContentExport/`):**
- Backoffice UI for content export

---

### 12. CookiePro/

**Purpose:** OneTrust CookiePro consent management integration.

**Functionality:**
- Cookie consent tracking
- Privacy compliance
- Cookie preference management

---

### 13. CustomPickers/

**Purpose:** Additional project-specific picker controls beyond those in Seed.DataTypes.

**Functionality:**
- Custom content pickers with specific filtering
- Specialized node selectors
- Context-aware picker controls

---

### 14. FlexibleLinks/

**Purpose:** Custom link type implementations for the FlexibleLinks system.

#### Link Types

**`BoatBuilderLinkType.cs`**
- Links to boat builder with configuration
- Passes boat selection to builder

**`PrintLinkType.cs`**
- Generates print-friendly page links
- Triggers print dialog

**Integration:** Extends `Seed.DataTypes.FlexibleLinks` with project-specific link types.

---

### 15. wwwroot/App_Plugins/

**Purpose:** Frontend assets for Umbraco backoffice customizations.

#### Structure

```
wwwroot/App_Plugins/
├── ContentExport/          # Content export UI
├── Fixes/                  # Backoffice bug fixes
├── FormExtensions/         # Form customization UI
│   ├── *.controller.js     # Angular controllers
│   └── *.css               # Styles
├── Products/               # Product management UI
│   ├── EpicorDummyData.json
│   └── EpicorUDCodesDummyData.json
├── QuoteBuilder/           # Quote builder UI
├── TableColumn/            # Table column picker
└── UmbracoForms/           # Forms field/setting templates
    └── backoffice/
        └── Common/
            ├── FieldTypes/ # Custom field HTML
            └── SettingTypes/ # Custom setting HTML
```

**Technologies:**
- AngularJS (Umbraco backoffice framework)
- HTML templates
- CSS stylesheets
- JSON configuration files

---

## Key Helper Classes

### BoatHelper.cs

**Purpose:** Centralized boat-specific business logic.

**Methods:**

**`GetBoatGroups(string labelPattern, Func<IPublishedContent, string> getUrl)`**
- Retrieves all boats from Examine
- Groups boats for display
- Transforms to `BoatTileModel` for frontend
- Uses `MediaApiSafeConverter` for images

**`GetBuilderUrl(IPublishedContent boat, string? culture)`**
- Gets boat builder URL from boat content
- Culture-aware for multi-language sites

**Dependencies:**
- `IExamineService` - Search functionality
- `IUmbracoContextFactory` - Content access
- `ApiSafeConvertersCollection` - Image transformation

**Registration:** Singleton in `ExtensionComposer`

---

## Dependency Injection Pattern

### ExtensionComposer.cs

**Purpose:** Umbraco composer for registering services.

```csharp
public class ExtensionComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        builder.Services.AddSingleton<BoatHelper>();
        builder.Services.AddSingleton<IProfileManager, ProfileManager>();
        // ApiSafeConverters auto-registered by EditorAlias
    }
}
```

**Pattern:**
- Singletons for stateless services (BoatHelper, ProfileManager)
- ApiSafeConverters auto-discovered via reflection
- Composers chain with Seed.Core and Seed.DataTypes composers

---

## Integration with Epicor ERP

### EpicorRESTAPICore Package

**Purpose:** Integration with Epicor ERP system for product data.

**Data Flow:**
1. **External Process** → Fetches data from Epicor REST API
2. **Examine Index** → Stores Epicor data in "productIndex"
3. **ProductService** → Reads from index
4. **Import** → Creates/updates Umbraco content from Epicor data

**Key Fields from Epicor:**
- Product SKU
- Name/Description
- Pricing (UnitPrice)
- Categories
- Product Groups
- Variants
- Options
- Dimensions (Length, Width, Height, Weight)
- Quick Ship availability

**Benefits:**
- Offline access to product data
- Fast search via Examine
- Umbraco content remains source of truth for display
- Epicor remains source of truth for pricing/inventory

---

## Frontend Asset Organization

### App_Plugins Structure

**Controllers Pattern:**
```javascript
// Angular controller for Umbraco backoffice
angular.module("umbraco").controller("CustomController",
    function ($scope, $http) {
        // Controller logic
    }
);
```

**HTML Templates Pattern:**
```html
<!-- Backoffice property editor view -->
<div ng-controller="CustomController">
    <!-- Angular bindings and Umbraco directives -->
</div>
```

**Integration:**
- JavaScript controllers loaded by Umbraco backoffice
- HTML templates referenced in C# property editor definitions
- CSS automatically loaded when property editors are used

---

## Best Practices Observed

### ApiSafeConverter Design

1. **Single Responsibility:** Each converter handles one content type
2. **Composition:** Converters call other converters for nested structures
3. **Null Safety:** Always check for null values before processing
4. **Culture Awareness:** Pass culture parameter through conversion chain
5. **Circular Prevention:** Track processed IDs to prevent infinite loops

### Service Design

1. **Dependency Injection:** All services use constructor injection
2. **Interface Contracts:** Key services implement interfaces (IProfileManager)
3. **Singleton Pattern:** Stateless services registered as singletons
4. **Lazy Loading:** ApiSafeConvertersCollection injected as `Lazy<>` to prevent circular dependencies

### Product Import Design

1. **Blueprint Pattern:** Use content blueprints for consistent structure
2. **Transaction Safety:** Scope-based rollback on errors
3. **Idempotency:** Can re-run import without creating duplicates
4. **Relationship Management:** Updates references between products, collections, categories

---

## Common Patterns

### Examine Search Pattern

```csharp
var results = _examineService.Search(new PublishedContentSearchParameters {
    ExamineIndex = "ProductIndex",
    AllowedContentTypes = ["product"],
    SortingDefinition = new SortingDefinition {
        SortType = Examine.Search.SortType.String,
        Alias = "nodeName",
        Direction = Core.Enums.SortDirectionEnum.Ascending
    },
    Filters = new List<ExamineSearchModel> {
        new ExamineSearchModel {
            Keywords = [searchTerm],
            Fields = new List<ExamineSearchFieldWeight> {
                new ExamineSearchFieldWeight {
                    Name = "nodeName",
                    Weight = 5,
                    Wildcard = true
                }
            }
        }
    }
});
```

### ApiSafeConverter Usage Pattern

```csharp
var mediaConverter = _apiSafeConverters.Value
    .FirstOrDefault(x => x.IsEditor(Constants.PropertyEditors.Aliases.MediaPicker3));

var image = (ApiSafeImage)mediaConverter?.ConvertToApiSafeValue(
    element.Value<MediaWithCrops>("image"),
    culture,
    segment,
    ids,
    additionalData
);
```

### Umbraco Context Pattern

```csharp
using (var cref = _umbracoContextFactory.EnsureUmbracoContext())
{
    var node = cref.UmbracoContext.Content.GetById(id);
    // Work with node
}
```

---

## Key Architectural Decisions

### 1. Context-Specific Converters

**Decision:** Create 53 specialized converters instead of generic ones.

**Rationale:**
- Each component has unique transformation needs
- Easier to maintain (one converter = one component)
- Clear mapping to frontend components
- No complex conditional logic

**Trade-off:** More files, but better clarity and maintainability.

### 2. Examine-Based Product Catalog

**Decision:** Use Examine indexes instead of direct Epicor API calls.

**Rationale:**
- Fast search performance
- Offline availability
- Reduces load on Epicor system
- Umbraco-native search capabilities

**Trade-off:** Requires synchronization process, eventual consistency.

### 3. Boat Builder via Forms

**Decision:** Use Umbraco Forms with custom fields for boat configuration.

**Rationale:**
- Leverage Forms workflow capabilities
- Easy content editor management
- Built-in validation
- Custom fields for specific needs

**Trade-off:** Complex form setup, but flexible and maintainable.

### 4. Singleton Services

**Decision:** BoatHelper and ProfileManager as singletons.

**Rationale:**
- Stateless services with no per-request state
- Better performance (no allocation per request)
- Thread-safe implementations

**Trade-off:** Must be thread-safe.

---

## Extension Points

### Adding a New ApiSafeConverter

1. Create class inheriting `BaseContentTypeApiSafeConverter`
2. Override `ContentTypes` property with content type alias(es)
3. Implement `ConvertElement` method
4. Return JSON-serializable object
5. Converter auto-registers via reflection

### Adding a New Custom Form Field

1. Create class inheriting appropriate Forms field base class
2. Create HTML template in `wwwroot/App_Plugins/UmbracoForms/`
3. Create AngularJS controller if needed
4. Field auto-registers in Forms

### Adding a New Product Health Check

1. Create class in `Products/HealthChecks/`
2. Inherit from Umbraco health check base class
3. Implement check logic
4. Appears in backoffice health check dashboard

---

## Performance Considerations

### Examine Indexing

**Optimization:**
- Products indexed separately from main content (ProductIndex)
- Blog indexed separately (BlogIndex)
- Reduces index size and improves search speed

### ApiSafeConverter Caching

**Pattern:** Converters are stateless and call-per-request.

**Consideration:** Heavy conversion should cache results at controller/service level, not in converters.

### Lazy Loading

**Pattern:** `Lazy<ApiSafeConvertersCollection>` prevents circular dependencies and delays initialization.

---

## Testing Considerations

### Unit Testing Targets

**Services:**
- ProductService.List methods
- ProductService.GetQuoteData
- ProductService.GetProductConfiguration
- BoatHelper.GetBoatGroups

**Converters:**
- Each converter's ConvertElement method
- Mock IPublishedElement and dependencies
- Assert output structure matches TypeScript types

### Integration Testing Targets

**Product Import:**
- ProductService.Import with test Epicor data
- Verify content creation
- Verify relationship linking

**Health Checks:**
- Run checks against test data
- Verify detection of issues

---

## Security Considerations

### Authentication

**Membership:**
- Custom member authentication via ProfileManager
- JWT token validation (in main app)

### Authorization

**Product Import:**
- Requires backoffice user authentication
- Uses `IBackOfficeSecurityAccessor` to get current user

**API Controllers:**
- Should validate user permissions
- Use Umbraco's authorization attributes

---

## Troubleshooting Guide

### Common Issues

**Issue:** ApiSafeConverter not being called

**Solution:**
- Verify `ContentTypes` array contains correct alias
- Check converter is in Seed.Backoffice.Extensions namespace
- Ensure project is referenced by UmbracoProject

**Issue:** Product import failing

**Solution:**
- Check Epicor data in ProductIndex
- Verify blueprints exist with correct GUIDs
- Check user has permission to create content
- Review logs for specific error

**Issue:** Form field not appearing

**Solution:**
- Verify HTML template in correct wwwroot location
- Check AngularJS controller registration
- Clear browser cache
- Restart application

---

## Dependency Graph

```
ExtensionComposer
    ├── BoatHelper (singleton)
    │   ├── IExamineService
    │   ├── IUmbracoContextFactory
    │   └── Lazy<ApiSafeConvertersCollection>
    │
    └── ProfileManager (singleton)
        └── IProfileManager interface

ApiSafeConverters (auto-registered)
    ├── BaseContentTypeApiSafeConverter
    ├── IUmbracoContextAccessor
    └── Lazy<ApiSafeConvertersCollection> (for nested conversion)

ProductService
    ├── IExamineService
    ├── IUmbracoContextFactory
    ├── Lazy<ApiSafeConvertersCollection>
    ├── IShortStringHelper
    ├── IScopeProvider
    ├── IContentService
    └── IBackOfficeSecurityAccessor
```

---

## Summary

**Seed.Backoffice.Extensions** is the heart of project-specific business logic, containing:

- **53 ApiSafeConverters** that transform Umbraco content into JSON for the Next.js frontend
- **Product catalog system** with Epicor ERP integration
- **Boat builder** with custom form fields and quote generation
- **Blog system** with custom indexing
- **Membership management** with custom authentication
- **Content export** for backup/migration
- **Extensive backoffice customizations** via App_Plugins

**Key Strength:** Clear separation of concerns - each converter handles one content type, each service handles one domain area.

**Main Integration Point:** Provides the data transformation layer between Umbraco CMS and the Next.js frontend, ensuring clean, type-safe API responses.
