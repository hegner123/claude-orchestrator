#!/usr/bin/env python3
"""
Vision Agent Test

Tests the Vision Agent with design images.

Usage:
    python3 test_vision_agent.py path/to/design.png

Requirements:
    - Design image (PNG, JPG, or WebP)
    - Anthropic API key in .env
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    from anthropic import Anthropic
    from agents import VisionAgent
    from models import ComponentContract
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the prototype/ directory")
    sys.exit(1)


def test_vision_agent_with_image(image_path: str):
    """
    Test vision agent with a real design image.

    Args:
        image_path: Path to design image
    """
    print("=" * 60)
    print("🧪 Vision Agent Test")
    print("=" * 60)

    # Check image exists
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        sys.exit(1)

    # Initialize API client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    # Initialize vision agent
    print("\n✅ Initializing Vision Agent...")
    vision_agent = VisionAgent(client=client)

    # Run analysis
    print(f"\n📸 Analyzing design: {image_path}")
    print("   This may take 10-30 seconds depending on image complexity...")

    try:
        contract = vision_agent.analyze_design(
            desktop_image_path=image_path,
            context="Test analysis for component build system"
        )

        print("\n" + "=" * 60)
        print("📊 Analysis Results")
        print("=" * 60)

        # Print visual structure
        if contract.visual_structure:
            vs = contract.visual_structure
            print(f"\n📐 Visual Structure:")
            print(f"   Layout Type: {vs.layout_type}")
            print(f"   Regions: {len(vs.regions)}")
            for region in vs.regions:
                print(f"      • {region.name}: {region.semantic_role}")
                if region.ui_patterns:
                    print(f"        Patterns: {', '.join(region.ui_patterns)}")

            if vs.design_tokens:
                print(f"\n🎨 Design Tokens:")
                tokens = vs.design_tokens
                if 'colors' in tokens:
                    print(f"   Colors: {len(tokens['colors'])} defined")
                if 'typography' in tokens:
                    print(f"   Typography: {len(tokens['typography'])} styles")
                if 'spacing' in tokens:
                    print(f"   Spacing: {len(tokens['spacing'])} values")

            if vs.responsive_breakpoints:
                print(f"\n📱 Responsive Breakpoints:")
                for name, width in vs.responsive_breakpoints.items():
                    print(f"   {name}: {width}px")

        # Print interactions
        if contract.functionality and contract.functionality.interactions:
            print(f"\n⚡ Interactions:")
            for interaction in contract.functionality.interactions:
                print(f"   • {interaction.type.value}: {interaction.trigger}")
                print(f"     → {interaction.behavior}")

        # Print confidence scores
        if contract.confidence_scores:
            print(f"\n📊 Confidence Scores:")
            for score in contract.confidence_scores:
                status = "⚠️ NEEDS REVIEW" if score.requires_review else "✅"
                print(f"   {status} {score.decision}: {score.score:.2f}")
                print(f"      Reasoning: {score.reasoning}")

        # Overall confidence
        print(f"\n📈 Overall Confidence: {contract.metadata.confidence_score:.2f}")

        # Check if operator review needed
        if contract.needs_operator_review():
            low_conf = contract.get_low_confidence_decisions()
            print(f"\n⚠️  Operator Review Required: {len(low_conf)} decisions")
        else:
            print(f"\n✅ No operator review needed (all confidence > 0.75)")

        # Save contract
        output_path = "./workflow/vision-test-contract.json"
        contract.to_json_file(output_path)
        print(f"\n💾 Contract saved to: {output_path}")

        # Print raw analysis if available
        if 'vision_analysis' in contract.artifacts:
            analysis_path = "./workflow/vision-analysis-raw.json"
            with open(analysis_path, 'w') as f:
                f.write(contract.artifacts['vision_analysis'])
            print(f"💾 Raw analysis saved to: {analysis_path}")

        print("\n✨ Vision agent test completed successfully!")

    except Exception as e:
        print(f"\n❌ Vision analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def print_usage():
    """Print usage instructions"""
    print("""
Vision Agent Test
=================

This script tests the Vision Agent with real design images.

Usage:
    python3 test_vision_agent.py <image_path>

Example:
    python3 test_vision_agent.py ../samples/hero-section.png

Requirements:
    - Design image file (PNG, JPG, WebP)
    - ANTHROPIC_API_KEY in .env file

The agent will:
    1. Load and encode the image
    2. Send to Claude Vision API for analysis
    3. Extract semantic structure, patterns, and design tokens
    4. Assign confidence scores
    5. Generate Component Contract
    6. Save results to workflow/

Expected output:
    - Component Contract JSON
    - Raw vision analysis JSON
    - Console summary of findings
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: No image path provided")
        print_usage()
        sys.exit(1)

    if sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        sys.exit(0)

    image_path = sys.argv[1]
    test_vision_agent_with_image(image_path)
