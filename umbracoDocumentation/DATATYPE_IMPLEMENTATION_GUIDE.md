# Data Type Implementation - LLM Action Guide

## Completion Criteria (MANDATORY)

```
WORKFLOW COMPLETE = ALL 5 CRITERIA MET:
├─ ✅ UDA file created/modified with valid JSON
├─ ✅ Converter requirement satisfied (existing/custom/automatic)
├─ ✅ Property added to document type (if applicable)
├─ ✅ TypeScript types updated in ALL consuming components
└─ ✅ TypeScript compilation succeeds: npx tsc --noEmit (zero errors)

INCOMPLETE WORKFLOWS:
❌ Only UDA modified without frontend updates
❌ TypeScript compilation has errors
❌ Some components updated (must be ALL)
❌ TypeScript types not synchronized with schema
```

## Converter Decision Matrix (Primary Gate)

```
EDITORALIAS                       CONVERTER STATUS              TYPESCRIPT TYPE              ACTION
===============================================================================================================
Umbraco.TextBox                   ✅ Automatic passthrough       string                       None
Umbraco.TextArea                  ✅ Automatic passthrough       string                       None
Umbraco.Integer                   ✅ Automatic passthrough       number                       None
Umbraco.Decimal                   ✅ Automatic passthrough       number                       None
Umbraco.TrueFalse                 ✅ Automatic passthrough       boolean                      None
Umbraco.DateTime                  ✅ Automatic passthrough       string (ISO 8601)            None
Umbraco.DropDown.Flexible         ✅ Automatic passthrough       string | union type          None
Umbraco.RadioButtonList           ✅ Automatic passthrough       string                       None
Umbraco.CheckBoxList              ✅ Automatic passthrough       string[]                     None
Umbraco.Slider                    ✅ Automatic passthrough       number                       None
Umbraco.ColorPicker               ✅ Automatic passthrough       string                       None
Umbraco.Label                     ✅ Automatic passthrough       string                       None

Umbraco.MediaPicker3              ⚙️ Use existing converter      ImageModel                   Import from @lib/umbraco/types
Umbraco.ContentPicker             ⚙️ Use existing converter      UmbracoNode                  Import from @lib/umbraco/types
Umbraco.MultiNodeTreePicker       ⚙️ Use existing converter      UmbracoNode[]                Import from @lib/umbraco/types
Umbraco.BlockGrid                 ⚙️ Use existing converter      BlockGridItem[]              Import from @lib/umbraco/types
Umbraco.BlockList                 ⚙️ Use existing converter      BlockListItem[]              Import from @lib/umbraco/types
Umbraco.TinyMCE                   ⚙️ Use existing converter      string (HTML)                None
Umbraco.RichText                  ⚙️ Use existing converter      string (HTML)                None
UmbracoForms.FormPicker           ⚙️ Use existing converter      ApiSafeForm                  Custom type

Custom/Other                      ❓ Evaluate:
                                  ├─ Complex objects → Create converter
                                  ├─ References → Create converter
                                  ├─ Business logic → Create converter
                                  └─ Simple JSON → Automatic passthrough

COVERAGE: ~80% use automatic passthrough
```

## Quick Action Lookup

```
TASK                                    WORKFLOW SECTION                          TIME ESTIMATE
=============================================================================================================
Create new data type                    § WORKFLOW 1                              5-15 mins
Edit existing data type                 § WORKFLOW 2                              3-10 mins
Add property to document type           § WORKFLOW 3                              5-20 mins
Determine if converter needed           § Converter Decision Matrix               1 min
Create custom converter                 § WORKFLOW 1 STEP 6                       10-30 mins
Update TypeScript types                 § WORKFLOW 3 STEP 7                       2-5 mins per component
Validate implementation                 § Validation Checklist                    2-5 mins
```

## File Path Reference

```
COMPONENT                           ABSOLUTE PATH
====================================================================================================
UDA Files                           src/UmbracoProject/umbraco/Deploy/Revision/
Core ApiSafeConverters              src/Seed.Core/ApiSafeConverters/
Extension ApiSafeConverters         src/Seed.Backoffice.Extensions/ApiSafeConverters/
DataType Converters                 src/Seed.DataTypes/*/Core/
TypeScript Types (shared)           src/Seed.Web/lib/umbraco/types/
Block Grid Components               src/Seed.Web/common/components/blockGrid/blocks/
Page Components                     src/Seed.Web/pages/
Common Components                   src/Seed.Web/common/components/
```

## WORKFLOW 1: Create New Data Type

```
STEP 1: Determine Specification
├─ DECIDE: EditorAlias (e.g., Umbraco.MediaPicker3)
├─ DECIDE: Configuration (crops, limits, options)
├─ DECIDE: DatabaseType (Nvarchar, Integer, Decimal, Date)
└─ DECIDE: Context/usage location

STEP 2: Generate Naming
├─ FORMAT: {Component/Feature} - {Property Name} - {Editor Type}
├─ EXAMPLE: "Headline - Full Background Image - Image - Media Picker"
├─ EXAMPLE: "Filter - Count Mode - Dropdown"
└─ EXAMPLE: "Team - Athlete - Image - Media Picker"
RATIONALE: Context-specific names prevent accidental reuse

STEP 3: Generate UUID
├─ ACTION: uuidgen
├─ FORMAT: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX (with dashes)
├─ USE WITH DASHES: Filename, property Keys
└─ USE WITHOUT DASHES: UDI values (remove all dashes)

STEP 4: Create UDA File
├─ LOCATION: src/UmbracoProject/umbraco/Deploy/Revision/
├─ FILENAME: data-type__{uuid-with-dashes}.uda
└─ STRUCTURE:
    {
      "Name": "{Name from STEP 2}",
      "Alias": "",
      "EditorAlias": "{Property editor alias}",
      "DatabaseType": "{Nvarchar|Integer|Decimal|Date}",
      "Configuration": {
        // Editor-specific configuration
      },
      "Udi": "umb://data-type/{uuid-without-dashes}",
      "Dependencies": [],
      "__type": "Umbraco.Deploy.Infrastructure,Umbraco.Deploy.Infrastructure.Artifacts.DataTypeArtifact",
      "__version": "13.4.3"
    }

STEP 5: Determine Converter Requirement
├─ USE: Converter Decision Matrix (above)
├─ OUTPUT: NO_CONVERTER_NEEDED → Skip to STEP 7
├─ OUTPUT: USE_EXISTING_CONVERTER → Skip to STEP 7
└─ OUTPUT: CREATE_CUSTOM_CONVERTER → Proceed to STEP 6

STEP 6: Create Custom Converter (CONDITIONAL - only if STEP 5 = CREATE_CUSTOM_CONVERTER)
├─ LOCATION OPTIONS:
│  ├─ src/Seed.Core/ApiSafeConverters/ (generic converters)
│  └─ src/Seed.Backoffice.Extensions/ApiSafeConverters/ (project-specific)
├─ FILENAME: {DescriptiveName}ApiSafeConverter.cs
└─ STRUCTURE:
    public class MyApiSafeConverter : BaseApiSafeConverter
    {
        public override string[] EditorAlias => new[] { "{EditorAlias from STEP 4}" };

        public override object ConvertToApiSafeValue(
            object value,
            string culture,
            string? segment,
            List<int> ids,
            Dictionary<string, object> additionalData)
        {
            if (value == null) return value;
            // Transformation logic
            return apiSafeValue;
        }
    }
CRITICAL: EditorAlias must exactly match UDA EditorAlias

STEP 7: Document TypeScript Type Mapping
├─ IF NO_CONVERTER_NEEDED: Use simple type (string, number, boolean)
├─ IF USE_EXISTING_CONVERTER: Use existing type (ImageModel, UmbracoNode, etc.)
└─ IF CREATE_CUSTOM_CONVERTER: Define custom TypeScript type matching converter output

STEP 8: Validate Data Type Creation
├─ [ ] UDA file has valid JSON syntax
├─ [ ] UUID in filename has dashes
├─ [ ] UUID in Udi has no dashes
├─ [ ] EditorAlias is correct
├─ [ ] Configuration is valid
├─ [ ] DatabaseType is appropriate
├─ [ ] Name follows context-specific convention
├─ [ ] Converter decision logic executed
└─ [ ] If custom converter created, EditorAlias matches exactly

STATUS: Data type created, ready to use in document type properties
```

## WORKFLOW 2: Edit Existing Data Type

```
STEP 1: Locate UDA File
├─ METHOD A: grep -l "\"Name\": \"Data Type Name\"" src/UmbracoProject/umbraco/Deploy/Revision/data-type__*.uda
├─ METHOD B: grep -l "\"EditorAlias\": \"Umbraco.MediaPicker3\"" src/UmbracoProject/umbraco/Deploy/Revision/data-type__*.uda
└─ METHOD C: Extract UUID from backoffice URL → data-type__{uuid-with-dashes}.uda

STEP 2: Assess Impact
├─ FIND USAGE: grep -r "{data-type-udi}" src/UmbracoProject/umbraco/Deploy/Revision/document-type__*.uda
├─ QUESTIONS:
│  ├─ How many document types reference this?
│  ├─ Is existing content using this?
│  ├─ Will change affect existing data?
│  └─ Are frontend components depending on structure?

STEP 3: Classify Change Risk Level
├─ LOW RISK (Safe):
│  ├─ Modifying Name field
│  ├─ Adding new crop sizes (preserves existing)
│  ├─ Increasing maxChars limit
│  ├─ Adding new dropdown items
│  └─ Adding new configuration options (additive)
│
└─ HIGH RISK (Potentially Breaking):
   ├─ Changing EditorAlias (BREAKS EVERYTHING - avoid)
   ├─ Reducing maxChars limit (truncates content)
   ├─ Removing dropdown items (invalidates selections)
   ├─ Removing crops (loses crop data)
   ├─ Changing DatabaseType (type incompatibility)
   └─ Modifying configuration affecting data structure

STEP 4: Execute Modification
├─ RULE: Preserve all existing UUID values
├─ RULE: Maintain JSON syntax validity
├─ RULE: If adding crops/options, append to arrays
└─ RULE: If removing items, verify no content depends on them

STEP 5: Evaluate Converter Impact
├─ USUALLY NO:
│  ├─ Adding crops (converter includes all automatically)
│  ├─ Changing validation limits
│  ├─ Adding dropdown options
│  └─ Changing display names
│
├─ SOMETIMES YES:
│  ├─ Custom converter with hardcoded config references
│  ├─ Structural changes to data format
│  └─ Changes affecting transformation logic
│
└─ IF YES: Update converter code to handle new configuration

STEP 6: Evaluate TypeScript Impact
├─ USUALLY NO:
│  ├─ Adding crops (ImageModel supports arbitrary crops)
│  ├─ Changing validation limits
│  └─ Adding dropdown options (if using string type)
│
├─ YES IF:
│  ├─ Using union types for dropdowns (must add new options)
│  ├─ Custom types referencing specific config values
│  ├─ Structural changes affecting type shape
│  └─ Changing EditorAlias (changes type mapping)
│
├─ IF NO: Skip to STEP 8
└─ IF YES: Proceed to STEP 7

STEP 7: Update TypeScript Types (CONDITIONAL - only if STEP 6 = YES)
├─ 7.1: Locate components using this data type
│  └─ grep -r "{data-type-udi}" src/UmbracoProject/umbraco/Deploy/Revision/document-type__*.uda
├─ 7.2: Evaluate required type changes
│  ├─ Dropdown union type → Add new option to union
│  ├─ Custom converter output → Match new structure
│  └─ EditorAlias changed → Determine new type mapping
├─ 7.3: Apply type changes to ALL affected components
├─ 7.4: Validate TypeScript compilation
│  └─ npx tsc --noEmit --project src/Seed.Web/tsconfig.json

STEP 8: Final Validation
├─ [ ] UDA file modified with valid JSON
├─ [ ] Changes backward compatible OR migration plan exists
├─ [ ] If TypeScript impact, all type definitions updated
├─ [ ] TypeScript compilation succeeds (no errors)
└─ [ ] Existing content verified compatible

STATUS: Only deploy after all criteria met
```

## WORKFLOW 3: Add Property to Document Type

```
STEP 1: Locate Document Type UDA File
├─ METHOD A: grep -l "\"Alias\": \"{documentTypeAlias}\"" src/UmbracoProject/umbraco/Deploy/Revision/document-type__*.uda
└─ METHOD B: grep -l "\"Name\": \"{Document Type Name}\"" src/UmbracoProject/umbraco/Deploy/Revision/document-type__*.uda

STEP 2: Identify or Create Data Type
├─ OPTION A: Use existing data type
│  ├─ Search for data type in UDA files or backoffice
│  ├─ Extract UDI: umb://data-type/{uuid-without-dashes}
│  └─ Proceed to STEP 3
│
└─ OPTION B: Create new data type
   ├─ Execute WORKFLOW 1 (Create New Data Type)
   ├─ Obtain UDI from newly created data type
   └─ Proceed to STEP 3

BEST PRACTICE: Create context-specific data types, not generic reusables

STEP 3: Generate UUID for Property
├─ ACTION: uuidgen
└─ SAVE: UUID with dashes for use in STEP 4

STEP 4: Add Property to PropertyGroup
├─ OPEN: Document type UDA file
├─ LOCATE: Target PropertyGroup
└─ ADD PropertyType object:
    {
      "Key": "{uuid-from-step-3-with-dashes}",
      "Alias": "{camelCasePropertyName}",
      "DataType": "{data-type-udi-from-step-2}",
      "Mandatory": {true|false},
      "Name": "{Display Name in Title Case}",
      "Description": "{Optional help text}",
      "SortOrder": {integer}
    }

FIELD REQUIREMENTS:
├─ Key: UUID from STEP 3 (with dashes)
├─ Alias: camelCase identifier (used in code)
├─ DataType: UDI from STEP 2
├─ Mandatory: Boolean (true = required, false = optional)
├─ Name: Display name in backoffice
├─ Description: Optional help text
└─ SortOrder: Integer (0, 1, 2, ...) for display order

STEP 5: Update Dependencies Array
├─ CHECK: Does data type UDI exist in Dependencies?
├─ IF NO: Add dependency
│  └─ {"Udi": "{data-type-udi}", "Ordering": true}
└─ IF YES: No action needed

STEP 6: Locate Component Using Document Type
├─ METHOD A: grep -r "as {DocumentTypeAlias}Model" src/Seed.Web/common/components/blockGrid/blocks/
├─ METHOD B: grep -r 'contentTypeAlias.*===.*"{documentTypeAlias}"' src/Seed.Web/
├─ METHOD C: Known locations:
│  ├─ Block Grid: src/Seed.Web/common/components/blockGrid/blocks/{componentName}.tsx
│  ├─ Pages: src/Seed.Web/pages/{pageName}/index.tsx
│  └─ Common: src/Seed.Web/common/components/{category}/{componentName}.tsx
│
├─ IF NO COMPONENT FOUND: Skip to STEP 8 (property works in backoffice)
└─ IF COMPONENT(S) FOUND: Proceed to STEP 7

STEP 7: Update TypeScript Type Definition (MANDATORY for all components)
├─ 7.1: Locate type definition in component
│  └─ export type {ComponentName}Model = { ... }
│
├─ 7.2: Determine TypeScript type for new property
│  └─ USE: Converter Decision Matrix (see above)
│
├─ 7.3: Add import statements (if required)
│  ├─ import { ImageModel } from "@lib/umbraco/types/imageModel.type";
│  ├─ import { UmbracoNode } from "@lib/umbraco/types/umbracoNode.type";
│  └─ import BlockGridItem from "@lib/umbraco/types/blockGridItem.type";
│
├─ 7.4: Add property to type definition
│  └─ export type {ComponentName}Model = {
│       existingProperty: type,
│       {newPropertyAlias}: {TypeFromStep7.2},  // NEW
│       optionalProperty?: type
│     }
│
│  OPTIONALITY RULE:
│  ├─ "Mandatory": true → required (no ?)
│  └─ "Mandatory": false → optional (add ?)
│
├─ 7.5: Verify type usage in component
│  └─ const { existingProperty, {newPropertyAlias} } = content as {ComponentName}Model;
│
└─ 7.6: Validate TypeScript compilation
   ├─ RUN: npx tsc --noEmit --project src/Seed.Web/tsconfig.json
   ├─ EXPECT: No type errors
   └─ IF ERRORS:
      ├─ Verify alias matches exactly (case-sensitive)
      ├─ Verify type matches converter output
      └─ Verify import statements correct

STEP 8: Final Validation
├─ [ ] UDA file modified with valid JSON
├─ [ ] Property added with correct data type reference
├─ [ ] Dependencies array updated
├─ [ ] TypeScript types updated in ALL components
├─ [ ] TypeScript compilation succeeds (no errors)
└─ [ ] Component can destructure new property

STATUS: Only commit after all criteria met
```

## Validation Checklist (Pre-Deployment)

```
JSON VALIDATION:
├─ [ ] No trailing commas
├─ [ ] All brackets matched {} []
├─ [ ] Double quotes only "
├─ [ ] String values properly escaped
└─ [ ] Passes JSON linter

UUID VALIDATION:
├─ [ ] All UUIDs unique (not copied)
├─ [ ] UUIDs in UDI format: no dashes
├─ [ ] UUIDs in Key fields: with dashes
└─ [ ] New UUIDs generated (not from examples)

NAMING VALIDATION:
├─ [ ] Property Alias: camelCase
├─ [ ] Property Name: Title Case
├─ [ ] Data type Name: context-specific convention
└─ [ ] No regex patterns (project standard)

REFERENCE VALIDATION:
├─ [ ] All data type UDIs reference actual files
├─ [ ] Dependencies array complete
└─ [ ] No circular dependencies

ORDER VALIDATION:
├─ [ ] SortOrder values sequential integers
└─ [ ] SortOrder reflects desired display order

TYPE VALIDATION (MANDATORY):
├─ [ ] ALL components using document type identified
├─ [ ] TypeScript types updated in EVERY component
├─ [ ] Property alias matches UDA exactly (case-sensitive)
├─ [ ] TypeScript type matches converter output
├─ [ ] Optional properties marked with ? if not mandatory
├─ [ ] Import statements for complex types
├─ [ ] npx tsc --noEmit executed
├─ [ ] Zero TypeScript errors
├─ [ ] Component can destructure property
└─ [ ] IntelliSense shows correct type

CONVERTER VALIDATION:
├─ [ ] Converter decision logic executed
├─ [ ] If custom converter needed, exists and registered
└─ [ ] EditorAlias in converter matches UDA exactly
```

## TypeScript Type Correspondence

```
EDITORALIAS                       TYPESCRIPT TYPE                      IMPORT
==================================================================================================
Umbraco.TextBox                   string                               None
Umbraco.TextArea                  string                               None
Umbraco.Integer                   number                               None
Umbraco.Decimal                   number                               None
Umbraco.TrueFalse                 boolean                              None
Umbraco.DateTime                  string                               None (ISO 8601)
Umbraco.DropDown.Flexible         string OR "Opt1" | "Opt2"            None
Umbraco.CheckBoxList              string[]                             None
Umbraco.MediaPicker3              ImageModel                           @lib/umbraco/types/imageModel.type
Umbraco.ContentPicker             UmbracoNode                          @lib/umbraco/types/umbracoNode.type
Umbraco.MultiNodeTreePicker       UmbracoNode[]                        @lib/umbraco/types/umbracoNode.type
Umbraco.BlockGrid                 BlockGridItem[]                      @lib/umbraco/types/blockGridItem.type
Umbraco.BlockList                 BlockListItem[]                      @lib/umbraco/types/blockListItem.type
Umbraco.TinyMCE                   string                               None (HTML string)
UmbracoForms.FormPicker           ApiSafeForm                          Custom type
```

## Common Patterns

### PATTERN: Add ImageModel Property

```
SCENARIO: Add background image to component

STEP 1: Create/locate media picker data type
├─ EditorAlias: Umbraco.MediaPicker3
├─ Configuration: Define crop sizes for this component
└─ Name: "{Component} - Background Image - Media Picker"

STEP 2: Add property to document type UDA
├─ Generate UUID: uuidgen
├─ Alias: "backgroundImage"
├─ DataType: umb://data-type/{media-picker-uuid}
└─ Mandatory: true/false

STEP 3: Update TypeScript type in component
├─ ADD IMPORT: import { ImageModel } from "@lib/umbraco/types/imageModel.type";
├─ ADD TO TYPE: backgroundImage: ImageModel
└─ DESTRUCTURE: const { backgroundImage } = content as ComponentModel;

STEP 4: Validate
└─ RUN: npx tsc --noEmit (expect zero errors)
```

### PATTERN: Add Dropdown with Union Type

```
SCENARIO: Add size selector with specific options

STEP 1: Create dropdown data type
├─ EditorAlias: Umbraco.DropDown.Flexible
├─ Configuration: Add items ["Small", "Medium", "Large"]
└─ Name: "{Component} - Size - Dropdown"

STEP 2: Add property to document type UDA
├─ Generate UUID: uuidgen
├─ Alias: "size"
└─ DataType: umb://data-type/{dropdown-uuid}

STEP 3: Update TypeScript type in component
├─ NO IMPORT NEEDED
├─ ADD TO TYPE: size: "Small" | "Medium" | "Large"
└─ DESTRUCTURE: const { size } = content as ComponentModel;

STEP 4: Validate
└─ RUN: npx tsc --noEmit (expect zero errors)
```

### PATTERN: Add Boolean Toggle

```
SCENARIO: Add toggle switch for feature enable/disable

STEP 1: Create/locate toggle data type
├─ EditorAlias: Umbraco.TrueFalse
├─ Configuration: Default value (usually false)
└─ Name: "{Component} - {Feature} - Toggle"

STEP 2: Add property to document type UDA
├─ Generate UUID: uuidgen
├─ Alias: "enableFeature"
└─ DataType: umb://data-type/{toggle-uuid}

STEP 3: Update TypeScript type in component
├─ NO IMPORT NEEDED
├─ ADD TO TYPE: enableFeature: boolean
└─ DESTRUCTURE: const { enableFeature } = content as ComponentModel;

STEP 4: Validate
└─ RUN: npx tsc --noEmit (expect zero errors)
```

## Risk Assessment Matrix

```
CHANGE TYPE                       RISK    MIGRATION NEEDED    TESTING SCOPE
==========================================================================================
Add new data type                 LOW     No                  New content only
Add property to document type     LOW     No                  Components using doc type
Edit data type name               LOW     No                  None
Add crop to media picker          LOW     No                  None (preserves existing)
Add dropdown option               LOW     No                  None (preserves existing)
Increase field limit              LOW     No                  None

Remove crop from media picker     HIGH    Yes                 All content using data type
Remove dropdown option            HIGH    Yes                 All content using data type
Reduce field limit                HIGH    Maybe               All content using data type
Change EditorAlias                CRITICAL DON'T DO THIS      Everything breaks
Change DatabaseType               CRITICAL DON'T DO THIS      Data loss
Remove property from doc type     HIGH    Yes                 All content + all components
```

## Anti-Patterns (What NOT to Do)

```
❌ NEVER: Change EditorAlias in existing data type (breaks everything)
   ✅ INSTEAD: Create new data type, migrate content

❌ NEVER: Reuse generic data types with different configs
   ✅ INSTEAD: Create context-specific data types

❌ NEVER: Skip TypeScript type updates
   ✅ INSTEAD: Update ALL components before committing

❌ NEVER: Commit UDA changes without validating TypeScript compilation
   ✅ INSTEAD: Always run npx tsc --noEmit before commit

❌ NEVER: Copy UUIDs from examples or other properties
   ✅ INSTEAD: Generate new UUIDs with uuidgen

❌ NEVER: Use trailing commas in UDA JSON
   ✅ INSTEAD: Remove all trailing commas (JSON spec)

❌ NEVER: Remove properties without data migration plan
   ✅ INSTEAD: Mark deprecated, migrate data, then remove

❌ NEVER: Assume converter exists without checking decision matrix
   ✅ INSTEAD: Execute converter decision logic first

❌ NEVER: Deploy without testing TypeScript compilation
   ✅ INSTEAD: npx tsc --noEmit must return zero errors
```

## Troubleshooting Lookup

```
ISSUE                                       SOLUTION
==================================================================================================
TypeScript error: Property doesn't exist    ├─ Verify alias matches UDA exactly (case-sensitive)
                                            ├─ Verify property added to type definition
                                            └─ Verify component imports correct type

TypeScript error: Type mismatch             ├─ Check Converter Decision Matrix for correct type
                                            ├─ Verify converter output matches type definition
                                            └─ Import complex types (ImageModel, UmbracoNode)

UDA file won't save                         ├─ Validate JSON syntax (no trailing commas)
                                            ├─ Check all brackets matched
                                            └─ Verify UUIDs formatted correctly

Property not appearing in backoffice        ├─ Check Dependencies array includes data type
                                            ├─ Verify UDI references correct data type file
                                            └─ Restart Umbraco application

Property not in API response                ├─ Verify property added to document type UDA
                                            ├─ Check converter handles this EditorAlias
                                            └─ Clear cache, republish content

Converter not found                         ├─ Verify EditorAlias matches exactly
                                            ├─ Check converter in correct project
                                            └─ Restart application

TypeScript compilation slow                 ├─ Use --project flag with specific tsconfig
                                            └─ npx tsc --noEmit --project src/Seed.Web/tsconfig.json

IntelliSense not showing type               ├─ Restart TypeScript server in IDE
                                            ├─ Verify type is exported
                                            └─ Check import path is correct
```

## Document Cross-Reference

```
NEED                                        CONSULT
==================================================================================================
UDA field descriptions                      UDA_FILE_FORMAT.md § Common JSON Structure
UDA syntax reference                        UDA_FILE_FORMAT.md § Artifact Types
UUID format specifications                  UDA_FILE_FORMAT.md § UUID Requirements
Best practices for schema                   UDA_FILE_FORMAT.md § Best Practices

Converter automatic fallback                UDA_APISAFECONVERTERS_RELATIONSHIP.md § Automatic Fallback
When to create custom converter             UDA_APISAFECONVERTERS_RELATIONSHIP.md § When to Create
EditorAlias binding mechanism               UDA_APISAFECONVERTERS_RELATIONSHIP.md § The Connection
Converter examples                          UDA_APISAFECONVERTERS_RELATIONSHIP.md § Examples

C# to TypeScript type mapping               TYPESCRIPT_TYPES_RELATIONSHIP.md § Type Correspondence Map
Component type definition patterns          TYPESCRIPT_TYPES_RELATIONSHIP.md § Block Grid Pattern
Type mismatch debugging                     TYPESCRIPT_TYPES_RELATIONSHIP.md § Troubleshooting
Complex type structures                     TYPESCRIPT_TYPES_RELATIONSHIP.md § Examples
```

## Command Reference

```
COMMAND                                                                         PURPOSE
==================================================================================================
uuidgen                                                                         Generate new UUID
grep -l "\"Name\": \"X\"" src/UmbracoProject/umbraco/Deploy/Revision/*.uda    Find UDA by name
grep -r "{udi}" src/UmbracoProject/umbraco/Deploy/Revision/document-type__*.uda  Find usage
grep -r "as {Alias}Model" src/Seed.Web/common/components/blockGrid/blocks/    Find component
npx tsc --noEmit --project src/Seed.Web/tsconfig.json                         Validate TypeScript
```

## Three-Layer Architecture Summary

```
LAYER 1: SCHEMA (UDA Files)
├─ DEFINES: WHAT exists and HOW it's configured
├─ FORMAT: JSON (.uda extension)
├─ LOCATION: src/UmbracoProject/umbraco/Deploy/Revision/
└─ ROLE: Source of truth for CMS schema

LAYER 2: TRANSFORM (ApiSafeConverters)
├─ DEFINES: HOW data transforms for API delivery
├─ FORMAT: C# classes
├─ LOCATION: src/Seed.Core/ApiSafeConverters/ OR src/Seed.Backoffice.Extensions/ApiSafeConverters/
├─ ROLE: Convert Umbraco objects → JSON-safe structures
└─ NOTE: ~80% automatic passthrough (no converter needed)

LAYER 3: CONSUME (TypeScript Types)
├─ DEFINES: WHAT shape data has in frontend
├─ FORMAT: TypeScript interfaces/types
├─ LOCATION: src/Seed.Web/lib/umbraco/types/ OR component files
├─ ROLE: Type-safe consumption of API data
└─ MUST: Match Layer 2 converter output OR Layer 1 automatic passthrough

CRITICAL: All three layers must stay synchronized
```
