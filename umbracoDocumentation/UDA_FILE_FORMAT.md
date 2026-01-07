# UDA File Format - LLM Quick Reference

## File Classification

```
TYPE: Umbraco Deploy Artifact (JSON)
LOCATION: src/UmbracoProject/umbraco/Deploy/Revision/
PURPOSE: Version-controlled schema definitions
DEPLOYMENT: Umbraco Deploy sync across environments
ROLE: Source of truth for CMS structure
```

## Artifact Type Matrix

```
ARTIFACT TYPE               FILENAME PATTERN                    UDI PATTERN                      USE CASE
=============================================================================================================================================================
data-type                   data-type__{uuid}.uda               umb://data-type/{uuid}           Property editor definitions + config
document-type               document-type__{uuid}.uda           umb://document-type/{uuid}       Content type schemas
document-type-container     document-type-container__{uuid}.uda umb://document-type-container/{} Folders for organization
member-type                 member-type__{uuid}.uda             umb://member-type/{uuid}         Member schemas
relation-type               relation-type__{uuid}.uda           umb://relation-type/{uuid}       Relationship definitions
```

## UUID Format Rules (CRITICAL)

```
CONTEXT                     UUID FORMAT                         EXAMPLE
=============================================================================================
Filename                    WITH dashes                         data-type__215cb418-2153-4429-9aef-8c0f0041191b.uda
UDI field                   WITHOUT dashes                      umb://data-type/215cb418215344299aef8c0f0041191b
Property Key field          WITH dashes                         "Key": "215cb418-2153-4429-9aef-8c0f0041191b"
PropertyGroup Key           WITH dashes                         "Key": "4ce2b940-ee62-4e0a-a18f-4b03e31e7407"

GENERATION:
├─ COMMAND: uuidgen
├─ FORMAT: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
├─ UNIQUENESS: Must be globally unique
└─ NEVER: Reuse existing UUIDs (causes deployment conflicts)
```

## Common JSON Structure (All Artifacts)

```json
{
  "Name": "Human-readable display name",
  "Alias": "machineReadableAlias",
  "Udi": "umb://artifact-type/uuidwithoutdashes",
  "Dependencies": [],
  "__type": "Umbraco.Deploy.Infrastructure,Umbraco.Deploy.Infrastructure.Artifacts.{ArtifactType}",
  "__version": "13.4.3"
}

FIELD REFERENCE:
├─ Name: Display name in backoffice (Title Case with spaces)
├─ Alias: camelCase identifier (empty string "" for data types)
├─ Udi: Universal identifier (UUID without dashes)
├─ Dependencies: Array of artifacts this depends on
├─ __type: Fully qualified .NET type (do not modify)
└─ __version: Umbraco Deploy version (13.4.3 current)
```

## Data Type Structure

```json
{
  "Name": "Component - Property Name - Editor Type",
  "Alias": "",
  "EditorAlias": "Umbraco.{PropertyEditor}",
  "DatabaseType": "Nvarchar|Integer|Decimal|Date",
  "Configuration": {
    // Editor-specific JSON config
  },
  "Udi": "umb://data-type/{uuid-without-dashes}",
  "Dependencies": [],
  "__type": "Umbraco.Deploy.Infrastructure,Umbraco.Deploy.Infrastructure.Artifacts.DataTypeArtifact",
  "__version": "13.4.3"
}

KEY FIELDS:
├─ Name: Follow naming convention (see Best Practices)
├─ Alias: ALWAYS empty string "" for data types
├─ EditorAlias: Property editor (Umbraco.MediaPicker3, Umbraco.TextBox, etc.)
├─ DatabaseType: Storage type (Nvarchar most common)
├─ Configuration: Editor-specific settings (varies by EditorAlias)
└─ Dependencies: Usually empty [] unless referencing other artifacts
```

## EditorAlias Quick Lookup

```
EDITORALIAS                       DATABASE TYPE    CONFIGURATION KEYS
================================================================================================
Umbraco.TextBox                   Nvarchar         maxChars
Umbraco.TextArea                  Nvarchar         maxChars, rows
Umbraco.Integer                   Integer          min, max, step
Umbraco.Decimal                   Decimal          min, max, step
Umbraco.TrueFalse                 Integer          default, showLabels, labelOn, labelOff
Umbraco.DateTime                  Date             format, offsetTime
Umbraco.DropDown.Flexible         Nvarchar         multiple, items[]
Umbraco.CheckBoxList              Nvarchar         items[]
Umbraco.RadioButtonList           Nvarchar         items[]
Umbraco.Slider                    Decimal          enableRange, initVal1, initVal2, minVal, maxVal, step
Umbraco.ColorPicker               Nvarchar         items[], useLabel
Umbraco.Label                     Nvarchar         valueType

Umbraco.MediaPicker3              Nvarchar         crops[], filter, multiple, validationLimit
Umbraco.ContentPicker             Nvarchar         startNodeId, showOpenButton, ignoreUserStartNodes
Umbraco.MultiNodeTreePicker       Nvarchar         startNode, filter, minNumber, maxNumber
Umbraco.BlockGrid                 Nvarchar         blocks[], validationLimit, useLiveEditing, gridColumns
Umbraco.BlockList                 Nvarchar         blocks[], validationLimit, useLiveEditing, useSingleBlockMode
Umbraco.TinyMCE                   Nvarchar         editor.toolbar[], editor.stylesheets[], editor.maxImageSize
Umbraco.UploadField               Nvarchar         fileExtensions[]
Umbraco.MultiUrlPicker            Nvarchar         minNumber, maxNumber, hideAnchor
Umbraco.Tags                      Nvarchar         group, storageType
UmbracoForms.FormPicker           Nvarchar         allowedForms
```

## Document Type Structure

```json
{
  "Name": "Document Type Name",
  "Alias": "documentTypeAlias",
  "AllowedTemplates": [],
  "HistoryCleanup": {},
  "Icon": "icon-name color-name",
  "Thumbnail": "folder.png",
  "Permissions": {
    "IsElementType": true|false,
    "AllowedChildContentTypes": []
  },
  "Parent": "umb://document-type-container/{uuid}",
  "CompositionContentTypes": [],
  "PropertyGroups": [
    {
      "Key": "{uuid-with-dashes}",
      "Name": "Tab Name",
      "Alias": "tabAlias",
      "SortOrder": 0,
      "PropertyTypes": [
        {
          "Key": "{uuid-with-dashes}",
          "Alias": "propertyAlias",
          "DataType": "umb://data-type/{uuid}",
          "Mandatory": true|false,
          "Name": "Display Name",
          "Description": "Help text",
          "SortOrder": 0
        }
      ]
    }
  ],
  "PropertyTypes": [],
  "Udi": "umb://document-type/{uuid-without-dashes}",
  "Dependencies": [
    {
      "Udi": "umb://data-type/{uuid}",
      "Ordering": true
    }
  ],
  "__type": "Umbraco.Deploy.Infrastructure,Umbraco.Deploy.Infrastructure.Artifacts.ContentType.DocumentTypeArtifact",
  "__version": "13.4.3"
}

KEY FIELDS:
├─ IsElementType: true = Block Grid/List element, false = Page/content
├─ AllowedChildContentTypes: Child document types allowed
├─ Parent: Folder (document-type-container) UDI
├─ CompositionContentTypes: Inheritance from other document types
├─ PropertyGroups: Tabs containing properties
├─ PropertyTypes: Ungrouped properties (usually empty, use PropertyGroups)
└─ Dependencies: All referenced data types + containers
```

## Property Type Structure

```json
{
  "Key": "{uuid-with-dashes}",
  "Alias": "camelCasePropertyName",
  "DataType": "umb://data-type/{uuid-without-dashes}",
  "Mandatory": true|false,
  "MandatoryMessage": "Custom validation message",
  "Name": "Display Name (Title Case)",
  "Description": "Help text for editors",
  "SortOrder": 0,
  "LabelOnTop": false,
  "ValidationRegExp": ""
}

FIELD REQUIREMENTS:
├─ Key: REQUIRED - Unique UUID with dashes
├─ Alias: REQUIRED - camelCase identifier (used in code)
├─ DataType: REQUIRED - UDI reference to data type
├─ Name: REQUIRED - Display name in backoffice
├─ Mandatory: OPTIONAL - Default false
├─ MandatoryMessage: OPTIONAL - Custom message when empty
├─ Description: OPTIONAL - Help text
├─ SortOrder: OPTIONAL - Default 0
├─ LabelOnTop: OPTIONAL - Default false
└─ ValidationRegExp: AVOID - Project standard forbids regex
```

## Dependency Rules

```
ARTIFACT TYPE               MUST DEPEND ON
================================================================================================
Data Type                   ├─ None (usually)
                            └─ Content nodes (if using startNodeId in ContentPicker)

Document Type               ├─ All data types used in properties
                            ├─ Parent container (document-type-container)
                            ├─ Composition content types (if inheriting)
                            └─ All element types (if Block Grid/List config)

Block Grid/List Data Type   ├─ All document types in blocks[] array
                            └─ All element types in specifiedAllowance[] arrays

Content Picker Data Type    └─ Start node document (if startNodeId configured)

DEPENDENCY FORMAT:
{
  "Udi": "umb://artifact-type/{uuid}",
  "Ordering": true,          // Affects deployment order
  "Mode": "Exist"            // For content references (startNodeId)
}
```

## Naming Conventions (Project Standard)

```
ELEMENT                     CONVENTION                          EXAMPLES
================================================================================================
Data Type Name              {Component} - {Property} - {Editor} ├─ "Headline - Full Background Image - Image - Media Picker"
                                                                ├─ "Filter - Count Mode - Dropdown"
                                                                └─ "Team - Athlete - Image - Media Picker"

Document Type Alias         camelCase                           ├─ richtext
                                                                ├─ bannerStandard
                                                                └─ productListing

Property Alias              camelCase                           ├─ backgroundImage
                                                                ├─ showInNavigation
                                                                └─ metaDescription

Property Name               Title Case with Spaces              ├─ Background Image
                                                                ├─ Show in Navigation
                                                                └─ Meta Description

PropertyGroup Name          Title Case                          ├─ Content
                                                                ├─ SEO
                                                                └─ Settings

Icon                        kebab-case with optional color      ├─ icon-script color-black
                                                                ├─ icon-user
                                                                └─ icon-folder color-orange

RATIONALE: Context-specific names prevent accidental reuse and document usage
```

## Safe vs. Risky Modifications

```
MODIFICATION TYPE           RISK     DATA LOSS    NOTES
================================================================================================
Add new property            LOW      No           Generate new UUID
Remove property             HIGH     Yes          All property data deleted
Change property Name        LOW      No           Display name only
Change property Alias       CRITICAL Yes          Breaks connection to data + frontend code
Change property DataType    HIGH     Maybe        Type incompatibility possible
Change Mandatory false→true HIGH     No data loss But breaks content without values
Change Mandatory true→false LOW      No           Safe relaxation
Add SortOrder              LOW       No           Display order only
Change Icon/Thumbnail       LOW      No           Visual only
Add PropertyGroup           LOW      No           New tab
Remove PropertyGroup        HIGH     Yes          All contained properties deleted
Add to Dependencies         LOW      No           Ensures deployment order
Remove from Dependencies    MEDIUM   No           May break deployment
Change EditorAlias          CRITICAL Yes          NEVER DO THIS - breaks everything
Change DatabaseType         CRITICAL Yes          NEVER DO THIS - type incompatibility
Change UUID (Key/Udi)       CRITICAL Yes          NEVER DO THIS - creates new artifact
```

## Common Patterns

### PATTERN: Create New Data Type

```
STEP 1: Generate UUID
└─ uuidgen → a1b2c3d4-e5f6-4789-0123-456789abcdef

STEP 2: Create file
└─ src/UmbracoProject/umbraco/Deploy/Revision/data-type__a1b2c3d4-e5f6-4789-0123-456789abcdef.uda

STEP 3: Define structure
{
  "Name": "{Component} - {Property} - {Editor}",
  "Alias": "",
  "EditorAlias": "Umbraco.{Editor}",
  "DatabaseType": "Nvarchar",
  "Configuration": {
    // Editor-specific config
  },
  "Udi": "umb://data-type/a1b2c3d4e5f6478901234567 89abcdef",
  "Dependencies": [],
  "__type": "Umbraco.Deploy.Infrastructure,Umbraco.Deploy.Infrastructure.Artifacts.DataTypeArtifact",
  "__version": "13.4.3"
}

STEP 4: Validate
├─ [ ] JSON syntax valid (no trailing commas)
├─ [ ] UUID in filename has dashes
├─ [ ] UUID in Udi has no dashes
├─ [ ] EditorAlias is correct
├─ [ ] Configuration matches editor requirements
└─ [ ] DatabaseType appropriate for editor
```

### PATTERN: Add Property to Document Type

```
STEP 1: Generate UUID for property
└─ uuidgen → f1e2d3c4-b5a6-4789-0321-654987fedcba

STEP 2: Locate PropertyGroup in document type UDA
└─ Find appropriate tab (e.g., "Content", "SEO", "Settings")

STEP 3: Add PropertyType object
{
  "Key": "f1e2d3c4-b5a6-4789-0321-654987fedcba",
  "Alias": "newPropertyName",
  "DataType": "umb://data-type/{existing-data-type-uuid}",
  "Mandatory": false,
  "Name": "New Property Name",
  "Description": "Help text for editors",
  "SortOrder": 2
}

STEP 4: Add dependency (if data type not already in Dependencies)
{
  "Udi": "umb://data-type/{data-type-uuid}",
  "Ordering": true
}

STEP 5: Validate
├─ [ ] New UUID generated (not copied)
├─ [ ] DataType UDI references existing data type file
├─ [ ] Added to Dependencies if not present
├─ [ ] SortOrder reflects desired display position
└─ [ ] JSON syntax valid
```

### PATTERN: Media Picker with Crops

```
CONFIGURATION:
{
  "EditorAlias": "Umbraco.MediaPicker3",
  "DatabaseType": "Nvarchar",
  "Configuration": {
    "filter": "Image",
    "multiple": false,
    "crops": [
      {
        "alias": "mobile",
        "label": "Mobile",
        "width": 375,
        "height": 667
      },
      {
        "alias": "desktop",
        "label": "Desktop",
        "width": 1920,
        "height": 1080
      }
    ],
    "validationLimit": {}
  }
}

BEST PRACTICE: Create context-specific media pickers with exact crop sizes needed
```

### PATTERN: Dropdown with Options

```
CONFIGURATION:
{
  "EditorAlias": "Umbraco.DropDown.Flexible",
  "DatabaseType": "Nvarchar",
  "Configuration": {
    "multiple": false,
    "items": [
      {
        "id": 1,
        "value": "Option 1"
      },
      {
        "id": 2,
        "value": "Option 2"
      },
      {
        "id": 3,
        "value": "Option 3"
      }
    ]
  }
}

BEST PRACTICE: Create context-specific dropdowns, not generic reusable ones
```

### PATTERN: Content Picker with Start Node

```
CONFIGURATION:
{
  "EditorAlias": "Umbraco.ContentPicker",
  "DatabaseType": "Nvarchar",
  "Configuration": {
    "startNodeId": "umb://document/{content-node-uuid}",
    "showOpenButton": true,
    "ignoreUserStartNodes": false
  },
  "Dependencies": [
    {
      "Udi": "umb://document/{content-node-uuid}",
      "Mode": "Exist"
    }
  ]
}

CRITICAL: Add dependency with Mode: "Exist" when using startNodeId
```

### PATTERN: Block Grid Configuration

```
CONFIGURATION:
{
  "EditorAlias": "Umbraco.BlockGrid",
  "DatabaseType": "Nvarchar",
  "Configuration": {
    "blocks": [
      {
        "contentElementTypeKey": "{element-uuid}",
        "allowAtRoot": true,
        "allowInAreas": false,
        "label": "{{heading || '(empty)'}}",
        "areas": []
      }
    ],
    "validationLimit": {
      "min": 0,
      "max": 0
    },
    "useLiveEditing": false,
    "gridColumns": 12
  },
  "Dependencies": [
    {
      "Udi": "umb://document-type/{element-uuid}"
    }
  ]
}

BLOCK TYPES:
├─ Layout blocks: allowAtRoot: true, allowInAreas: false
├─ Content blocks: allowAtRoot: false, allowInAreas: true
└─ Flexible blocks: allowAtRoot: true, allowInAreas: true

CRITICAL: Dependencies must include all element types referenced in blocks[] and areas[]
```

## Best Practices Summary

```
PRINCIPLE                   GUIDELINE
================================================================================================
Naming                      ├─ Data types: {Component} - {Property} - {Editor}
                            ├─ Document types: Descriptive, clear purpose
                            └─ Properties: camelCase aliases, Title Case names

Context-Specific Config     ├─ Create new data types for each use case
                            ├─ Don't reuse generic data types
                            ├─ Each media picker has specific crops
                            └─ Each dropdown has specific options

UUID Management             ├─ Always generate new UUIDs (uuidgen)
                            ├─ Never reuse existing UUIDs
                            ├─ Never modify existing UUIDs
                            └─ Dashes in files/Keys, no dashes in UDIs

Dependencies                ├─ Include all referenced data types
                            ├─ Include parent containers
                            ├─ Include all Block Grid/List elements
                            └─ Include content nodes for startNodeId

Validation                  ├─ Use validationLimit for min/max
                            ├─ Use fileExtensions for uploads
                            ├─ Use filter for media types
                            └─ Avoid ValidationRegExp (project standard)

JSON Syntax                 ├─ No trailing commas
                            ├─ 2-space indentation
                            ├─ Double quotes for strings
                            └─ Empty arrays [] and objects {}

Deployment Safety           ├─ Test in development first
                            ├─ Understand data loss risks
                            ├─ Never change EditorAlias or DatabaseType
                            └─ Commit to version control
```

## Configuration Examples by Editor

### TextBox

```json
{
  "Configuration": {
    "maxChars": 100
  }
}
```

### TextArea

```json
{
  "Configuration": {
    "maxChars": 500,
    "rows": 10
  }
}
```

### TrueFalse (Toggle)

```json
{
  "Configuration": {
    "default": false,
    "showLabels": true,
    "labelOn": "Yes",
    "labelOff": "No"
  }
}
```

### RichText (TinyMCE)

```json
{
  "Configuration": {
    "editor": {
      "toolbar": ["styles", "bold", "italic", "bullist", "numlist", "link"],
      "stylesheets": ["/css/rte.css"],
      "maxImageSize": 500,
      "mode": "inline"
    }
  },
  "Dependencies": [
    {
      "Udi": "umb://stylesheet/rte.css",
      "Mode": "Exist"
    }
  ]
}
```

### MultiNodeTreePicker

```json
{
  "Configuration": {
    "startNode": {
      "type": "content"
    },
    "filter": "boat,product",
    "minNumber": 0,
    "maxNumber": 5,
    "showOpenButton": false,
    "ignoreUserStartNodes": false
  }
}
```

### UploadField

```json
{
  "Configuration": {
    "fileExtensions": [
      {"id": 0, "value": "pdf"},
      {"id": 1, "value": "docx"},
      {"id": 2, "value": "xlsx"}
    ]
  }
}
```

### MultiUrlPicker

```json
{
  "Configuration": {
    "minNumber": 0,
    "maxNumber": 5,
    "hideAnchor": false
  }
}
```

## Anti-Patterns (What NOT to Do)

```
❌ NEVER: Change EditorAlias in existing data type
   ✅ INSTEAD: Create new data type, migrate content

❌ NEVER: Change DatabaseType
   ✅ INSTEAD: Create new data type with correct type

❌ NEVER: Modify existing UUIDs (Key, Udi)
   ✅ INSTEAD: UUIDs are immutable identifiers

❌ NEVER: Reuse UUIDs from other properties
   ✅ INSTEAD: Generate new UUID with uuidgen

❌ NEVER: Copy UUIDs from examples/documentation
   ✅ INSTEAD: Always generate fresh UUIDs

❌ NEVER: Use trailing commas in JSON
   ✅ INSTEAD: Remove all trailing commas

❌ NEVER: Include dashes in UDI values
   ✅ INSTEAD: UDI format is umb://type/uuidwithoutdashes

❌ NEVER: Remove properties without backup
   ✅ INSTEAD: Export data first or deprecate gradually

❌ NEVER: Create generic reusable data types
   ✅ INSTEAD: Create context-specific configurations

❌ NEVER: Skip Dependencies for referenced artifacts
   ✅ INSTEAD: Include all data types, containers, elements

❌ NEVER: Use regex in ValidationRegExp
   ✅ INSTEAD: Project standard forbids regex

❌ NEVER: Change property Alias casually
   ✅ INSTEAD: Breaks frontend code + data connection
```

## Troubleshooting Lookup

```
ISSUE                               SOLUTION
================================================================================================
Dependency not found                ├─ Verify referenced UDI exists in target environment
                                    ├─ Check Dependencies array includes artifact
                                    └─ Ensure all files committed and deployed

Duplicate UUID error                ├─ Generate new UUID for new artifacts
                                    ├─ Never copy UUIDs from other properties
                                    └─ Check for accidental UUID reuse

Invalid UDI format                  ├─ UDIs must NOT have dashes
                                    ├─ Keys and filenames MUST have dashes
                                    └─ Format: umb://artifact-type/uuidwithoutdashes

Ordering/deployment errors          ├─ Check Dependencies array complete
                                    ├─ Verify Ordering: true for dependencies
                                    └─ Ensure artifacts deploy before dependents

Property not appearing              ├─ Verify property added to PropertyGroup
                                    ├─ Check DataType UDI is correct
                                    ├─ Ensure Dependencies includes data type
                                    └─ Restart Umbraco application

JSON parse error                    ├─ Remove trailing commas
                                    ├─ Check all brackets matched
                                    ├─ Verify quotes are double quotes "
                                    └─ Validate JSON syntax

Data loss after modification        ├─ Restore from version control (git)
                                    ├─ Check if change was to Alias or DataType
                                    ├─ Revert and follow safe modification patterns
                                    └─ Contact team if production data affected

Content can't be saved              ├─ Check Mandatory fields have values
                                    ├─ Verify validation rules not blocking
                                    ├─ Check data type configuration
                                    └─ Review error message for specific field
```

## JSON Syntax Rules

```
RULE                        EXAMPLE CORRECT                     EXAMPLE INCORRECT
================================================================================================
Indentation                 2 spaces                            Tabs or 4 spaces
Property names              "Name": "value"                     'Name': "value"
String values               "value"                             'value'
No trailing commas          "Name": "value"                     "Name": "value",
                           }                                    } ← comma before bracket
Empty arrays                []                                  [,]
Empty objects               {}                                  {,}
Boolean values              true, false                         True, False, "true"
Null values                 null                                NULL, "null"
```

## Validation Checklist

```
PRE-DEPLOYMENT VALIDATION:
├─ [ ] All new properties have unique UUIDs (generated with uuidgen)
├─ [ ] UUID format correct (dashes in files/Keys, no dashes in UDIs)
├─ [ ] All referenced data types exist
├─ [ ] Dependencies array complete
├─ [ ] No trailing commas in JSON
├─ [ ] All brackets properly matched
├─ [ ] EditorAlias correct for intended property editor
├─ [ ] DatabaseType appropriate for editor
├─ [ ] Configuration valid for editor type
├─ [ ] SortOrder values sequential (if order matters)
├─ [ ] Property aliases camelCase
├─ [ ] Property names Title Case
├─ [ ] Data type names follow convention
├─ [ ] No regex in ValidationRegExp (project standard)
├─ [ ] Icon/Thumbnail values valid
├─ [ ] Mandatory fields appropriate
├─ [ ] Frontend code updated for new/changed properties
├─ [ ] TypeScript types synchronized (see DATATYPE_IMPLEMENTATION_GUIDE.md)
└─ [ ] Tested in development environment

POST-DEPLOYMENT VALIDATION:
├─ [ ] Document type appears in backoffice
├─ [ ] Properties display in correct order
├─ [ ] Property editors load without errors
├─ [ ] Can create/edit content
├─ [ ] Mandatory validation works
├─ [ ] API response includes property
└─ [ ] Frontend displays correctly
```

## Quick Reference Commands

```
COMMAND                                                             PURPOSE
================================================================================================
uuidgen                                                             Generate new UUID
find . -name "data-type__*.uda"                                    List all data type files
find . -name "document-type__*.uda"                                List all document type files
grep -r "EditorAlias.*MediaPicker3" *.uda                          Find media picker data types
grep -r "\"Alias\": \"myAlias\"" document-type__*.uda             Find document type by alias
cat data-type__*.uda | json_pp                                     Validate JSON syntax
```

## Cross-Reference

```
NEED                                    CONSULT
================================================================================================
End-to-end workflow                     DATATYPE_IMPLEMENTATION_GUIDE.md
Converter requirements                  UDA_APISAFECONVERTERS_RELATIONSHIP.md
TypeScript type mapping                 TYPESCRIPT_TYPES_RELATIONSHIP.md
Project structure                       SRC_DIRECTORY_STRUCTURE.md
Umbraco Deploy docs                     https://docs.umbraco.com/umbraco-deploy
Property editors reference              https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors
```
