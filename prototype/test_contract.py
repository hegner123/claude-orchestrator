#!/usr/bin/env python3
"""
Test script for Component Contract
Demonstrates how agents would populate the contract during the workflow
"""

from models import (
    ComponentContract,
    ContentTypeDefinition,
    PropertyDefinition,
    DataTypeReference,
    VisualStructureDefinition,
    VisualRegion,
    FunctionalityDefinition,
    InteractionDefinition,
    InteractionType,
    DependenciesDefinition,
    ConverterRequirement,
    ConverterType,
    ValidationResults,
    ValidationGate,
    GateStatus,
)


def create_hero_section_contract():
    """
    Create a sample Component Contract for a Hero Section component.
    Simulates what the workflow would generate.
    """

    print("=" * 60)
    print("🧪 Component Contract Test - Hero Section")
    print("=" * 60)

    # Create new contract
    contract = ComponentContract()
    print(f"\n✅ Created contract: {contract.component_id}")

    # ============================================================
    # Phase 1: Vision Agent populates Visual Structure
    # ============================================================
    print("\n📸 Phase 1: Vision Agent Analysis")

    contract.visual_structure = VisualStructureDefinition(
        layout_type="single-column",
        regions=[
            VisualRegion(
                name="hero-background",
                semantic_role="Background image container",
                z_index=0,
                ui_patterns=["full-bleed-image", "gradient-overlay"]
            ),
            VisualRegion(
                name="hero-content",
                semantic_role="Text content overlay",
                z_index=1,
                ui_patterns=["centered-text", "call-to-action"]
            )
        ],
        responsive_breakpoints={
            "mobile": 768,
            "tablet": 1024,
            "desktop": 1440
        },
        design_tokens={
            "colors": {
                "overlay": "rgba(0, 0, 0, 0.4)",
                "text": "#ffffff",
                "cta-bg": "#0066cc"
            },
            "typography": {
                "heading-size": "48px",
                "heading-weight": "700",
                "body-size": "18px"
            },
            "spacing": {
                "padding-y": "120px",
                "content-max-width": "1200px"
            }
        },
        desktop_image_path="./samples/hero-desktop.jpg",
        mobile_image_path="./samples/hero-mobile.jpg"
    )

    # Vision agent adds confidence scores
    contract.add_confidence_score(
        decision="Identified as Hero Section pattern",
        score=0.95,
        reasoning="Strong match to existing hero patterns: centered text, full-bleed image, CTA button"
    )

    contract.add_confidence_score(
        decision="CTA button leads to modal vs navigation",
        score=0.68,
        reasoning="Visual cues ambiguous - could be modal or page navigation"
    )

    print(f"   ✅ Visual structure defined")
    print(f"   ✅ 2 regions identified")
    print(f"   ⚠️  1 low-confidence decision (needs operator review)")

    # ============================================================
    # Phase 2: Operator Review (for low-confidence decisions)
    # ============================================================
    print("\n👤 Phase 2: Operator Review")
    if contract.needs_operator_review():
        low_conf = contract.get_low_confidence_decisions()
        print(f"   Reviewing: {low_conf[0].decision}")
        print(f"   Operator decision: Navigation (not modal)")

        # Update confidence after operator clarification
        contract.confidence_scores[1].score = 1.0
        contract.confidence_scores[1].requires_review = False
        contract.mark_operator_approved(notes="Confirmed CTA navigates to /contact page")

        print(f"   ✅ Operator approved")
    else:
        print(f"   ⚠️  No low-confidence decisions found (this shouldn't happen)")

    # ============================================================
    # Phase 3a: Backend Agent populates Content Type
    # ============================================================
    print("\n🔧 Phase 3a: Backend Agent - Schema Definition")

    contract.content_type = ContentTypeDefinition(
        name="HeroSection",
        alias="heroSection",
        description="Full-width hero section with background image and centered content",
        icon="icon-picture",
        is_element=True,
        properties=[
            PropertyDefinition(
                alias="backgroundImage",
                label="Background Image",
                data_type=DataTypeReference(
                    name="Hero Section - Background Image - Media Picker",
                    udi="umb://data-type/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
                    editor_alias="Umbraco.MediaPicker3",
                    configuration={
                        "multiple": False,
                        "validationLimit": {"min": 1, "max": 1}
                    },
                    reuse_existing=False
                ),
                mandatory=True,
                sort_order=1,
                tab="Content"
            ),
            PropertyDefinition(
                alias="heading",
                label="Heading",
                data_type=DataTypeReference(
                    name="Textstring",
                    udi="umb://data-type/0cc0eba1996042c9bf9b60e150b429ae",
                    editor_alias="Umbraco.TextBox",
                    reuse_existing=True
                ),
                mandatory=True,
                sort_order=2,
                tab="Content"
            ),
            PropertyDefinition(
                alias="subheading",
                label="Subheading",
                data_type=DataTypeReference(
                    name="Textarea",
                    udi="umb://data-type/c6bac0dd4ab945b18e55e4e07ddee98f",
                    editor_alias="Umbraco.TextArea",
                    reuse_existing=True
                ),
                mandatory=False,
                sort_order=3,
                tab="Content"
            ),
            PropertyDefinition(
                alias="ctaButtonText",
                label="CTA Button Text",
                data_type=DataTypeReference(
                    name="Textstring",
                    udi="umb://data-type/0cc0eba1996042c9bf9b60e150b429ae",
                    editor_alias="Umbraco.TextBox",
                    reuse_existing=True
                ),
                mandatory=True,
                sort_order=4,
                tab="Content"
            ),
            PropertyDefinition(
                alias="ctaButtonLink",
                label="CTA Button Link",
                data_type=DataTypeReference(
                    name="Content Picker",
                    udi="umb://data-type/fd1e0da556434a8a82d5e1cb5f7e4e9a",
                    editor_alias="Umbraco.ContentPicker",
                    reuse_existing=True
                ),
                mandatory=True,
                sort_order=5,
                tab="Content"
            )
        ]
    )

    print(f"   ✅ Document type 'HeroSection' defined")
    print(f"   ✅ 5 properties configured")
    print(f"   ✅ 1 new data type, 4 reused")

    # ============================================================
    # Phase 3b: Backend Agent determines Converter requirements
    # ============================================================
    print("\n🔄 Phase 3b: Backend Agent - Converter Analysis")

    contract.dependencies = DependenciesDefinition(
        converters=[
            ConverterRequirement(
                property_alias="backgroundImage",
                editor_alias="Umbraco.MediaPicker3",
                converter_type=ConverterType.CUSTOM_GENERIC,
                converter_class="MediaApiSafeConverter",
                project="Seed.Core",
                needs_custom_implementation=False
            ),
            ConverterRequirement(
                property_alias="heading",
                editor_alias="Umbraco.TextBox",
                converter_type=ConverterType.AUTOMATIC,
                needs_custom_implementation=False
            ),
            ConverterRequirement(
                property_alias="subheading",
                editor_alias="Umbraco.TextArea",
                converter_type=ConverterType.AUTOMATIC,
                needs_custom_implementation=False
            ),
            ConverterRequirement(
                property_alias="ctaButtonText",
                editor_alias="Umbraco.TextBox",
                converter_type=ConverterType.AUTOMATIC,
                needs_custom_implementation=False
            ),
            ConverterRequirement(
                property_alias="ctaButtonLink",
                editor_alias="Umbraco.ContentPicker",
                converter_type=ConverterType.CUSTOM_GENERIC,
                converter_class="PublishedContentApiSafeConverter",
                project="Seed.Core",
                needs_custom_implementation=False
            )
        ]
    )

    print(f"   ✅ 5 converter requirements analyzed")
    print(f"   ✅ 3 automatic (60%), 2 custom (40%)")
    print(f"   ✅ All converters exist in Seed.Core")

    # ============================================================
    # Phase 3c: Add Functionality (interactions)
    # ============================================================
    print("\n⚡ Phase 3c: Functionality Agent")

    contract.functionality = FunctionalityDefinition(
        interactions=[
            InteractionDefinition(
                type=InteractionType.CLICK,
                trigger="CTA button click",
                target="ctaButtonLink",
                behavior="Navigate to linked page"
            ),
            InteractionDefinition(
                type=InteractionType.HOVER,
                trigger="CTA button hover",
                target="button element",
                behavior="Darken background color, scale 1.05"
            )
        ],
        accessibility_requirements=[
            "ARIA label on CTA button",
            "Alt text on background image",
            "Sufficient color contrast (4.5:1)",
            "Keyboard navigation support"
        ],
        performance_considerations=[
            "Lazy load background image",
            "Use responsive images (srcset)",
            "Optimize image sizes for mobile"
        ]
    )

    print(f"   ✅ 2 interactions defined")
    print(f"   ✅ 4 accessibility requirements")
    print(f"   ✅ 3 performance considerations")

    # ============================================================
    # Phase 4: Validation Gates
    # ============================================================
    print("\n✅ Phase 4: Validation Gates")

    contract.validation_results = ValidationResults()

    # Gate 1: Structural
    contract.validation_results.gate_1_structural = ValidationGate(
        gate_name="Gate 1: Structural",
        status=GateStatus.PASSED,
        score=1.0,
        errors=[],
        warnings=[],
        details={
            "typescript_compiled": True,
            "component_renders": True,
            "all_fields_mapped": True
        }
    )
    print(f"   ✅ Gate 1 (Structural): PASSED")

    # Gate 2: Layout
    contract.validation_results.gate_2_layout = ValidationGate(
        gate_name="Gate 2: Layout",
        status=GateStatus.PASSED,
        score=0.87,
        errors=[],
        warnings=["Mobile padding slightly different from design"],
        details={
            "screenshot_similarity": 0.87,
            "responsive_breakpoints_ok": True
        }
    )
    print(f"   ✅ Gate 2 (Layout): PASSED (87% similarity)")

    # Gate 3: Visual
    contract.validation_results.gate_3_visual = ValidationGate(
        gate_name="Gate 3: Visual",
        status=GateStatus.PASSED,
        score=0.91,
        errors=[],
        warnings=[],
        details={
            "screenshot_similarity": 0.91,
            "iterations": 2,
            "color_accuracy": 0.95,
            "typography_match": 0.88
        }
    )
    contract.validation_results.iteration_count = 2
    print(f"   ✅ Gate 3 (Visual): PASSED (91% similarity, 2 iterations)")

    # Gate 4: Functional
    contract.validation_results.gate_4_functional = ValidationGate(
        gate_name="Gate 4: Functional",
        status=GateStatus.PASSED,
        score=1.0,
        errors=[],
        warnings=[],
        details={
            "interactions_work": True,
            "accessibility_score": 100,
            "keyboard_nav": True
        }
    )
    print(f"   ✅ Gate 4 (Functional): PASSED")

    contract.validation_results.update_all_gates_status()
    print(f"\n   🎉 All validation gates passed!")

    # ============================================================
    # Phase 5: Delivery - Track artifacts
    # ============================================================
    print("\n📦 Phase 5: Delivery - Generated Artifacts")

    contract.artifacts = {
        "uda_data_type": "src/UmbracoProject/umbraco/Deploy/Revision/data-type__hero-section-bg-image.uda",
        "uda_document_type": "src/UmbracoProject/umbraco/Deploy/Revision/document-type__hero-section.uda",
        "typescript_type": "src/Seed.Web/lib/umbraco/types/heroSection.type.ts",
        "react_component": "src/Seed.Web/common/components/HeroSection.tsx",
        "styles": "src/Seed.Web/common/components/HeroSection.module.scss"
    }

    for artifact_type, path in contract.artifacts.items():
        print(f"   ✅ {artifact_type}: {path}")

    # ============================================================
    # Save contract
    # ============================================================
    print("\n💾 Saving Component Contract")

    output_path = "./workflow/hero-section-contract.json"
    contract.to_json_file(output_path)
    print(f"   ✅ Saved to: {output_path}")

    # ============================================================
    # Summary
    # ============================================================
    print("\n" + "=" * 60)
    print("📊 Component Contract Summary")
    print("=" * 60)
    print(f"Component ID: {contract.component_id}")
    print(f"Version: {contract.version}")
    print(f"Overall Confidence: {contract.metadata.confidence_score:.2f}")
    print(f"Operator Approved: {'✅' if contract.metadata.operator_approved else '❌'}")
    print(f"Content Type: {contract.content_type.name}")
    print(f"Properties: {len(contract.content_type.properties)}")
    print(f"Converters: {len(contract.dependencies.converters)}")
    print(f"Interactions: {len(contract.functionality.interactions)}")
    print(f"Validation Gates: {'✅ All Passed' if contract.validation_results.all_gates_passed else '❌ Failed'}")
    print(f"Artifacts Generated: {len(contract.artifacts)}")
    print(f"Operator Intervention: 1 decision")
    print("=" * 60)

    return contract


if __name__ == "__main__":
    contract = create_hero_section_contract()
    print("\n✨ Test completed successfully!")
