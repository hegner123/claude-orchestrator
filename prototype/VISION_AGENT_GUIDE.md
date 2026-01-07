# Vision Agent Guide

The Vision Agent analyzes design images to extract component structure, patterns, and design tokens using Claude's vision API.

## Features

✅ **Image Analysis**
- Load images from disk (PNG, JPG, WebP, GIF)
- Base64 encoding for API transmission
- Support for desktop and mobile variants

✅ **Semantic Structure Extraction**
- Identify visual regions (header, content, footer, etc.)
- Detect UI patterns (cards, buttons, forms, navbars)
- Extract visual hierarchy and layering

✅ **Design Token Extraction**
- Colors (backgrounds, text, accents)
- Typography (fonts, sizes, weights)
- Spacing (padding, margins, gaps)
- Effects (shadows, border radius)

✅ **Pattern Matching**
- Compare against known component patterns
- Confidence scoring for pattern matches
- Built-in patterns: hero-section, card-grid, navigation, contact-form, footer

✅ **Interaction Detection**
- Infer interactive elements (buttons, links)
- Identify hover states
- Detect expected behaviors

✅ **Confidence Scoring**
- Assign confidence (0.0-1.0) to each decision
- Flag low-confidence decisions (< 0.75) for operator review
- Track ambiguities and multiple interpretations

✅ **Component Contract Generation**
- Populate VisualStructureDefinition
- Create FunctionalityDefinition
- Store design tokens and breakpoints
- Ready for backend/TypeScript agents

---

## Usage

### Basic Usage

```python
from anthropic import Anthropic
from agents import VisionAgent

# Initialize
client = Anthropic(api_key="your-api-key")
vision_agent = VisionAgent(client=client)

# Analyze design
contract = vision_agent.analyze_design(
    desktop_image_path="./designs/hero-section.png"
)

# Check results
print(f"Layout: {contract.visual_structure.layout_type}")
print(f"Regions: {len(contract.visual_structure.regions)}")
print(f"Confidence: {contract.metadata.confidence_score:.2f}")

# Check if operator review needed
if contract.needs_operator_review():
    for decision in contract.get_low_confidence_decisions():
        print(f"Review: {decision.decision} ({decision.score:.2f})")
```

### With Mobile Variant

```python
contract = vision_agent.analyze_design(
    desktop_image_path="./designs/hero-desktop.png",
    mobile_image_path="./designs/hero-mobile.png",
    context="Hero section for homepage"
)
```

### Using the Orchestrator

```python
from orchestrator import ComponentBuilderOrchestrator

orchestrator = ComponentBuilderOrchestrator()
success = orchestrator.run_vision_analysis(
    desktop_image="./designs/component.png",
    context="Contact form with validation"
)
```

---

## Testing

### Quick Test

```bash
# Test with a single image
python3 test_vision_agent.py path/to/design.png
```

### Expected Output

```
🧪 Vision Agent Test
============================================================

✅ Initializing Vision Agent...

📸 Analyzing design: ./samples/hero-section.png
   This may take 10-30 seconds depending on image complexity...

🔍 Analyzing design image: ./samples/hero-section.png
🤖 Sending to Claude Vision API (claude-sonnet-4-5-20250929)...
✅ Received analysis (1542 in / 892 out)

📊 Vision Analysis Complete:
   Pattern: hero-section (0.95)
   Regions: 2
   Interactions: 2
   Confidence scores: 3

============================================================
📊 Analysis Results
============================================================

📐 Visual Structure:
   Layout Type: single-column
   Regions: 2
      • background: Background image container
        Patterns: full-bleed-image, gradient-overlay
      • content: Text content overlay
        Patterns: centered-text, call-to-action

🎨 Design Tokens:
   Colors: 3 defined
   Typography: 5 styles
   Spacing: 3 values

📱 Responsive Breakpoints:
   mobile: 768px
   tablet: 1024px
   desktop: 1440px

⚡ Interactions:
   • CLICK: CTA button click
     → Navigate to linked page
   • HOVER: CTA button hover
     → Darken background, scale 1.05

📊 Confidence Scores:
   ✅ Identified as hero-section pattern: 0.95
      Reasoning: Strong match to existing patterns...
   ⚠️ NEEDS REVIEW CTA button behavior: 0.68
      Reasoning: Visual cues ambiguous...

📈 Overall Confidence: 0.81

⚠️  Operator Review Required: 1 decisions

💾 Contract saved to: ./workflow/vision-test-contract.json
💾 Raw analysis saved to: ./workflow/vision-analysis-raw.json

✨ Vision agent test completed successfully!
```

---

## Vision Analysis Output Structure

The vision agent returns a `ComponentContract` with these populated fields:

### Visual Structure
```python
contract.visual_structure = {
    "layout_type": "single-column",  # or "two-column", "grid", etc.
    "regions": [
        {
            "name": "hero-background",
            "semantic_role": "Background image container",
            "z_index": 0,
            "bounding_box": {"x": 0, "y": 0, "width": 1440, "height": 600},
            "ui_patterns": ["full-bleed-image", "gradient-overlay"]
        }
    ],
    "responsive_breakpoints": {
        "mobile": 768,
        "tablet": 1024,
        "desktop": 1440
    },
    "design_tokens": {
        "colors": {...},
        "typography": {...},
        "spacing": {...}
    }
}
```

### Functionality
```python
contract.functionality = {
    "interactions": [
        {
            "type": InteractionType.CLICK,
            "trigger": "CTA button click",
            "target": "button element",
            "behavior": "Navigate to page"
        }
    ]
}
```

### Confidence Scores
```python
contract.confidence_scores = [
    {
        "decision": "Identified as hero-section pattern",
        "score": 0.95,
        "reasoning": "Strong match...",
        "requires_review": False
    },
    {
        "decision": "CTA button behavior",
        "score": 0.68,
        "reasoning": "Ambiguous visual cues",
        "requires_review": True  # < 0.75 threshold
    }
]
```

---

## Known Component Patterns

The vision agent has built-in knowledge of common patterns:

### Hero Section (threshold: 0.85)
- Full-width background image
- Centered text overlay
- Call-to-action button
- Large heading typography

### Card Grid (threshold: 0.80)
- Repeating card pattern
- Grid layout
- Image + text + CTA structure
- Consistent spacing

### Navigation (threshold: 0.90)
- Horizontal menu items
- Logo placement
- Sticky/fixed positioning
- Dropdown menus

### Contact Form (threshold: 0.85)
- Form fields (input, textarea)
- Labels and placeholders
- Submit button
- Validation indicators

### Footer (threshold: 0.88)
- Bottom placement
- Multi-column layout
- Links and contact info
- Social media icons

---

## Confidence Score Thresholds

**High Confidence (≥ 0.75):**
- Proceed automatically
- No operator review needed
- Agent decisions trusted

**Low Confidence (< 0.75):**
- Flag for operator review
- Present options to operator
- Require confirmation before proceeding

---

## Best Practices

### 1. **Provide Clear Images**
- Use high-resolution images (1440px+ for desktop)
- Include both desktop and mobile variants when possible
- Ensure text is readable in the image

### 2. **Add Context**
```python
contract = vision_agent.analyze_design(
    desktop_image_path="hero.png",
    context="Homepage hero section with video background and email signup form"
)
```

### 3. **Review Low-Confidence Decisions**
```python
if contract.needs_operator_review():
    for decision in contract.get_low_confidence_decisions():
        print(f"Please review: {decision.decision}")
        print(f"Reasoning: {decision.reasoning}")
        # Present options to operator
```

### 4. **Save Contracts Immediately**
```python
contract.to_json_file("./workflow/my-component-contract.json")
```

### 5. **Check Artifacts**
```python
# Raw JSON analysis from Claude
raw_analysis = contract.artifacts.get('vision_analysis')
if raw_analysis:
    import json
    analysis_data = json.loads(raw_analysis)
    # Access detailed analysis
```

---

## Limitations

### Current Limitations:
- ❌ Cannot analyze live websites (only static images)
- ❌ Cannot detect animations or video content
- ❌ May miss subtle color gradients
- ❌ Cannot determine exact font families without context
- ❌ Interaction detection is inference-based (not definitive)

### Mitigation:
- Provide additional context in the `context` parameter
- Review low-confidence decisions manually
- Supplement with design specifications when available
- Use mobile + desktop images for better responsive analysis

---

## Error Handling

### Common Errors:

**FileNotFoundError**
```python
# Error: Image not found
# Fix: Check image path is correct
vision_agent.load_image("./designs/hero.png")  # Must exist
```

**AuthenticationError**
```python
# Error: Invalid API key
# Fix: Check .env file has ANTHROPIC_API_KEY
```

**JSONDecodeError**
```python
# Error: Failed to parse Claude's response
# Fix: The agent handles this gracefully and returns minimal contract
# Check artifacts['vision_analysis'] for raw response
```

---

## Next Steps After Vision Analysis

Once vision analysis is complete:

1. **Operator Review** (if needed)
   - Review low-confidence decisions
   - Clarify ambiguities
   - Approve or correct agent decisions

2. **Backend Agent**
   - Generate UDA files based on visual structure
   - Create data types for content fields
   - Determine converter requirements

3. **TypeScript Agent**
   - Generate type definitions
   - Map properties to TypeScript types

4. **Style Agent**
   - Generate CSS/SCSS from design tokens
   - Create responsive styles

5. **Validation**
   - Run Gate 1: Structural validation
   - Run Gate 2: Layout similarity
   - Run Gate 3: Visual similarity
   - Run Gate 4: Functional validation

---

## Advanced Usage

### Custom Pattern Matching

```python
# Extend known patterns
vision_agent.known_patterns['custom-banner'] = {
    'characteristics': [
        'horizontal layout',
        'promotional message',
        'close button',
        'bright background'
    ],
    'confidence_threshold': 0.80
}

# Run analysis
contract = vision_agent.analyze_design('banner.png')

# Check pattern match
pattern, score = vision_agent.match_pattern(contract)
print(f"Matched: {pattern} ({score:.2f})")
```

### Batch Processing

```python
import glob

for image_path in glob.glob('./designs/*.png'):
    print(f"Processing {image_path}...")
    contract = vision_agent.analyze_design(image_path)

    output_name = Path(image_path).stem
    contract.to_json_file(f"./workflow/{output_name}-contract.json")
```

---

## API Token Usage

Vision analysis typically uses:
- **Input tokens:** 1000-2000 (depends on image size + prompt)
- **Output tokens:** 500-1500 (depends on complexity)
- **Total cost:** ~$0.02-0.05 per image (Sonnet 4.5 pricing)

---

## Troubleshooting

### Analysis returns empty regions
- **Cause:** Image is too simple or unclear
- **Fix:** Provide context parameter, use higher resolution image

### Low confidence scores across the board
- **Cause:** Unusual or novel component pattern
- **Fix:** Add detailed context, expect operator review

### Pattern matching always returns "unknown"
- **Cause:** Component doesn't match known patterns
- **Fix:** This is normal for custom components, backend agent will still work

### JSON parsing fails
- **Cause:** Claude returned non-JSON response
- **Fix:** Check artifacts['vision_analysis'] for raw response, may need to adjust prompt

---

## Files

```
prototype/
├── agents/
│   ├── __init__.py
│   └── vision_agent.py          # Vision Agent implementation
├── test_vision_agent.py          # Test script
├── VISION_AGENT_GUIDE.md         # This file
└── workflow/
    ├── vision-test-contract.json # Generated contracts
    └── vision-analysis-raw.json  # Raw Claude analysis
```

---

**Version:** 1.0.0
**Last Updated:** 2026-01-07
**Status:** ✅ Complete and tested
