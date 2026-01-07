# Tasks for Seed.Backoffice.Extensions

This document describes the types of tasks that should be implemented in the `Seed.Backoffice.Extensions` project, with examples and guidance on when to work here versus other projects.

## Overview

**Seed.Backoffice.Extensions** is for **project-specific** business logic, content transformation, and Umbraco customizations. If it's unique to the Keystone Ridge Designs website and not reusable across projects, it belongs here.

---

## Task Categories

### 1. Creating ApiSafeConverters for Custom Content Types

**When:** You need to transform a custom Umbraco document type or element type into JSON for the Delivery API.

**Examples:**

#### New Component Converter
```
Task: "Create a converter for the new 'Video Testimonial' block grid element"

Steps:
1. Create VideoTestimonialApiSafeConverter.cs in ApiSafeConverters/
2. Inherit from BaseContentTypeApiSafeConverter
3. Set ContentTypes = ["videoTestimonial"]
4. Implement ConvertElement method
5. Return JSON-safe object matching frontend TypeScript type
```

#### Complex Nested Converter
```
Task: "Add converter for 'Product Comparison Table' that needs to fetch and compare multiple products"

Steps:
1. Create ProductComparisonTableApiSafeConverter.cs
2. Inject IExamineService for product lookups
3. Inject Lazy<ApiSafeConvertersCollection> for nested conversions
4. Transform product data and comparison metrics
5. Create model in ApiSafeConverters/Models/ if needed
```

**Indicators this task belongs here:**
- ✅ Content type is specific to this project (boats, dealers, products)
- ✅ Requires business logic or data aggregation
- ✅ Needs to call other services (ProductService, BoatHelper)
- ✅ Transforms Block Grid/List items with project-specific structure

**Indicators it belongs in Seed.Core:**
- ❌ Generic converter for standard Umbraco types (media, content pickers)
- ❌ Reusable across multiple projects
- ❌ No project-specific business logic

---

### 2. Implementing Business Logic Services

**When:** You need project-specific services that encapsulate complex business rules or data operations.

**Examples:**

#### Boat-Related Services
```
Task: "Add method to BoatHelper to get boats by length range"

File: BoatHelper.cs
Method: public IEnumerable<BoatTileModel> GetBoatsByLengthRange(int minLength, int maxLength)

Implementation:
- Use IExamineService to search boats
- Filter by length property
- Transform to BoatTileModel
- Return sorted results
```

#### Product Services
```
Task: "Add method to ProductService to get related products based on categories"

File: Products/ProductService.cs
Method: public IEnumerable<ProductListing> GetRelatedProducts(int productId, int count)

Implementation:
- Get product's categories
- Search for products in same categories
- Exclude original product
- Limit to count
- Return with images via MediaApiSafeConverter
```

#### New Service
```
Task: "Create DealerService to manage dealer locator logic"

Steps:
1. Create Products/DealerService.cs
2. Add constructor with IExamineService, IUmbracoContextFactory
3. Implement methods:
   - FindNearestDealers(latitude, longitude, radius)
   - GetDealersByState(string state)
   - GetDealerDetails(int dealerId)
4. Register in ExtensionComposer.cs
5. Inject into relevant converters
```

**Indicators this task belongs here:**
- ✅ Business logic specific to boats, products, dealers, or members
- ✅ Aggregates data from multiple sources
- ✅ Implements project-specific calculations or rules
- ✅ Used by multiple ApiSafeConverters

**Indicators it belongs in Seed.Core:**
- ❌ Generic utility functions
- ❌ Umbraco infrastructure code
- ❌ Reusable across projects

---

### 3. Custom Umbraco Forms Fields and Workflows

**When:** You need custom form functionality specific to this project.

**Examples:**

#### Custom Form Field
```
Task: "Create a 'Dealer Selector' form field that shows dealers near a zip code"

Steps:
1. Create FormExtensions/Fields/DealerSelectorField.cs
2. Inherit from FieldType
3. Add properties: ZipCode, Radius
4. Create HTML template: wwwroot/App_Plugins/UmbracoForms/backoffice/Common/FieldTypes/dealerSelector.html
5. Create AngularJS controller if needed
6. Field auto-registers in Forms
```

#### Custom Workflow
```
Task: "Create workflow to send quote data to Epicor after form submission"

Steps:
1. Create FormExtensions/Workflows/SendToEpicorWorkflow.cs
2. Inherit from WorkflowType
3. Add settings: EpicorEndpoint, ApiKey
4. Implement Execute method
5. Parse form data
6. Call Epicor API
7. Log results
```

#### PreValue Source
```
Task: "Create dynamic dropdown that loads product categories from Umbraco"

Steps:
1. Create FormExtensions/PreValueSourceTypes/ProductCategoryPreValueSource.cs
2. Inject IExamineService
3. Query product categories
4. Return as FormFieldPrevalueDto[]
```

**Indicators this task belongs here:**
- ✅ Form field specific to boats, products, or dealers
- ✅ Workflow that integrates with project systems (Epicor, quotes, etc.)
- ✅ PreValue source that queries project content
- ✅ Requires project-specific validation or processing

---

### 4. Product Catalog Extensions

**When:** You need to extend product-related functionality.

**Examples:**

#### Search Enhancement
```
Task: "Add faceted search to product catalog by material type"

Steps:
1. Update Products/ProductIndexValueSetBuilder.cs to index material field
2. Add method to ProductService: SearchByMaterial(string material)
3. Create ProductMaterialApiSafeConverter if needed for display
4. Update health checks to validate material data
```

#### Epicor Integration
```
Task: "Add real-time inventory check from Epicor"

Steps:
1. Add method to ProductService: GetInventoryLevel(string sku)
2. Use EpicorRESTAPICore to call API
3. Cache results for performance
4. Update ProductQuoteData model to include inventory
5. Modify ProductOptionsApiSafeConverter to include availability
```

#### New Health Check
```
Task: "Create health check to validate all products have pricing"

Steps:
1. Create Products/HealthChecks/PricingCheck.cs
2. Inherit from HealthCheck
3. Query products via ProductService
4. Check for missing or zero prices
5. Return health check results with details
```

**Indicators this task belongs here:**
- ✅ Product-specific business logic
- ✅ Epicor integration
- ✅ Product data validation
- ✅ Quote/pricing calculations

---

### 5. Custom Backoffice UI and Pickers

**When:** You need custom controls or UI in the Umbraco backoffice.

**Examples:**

#### Custom Picker
```
Task: "Create a 'Boat Collection Picker' that shows boats grouped by series"

Steps:
1. Create CustomPickers/BoatCollectionPicker.cs
2. Create AngularJS controller: wwwroot/App_Plugins/CustomPickers/boatCollectionPicker.controller.js
3. Create HTML template: wwwroot/App_Plugins/CustomPickers/boatCollectionPicker.html
4. Implement search/filter logic
5. Return selected boat IDs
```

#### Dashboard Widget
```
Task: "Add dashboard widget showing product import status"

Steps:
1. Create Products/ProductImportDashboard.cs
2. Create HTML view: wwwroot/App_Plugins/Products/dashboard.html
3. Create AngularJS controller for dashboard
4. Display import history, errors, statistics
```

#### Menu Item
```
Task: "Add 'Export Products' menu item to backoffice"

Steps:
1. Update ContentExport/MenuHandler.cs
2. Add new menu item configuration
3. Create controller action
4. Create view if needed
```

**Indicators this task belongs here:**
- ✅ Project-specific backoffice functionality
- ✅ Custom pickers for boats, products, dealers
- ✅ Dashboard widgets for project metrics
- ✅ Backoffice automation tools

---

### 6. Membership and Authentication Extensions

**When:** You need custom member functionality beyond standard Umbraco members.

**Examples:**

#### Member Profile Features
```
Task: "Add 'Saved Boats' functionality to member profiles"

Steps:
1. Update Membership/Models/ with SavedBoat model
2. Add methods to ProfileManager:
   - AddSavedBoat(int memberId, int boatId)
   - GetSavedBoats(int memberId)
   - RemoveSavedBoat(int memberId, int boatId)
3. Update CustomMembershipApiController with endpoints
4. Create converter to expose saved boats in API
```

#### Member Workflows
```
Task: "Create workflow to assign member to dealer territory after registration"

Steps:
1. Create Membership/Workflows/AssignDealerTerritoryWorkflow.cs
2. Get member's zip code
3. Query dealers by location
4. Assign nearest dealer to member property
5. Send notification email
```

#### Custom Member Field
```
Task: "Add 'Preferred Boat Type' field to registration form"

Steps:
1. Create Membership/Fields/BoatTypeSelector.cs
2. Load boat types from Umbraco
3. Create HTML template
4. Save to member profile on registration
```

**Indicators this task belongs here:**
- ✅ Member features specific to boats or dealers
- ✅ Member-dealer relationships
- ✅ Custom member properties for this project
- ✅ Member-specific business logic

---

### 7. Blog Functionality Extensions

**When:** You need to extend blog features beyond standard content.

**Examples:**

#### Blog Search Enhancement
```
Task: "Add tag-based search to blog"

Steps:
1. Update Blog/BlogIndexingComponent.cs to index tags
2. Add method to search by tags
3. Create BlogTagApiSafeConverter for tag displays
4. Update blog feed to support tag filtering
```

#### Related Posts
```
Task: "Add 'Related Posts' based on shared tags"

Steps:
1. Add method to get related posts
2. Compare tags between posts
3. Return most relevant
4. Create converter for related posts display
```

**Indicators this task belongs here:**
- ✅ Blog features specific to this project
- ✅ Blog-boat relationships (e.g., "boats mentioned in post")
- ✅ Custom blog indexing needs

---

### 8. Quote Builder Features

**When:** You need to extend quote generation functionality.

**Examples:**

#### Quote Customization
```
Task: "Add 'Add Custom Message' to quotes"

Steps:
1. Update QuoteBuilder/Models/ with message property
2. Modify QuoteApiController to accept message
3. Include message in generated PDF/email
4. Create form field for message input
```

#### Quote Templates
```
Task: "Create different quote templates for different product categories"

Steps:
1. Add GetQuoteTemplate method to QuoteApiController
2. Determine template based on product category
3. Return template configuration
4. Frontend renders appropriate layout
```

**Indicators this task belongs here:**
- ✅ Quote-specific business logic
- ✅ Pricing calculations
- ✅ Quote formatting and templates
- ✅ Integration with ProductService

---

### 9. Site Search Enhancements

**When:** You need to improve or customize site-wide search.

**Examples:**

#### Search Filters
```
Task: "Add faceted search filters for content type, category, date"

Steps:
1. Update SiteSearch/Models/ with filter models
2. Create SearchFilterApiSafeConverter
3. Build facets from Examine results
4. Return filter options and counts
```

#### Search Boosting
```
Task: "Boost boat and product results in site search"

Steps:
1. Modify search query to apply boosting
2. Weight boats/products higher than blog posts
3. Consider recency for blog posts
4. Update search result ordering
```

**Indicators this task belongs here:**
- ✅ Project-specific search logic
- ✅ Custom result ranking
- ✅ Content-type specific search features

---

### 10. Content Export/Import Features

**When:** You need to export or import content in custom formats.

**Examples:**

#### Export Enhancement
```
Task: "Add 'Export Products to CSV' functionality"

Steps:
1. Update ContentExport/ContentExportService.cs
2. Add ExportProductsToCsv method
3. Query products via ProductService
4. Format as CSV with headers
5. Return downloadable file
6. Add menu item in backoffice
```

#### Bulk Operations
```
Task: "Create bulk product update from CSV import"

Steps:
1. Create ContentExport/ProductImportService.cs
2. Parse CSV file
3. Validate data
4. Update products via ContentService
5. Log changes
6. Report results
```

**Indicators this task belongs here:**
- ✅ Project-specific export formats
- ✅ Business-specific import logic
- ✅ Data transformation for external systems

---

### 11. FlexibleLinks Extensions

**When:** You need new link types beyond standard internal/external links.

**Examples:**

#### Custom Link Type
```
Task: "Create 'Build Your Boat' link that opens builder with pre-selected boat"

Steps:
1. Create FlexibleLinks/BuildYourBoatLinkType.cs
2. Add properties: BoatId, DefaultConfiguration
3. Implement GetUrl method
4. Generate URL with query parameters
5. Link type auto-registers
```

#### Dynamic Link
```
Task: "Create link that goes to user's nearest dealer"

Steps:
1. Create FlexibleLinks/NearestDealerLinkType.cs
2. Add setting: UseUserLocation
3. Implement GetUrl to calculate at runtime
4. Return dealer detail page URL
```

**Indicators this task belongs here:**
- ✅ Project-specific link behavior
- ✅ Dynamic URL generation
- ✅ Links to boats, products, dealers

---

### 12. Tagging System Extensions

**When:** You need to extend the content tagging functionality.

**Examples:**

#### Tag Management
```
Task: "Add auto-tagging based on content keywords"

Steps:
1. Update Tagging/ with auto-tag logic
2. Analyze content for keywords
3. Match against existing tags
4. Automatically apply relevant tags
```

#### Tag Analytics
```
Task: "Track most popular tags for analytics"

Steps:
1. Add tag tracking to Tagging/
2. Count tag usage
3. Create API endpoint for tag stats
4. Display in backoffice dashboard
```

**Indicators this task belongs here:**
- ✅ Project-specific tagging rules
- ✅ Tag relationships to boats/products
- ✅ Custom tag behavior

---

### 13. Video Management Extensions

**When:** You need custom video functionality.

**Examples:**

#### Video Analytics
```
Task: "Track which videos are most watched"

Steps:
1. Update Videos/Models/ with analytics model
2. Add tracking endpoint
3. Store view counts
4. Display popular videos in feeds
```

#### Video Thumbnails
```
Task: "Auto-generate custom thumbnails for videos"

Steps:
1. Add thumbnail generation to Videos/
2. Extract frame at specific timestamp
3. Store as media item
4. Link to video
```

**Indicators this task belongs here:**
- ✅ Project-specific video processing
- ✅ Video-boat relationships
- ✅ Custom video metadata

---

### 14. CookiePro Integration Extensions

**When:** You need to customize cookie consent functionality.

**Examples:**

#### Consent Tracking
```
Task: "Track which users have consented to marketing cookies"

Steps:
1. Update CookiePro/ with tracking logic
2. Store consent preferences
3. Use in analytics decisions
4. Provide API for frontend
```

**Indicators this task belongs here:**
- ✅ Cookie consent customizations
- ✅ Privacy compliance features

---

### 15. Health Checks

**When:** You need to validate data integrity or system health.

**Examples:**

#### Content Validation
```
Task: "Create health check to ensure all boats have images"

Steps:
1. Create HealthChecks/BoatImageCheck.cs
2. Query all boats
3. Verify listingImage property
4. Report boats without images
5. Provide fix suggestions
```

#### Integration Validation
```
Task: "Check Epicor API connectivity and data freshness"

Steps:
1. Create Products/HealthChecks/EpicorConnectivityCheck.cs
2. Attempt API call
3. Check last sync timestamp
4. Verify data consistency
5. Return status
```

**Indicators this task belongs here:**
- ✅ Project-specific data validation
- ✅ Integration health monitoring
- ✅ Content quality checks

---

## Decision Tree: Where Does This Task Belong?

```
Is it project-specific (boats, products, dealers, members)?
├─ NO → Consider Seed.Core or Seed.DataTypes
└─ YES
   │
   ├─ Is it a reusable property editor (custom backoffice control)?
   │  └─ YES → Seed.DataTypes
   │
   ├─ Is it content transformation for the API?
   │  └─ YES → Seed.Backoffice.Extensions/ApiSafeConverters/
   │
   ├─ Is it business logic or service layer?
   │  └─ YES → Seed.Backoffice.Extensions/{appropriate folder}/
   │
   ├─ Is it Umbraco Forms customization?
   │  └─ YES → Seed.Backoffice.Extensions/FormExtensions/
   │
   ├─ Is it product catalog functionality?
   │  └─ YES → Seed.Backoffice.Extensions/Products/
   │
   ├─ Is it membership/authentication?
   │  └─ YES → Seed.Backoffice.Extensions/Membership/
   │
   └─ Is it backoffice UI customization?
      └─ YES → Seed.Backoffice.Extensions/wwwroot/App_Plugins/
```

---

## Anti-Patterns: What NOT to Put Here

### ❌ Generic Umbraco Functionality
```
Bad: Creating a generic "RichTextApiSafeConverter"
Why: Already handled by automatic passthrough in Seed.Core

Good: Creating "BoatDescriptionApiSafeConverter" that adds boat-specific metadata
```

### ❌ Reusable Property Editors
```
Bad: Creating a generic "Color Picker" in Seed.Backoffice.Extensions
Why: Should be in Seed.DataTypes for reusability

Good: Using the color picker in a boat-specific converter
```

### ❌ Frontend Logic
```
Bad: Adding React component logic to ApiSafeConverters
Why: Frontend belongs in Seed.Web

Good: Creating API-safe data structure that frontend can easily consume
```

### ❌ Infrastructure Code
```
Bad: Creating generic caching service in Seed.Backoffice.Extensions
Why: Should be in Seed.Core for reusability

Good: Using Seed.Core caching in ProductService
```

---

## Common Task Patterns

### Pattern 1: New Component Needs Converter

**Scenario:** Frontend team creates new "Boat Comparison" component

**Tasks:**
1. Create `BoatComparisonApiSafeConverter.cs`
2. Create `BoatComparisonModel.cs` in Models/
3. Inject ProductService or BoatHelper if needed
4. Transform data to match TypeScript type
5. Test with real content

### Pattern 2: New Business Feature

**Scenario:** Add "Dealer Loyalty Program"

**Tasks:**
1. Create `DealerLoyalty/` folder
2. Create `DealerLoyaltyService.cs`
3. Create models in `DealerLoyalty/Models/`
4. Register service in ExtensionComposer
5. Create API controller if needed
6. Create converter for frontend data
7. Add health check if needed

### Pattern 3: Extend Existing System

**Scenario:** Add "Product Warranties" to existing products

**Tasks:**
1. Add to `Products/Models/ProductWarranty.cs`
2. Extend `ProductService` with warranty methods
3. Update `ProductIntroApiSafeConverter` to include warranty
4. Update TypeScript types in frontend
5. Add health check for warranty data

### Pattern 4: Custom Form Integration

**Scenario:** "Request Demo" form needs dealer assignment

**Tasks:**
1. Create `FormExtensions/Fields/DealerAssignmentField.cs`
2. Create `FormExtensions/Workflows/AssignDealerWorkflow.cs`
3. Create backoffice UI in wwwroot/App_Plugins/
4. Integrate with DealerService
5. Send notification email

---

## Checklist for New Tasks

Before implementing a task in Seed.Backoffice.Extensions:

- [ ] Is this project-specific to Keystone Ridge Designs?
- [ ] Does it involve boats, products, dealers, or members?
- [ ] Does it require business logic unique to this project?
- [ ] Will it be consumed by the frontend via Delivery API?
- [ ] Does it extend Umbraco functionality in a project-specific way?

If you answered YES to most of these, proceed with implementation in Seed.Backoffice.Extensions.

If NO, consider:
- **Seed.Core** - For reusable, generic functionality
- **Seed.DataTypes** - For reusable property editors
- **Seed.Web** - For frontend logic
- **UmbracoProject** - For configuration or startup logic

---

## Getting Started Template

When starting a new task in Seed.Backoffice.Extensions:

1. **Identify the category** from this document
2. **Find similar existing code** to use as a template
3. **Follow the pattern** established in that category
4. **Create models** in appropriate Models/ folder if needed
5. **Register services** in ExtensionComposer if needed
6. **Create tests** for business logic
7. **Update TypeScript types** in Seed.Web if creating converter
8. **Document** any complex logic

---

## Summary

**Seed.Backoffice.Extensions is for:**
- ✅ Project-specific ApiSafeConverters
- ✅ Business logic services (products, boats, dealers, members)
- ✅ Umbraco Forms customizations
- ✅ Custom backoffice UI and pickers
- ✅ Integration with external systems (Epicor)
- ✅ Data validation and health checks
- ✅ Content transformation and export

**Seed.Backoffice.Extensions is NOT for:**
- ❌ Generic, reusable Umbraco functionality
- ❌ Reusable property editors (use Seed.DataTypes)
- ❌ Frontend React components (use Seed.Web)
- ❌ Infrastructure code (use Seed.Core)
- ❌ Configuration (use UmbracoProject)

**Key Principle:** If it's specific to this project's business domain (boats, products, dealers), it belongs here. If it's generic Umbraco functionality, it belongs elsewhere.
