#!/usr/bin/env python3
"""
Component Builder Orchestrator - Prototype
Multi-agent workflow for generating Umbraco components from design images
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    from anthropic import Anthropic
    import anthropic
except ImportError:
    print("❌ Error: anthropic library not installed")
    print("Install with: pip install anthropic python-dotenv")
    sys.exit(1)

# Import Component Contract models
try:
    from models import ComponentContract
except ImportError:
    print("❌ Error: Component Contract models not found")
    print("Make sure models/component_contract.py exists")
    sys.exit(1)


class ComponentBuilderOrchestrator:
    """Orchestrates multi-agent workflow for component generation"""

    def __init__(self):
        """Initialize orchestrator and validate API connection"""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            print("❌ Error: ANTHROPIC_API_KEY not found in environment")
            print("\nSet it with:")
            print("  export ANTHROPIC_API_KEY='your-api-key'")
            print("  OR create a .env file with: ANTHROPIC_API_KEY=your-api-key")
            sys.exit(1)

        # Initialize Anthropic client
        self.client = Anthropic(api_key=self.api_key)

        # Workflow state
        self.workflow_dir = Path("./workflow")
        self.workflow_dir.mkdir(exist_ok=True)
        self.contract_path = self.workflow_dir / "component-contract.json"

        # Initialize or load Component Contract
        if self.contract_path.exists():
            self.contract = ComponentContract.from_json_file(str(self.contract_path))
            print("✅ ComponentBuilderOrchestrator initialized (loaded existing contract)")
        else:
            self.contract = ComponentContract()
            print("✅ ComponentBuilderOrchestrator initialized (new contract created)")

    def test_connection(self):
        """Test Anthropic API connection"""
        print("\n🔌 Testing Anthropic API connection...")

        try:
            # Make a simple API call to verify connection
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": "Reply with just 'Connection successful' if you can read this."
                }]
            )

            # Extract response text
            response_text = response.content[0].text

            print(f"✅ API Connection successful!")
            print(f"\n📊 Connection Details:")
            print(f"   Model: {response.model}")
            print(f"   Response ID: {response.id}")
            print(f"   Response: {response_text}")
            print(f"   Input tokens: {response.usage.input_tokens}")
            print(f"   Output tokens: {response.usage.output_tokens}")

            return True

        except anthropic.AuthenticationError:
            print("❌ Authentication failed - Invalid API key")
            return False
        except anthropic.APIConnectionError as e:
            print(f"❌ Connection failed - Network error: {e}")
            return False
        except anthropic.RateLimitError:
            print("❌ Rate limit exceeded - Too many requests")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

    def save_contract(self):
        """Save Component Contract to JSON file"""
        self.contract.update_timestamp()
        self.contract.to_json_file(str(self.contract_path))
        print(f"💾 Contract saved: {self.contract_path}")

    def load_contract(self):
        """Load Component Contract from JSON file"""
        if self.contract_path.exists():
            self.contract = ComponentContract.from_json_file(str(self.contract_path))
            print(f"📂 Contract loaded: {self.contract_path}")
            return True
        else:
            print(f"⚠️  No contract found at: {self.contract_path}")
            return False

    def create_new_contract(self):
        """Create a new Component Contract"""
        self.contract = ComponentContract()
        print("✨ New contract created")

    def print_status(self):
        """Print orchestrator status"""
        print("\n📋 Orchestrator Status:")
        print(f"   API Key: {'✅ Set' if self.api_key else '❌ Missing'}")
        print(f"   Workflow Directory: {self.workflow_dir.absolute()}")
        print(f"   Contract Path: {self.contract_path}")
        print(f"\n📄 Component Contract:")
        print(f"   Version: {self.contract.version}")
        print(f"   Component ID: {self.contract.component_id}")
        print(f"   Created: {self.contract.metadata.created.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Last Modified: {self.contract.metadata.last_modified.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Confidence Score: {self.contract.metadata.confidence_score:.2f}")
        print(f"   Operator Approved: {'✅ Yes' if self.contract.metadata.operator_approved else '⏸️  Pending'}")
        print(f"   Content Type: {'✅ Defined' if self.contract.content_type else '⏸️  Not defined'}")
        print(f"   Visual Structure: {'✅ Defined' if self.contract.visual_structure else '⏸️  Not defined'}")
        print(f"   Functionality: {'✅ Defined' if self.contract.functionality else '⏸️  Not defined'}")
        print(f"   Dependencies: {'✅ Defined' if self.contract.dependencies else '⏸️  Not defined'}")

        # Show confidence scores requiring review
        low_conf = self.contract.get_low_confidence_decisions()
        if low_conf:
            print(f"\n⚠️  Low Confidence Decisions ({len(low_conf)}):")
            for score in low_conf[:3]:  # Show first 3
                print(f"      • {score.decision} (score: {score.score:.2f})")
        else:
            print(f"\n✅ No low-confidence decisions")


def main():
    """Main entry point"""
    print("=" * 60)
    print("🤖 Component Builder Orchestrator - Prototype")
    print("=" * 60)

    # Initialize orchestrator
    orchestrator = ComponentBuilderOrchestrator()

    # Test connection
    connection_ok = orchestrator.test_connection()

    # Print status
    orchestrator.print_status()

    # Save initial contract
    orchestrator.save_contract()

    if connection_ok:
        print("\n✨ Ready to build components!")
        print("\n💡 Next steps:")
        print("   1. ✅ Component Contract schema - COMPLETE")
        print("   2. Implement vision agent (design image analysis)")
        print("   3. Implement backend agent (UDA generation)")
        print("   4. Implement TypeScript agent (type definitions)")
        print("   5. Implement style agent (CSS/SCSS generation)")
        print("   6. Add validation gates (4 quality checks)")
    else:
        print("\n⚠️  Fix connection issues before proceeding")
        sys.exit(1)


if __name__ == "__main__":
    main()
