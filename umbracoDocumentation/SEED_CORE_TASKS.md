# Tasks for Seed.Core

This document describes the types of tasks that should be implemented in the `Seed.Core` project, with examples and guidance on when to work here versus other projects.

## Overview

**Seed.Core** is for **reusable, generic** infrastructure code that could be used across multiple Umbraco projects. If it's specific to boats, products, or dealers, it belongs elsewhere. If it's reusable Umbraco functionality, it belongs here.

**Key Principle:** "Could this be used in a different Umbraco project?" If YES → Seed.Core. If NO → Seed.Backoffice.Extensions.

---

## Task Categories

### 1. Creating Base ApiSafeConverters for Standard Umbraco Types

**When:** You need to transform a standard Umbraco property editor (not project-specific) into JSON for the Delivery API.

**Examples:**

#### New Standard Property Editor Converter
```
Task: "Create converter for the new Umbraco.Tags property editor"

Steps:
1. Create TagsApiSafeConverter.cs in ApiSafeConverters/
2. Inherit from BaseApiSafeConverter
3. Set EditorAlias = ["Umbraco.Tags"]
4. Implement ConvertToApiSafeValue method
5. Return string[] of tag names
6. Converter auto-registers
```

#### Multi-Picker Converter Enhancement
```
Task: "Enhance MultiNodeTreePicker converter to include node depth"

Steps:
1. Update PublishedContentApiSafeConverter.cs
2. Add depth calculation to node conversion
3. Include in JsonPublishedContent model
4. Update all consuming code
```

#### New Media Type Converter
```
Task: "Add support for Audio media type in MediaApiSafeConverter"

Steps:
1. Update MediaApiSafeConverter.cs
2. Add case for "umbracoMediaAudio"
3. Create ApiSafeAudio model in Models/
4. Extract audio metadata (duration, bitrate, etc.)
5. Return ApiSafeAudio instance
```

**Indicators this task belongs here:**
- ✅ Converts a standard Umbraco property editor (shipped with Umbraco)
- ✅ Reusable across any Umbraco project
- ✅ No business logic specific to this project
- ✅ Creates generic, JSON-safe output

**Indicators it belongs in Seed.Backoffice.Extensions:**
- ❌ Converts project-specific content types (boats, products, dealers)
- ❌ Requires business logic or calculations
- ❌ Needs to aggregate data from multiple sources
- ❌ Specific to component structure (accordions, carousels, etc.)

---

### 2. Implementing Core Services

**When:** You need reusable service functionality that multiple projects could use.

**Examples:**

#### Search Service Enhancement
```
Task: "Add faceted search support to ExamineService"

File: Services/ExamineService.cs
Method: public FacetedSearchResults SearchWithFacets(PublishedContentSearchParameters config)

Implementation:
- Build Examine query as usual
- Group results by facet fields
- Count results per facet value
- Return results + facet counts
```

#### Image Processing Service
```
Task: "Add WebP conversion to ImageService"

File: Services/ImageService.cs
Method: public string ConvertToWebP(string imagePath, int quality)

Implementation:
- Use ImageSharp library
- Load image
- Convert to WebP format
- Save with quality setting
- Return new path
```

#### Email Service Queue
```
Task: "Add email queueing to EmailService for retry on failure"

File: Services/EmailService.cs

Implementation:
- Create email queue storage (database or file)
- Queue emails instead of immediate send
- Background task processes queue
- Retry failed emails with exponential backoff
- Log failures
```

#### Cache Service
```
Task: "Create CacheService for distributed caching support"

Steps:
1. Create Services/ICacheService.cs interface
2. Create Services/CacheService.cs implementation
3. Support both memory cache and Redis
4. Provide methods: Get, Set, Remove, Clear
5. Register in CoreComposer
```

#### PDF Generation Service
```
Task: "Create PdfService for generating PDFs from HTML"

Steps:
1. Create Services/IPdfService.cs
2. Create Services/PdfService.cs
3. Use library like PdfSharpCore or Puppeteer
4. Method: GeneratePdf(string html, PdfOptions options)
5. Return byte array or save to media library
```

**Indicators this task belongs here:**
- ✅ Generic functionality (search, caching, email, file processing)
- ✅ No business rules specific to boats/products
- ✅ Could be used in any Umbraco project
- ✅ Infrastructure-level concern

**Indicators it belongs in Seed.Backoffice.Extensions:**
- ❌ Service is for boats, products, dealers, or quotes
- ❌ Contains project-specific business logic
- ❌ Calls project-specific converters or models
- ❌ Specific to this website's domain

---

### 3. Adding Extension Methods

**When:** You need helper methods that extend Umbraco or .NET types with reusable functionality.

**Examples:**

#### IPublishedContent Extensions
```
Task: "Add GetAncestorOrSelfOfTypes extension method"

File: Extensions/IPublishedContentExtensions.cs

public static IPublishedContent? GetAncestorOrSelfOfTypes(
    this IPublishedContent content,
    params string[] contentTypeAliases)
{
    // Walk up tree
    // Check if current or ancestor matches any alias
    // Return first match
}

Usage:
var container = content.GetAncestorOrSelfOfTypes("containerPage", "folder");
```

#### String Extensions
```
Task: "Add ToSlug extension for URL-safe strings"

File: Extensions/StringExtensions.cs

public static string ToSlug(this string input)
{
    // Convert to lowercase
    // Replace spaces with hyphens
    // Remove special characters
    // Handle accented characters
    // Return URL-safe string
}

Usage:
var slug = "Hello World!".ToSlug(); // "hello-world"
```

#### IEnumerable Extensions
```
Task: "Add Chunk extension for pagination"

File: Extensions/IEnumerableExtensions.cs

public static IEnumerable<IEnumerable<T>> Chunk<T>(
    this IEnumerable<T> source,
    int size)
{
    // Split collection into chunks of size
}

Usage:
var pages = items.Chunk(10); // Groups of 10
```

#### DateTime Extensions
```
Task: "Add ToRelativeTime extension"

File: Extensions/DateTimeExtensions.cs

public static string ToRelativeTime(this DateTime dateTime)
{
    // Calculate difference from now
    // Return "2 hours ago", "3 days ago", etc.
}
```

**Indicators this task belongs here:**
- ✅ Extends standard .NET or Umbraco types
- ✅ Generic functionality useful in any project
- ✅ No project-specific logic
- ✅ Pure utility/helper methods

**Indicators it belongs elsewhere:**
- ❌ Extends project-specific types (BoatModel, ProductModel, etc.)
- ❌ Contains business logic
- ❌ Specific to this project's domain

---

### 4. Creating Content Importers/Migrators

**When:** You need to migrate content from old formats or external systems (in a generic way).

**Examples:**

#### New Property Editor Importer
```
Task: "Create importer for migrating old Repeater to Block List"

Steps:
1. Create Import/RepeaterImporter.cs
2. Inherit from ImporterBase
3. Override CanImport to check for "Umbraco.Repeater"
4. Implement Import method:
   - Parse old repeater JSON
   - Convert to Block List format
   - Map item properties
   - Return new Block List value
5. Importer auto-registers
```

#### External System Importer
```
Task: "Create generic CSV content importer"

Steps:
1. Create Import/CsvImporter.cs
2. Accept CSV file and mapping configuration
3. Parse CSV rows
4. Map columns to Umbraco properties
5. Create or update content nodes
6. Handle errors gracefully
7. Return import results
```

#### Media Format Converter
```
Task: "Create importer to convert old Image Cropper format to new format"

Steps:
1. Create Import/ImageCropperImporter.cs
2. Parse old crop JSON structure
3. Convert to new ImageCropperValue format
4. Preserve crop names and coordinates
5. Return converted value
```

**Indicators this task belongs here:**
- ✅ Migrates standard Umbraco property editors
- ✅ Generic import logic (CSV, JSON, XML, etc.)
- ✅ Could be reused in different projects
- ✅ No business-specific transformations

**Indicators it belongs in Seed.Backoffice.Extensions:**
- ❌ Imports from project-specific system (Epicor)
- ❌ Contains business logic for products/boats
- ❌ Project-specific data transformations

---

### 5. Creating Stringifiers for Search Indexing

**When:** You need to extract searchable text from complex property editors.

**Examples:**

#### Block List Stringifier
```
Task: "Create stringifier for Block List to extract text from all blocks"

Steps:
1. Create Stringifier/BlockListStringifier.cs
2. Inherit from BaseStringifier
3. Override CanStringify to check for "Umbraco.BlockList"
4. Implement Stringify:
   - Parse Block List JSON
   - Recursively extract text from each block
   - Combine into searchable string
   - Return concatenated text
5. Stringifier auto-registers
```

#### Tags Stringifier
```
Task: "Create stringifier for Tags property editor"

Steps:
1. Create Stringifier/TagsStringifier.cs
2. Extract tag names from JSON
3. Join with spaces
4. Return as searchable string
```

#### Multi-picker Stringifier
```
Task: "Create stringifier for MultiNodeTreePicker to include picked node names"

Steps:
1. Create Stringifier/MultiPickerStringifier.cs
2. Parse picker UDIs
3. Get IPublishedContent for each
4. Extract names
5. Join and return
```

**Indicators this task belongs here:**
- ✅ Stringifies standard Umbraco property editors
- ✅ Generic text extraction
- ✅ Reusable across projects
- ✅ No business logic

**Indicators it belongs elsewhere:**
- ❌ Stringifies project-specific data types
- ❌ Requires business logic to determine text

---

### 6. Adding Shared Models/DTOs

**When:** You need data models that are reusable and not project-specific.

**Examples:**

#### API Response Models
```
Task: "Create generic PaginatedResponse<T> model"

File: Models/PaginatedResponse.cs

public class PaginatedResponse<T>
{
    public IEnumerable<T> Items { get; set; }
    public int TotalItems { get; set; }
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
    public int TotalPages => (int)Math.Ceiling(TotalItems / (double)PageSize);
}

Usage: For any paginated API endpoint
```

#### Error Response Model
```
Task: "Create ErrorResponse model for consistent error handling"

File: Models/ErrorResponse.cs

public class ErrorResponse
{
    public string Message { get; set; }
    public string ErrorCode { get; set; }
    public Dictionary<string, string[]> ValidationErrors { get; set; }
    public string StackTrace { get; set; } // Only in dev
}
```

#### Search Request Model
```
Task: "Create generic SearchRequest model"

File: Models/SearchRequest.cs

public class SearchRequest
{
    public string Query { get; set; }
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public string[] ContentTypes { get; set; }
    public Dictionary<string, string> Filters { get; set; }
    public string SortBy { get; set; }
    public bool SortDescending { get; set; }
}
```

#### File Upload Model
```
Task: "Create FileUploadRequest model"

File: Models/FileUploadRequest.cs

public class FileUploadRequest
{
    public IFormFile File { get; set; }
    public string FileName { get; set; }
    public string FolderPath { get; set; }
    public bool Overwrite { get; set; }
}
```

**Indicators this task belongs here:**
- ✅ Generic data structures
- ✅ Reusable across projects
- ✅ Not tied to specific business domain
- ✅ Infrastructure/framework models

**Indicators it belongs elsewhere:**
- ❌ Boat, product, dealer, or quote models
- ❌ Business domain entities
- ❌ Project-specific DTOs

---

### 7. Creating Virtual Page Handlers

**When:** You need dynamically generated pages for common scenarios.

**Examples:**

#### Sitemap Virtual Page
```
Task: "Create virtual page handler for XML sitemap"

Steps:
1. Create VirtualPages/SitemapVirtualPageHandler.cs
2. Implement IVirtualPageHandler
3. ShouldHandle: return url.Equals("/sitemap.xml")
4. HandleRequest:
   - Query all published content
   - Generate XML sitemap
   - Return with XML content type
```

#### Search Results Virtual Page
```
Task: "Create virtual page handler for search results"

Steps:
1. Create VirtualPages/SearchVirtualPageHandler.cs
2. ShouldHandle: return url.StartsWith("/search")
3. HandleRequest:
   - Parse query from URL
   - Execute search via ExamineService
   - Format results
   - Return VirtualPageModel
```

#### RSS Feed Virtual Page
```
Task: "Create virtual page handler for RSS feed"

Steps:
1. Create VirtualPages/RssFeedVirtualPageHandler.cs
2. ShouldHandle: return url.EndsWith(".rss")
3. HandleRequest:
   - Query recent content
   - Generate RSS XML
   - Return with RSS content type
```

**Indicators this task belongs here:**
- ✅ Generic functionality (sitemap, RSS, search)
- ✅ Could be used in any website
- ✅ No business logic
- ✅ Standard web patterns

**Indicators it belongs in Seed.Backoffice.Extensions:**
- ❌ Boat-specific pages
- ❌ Product configurator pages
- ❌ Quote builder pages

---

### 8. Adding DataApiController Endpoints

**When:** You need generic API endpoints for content delivery.

**Examples:**

#### Breadcrumb Endpoint
```
Task: "Add endpoint to get breadcrumb trail for any page"

Method: GET /api/data/breadcrumbs?nodeId={id}

Implementation in DataApiController.cs:
- Get IPublishedContent by ID
- Walk up ancestors
- Build breadcrumb array
- Return BreadcrumbModel[]
```

#### Menu Endpoint
```
Task: "Add endpoint to get navigation menu from root"

Method: GET /api/data/menu?rootId={id}&maxDepth={depth}

Implementation:
- Get root node
- Get children recursively up to maxDepth
- Transform to menu structure
- Return MenuModel
```

#### Related Content Endpoint
```
Task: "Add endpoint to get related content by tags"

Method: GET /api/data/related?nodeId={id}&count={count}

Implementation:
- Get current node's tags
- Search for content with same tags
- Sort by relevance
- Limit to count
- Return RelatedContent[]
```

**Indicators this task belongs here:**
- ✅ Generic content endpoints
- ✅ No business logic
- ✅ Useful for any website
- ✅ Standard CMS patterns

**Indicators it belongs in Seed.Backoffice.Extensions:**
- ❌ Product-specific endpoints
- ❌ Boat builder endpoints
- ❌ Quote generation endpoints

---

### 9. Creating Notification Handlers

**When:** You need to respond to Umbraco events in a generic way.

**Examples:**

#### Auto-Generate Slug Handler
```
Task: "Create handler to auto-generate URL slug from node name"

Steps:
1. Create ContentSavingHandler.cs
2. Implement INotificationHandler<ContentSavingNotification>
3. On content save:
   - Check if slug property is empty
   - Generate from node name
   - Set slug property
```

#### Image Optimization Handler
```
Task: "Create handler to optimize images on upload"

Steps:
1. Update existing MediaSavingHandler.cs (or create new)
2. Implement INotificationHandler<MediaSavingNotification>
3. On image upload:
   - Check file size
   - If > threshold, resize/compress
   - Update file
   - Update dimensions
```

#### Cache Invalidation Handler
```
Task: "Create handler to invalidate cache when content published"

Steps:
1. Create CacheInvalidationHandler.cs
2. Implement INotificationHandler<ContentPublishedNotification>
3. On publish:
   - Identify affected cache keys
   - Clear from cache
   - Log invalidation
```

#### Metadata Extraction Handler
```
Task: "Create handler to extract file metadata on upload"

Steps:
1. Create MetadataExtractionHandler.cs
2. Implement INotificationHandler<MediaSavingNotification>
3. On file upload:
   - Extract metadata (EXIF, file size, dimensions, etc.)
   - Store in custom properties
```

**Indicators this task belongs here:**
- ✅ Generic event handling
- ✅ Infrastructure concerns (caching, optimization, metadata)
- ✅ Reusable across projects
- ✅ No business logic

**Indicators it belongs in Seed.Backoffice.Extensions:**
- ❌ Boat-specific event handling
- ❌ Product import triggers
- ❌ Business rule enforcement

---

### 10. Adding Helper Utilities

**When:** You need reusable utility methods.

**Examples:**

#### SeedHelper Enhancements
```
Task: "Add method to generate short GUID for URLs"

File: SeedHelper.cs
Method: public string GenerateShortGuid()

Implementation:
- Generate Guid
- Convert to Base64
- Remove special characters
- Take first 8 characters
- Return short ID
```

#### Hash Helper
```
Task: "Add method to generate file hash for integrity checking"

File: SeedHelper.cs
Method: public string GenerateFileHash(Stream stream, HashAlgorithm algorithm)

Implementation:
- Read stream
- Compute hash
- Return base64 string
```

#### URL Helper
```
Task: "Add method to build absolute URLs with domain"

File: SeedHelper.cs
Method: public string ToAbsoluteUrl(string relativePath, string domain)

Implementation:
- Combine domain and path
- Handle leading/trailing slashes
- Ensure HTTPS
- Return absolute URL
```

**Indicators this task belongs here:**
- ✅ Generic utilities
- ✅ No business logic
- ✅ Reusable helpers
- ✅ Infrastructure support

---

### 11. Creating Middleware

**When:** You need request/response pipeline processing.

**Examples:**

#### Response Compression Middleware
```
Task: "Create middleware to compress API responses"

Steps:
1. Create Middleware/CompressionMiddleware.cs
2. Check Accept-Encoding header
3. Compress response if supported
4. Set Content-Encoding header
5. Register in pipeline
```

#### API Versioning Middleware
```
Task: "Create middleware to handle API versioning"

Steps:
1. Create Middleware/ApiVersioningMiddleware.cs
2. Check API version header or query string
3. Route to appropriate API version
4. Return version mismatch error if invalid
```

#### Request Logging Middleware
```
Task: "Create middleware to log all API requests"

Steps:
1. Create Middleware/RequestLoggingMiddleware.cs
2. Log request URL, method, headers
3. Log response status, duration
4. Log to structured logging system
```

**Indicators this task belongs here:**
- ✅ HTTP pipeline concerns
- ✅ Infrastructure-level
- ✅ Reusable across projects
- ✅ No business logic

---

### 12. Adding Examine Index Configuration

**When:** You need custom index configurations for better search.

**Examples:**

#### Custom Field Analyzer
```
Task: "Add custom analyzer for better text search"

File: ConfigureIndexOptions.cs

Implementation:
- Define custom analyzer
- Configure tokenization
- Set stop words
- Configure stemming
- Apply to specific fields
```

#### Multi-language Index Configuration
```
Task: "Configure multi-language field indexing"

File: ConfigureIndexOptions.cs

Implementation:
- Index culture-specific fields
- Configure language analyzers
- Handle culture-variant content
- Set up boost factors
```

**Indicators this task belongs here:**
- ✅ Generic search configuration
- ✅ Infrastructure-level indexing
- ✅ Reusable patterns

**Indicators it belongs in Seed.Backoffice.Extensions:**
- ❌ Product-specific indexes
- ❌ Business logic in indexing

---

### 13. GraphQL Support

**When:** You need GraphQL functionality (if implementing GraphQL API).

**Examples:**

#### GraphQL Schema Builder
```
Task: "Add helper to build GraphQL schema from Umbraco content types"

Steps:
1. Update GraphQL/ directory
2. Create schema builder
3. Map content types to GraphQL types
4. Map properties to fields
5. Handle relationships
```

#### GraphQL Resolver
```
Task: "Add resolver for nested content queries"

Steps:
1. Create resolver for content relationships
2. Handle circular references
3. Apply filtering
4. Return typed data
```

**Indicators this task belongs here:**
- ✅ Generic GraphQL infrastructure
- ✅ Reusable across projects
- ✅ No business logic

---

### 14. Caching Infrastructure

**When:** You need caching support beyond basic memory cache.

**Examples:**

#### Distributed Cache Provider
```
Task: "Add Redis cache provider for multi-server scenarios"

File: Caching/Core/RedisCacheProvider.cs

Implementation:
- Implement ICacheProvider interface
- Connect to Redis
- Implement Get, Set, Remove operations
- Handle serialization
- Support cache expiration
```

#### Cache Key Generator
```
Task: "Add cache key generator with namespace support"

File: Caching/Core/CacheKeyGenerator.cs

Implementation:
- Generate consistent cache keys
- Support namespaces
- Handle culture variations
- Include version in key
```

**Indicators this task belongs here:**
- ✅ Generic caching infrastructure
- ✅ Reusable across projects
- ✅ No business logic

---

## Decision Tree: Where Does This Task Belong?

```
Is it reusable across multiple Umbraco projects?
├─ NO → Not Seed.Core
│   │
│   └─ Is it project-specific (boats, products, dealers)?
│      └─ YES → Seed.Backoffice.Extensions
│
└─ YES
   │
   ├─ Is it a standard Umbraco type converter?
   │  └─ YES → Seed.Core/ApiSafeConverters/
   │
   ├─ Is it infrastructure (search, cache, email, etc.)?
   │  └─ YES → Seed.Core/Services/
   │
   ├─ Is it an extension method for common types?
   │  └─ YES → Seed.Core/Extensions/
   │
   ├─ Is it content migration functionality?
   │  └─ YES → Seed.Core/Import/
   │
   ├─ Is it search indexing support?
   │  └─ YES → Seed.Core/Stringifier/
   │
   ├─ Is it a generic API endpoint?
   │  └─ YES → Seed.Core/DataApiController.cs
   │
   ├─ Is it a generic data model?
   │  └─ YES → Seed.Core/Models/
   │
   └─ Is it generic middleware/events?
      └─ YES → Seed.Core/ (appropriate location)
```

---

## Anti-Patterns: What NOT to Put Here

### ❌ Project-Specific Business Logic
```
Bad: Creating "BoatService" in Seed.Core
Why: Boats are project-specific, not reusable

Good: Creating "SearchService" that can search any content
```

### ❌ Project-Specific Converters
```
Bad: Creating "AccordionApiSafeConverter" in Seed.Core
Why: Accordion is a project-specific component

Good: Creating "BlockListApiSafeConverter" for standard Block List editor
```

### ❌ Project-Specific Models
```
Bad: Creating "ProductQuoteData" model in Seed.Core
Why: Products and quotes are project-specific

Good: Creating "PaginatedResponse<T>" generic model
```

### ❌ Hard-Coded Business Rules
```
Bad: Adding validation logic specific to boat configurations
Why: Business rules don't belong in infrastructure

Good: Adding generic validation framework
```

---

## Common Task Patterns

### Pattern 1: New Umbraco Property Editor Released

**Scenario:** Umbraco releases new "ContentBlocks" property editor

**Tasks in Seed.Core:**
1. Create ContentBlocksApiSafeConverter
2. Create ContentBlocksStringifier
3. Create ContentBlocksImporter (if migrating from old format)
4. Update documentation

### Pattern 2: Need Better Search

**Scenario:** Search needs to be faster and more accurate

**Tasks in Seed.Core:**
1. Update ExamineService with new query methods
2. Add field boosting configuration
3. Create custom analyzers in ConfigureIndexOptions
4. Add search result highlighting
5. Update SearchRequest model if needed

### Pattern 3: Need File Processing

**Scenario:** Need to process uploaded files

**Tasks in Seed.Core:**
1. Create FileProcessingService
2. Add notification handler for file uploads
3. Add processing methods (resize, convert, optimize, etc.)
4. Create models for file metadata
5. Register in CoreComposer

### Pattern 4: Need API Enhancement

**Scenario:** Frontend needs new generic endpoint

**Tasks in Seed.Core:**
1. Add endpoint method to DataApiController
2. Create request/response models in Models/
3. Use existing services (ExamineService, etc.)
4. Add API key validation
5. Document endpoint

---

## Checklist for New Tasks

Before implementing a task in Seed.Core:

- [ ] Is this functionality reusable across different Umbraco projects?
- [ ] Does it NOT contain business logic specific to this project?
- [ ] Does it work with standard Umbraco types (not custom project types)?
- [ ] Could it be useful in a different industry/domain?
- [ ] Is it infrastructure, framework, or utility code?

If you answered YES to most of these, proceed with implementation in Seed.Core.

If NO, consider:
- **Seed.Backoffice.Extensions** - For project-specific functionality
- **Seed.DataTypes** - For custom property editors
- **UmbracoProject** - For configuration or startup logic

---

## Examples: Correct Project Placement

### ✅ Seed.Core

**Task:** "Create converter for Umbraco.Tags property editor"
- **Why:** Standard Umbraco type, reusable, generic

**Task:** "Add distributed caching support"
- **Why:** Infrastructure, reusable, no business logic

**Task:** "Create email service with templates"
- **Why:** Generic utility, useful in any project

**Task:** "Add slug generation from node name"
- **Why:** Common pattern, reusable, generic

### ❌ NOT Seed.Core (use Seed.Backoffice.Extensions)

**Task:** "Create converter for Boat Details component"
- **Why:** Project-specific content type

**Task:** "Add ProductService for Epicor integration"
- **Why:** Project-specific business logic

**Task:** "Create quote calculation logic"
- **Why:** Project-specific business rules

**Task:** "Add boat comparison functionality"
- **Why:** Domain-specific feature

---

## Testing Strategy

### Unit Tests for Seed.Core

**What to test:**
- Converter output structure
- Service method behavior
- Extension method logic
- Helper utilities
- Model validation

**Example:**
```csharp
[Test]
public void MediaApiSafeConverter_Image_ReturnsApiSafeImage()
{
    // Arrange
    var mockMedia = CreateMockImage();
    var converter = new MediaApiSafeConverter(_mockConverters);

    // Act
    var result = converter.ConvertToApiSafeValue(mockMedia, null, null, new List<int>(), new Dictionary<string, object>());

    // Assert
    Assert.IsInstanceOf<ApiSafeImage>(result);
    Assert.AreEqual(mockMedia.Url(), ((ApiSafeImage)result).Url);
}
```

### Integration Tests

**What to test:**
- DataApiController endpoints
- Examine queries with actual index
- Database operations
- File system operations

---

## Documentation Requirements

When adding to Seed.Core:

1. **XML Comments** on all public methods and classes
2. **README updates** if adding new major feature
3. **Example usage** in comments
4. **Breaking changes** documented if changing existing APIs
5. **Migration guide** if replacing old functionality

---

## Performance Considerations

### Keep It Fast

**Seed.Core is called frequently:**
- Converters run on every API request
- Services may be called thousands of times
- Extension methods used throughout code

**Optimization tips:**
- Cache expensive operations
- Avoid N+1 queries
- Use lazy loading appropriately
- Profile performance regularly

### Memory Usage

**Be mindful of:**
- Large object allocations in converters
- Collection sizes in models
- Cache memory footprint
- String allocations (use StringBuilder for concatenation)

---

## Versioning and Breaking Changes

### Semantic Versioning

**Seed.Core should follow semantic versioning:**
- **Major:** Breaking changes to public APIs
- **Minor:** New features, backward compatible
- **Patch:** Bug fixes

### Avoid Breaking Changes

**Before making breaking changes:**
1. Check if old API can be deprecated instead
2. Provide migration path
3. Document changes thoroughly
4. Communicate to team
5. Update all consuming code

---

## Getting Started Template

When starting a new task in Seed.Core:

1. **Identify the category** from this document
2. **Find similar existing code** to use as template
3. **Follow established patterns** (interfaces, base classes, etc.)
4. **Write tests** before or during implementation
5. **Add XML comments** for documentation
6. **Update CoreComposer** if registering new service
7. **Check that it's truly generic** (would work in different project)

---

## Summary

**Seed.Core is for:**
- ✅ Generic ApiSafeConverters for standard Umbraco types
- ✅ Infrastructure services (search, cache, email, image processing)
- ✅ Extension methods for common types
- ✅ Content migration/import tools
- ✅ Search indexing support (stringifiers)
- ✅ Generic API endpoints
- ✅ Shared data models and DTOs
- ✅ Notification handlers for infrastructure
- ✅ Helper utilities
- ✅ Middleware
- ✅ Virtual page handlers for common patterns

**Seed.Core is NOT for:**
- ❌ Project-specific business logic (boats, products, dealers)
- ❌ Custom property editors (use Seed.DataTypes)
- ❌ Project-specific converters (use Seed.Backoffice.Extensions)
- ❌ Business domain models
- ❌ Hard-coded business rules

**Key Principle:** If you can imagine using this code in a completely different Umbraco project (e.g., an e-commerce site, a blog, a university website), it belongs in Seed.Core. If it's specific to boats or this business, it belongs elsewhere.
