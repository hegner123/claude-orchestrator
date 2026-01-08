# STARTUP - Project Context Recovery

Execute these steps sequentially to understand project state and identify next actions.

---

## STEP 1: Read Implementation Status

**Action:** Read file `IMPLEMENTATION.md`

**Extract:**
- Phase completion status (✅ complete, 🚧 in progress, ⏸️ not started)
- Overall progress percentage
- Recent changes section
- Current blockers
- Next phase recommendation

---

## STEP 2: Check Recent Activity

**Action:** Execute command `git log --oneline --stat -5`

**Extract:**
- Last 5 commit messages
- Files changed in recent commits
- Pattern of recent development focus

---

## STEP 3: Verify Implementation

**Action:** Read file `prototype/orchestrator.py`

**Extract:**
- Which agents are imported/initialized
- Available workflow methods
- Integration status

**Action:** Execute commands
```bash
ls -la prototype/agents/
ls -la prototype/workflow/
```

**Extract:**
- Agent files present (filename = phase complete)
- Example output files in workflow directory

---

## STEP 4: Architecture Review (OPTIONAL)

**Condition:** Only if Steps 1-3 don't provide clear understanding

**Action:** Read `CLAUDE.md`
**Focus:** "Architecture Overview" and "AI Component Build Workflow" sections

**Action:** Read `mh-ai-compoent-build.md`
**Focus:** "Recommended Workflow Enhancement" section

---

## OUTPUT REQUIREMENTS

Provide response in this exact format:

```
## Project Status
- Progress: X%
- Complete: Phase N (name), Phase N (name)
- Pending: Phase N (name), Phase N (name)
- Blockers: [list or "None"]

## What's Working
[2-3 sentence summary of completed phases and capabilities]

## Recommended Next Step
- Phase: [number and name]
- Rationale: [why this phase is next]
- Complexity: [LOW/MEDIUM/HIGH]
```

---

## File Priority Map

**Always read (Steps 1-3):**
- `IMPLEMENTATION.md`
- `prototype/orchestrator.py`
- Git log + directory listings

**Read if unclear (Step 4):**
- `CLAUDE.md`
- `mh-ai-compoent-build.md`

**Never read during startup:**
- Phase-specific implementation guides
- Umbraco documentation files
- Test files or example outputs
