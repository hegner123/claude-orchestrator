# uSync vs UDA - LLM Action Guide

## System Identification

```
PROJECT STATUS: Both systems active (DUAL SYNC)
- uSync files: 922 .config files in uSync/v9/
- UDA files: 619 .uda files in umbraco/Deploy/Revision/
PRIMARY: UDA (Umbraco Deploy) = production source of truth
SECONDARY: uSync = local dev convenience
```

## File Location Pattern Matching

```
PATTERN: uSync/v9/**/*.config
├─ System: uSync
├─ Format: XML
├─ Naming: Human-readable (productPage.config)
└─ Scope: Schema + Content (optional)

PATTERN: umbraco/Deploy/Revision/**/*.uda
├─ System: UDA (Umbraco Deploy)
├─ Format: JSON
├─ Naming: GUID-based (document-type__a1b2c3d4.uda)
└─ Scope: Schema only
```

## System Comparison Matrix

| Property | uSync | UDA (Umbraco Deploy) |
|----------|-------|---------------------|
| Format | XML | JSON |
| Extension | `.config` | `.uda` |
| Location | `uSync/v9/` | `umbraco/Deploy/Revision/` |
| Auto-generate on save | ❌ No (manual export) | ✅ Yes |
| Auto-apply on startup | ⚠️ Optional config | ✅ Yes |
| File naming | `productPage.config` | `document-type__<GUID>.uda` |
| Developer | Community (Jumoo) | Umbraco HQ |
| License | MIT (free) | Commercial |
| Content sync | ✅ Yes | ❌ No |
| Cloud deployment | ❌ No | ✅ Yes |
| File count (this project) | 922 | 619 |

## Decision Tree: Which System to Use?

```
QUERY: Schema change needed
├─ Is Umbraco Cloud in use?
│  ├─ YES → Use UDA (required)
│  └─ NO → Continue to next check
├─ Want automatic sync?
│  ├─ YES → Use UDA
│  └─ NO → Continue to next check
├─ Need to sync content too?
│  ├─ YES → Use uSync (only system that syncs content)
│  └─ NO → Continue to next check
├─ Budget constraints?
│  ├─ YES → Use uSync (free)
│  └─ NO → Use UDA (commercial but better automation)
└─ Default recommendation
   └─ UDA for production, uSync for local dev (or pick one)
```

## Action Patterns

### PATTERN: Schema Change Made in Backoffice

```
CONDITION: User edited document type in Settings → Document Types
├─ UDA System
│  ├─ FILE CREATED: umbraco/Deploy/Revision/document-type__<GUID>.uda
│  ├─ AUTOMATIC: On save
│  ├─ ACTION: git add umbraco/Deploy/Revision/*.uda
│  └─ ACTION: git commit -m "Add field to document type"
│
└─ uSync System
   ├─ FILE CREATED: None (requires manual export)
   ├─ ACTION REQUIRED: Settings → uSync → Dashboard → Export
   ├─ FILE CREATED: uSync/v9/ContentTypes/<alias>.config
   ├─ ACTION: git add uSync/v9/**/*.config
   └─ ACTION: git commit -m "Add field to document type"
```

### PATTERN: After Git Pull

```
CONDITION: git pull shows changes to schema files

IF changes to: umbraco/Deploy/Revision/**/*.uda
├─ UDA auto-applies on next startup
├─ ACTION: dotnet run (or restart if running)
├─ VERIFICATION: Check Deploy log in backoffice
└─ NO MANUAL IMPORT REQUIRED

IF changes to: uSync/v9/**/*.config
├─ Manual import required
├─ ACTION: Open backoffice
├─ ACTION: Settings → uSync → Dashboard
├─ ACTION: Click "Import" button
├─ VERIFICATION: Review import report (green = success)
└─ REQUIRED: Manual step

BEST PRACTICE: Always import/restart after pulling schema changes
```

### PATTERN: Branch Switching

```
CONDITION: git checkout <different-branch>

STEP 1: Switch branch
├─ ACTION: git checkout feature/new-schema

STEP 2: Apply schema for this branch
├─ UDA System
│  ├─ ACTION: dotnet run
│  └─ AUTO: Deploy detects and applies UDA changes
│
└─ uSync System
   ├─ ACTION: Open backoffice
   ├─ ACTION: Settings → uSync → Import
   └─ MANUAL: Import required

CRITICAL: Database schema = last imported state
└─ Switching branches changes files but NOT database
└─ Must import/apply to sync database with branch
```

### PATTERN: Merge Conflict in Schema Files

```
CONDITION: Git conflict in .uda or .config file

UDA Conflict (.uda file):
├─ FILE: umbraco/Deploy/Revision/document-type__abc123.uda
├─ FORMAT: JSON
├─ RESOLUTION STEPS:
│  ├─ 1. Choose version (or manually merge JSON)
│  ├─ 2. Ensure valid JSON (check commas, brackets, quotes)
│  ├─ 3. git add <file>
│  ├─ 4. dotnet run (Deploy applies)
│  ├─ 5. Open backoffice → verify schema
│  ├─ 6. Save document type again (regenerates clean UDA)
│  └─ 7. git add + commit clean version
└─ DIFFICULTY: Hard (GUID references, JSON structure)

uSync Conflict (.config file):
├─ FILE: uSync/v9/ContentTypes/productPage.config
├─ FORMAT: XML
├─ RESOLUTION STEPS:
│  ├─ 1. Choose version (or manually merge XML)
│  ├─ 2. Ensure valid XML (check tags, closing brackets)
│  ├─ 3. git add <file>
│  ├─ 4. Settings → uSync → Import
│  ├─ 5. Verify in backoffice
│  ├─ 6. Settings → uSync → Export (regenerates clean file)
│  └─ 7. git add + commit clean version
└─ DIFFICULTY: Easier (human-readable names, XML structure)

SAFEST APPROACH: Revert conflict, remake change in backoffice
├─ git checkout --theirs <file>  (or --ours)
├─ Import/restart to apply
├─ Remake the conflicting change in backoffice
└─ Commit auto-generated file
```

### PATTERN: New Project Setup

```
CONDITION: Developer joining project OR setting up new environment

STEP 1: Clone repository
├─ ACTION: git clone <repo-url>
├─ ACTION: cd src/UmbracoProject

STEP 2: Restore packages
├─ ACTION: dotnet restore
├─ ACTION: npm install

STEP 3: Start application (first time)
├─ ACTION: dotnet run
├─ UDA: Automatically applies all schema from UDA files
├─ uSync: May auto-apply if ImportAtStartup: true

STEP 4: Manual import (if needed)
├─ IF uSync not auto-imported:
│  ├─ Open backoffice: https://localhost:44373/umbraco
│  ├─ Settings → uSync → Dashboard
│  └─ Click "Import"
└─ Verify schema in backoffice

STEP 5: Verify sync status
├─ Check document types exist
├─ Check data types exist
└─ Ready to work
```

## Configuration Patterns

### uSync Configuration

```json
FILE: appsettings.json

{
  "uSync": {
    "Settings": {
      "ExportOnSave": true,        // RECOMMENDED: Auto-export on save
      "ImportAtStartup": true,      // RECOMMENDED: Auto-import on startup
      "ExportAtStartup": false,     // Don't export at startup
      "UseGuidFilenames": false,    // Use human-readable names
      "RebuildCacheOnCompletion": true
    },
    "Sets": {
      "Default": {
        "Enabled": true,
        "HandlerDefaults": [
          {"Handler": "ContentTypeHandler", "Enabled": true, "Actions": ["Import", "Export"]},
          {"Handler": "DataTypeHandler", "Enabled": true, "Actions": ["Import", "Export"]},
          {"Handler": "TemplateHandler", "Enabled": true, "Actions": ["Import", "Export"]},
          {"Handler": "ContentHandler", "Enabled": false, "Actions": []}  // Don't sync content
        ]
      }
    }
  }
}
```

### UDA Configuration

```json
FILE: appsettings.json

{
  "Umbraco": {
    "Deploy": {
      "Settings": {
        "TransferFormsAsContent": false,
        "ExportMemberGroups": true,
        "AllowMembersDeploymentOperations": false,
        "SessionTimeout": "00:20:00"
      }
    }
  }
}

NOTE: Minimal config required. Deploy is mostly automatic.
```

## Command Reference

### uSync Commands

```
LOCATION: Backoffice → Settings → uSync → Dashboard

ACTION: Import
├─ Reads files from uSync/v9/
├─ Applies to database
├─ Shows report (green = success, red = error)
└─ USE CASE: After git pull, after branch switch

ACTION: Export
├─ Reads schema from database
├─ Writes to uSync/v9/
├─ Overwrites existing files
└─ USE CASE: After schema changes, before commit

ACTION: Report
├─ Dry run (no changes)
├─ Shows what would change
└─ USE CASE: Preview before import

OPTIONS:
├─ Force: Overwrite database even if timestamps match
└─ USE CASE: When database and files are out of sync
```

### UDA Commands

```
AUTOMATIC OPERATIONS:
├─ On Save: UDA file created/updated
└─ On Startup: UDA files applied to database

MANUAL OPERATIONS (rarely needed):
LOCATION: Backoffice → Settings → Deploy Operations

ACTION: Schema Deployment → Extract
├─ Forces re-scan of database
├─ Regenerates all UDA files
└─ USE CASE: UDA files missing or corrupted

ACTION: Clear Signatures
├─ Clears Deploy cache
├─ Forces fresh deployment
└─ USE CASE: Deploy stuck or errors

FILE SYSTEM CACHE CLEAR:
├─ Delete: umbraco/Deploy/deploy-marker
├─ Delete: umbraco/Deploy/deploy.lock
├─ Restart application
└─ USE CASE: Deploy not detecting changes
```

## Error Resolution Patterns

### ERROR: Files out of sync with database

```
SYMPTOM: Schema files don't match backoffice content

DIAGNOSIS:
├─ Document types in backoffice ≠ schema files
├─ Properties missing or different
└─ Import/Deploy has no effect

RESOLUTION (uSync):
├─ Settings → uSync → Dashboard
├─ Check "Force" option
├─ Click "Import"
├─ Clears cache and overwrites database
└─ Database now matches files

RESOLUTION (UDA):
├─ Delete: umbraco/Deploy/deploy-marker
├─ Delete: umbraco/Deploy/deploy.lock
├─ Restart: dotnet run
├─ Deploy re-scans and applies all UDA files
└─ Database now matches files

PREVENTION:
└─ Always import/restart after pulling
```

### ERROR: Manual edit broke schema file

```
SYMPTOM: Import/Deploy fails with error

DIAGNOSIS:
├─ Developer edited .uda or .config manually
├─ Invalid JSON or XML
└─ Dependency references broken

RESOLUTION:
├─ STEP 1: Revert broken file
│  └─ git checkout HEAD -- <file-path>
├─ STEP 2: Import/restart with clean file
│  └─ Settings → uSync → Import OR dotnet run
├─ STEP 3: Make change properly in backoffice
│  └─ Settings → Document Types → Edit → Save
├─ STEP 4: Commit auto-generated file
│  └─ git add <file> && git commit
└─ NEVER manually edit schema files
```

### ERROR: Import after pull forgotten

```
SYMPTOM: ApiSafeConverter fails, properties missing, types don't match

DIAGNOSIS:
├─ Pulled code with schema changes
├─ Forgot to import
└─ Database is outdated

RESOLUTION:
├─ uSync: Settings → uSync → Import
└─ UDA: Restart application (dotnet run)

PREVENTION:
├─ Enable ImportAtStartup: true (uSync)
├─ UDA: Auto-applies on startup (already enabled)
└─ Workflow: git pull → import → code
```

## Dual System Management (This Project)

```
PROJECT STATUS: Uses BOTH uSync + UDA
├─ PRIMARY: UDA (production source of truth)
├─ SECONDARY: uSync (local dev, backup)
└─ TOTAL FILES: ~1,500 schema files (922 + 619)

DESIGNATED PRIMARY: UDA
├─ Reason: Production deployments use UDA
├─ Reason: Cloud-ready
└─ In conflict: Trust UDA

WORKFLOW:
├─ STEP 1: Make change in backoffice
├─ STEP 2: UDA auto-saves
├─ STEP 3: Optional - Export uSync
├─ STEP 4: Commit both
│  ├─ git add umbraco/Deploy/Revision/*.uda
│  ├─ git add uSync/v9/**/*.config
│  └─ git commit -m "Schema change"
└─ STEP 5: Push

ON PULL:
├─ UDA auto-applies on restart
└─ Optional: uSync Import for verification

CONFLICT RESOLUTION:
├─ IF UDA says X and uSync says Y
├─ TRUST: UDA (primary system)
├─ FIX: Re-export uSync from database
└─ RESULT: Both systems now agree
```

## Quick Decision Matrix

```
QUERY: What action to take?

git pull completed:
├─ *.uda changed? → Restart application
└─ *.config changed? → Settings → uSync → Import

Schema change made:
├─ Using UDA? → Automatic (just commit)
└─ Using uSync? → Export → Commit

Merge conflict:
├─ Resolve conflict in file
├─ Ensure valid JSON/XML
├─ Import/Restart
├─ Save in backoffice again (clean file)
└─ Commit

New environment setup:
├─ git clone
├─ dotnet run
├─ UDA auto-applies
└─ uSync: Import if needed

Files don't match database:
├─ uSync: Force Import
└─ UDA: Delete markers, restart

Deploy/Import failing:
├─ Check file validity (JSON/XML)
├─ Revert if manually edited
└─ Remake change in backoffice
```

## File Path References

```
uSync Files:
├─ uSync/v9/ContentTypes/*.config
├─ uSync/v9/DataTypes/*.config
├─ uSync/v9/Templates/*.config
├─ uSync/v9/MediaTypes/*.config
├─ uSync/v9/Forms/*.config
├─ uSync/v9/Languages/*.config
└─ uSync/v9/usync.config

UDA Files:
├─ umbraco/Deploy/Revision/document-type__*.uda
├─ umbraco/Deploy/Revision/data-type__*.uda
├─ umbraco/Deploy/Revision/template__*.uda
├─ umbraco/Deploy/Revision/media-type__*.uda
├─ umbraco/Deploy/Revision/data-type-container__*.uda
└─ umbraco/Deploy/Revision/document-type-container__*.uda

Deploy Cache:
├─ umbraco/Deploy/deploy-marker (delete to clear cache)
└─ umbraco/Deploy/deploy.lock (delete if stuck)

uSync Cache:
└─ uSync/.cache/ (delete to force re-import)
```

## System Selection Criteria

```
SELECT: UDA (Umbraco Deploy)
WHEN:
├─ Using Umbraco Cloud
├─ Want zero-manual-steps automation
├─ Production deployment pipeline
├─ Enterprise environment
├─ Official support required
└─ Schema-only sync sufficient

SELECT: uSync
WHEN:
├─ Self-hosted environment
├─ Budget constraints (free)
├─ Need to sync content
├─ Want manual control over sync
├─ Prefer human-readable file names
└─ Team prefers manual workflow

SELECT: Both
WHEN:
├─ Want redundancy
├─ Transition period (moving to Cloud)
├─ Mixed team preferences
└─ Already using both (this project)

RECOMMENDATION FOR NEW PROJECTS:
├─ Pick ONE system
├─ Using Cloud? → UDA only
├─ Self-hosted? → uSync only
└─ Don't use both unless specific need
```
