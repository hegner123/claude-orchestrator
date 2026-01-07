# Multi-Agent Workflow Architecture

## Overview

This document outlines how to implement multi-agent workflows where agents can communicate and coordinate their work. Based on official Claude Code and Claude Agent SDK documentation research.

## Key Finding: Direct Inter-Agent Communication Not Supported

**Claude Code subagents operate in parent-child hierarchies**, not peer-to-peer networks:
- Subagents have independent context windows
- They don't directly communicate with each other
- Each subagent returns results to the parent agent
- No built-in messaging system between agents

**Solution**: Use a **shared data structure (Component Contract)** as the communication medium.

## Recommended Implementation Patterns

### Pattern 1: Claude Code + External Orchestrator (Recommended for Prototyping)

**Complexity**: Low
**Control**: Medium
**Best For**: Quick prototypes, simpler workflows

#### Architecture

```
┌─────────────────────────────────────────────┐
│          Orchestrator Service               │
│  (Python/TypeScript/Node.js script)         │
│                                             │
│  Maintains: Component Contract (JSON)       │
└─────────────────────────────────────────────┘
           │
           ├─→ Calls Claude Code Subagent 1 (Vision)
           │   ├─ Reads: Component Contract
           │   ├─ Does: Image analysis
           │   └─ Writes: Component Contract updates
           │
           ├─→ Calls Claude Code Subagent 2 (Backend)
           │   ├─ Reads: Component Contract
           │   ├─ Does: UDA generation
           │   └─ Writes: Component Contract updates
           │
           ├─→ Calls Claude Code Subagent 3 (TypeScript)
           │   ├─ Reads: Component Contract
           │   ├─ Does: Type definitions
           │   └─ Writes: Component Contract updates
           │
           └─→ Calls Claude Code Subagent 4 (Styling)
               ├─ Reads: Component Contract
               ├─ Does: CSS generation
               └─ Writes: Component Contract updates
```

#### Implementation Example

```python
# orchestrator.py
import json
import subprocess
import asyncio

class ComponentContractOrchestrator:
    def __init__(self):
        self.contract_path = "./workflow/component-contract.json"
        self.contract = {}

    def load_contract(self):
        """Load shared Component Contract"""
        with open(self.contract_path, 'r') as f:
            self.contract = json.load(f)
        return self.contract

    def save_contract(self):
        """Persist Component Contract to disk"""
        with open(self.contract_path, 'w') as f:
            json.dump(self.contract, f, indent=2)

    async def call_agent(self, agent_name, task_description):
        """
        Call a Claude Code subagent with access to the contract

        Args:
            agent_name: Name of the agent (vision-agent, backend-agent, etc.)
            task_description: What the agent should do
        """
        # Save current contract state for agent to read
        self.save_contract()

        # Call Claude Code subagent
        # The agent will read the contract file, do work, and update it
        result = subprocess.run([
            'claude-code',
            'task',
            '--agent', agent_name,
            '--prompt', f"{task_description}\n\nComponent Contract available at: {self.contract_path}"
        ], capture_output=True, text=True)

        # Reload contract with agent's updates
        self.load_contract()

        return result.stdout

    async def run_workflow(self, design_image_path):
        """Execute the full multi-agent workflow"""

        # Initialize contract
        self.contract = {
            "componentId": f"component-{timestamp()}",
            "workflowState": "INITIALIZED",
            "metadata": {"created": datetime.now().isoformat()}
        }
        self.save_contract()

        # Phase 1: Vision Analysis
        print("Phase 1: Vision Agent analyzing design...")
        self.contract["workflowState"] = "VISION_ANALYSIS"
        await self.call_agent(
            "vision-agent",
            f"Analyze the design image at {design_image_path} and extract component structure. "
            f"Update the Component Contract with semantic structure, UI patterns, and confidence scores."
        )

        # Phase 2: Operator Confirmation (if needed)
        if self.contract.get("metadata", {}).get("confidence", 1.0) < 0.85:
            print("Phase 2: Low confidence detected, requesting operator review...")
            self.contract = await self.operator_review(self.contract)
            self.save_contract()

        # Phase 3: Parallel Agent Execution
        print("Phase 3: Executing backend, TypeScript, and styling agents in parallel...")
        self.contract["workflowState"] = "AGENT_EXECUTION"

        await asyncio.gather(
            self.call_agent(
                "backend-agent",
                "Generate UDA files and ApiSafeConverters based on the Component Contract. "
                "Update the contract with file paths and converter decisions."
            ),
            self.call_agent(
                "typescript-agent",
                "Generate TypeScript type definitions based on the Component Contract. "
                "Update the contract with type mappings."
            ),
            self.call_agent(
                "styling-agent",
                "Generate CSS/SCSS from design tokens in the Component Contract. "
                "Update the contract with style file paths."
            )
        )

        # Phase 4: Validation
        print("Phase 4: Running validation gates...")
        self.contract["workflowState"] = "VALIDATION"
        await self.call_agent(
            "validation-agent",
            "Validate the component against all gates. Update contract with validation results."
        )

        # Phase 5: Delivery
        print("Phase 5: Finalizing delivery...")
        self.contract["workflowState"] = "COMPLETED"
        self.save_contract()

        return self.contract

    async def operator_review(self, contract):
        """Present low-confidence decisions to operator for review"""
        # Implementation: CLI prompts, web UI, etc.
        pass

# Usage
if __name__ == "__main__":
    orchestrator = ComponentContractOrchestrator()
    asyncio.run(orchestrator.run_workflow("./designs/hero-section.png"))
```

### Pattern 2: Claude Agent SDK (Recommended for Production)

**Complexity**: High
**Control**: High
**Best For**: Production systems, complex coordination, fine-grained control

#### Architecture

Agents have access to custom tools that read/write shared state.

#### Custom Tool Definitions

```python
from anthropic import Anthropic

# Tools that all agents can use to communicate
tools = [
    {
        "name": "read_contract",
        "description": "Read the current Component Contract to understand what other agents have discovered",
        "input_schema": {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "description": "Optional: specific section to read (contentType, visualStructure, etc.)",
                    "enum": ["all", "contentType", "visualStructure", "derivedFunctionality", "dependencies", "metadata"]
                }
            }
        }
    },
    {
        "name": "update_contract",
        "description": "Update the Component Contract with your findings or results",
        "input_schema": {
            "type": "object",
            "properties": {
                "updates": {
                    "type": "object",
                    "description": "Partial Component Contract updates to merge"
                },
                "confidence": {
                    "type": "number",
                    "description": "Confidence score for this update (0.0-1.0)"
                }
            },
            "required": ["updates"]
        }
    },
    {
        "name": "query_agent",
        "description": "Ask another agent a question when you need information they have",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent": {
                    "type": "string",
                    "description": "Which agent to query",
                    "enum": ["vision-agent", "backend-agent", "typescript-agent", "styling-agent"]
                },
                "question": {
                    "type": "string",
                    "description": "The question to ask"
                }
            },
            "required": ["agent", "question"]
        }
    },
    {
        "name": "flag_for_review",
        "description": "Flag a decision for operator review when confidence is low",
        "input_schema": {
            "type": "object",
            "properties": {
                "decision": {
                    "type": "string",
                    "description": "What decision needs review"
                },
                "confidence": {
                    "type": "number",
                    "description": "Your confidence score (0.0-1.0)"
                },
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Possible options for the operator to choose from"
                },
                "context": {
                    "type": "string",
                    "description": "Additional context to help operator decide"
                }
            },
            "required": ["decision", "confidence", "options"]
        }
    }
]
```

#### Agent SDK Implementation

```python
from anthropic import Anthropic
import json

client = Anthropic()
component_contract = {}

def handle_tool_use(tool_name, tool_input):
    """Handle tool calls from agents"""
    global component_contract

    if tool_name == "read_contract":
        section = tool_input.get("section", "all")
        if section == "all":
            return json.dumps(component_contract, indent=2)
        else:
            return json.dumps(component_contract.get(section, {}), indent=2)

    elif tool_name == "update_contract":
        updates = tool_input["updates"]
        confidence = tool_input.get("confidence", 1.0)

        # Deep merge updates into contract
        component_contract = deep_merge(component_contract, updates)

        # Track confidence
        if "metadata" not in component_contract:
            component_contract["metadata"] = {}
        component_contract["metadata"]["lastConfidence"] = confidence

        return "Contract updated successfully"

    elif tool_name == "query_agent":
        agent_name = tool_input["agent"]
        question = tool_input["question"]

        # Recursively call the target agent
        response = run_agent(agent_name, question)
        return response

    elif tool_name == "flag_for_review":
        # Add to operator review queue
        if "operatorReview" not in component_contract:
            component_contract["operatorReview"] = []

        component_contract["operatorReview"].append({
            "decision": tool_input["decision"],
            "confidence": tool_input["confidence"],
            "options": tool_input["options"],
            "context": tool_input.get("context", "")
        })

        return "Flagged for operator review"

def run_agent(agent_name, task, system_prompt=None):
    """Run an agent with tool access"""

    if system_prompt is None:
        system_prompt = get_agent_system_prompt(agent_name)

    messages = [{"role": "user", "content": task}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        # Check stop reason
        if response.stop_reason == "end_turn":
            # Agent finished
            text_response = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text_response += block.text
            return text_response

        # Handle tool use
        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    # Execute the tool
                    result = handle_tool_use(block.name, block.input)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Continue conversation with tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

def get_agent_system_prompt(agent_name):
    """Get specialized system prompt for each agent"""

    prompts = {
        "vision-agent": """You are a UI/UX vision specialist.
        Analyze design images and extract component structure with confidence scores.
        Use the read_contract and update_contract tools to maintain shared state.
        Flag low-confidence decisions using flag_for_review.""",

        "backend-agent": """You are a backend architecture specialist.
        Generate UDA files and ApiSafeConverters based on the Component Contract.
        Use read_contract to see what the vision agent discovered.
        Use update_contract to record your decisions about converters and data types.""",

        "typescript-agent": """You are a TypeScript type system specialist.
        Generate type definitions that match the backend schema.
        Use query_agent if you need clarification from the backend-agent.
        Use update_contract to record type mappings.""",

        "styling-agent": """You are a CSS/design system specialist.
        Generate styles from design tokens and visual specifications.
        Use read_contract to see the visual structure from the vision agent.
        Use update_contract to record generated style files."""
    }

    return prompts.get(agent_name, "You are a helpful assistant.")

# Example workflow
def run_multi_agent_workflow(design_image_path):
    global component_contract

    # Initialize contract
    component_contract = {
        "componentId": "hero-section-v1",
        "workflowState": "INITIALIZED"
    }

    # Phase 1: Vision agent
    print("Running vision agent...")
    run_agent("vision-agent", f"Analyze {design_image_path}")

    # Phase 2: Operator review if needed
    if component_contract.get("operatorReview"):
        component_contract = handle_operator_review(component_contract)

    # Phase 3: Parallel execution
    print("Running parallel agents...")
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(run_agent, "backend-agent", "Generate backend structure"),
            executor.submit(run_agent, "typescript-agent", "Generate TypeScript types"),
            executor.submit(run_agent, "styling-agent", "Generate styles")
        ]
        concurrent.futures.wait(futures)

    return component_contract
```

## Communication Protocol: AgentMessage Pattern

Implement a structured message format for inter-agent communication:

```typescript
interface AgentMessage {
  from: string;                    // "vision-agent", "backend-agent", etc.
  to?: string;                     // Optional: specific recipient
  messageType: "query" | "update" | "error" | "completion";
  payload: any;                    // The actual data/question
  contractUpdate?: Partial<ComponentContract>;  // Changes to apply
  requiresOperatorReview?: boolean;
  confidence?: number;             // 0.0-1.0
  timestamp: string;
}
```

### Example Message Flow

**1. Vision Agent discovers structure:**
```json
{
  "from": "vision-agent",
  "messageType": "update",
  "contractUpdate": {
    "visualStructure": {
      "desktop": {
        "areas": [
          {
            "id": "headline",
            "type": "text",
            "mapsToProperty": "headline",
            "umbracoType": "string"
          }
        ]
      }
    }
  },
  "confidence": 0.92,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**2. Backend Agent queries for clarification:**
```json
{
  "from": "backend-agent",
  "to": "vision-agent",
  "messageType": "query",
  "payload": {
    "question": "Is the headline a rich text field or plain text?"
  },
  "timestamp": "2024-01-15T10:31:00Z"
}
```

**3. Vision Agent responds:**
```json
{
  "from": "vision-agent",
  "to": "backend-agent",
  "messageType": "update",
  "payload": {
    "answer": "Plain text - single line with custom typography"
  },
  "confidence": 0.85,
  "timestamp": "2024-01-15T10:31:15Z"
}
```

**4. Backend Agent flags low confidence decision:**
```json
{
  "from": "backend-agent",
  "messageType": "error",
  "payload": {
    "decision": "Should background image use responsive crops or single crop?",
    "options": ["responsive-crops", "single-crop", "art-direction"]
  },
  "requiresOperatorReview": true,
  "confidence": 0.48,
  "timestamp": "2024-01-15T10:32:00Z"
}
```

## State Machine for Workflow Orchestration

Track workflow progress explicitly:

```typescript
interface WorkflowState {
  workflowId: string;
  componentId: string;
  currentState: WorkflowPhase;
  states: {
    [key: string]: {
      status: "PENDING" | "IN_PROGRESS" | "COMPLETED" | "FAILED" | "BLOCKED";
      startedAt?: string;
      completedAt?: string;
      confidence?: number;
      iteration?: number;
      blockers?: string[];
      artifacts?: string[];  // File paths created
    }
  };
  operatorReview?: OperatorReviewItem[];
}

type WorkflowPhase =
  | "VISION_ANALYSIS"
  | "OPERATOR_CONFIRMATION"
  | "DATATYPE_GENERATION"
  | "CONVERTER_CHECK"
  | "TYPE_DEFINITION"
  | "COMPONENT_GENERATION"
  | "STRUCTURE_VALIDATION"
  | "STYLE_REFINEMENT"
  | "FUNCTIONAL_VALIDATION"
  | "COMPLETED";

interface OperatorReviewItem {
  decision: string;
  confidence: number;
  options: string[];
  context?: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  operatorResponse?: string;
}
```

### Example State Tracking

```json
{
  "workflowId": "workflow-2024-01-15-001",
  "componentId": "hero-section-v1",
  "currentState": "STYLE_REFINEMENT",
  "states": {
    "VISION_ANALYSIS": {
      "status": "COMPLETED",
      "startedAt": "2024-01-15T10:30:00Z",
      "completedAt": "2024-01-15T10:32:00Z",
      "confidence": 0.91,
      "artifacts": ["workflow/vision-analysis.json"]
    },
    "OPERATOR_CONFIRMATION": {
      "status": "COMPLETED",
      "startedAt": "2024-01-15T10:32:00Z",
      "completedAt": "2024-01-15T10:35:00Z"
    },
    "DATATYPE_GENERATION": {
      "status": "COMPLETED",
      "completedAt": "2024-01-15T10:40:00Z",
      "artifacts": [
        "src/UmbracoProject/umbraco/Deploy/Revision/data-type__abc-123.uda"
      ]
    },
    "STYLE_REFINEMENT": {
      "status": "IN_PROGRESS",
      "startedAt": "2024-01-15T10:42:00Z",
      "iteration": 2,
      "blockers": [
        "typography-weight-mismatch",
        "button-padding-off"
      ]
    }
  },
  "operatorReview": [
    {
      "decision": "Background image crop strategy",
      "confidence": 0.48,
      "options": ["responsive-crops", "single-crop"],
      "context": "Design shows different aspect ratios for mobile/desktop",
      "status": "APPROVED",
      "operatorResponse": "responsive-crops"
    }
  ]
}
```

## Confidence-Based Operator Intervention

Only interrupt operators for low-confidence decisions:

```typescript
interface DecisionWithConfidence {
  decision: string;
  confidence: number;
  autoApprove: boolean;      // true if confidence >= threshold
  requiresOperatorReview: boolean;
  operatorReview?: {
    question: string;
    options: string[];
    context: string;
    recommendation?: string;  // Agent's best guess
  };
}

// Configuration
const CONFIDENCE_THRESHOLDS = {
  AUTO_APPROVE: 0.85,        // confidence >= 0.85 → auto-approve
  OPERATOR_REVIEW: 0.75,     // confidence < 0.75 → require review
  BLOCK: 0.50                // confidence < 0.50 → must get review
};

function shouldReviewDecision(confidence: number): boolean {
  return confidence < CONFIDENCE_THRESHOLDS.OPERATOR_REVIEW;
}
```

### Example Confidence Scoring

**High Confidence (Auto-Approve):**
```json
{
  "decision": "headline field maps to 'title' property",
  "confidence": 0.92,
  "autoApprove": true,
  "requiresOperatorReview": false
}
```

**Low Confidence (Requires Review):**
```json
{
  "decision": "button behavior: modal vs navigation",
  "confidence": 0.48,
  "autoApprove": false,
  "requiresOperatorReview": true,
  "operatorReview": {
    "question": "Does the CTA button open a modal or navigate to a page?",
    "options": ["modal", "navigation", "form-submit"],
    "context": "Button labeled 'Learn More' appears near form section",
    "recommendation": "modal"
  }
}
```

## Best Practices

### 1. Version Component Contracts
```json
{
  "version": "1.0.0",
  "componentId": "hero-section-v1",
  "schemaVersion": "2024-01-15"
}
```

### 2. Enable Resumability
Store contract state to disk frequently so workflow can resume after failures:

```python
def save_checkpoint(contract, checkpoint_path):
    """Save workflow state for resumability"""
    with open(checkpoint_path, 'w') as f:
        json.dump(contract, f, indent=2)

def resume_workflow(checkpoint_path):
    """Resume from saved checkpoint"""
    with open(checkpoint_path, 'r') as f:
        contract = json.load(f)

    current_state = contract["currentState"]
    # Resume from current state...
```

### 3. Parallel Execution Where Possible
Agents with no dependencies can run in parallel:

```python
# These can run in parallel - they all read from contract
await asyncio.gather(
    backend_agent.execute(contract),
    typescript_agent.execute(contract),
    styling_agent.execute(contract)
)

# These must run sequentially - each depends on previous
vision_output = await vision_agent.analyze(image)
operator_approved = await operator.review(vision_output)
backend_output = await backend_agent.execute(operator_approved)
```

### 4. Track Agent Messages for Learning
Store all agent communications to learn patterns over time:

```python
def log_agent_message(message: AgentMessage):
    """Log messages for future training/learning"""
    with open("workflow/messages.jsonl", "a") as f:
        f.write(json.dumps(message) + "\n")
```

### 5. Implement Validation Gates
Each workflow phase should have clear success criteria:

```python
async def validate_structural_gate(contract):
    """Gate 1: Structural validation (must pass)"""
    checks = {
        "typescript_compiles": await check_typescript_compilation(),
        "component_renders": await check_component_renders(),
        "all_fields_mapped": check_all_fields_mapped(contract)
    }

    if not all(checks.values()):
        raise ValidationError("Structural validation failed", checks)

    return True
```

## Comparison: Claude Code vs Agent SDK

| Feature | Claude Code + Orchestrator | Claude Agent SDK |
|---------|---------------------------|------------------|
| **Setup Complexity** | Low - just scripts | High - custom tool implementation |
| **Agent Communication** | Via shared file | Via custom tools |
| **Context Sharing** | File read/write | Tool calls |
| **Parallel Execution** | External orchestration | ThreadPool/async |
| **Resumability** | Manual checkpointing | Manual checkpointing |
| **Development Speed** | Fast prototyping | Slower initial setup |
| **Production Ready** | Requires hardening | More control/robustness |
| **Debugging** | File inspection | Tool call logging |
| **Cost** | Same API costs | Same API costs |

## Recommended Starting Point

**For your Component Build System:**

1. **Start with Claude Code + Orchestrator**:
   - Quick to prototype
   - Easy to debug (inspect contract JSON)
   - Can iterate on agent prompts quickly
   - Move to Agent SDK when patterns stabilize

2. **Use the Component Contract as shared state**:
   - Single JSON file all agents read/write
   - Version controlled
   - Human-readable for debugging

3. **Implement confidence-based intervention**:
   - Reduces operator burden
   - Tracks where system needs improvement
   - Builds learning dataset

4. **Start with one pattern (hero sections)**:
   - Master the workflow end-to-end
   - Expand to more patterns after success
   - Build pattern library incrementally

## Implementation Checklist

- [ ] Define Component Contract JSON schema
- [ ] Create orchestrator script (Python/Node.js)
- [ ] Write system prompts for each agent
- [ ] Implement contract read/write utilities
- [ ] Set up confidence thresholds
- [ ] Build operator review interface (CLI/web)
- [ ] Implement validation gates
- [ ] Add checkpoint/resume functionality
- [ ] Create pattern library structure
- [ ] Test with first hero section design
- [ ] Measure metrics (intervention rate, success rate)
- [ ] Iterate based on operator feedback

## References

- Claude Code Documentation: https://docs.anthropic.com/en/docs/claude-code
- Claude Agent SDK: https://docs.anthropic.com/en/docs/build-with-claude/agent-sdk
- Component Build System: `/mh-ai-compoent-build.md`
- Data Type Implementation: `/umbracoDocumentation/DATATYPE_IMPLEMENTATION_GUIDE.md`
