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
        self.contract = {}
        self.workflow_dir = Path("./workflow")
        self.workflow_dir.mkdir(exist_ok=True)

        print("✅ ComponentBuilderOrchestrator initialized")

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

    def print_status(self):
        """Print orchestrator status"""
        print("\n📋 Orchestrator Status:")
        print(f"   API Key: {'✅ Set' if self.api_key else '❌ Missing'}")
        print(f"   Workflow Directory: {self.workflow_dir.absolute()}")
        print(f"   Contract Status: {'📝 Active' if self.contract else '📭 Empty'}")


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

    if connection_ok:
        print("\n✨ Ready to build components!")
        print("\n💡 Next steps:")
        print("   1. Implement vision agent")
        print("   2. Add Component Contract management")
        print("   3. Implement backend/TypeScript/style agents")
        print("   4. Add validation gates")
    else:
        print("\n⚠️  Fix connection issues before proceeding")
        sys.exit(1)


if __name__ == "__main__":
    main()
