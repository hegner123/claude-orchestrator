"""
Vision Agent

Analyzes design images to extract component structure, patterns, and design tokens.
Uses Claude's vision API to understand visual layouts and generate Component Contracts.
"""

import base64
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from anthropic import Anthropic
from PIL import Image
import io

from models import (
    ComponentContract,
    VisualStructureDefinition,
    VisualRegion,
    FunctionalityDefinition,
    InteractionDefinition,
    InteractionType,
)


class VisionAgent:
    """
    Vision Agent for design image analysis.

    Responsibilities:
    - Load and encode design images (desktop/mobile)
    - Extract semantic structure (regions, hierarchy)
    - Identify UI patterns (cards, buttons, forms, etc.)
    - Extract design tokens (colors, typography, spacing)
    - Generate initial Component Contract
    - Assign confidence scores to decisions
    - Match patterns against known component library
    """

    def __init__(self, client: Anthropic, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize Vision Agent.

        Args:
            client: Anthropic API client
            model: Claude model to use for vision analysis
        """
        self.client = client
        self.model = model
        self.known_patterns = self._load_known_patterns()

    def _load_known_patterns(self) -> Dict[str, Any]:
        """
        Load known component patterns for matching.

        Returns:
            Dictionary of known patterns with characteristics
        """
        return {
            "hero-section": {
                "characteristics": [
                    "full-width background image",
                    "centered text overlay",
                    "call-to-action button",
                    "large heading typography"
                ],
                "confidence_threshold": 0.85
            },
            "card-grid": {
                "characteristics": [
                    "repeating card pattern",
                    "grid layout",
                    "image + text + CTA structure",
                    "consistent spacing"
                ],
                "confidence_threshold": 0.80
            },
            "navigation": {
                "characteristics": [
                    "horizontal menu items",
                    "logo placement",
                    "sticky/fixed positioning",
                    "dropdown menus"
                ],
                "confidence_threshold": 0.90
            },
            "contact-form": {
                "characteristics": [
                    "form fields (input, textarea)",
                    "labels and placeholders",
                    "submit button",
                    "validation indicators"
                ],
                "confidence_threshold": 0.85
            },
            "footer": {
                "characteristics": [
                    "bottom placement",
                    "multi-column layout",
                    "links and contact info",
                    "social media icons"
                ],
                "confidence_threshold": 0.88
            }
        }

    def load_image(self, image_path: str) -> bytes:
        """
        Load image from file path.

        Args:
            image_path: Path to image file

        Returns:
            Image bytes

        Raises:
            FileNotFoundError: If image doesn't exist
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(path, 'rb') as f:
            return f.read()

    def encode_image(self, image_bytes: bytes) -> Tuple[str, str]:
        """
        Encode image to base64 and detect media type.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Tuple of (base64_string, media_type)
        """
        # Detect image format
        image = Image.open(io.BytesIO(image_bytes))
        format_lower = image.format.lower() if image.format else 'jpeg'

        media_type_map = {
            'jpeg': 'image/jpeg',
            'jpg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        media_type = media_type_map.get(format_lower, 'image/jpeg')

        # Encode to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        return base64_image, media_type

    def analyze_design(
        self,
        desktop_image_path: Optional[str] = None,
        mobile_image_path: Optional[str] = None,
        context: Optional[str] = None
    ) -> ComponentContract:
        """
        Analyze design images and generate Component Contract.

        Args:
            desktop_image_path: Path to desktop design image
            mobile_image_path: Path to mobile design image (optional)
            context: Additional context about the component (optional)

        Returns:
            ComponentContract with visual structure populated
        """
        if not desktop_image_path:
            raise ValueError("Desktop image path is required")

        print(f"\n🔍 Analyzing design image: {desktop_image_path}")

        # Load and encode desktop image
        desktop_bytes = self.load_image(desktop_image_path)
        desktop_b64, desktop_media = self.encode_image(desktop_bytes)

        # Load mobile image if provided
        mobile_b64 = None
        mobile_media = None
        if mobile_image_path:
            print(f"📱 Also analyzing mobile variant: {mobile_image_path}")
            mobile_bytes = self.load_image(mobile_image_path)
            mobile_b64, mobile_media = self.encode_image(mobile_bytes)

        # Build vision analysis prompt
        messages = self._build_vision_prompt(
            desktop_b64, desktop_media,
            mobile_b64, mobile_media,
            context
        )

        # Call Claude vision API
        print(f"🤖 Sending to Claude Vision API ({self.model})...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=messages
        )

        # Parse response
        analysis_text = response.content[0].text
        print(f"✅ Received analysis ({response.usage.input_tokens} in / {response.usage.output_tokens} out)")

        # Extract structured data from response
        contract = self._parse_vision_response(
            analysis_text,
            desktop_image_path,
            mobile_image_path
        )

        return contract

    def _build_vision_prompt(
        self,
        desktop_b64: str,
        desktop_media: str,
        mobile_b64: Optional[str],
        mobile_media: Optional[str],
        context: Optional[str]
    ) -> List[Dict[str, Any]]:
        """
        Build structured prompt for vision analysis.

        Args:
            desktop_b64: Base64 encoded desktop image
            desktop_media: Media type for desktop image
            mobile_b64: Base64 encoded mobile image (optional)
            mobile_media: Media type for mobile image (optional)
            context: Additional context

        Returns:
            List of message dictionaries for API
        """
        content = []

        # Add desktop image
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": desktop_media,
                "data": desktop_b64
            }
        })

        # Add mobile image if provided
        if mobile_b64:
            content.append({
                "type": "text",
                "text": "Here is the mobile variant:"
            })
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": mobile_media,
                    "data": mobile_b64
                }
            })

        # Add analysis instructions
        prompt = self._get_analysis_prompt(context)
        content.append({
            "type": "text",
            "text": prompt
        })

        return [{"role": "user", "content": content}]

    def _get_analysis_prompt(self, context: Optional[str]) -> str:
        """
        Generate detailed analysis prompt.

        Args:
            context: Additional context about the component

        Returns:
            Structured prompt for vision analysis
        """
        prompt = """Analyze this design image and extract component structure for a component build system.

Your task is to identify:

1. **Component Pattern**: What type of component is this? (hero section, card grid, navigation, form, footer, etc.)
   - Provide confidence score (0.0-1.0)
   - Explain reasoning

2. **Visual Structure**:
   - Layout type (single-column, two-column, grid, flex, etc.)
   - Regions/sections (name, semantic role, UI patterns present)
   - Visual hierarchy (z-index, layering)
   - Bounding boxes if identifiable (x, y, width, height in pixels)

3. **Design Tokens**:
   - Colors (hex values for backgrounds, text, accents)
   - Typography (font families, sizes, weights)
   - Spacing (padding, margins, gaps)
   - Border radius, shadows, other effects

4. **Interactions** (inferred from design):
   - Click targets (buttons, links)
   - Hover states visible
   - Interactive elements
   - Expected behaviors

5. **Responsive Breakpoints** (if mobile design provided):
   - Differences between desktop and mobile
   - Recommended breakpoints (mobile, tablet, desktop)

6. **Ambiguities** (low confidence decisions):
   - Any unclear functionality
   - Multiple valid interpretations
   - Areas needing operator clarification

7. **Content Fields** (data needed from CMS):
   - What text fields are needed? (heading, subheading, body, etc.)
   - What images/media are needed?
   - What links/CTAs are present?
   - What other data types? (dates, numbers, toggles, etc.)

"""

        if context:
            prompt += f"\n**Additional Context**: {context}\n"

        prompt += """
**Output Format**: Respond with a JSON object following this structure:

```json
{
  "pattern_match": {
    "pattern_name": "hero-section",
    "confidence": 0.95,
    "reasoning": "Strong match due to..."
  },
  "layout": {
    "type": "single-column",
    "regions": [
      {
        "name": "background",
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
    }
  },
  "design_tokens": {
    "colors": {
      "background": "#000000",
      "text": "#ffffff",
      "accent": "#0066cc"
    },
    "typography": {
      "heading_font": "Inter",
      "heading_size": "48px",
      "heading_weight": "700",
      "body_font": "Inter",
      "body_size": "18px"
    },
    "spacing": {
      "padding_y": "120px",
      "content_max_width": "1200px"
    }
  },
  "interactions": [
    {
      "type": "click",
      "trigger": "CTA button",
      "target": "button element",
      "behavior": "Navigate to page",
      "confidence": 0.85,
      "ambiguity": "Could be modal or navigation - needs clarification"
    }
  ],
  "content_fields": [
    {
      "field_name": "backgroundImage",
      "field_type": "media",
      "editor": "Umbraco.MediaPicker3",
      "mandatory": true,
      "description": "Full-width background image"
    },
    {
      "field_name": "heading",
      "field_type": "text",
      "editor": "Umbraco.TextBox",
      "mandatory": true,
      "description": "Main heading text"
    }
  ],
  "ambiguities": [
    {
      "decision": "CTA button behavior",
      "options": ["Navigate to page", "Open modal"],
      "confidence": 0.68,
      "reasoning": "Visual cues are ambiguous"
    }
  ]
}
```

Provide your analysis as a JSON object only. Do not include any text before or after the JSON.
"""

        return prompt

    def _parse_vision_response(
        self,
        response_text: str,
        desktop_path: str,
        mobile_path: Optional[str]
    ) -> ComponentContract:
        """
        Parse Claude's vision response and build Component Contract.

        Args:
            response_text: Raw response text from Claude
            desktop_path: Path to desktop image
            mobile_path: Path to mobile image

        Returns:
            ComponentContract with visual structure populated
        """
        # Extract JSON from response (handle markdown code blocks)
        json_text = response_text.strip()
        if json_text.startswith('```'):
            # Remove markdown code fence
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            if json_text.startswith('json'):
                json_text = json_text[4:].strip()

        try:
            analysis = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse JSON response: {e}")
            print(f"Raw response:\n{response_text[:500]}...")
            # Return minimal contract
            return ComponentContract()

        # Create Component Contract
        contract = ComponentContract()

        # Build Visual Structure
        layout_data = analysis.get('layout', {})
        regions_data = layout_data.get('regions', [])

        regions = []
        for region_data in regions_data:
            region = VisualRegion(
                name=region_data.get('name', 'unknown'),
                semantic_role=region_data.get('semantic_role', ''),
                bounding_box=region_data.get('bounding_box'),
                z_index=region_data.get('z_index', 0),
                ui_patterns=region_data.get('ui_patterns', [])
            )
            regions.append(region)

        contract.visual_structure = VisualStructureDefinition(
            layout_type=layout_data.get('type', 'unknown'),
            regions=regions,
            responsive_breakpoints=layout_data.get('responsive_breakpoints', {}),
            design_tokens=analysis.get('design_tokens', {}),
            desktop_image_path=desktop_path,
            mobile_image_path=mobile_path
        )

        # Add Functionality (interactions)
        interactions_data = analysis.get('interactions', [])
        interactions = []
        for interaction_data in interactions_data:
            interaction_type_str = interaction_data.get('type', 'click').upper()
            try:
                interaction_type = InteractionType[interaction_type_str]
            except KeyError:
                interaction_type = InteractionType.CLICK

            interaction = InteractionDefinition(
                type=interaction_type,
                trigger=interaction_data.get('trigger', ''),
                target=interaction_data.get('target', ''),
                behavior=interaction_data.get('behavior', '')
            )
            interactions.append(interaction)

        if interactions:
            contract.functionality = FunctionalityDefinition(
                interactions=interactions
            )

        # Add confidence scores
        pattern_match = analysis.get('pattern_match', {})
        if pattern_match:
            contract.add_confidence_score(
                decision=f"Identified as {pattern_match.get('pattern_name', 'unknown')} pattern",
                score=pattern_match.get('confidence', 1.0),
                reasoning=pattern_match.get('reasoning', 'Pattern analysis')
            )

        # Add ambiguities as low-confidence scores
        ambiguities = analysis.get('ambiguities', [])
        for ambiguity in ambiguities:
            contract.add_confidence_score(
                decision=ambiguity.get('decision', 'Unknown decision'),
                score=ambiguity.get('confidence', 0.5),
                reasoning=ambiguity.get('reasoning', 'Ambiguous from visual analysis')
            )

        # Store raw analysis for reference
        contract.artifacts['vision_analysis'] = json.dumps(analysis, indent=2)

        print(f"\n📊 Vision Analysis Complete:")
        print(f"   Pattern: {pattern_match.get('pattern_name', 'unknown')} ({pattern_match.get('confidence', 0):.2f})")
        print(f"   Regions: {len(regions)}")
        print(f"   Interactions: {len(interactions)}")
        print(f"   Confidence scores: {len(contract.confidence_scores)}")

        low_conf = contract.get_low_confidence_decisions()
        if low_conf:
            print(f"   ⚠️  Low confidence decisions: {len(low_conf)}")

        return contract

    def match_pattern(self, contract: ComponentContract) -> Tuple[str, float]:
        """
        Match component against known patterns.

        Args:
            contract: Component Contract with visual structure

        Returns:
            Tuple of (pattern_name, confidence_score)
        """
        if not contract.visual_structure:
            return ("unknown", 0.0)

        # Simple pattern matching based on UI patterns in regions
        all_patterns = []
        for region in contract.visual_structure.regions:
            all_patterns.extend(region.ui_patterns)

        # Check against known patterns
        best_match = "unknown"
        best_score = 0.0

        for pattern_name, pattern_data in self.known_patterns.items():
            characteristics = pattern_data['characteristics']
            matches = sum(1 for char in characteristics if any(char.lower() in p.lower() for p in all_patterns))
            score = matches / len(characteristics) if characteristics else 0.0

            if score > best_score:
                best_score = score
                best_match = pattern_name

        return (best_match, best_score)
