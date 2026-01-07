"""
Component Contract Schema

Central data model for AI-powered component generation workflow.
Maintains context across all agents (Vision, Backend, TypeScript, Style).

Based on the architecture defined in mh-ai-compoent-build.md
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator
import json
import uuid


# ============================================================
# Enums
# ============================================================

class GateStatus(str, Enum):
    """Validation gate status"""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ConverterType(str, Enum):
    """Type of converter required"""
    AUTOMATIC = "automatic"  # 80% - passthrough
    CUSTOM_GENERIC = "custom_generic"  # Seed.Core
    CUSTOM_PROJECT = "custom_project"  # Seed.Backoffice.Extensions


class InteractionType(str, Enum):
    """Types of UI interactions"""
    CLICK = "click"
    HOVER = "hover"
    FOCUS = "focus"
    SCROLL = "scroll"
    DRAG = "drag"
    KEYBOARD = "keyboard"
    SUBMIT = "submit"
    MODAL = "modal"


# ============================================================
# Confidence Scoring
# ============================================================

class ConfidenceScore(BaseModel):
    """
    Confidence score for a decision.
    Scores < 0.75 trigger operator review.
    """
    decision: str = Field(..., description="What decision was made")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence 0.0-1.0")
    reasoning: str = Field(..., description="Why this score was assigned")
    requires_review: bool = Field(default=False, description="If score < 0.75")

    @field_validator('requires_review', mode='before')
    @classmethod
    def check_review_threshold(cls, v, info):
        """Auto-set requires_review based on score"""
        score = info.data.get('score', 1.0)
        return score < 0.75


# ============================================================
# Metadata
# ============================================================

class ComponentMetadata(BaseModel):
    """Component contract metadata"""
    created: datetime = Field(default_factory=datetime.utcnow)
    last_modified: datetime = Field(default_factory=datetime.utcnow)
    operator_approved: bool = Field(default=False)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    agent_version: str = Field(default="0.1.0", description="Agent system version")
    notes: Optional[str] = Field(default=None, description="Operator notes")


# ============================================================
# Backend Schema (Content Type Definition)
# ============================================================

class DataTypeReference(BaseModel):
    """Reference to a Data Type (UDA file)"""
    name: str = Field(..., description="Data type name (e.g., 'Headline - Image - Media Picker')")
    udi: str = Field(..., description="UDI format: umb://data-type/{uuid-no-dashes}")
    editor_alias: str = Field(..., description="Property editor (e.g., 'Umbraco.MediaPicker3')")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Editor config")
    reuse_existing: bool = Field(default=False, description="If true, use existing data type")

    @field_validator('udi')
    @classmethod
    def validate_udi_format(cls, v):
        """Ensure UDI follows Umbraco format"""
        if not v.startswith('umb://data-type/'):
            raise ValueError("UDI must start with 'umb://data-type/'")
        return v


class PropertyDefinition(BaseModel):
    """Property definition for a document type"""
    alias: str = Field(..., description="Property alias (camelCase)")
    label: str = Field(..., description="Human-readable label")
    description: Optional[str] = Field(default=None)
    data_type: DataTypeReference = Field(..., description="Data type reference")
    mandatory: bool = Field(default=False)
    validation_regex: Optional[str] = Field(default=None)
    sort_order: int = Field(default=0)
    tab: Optional[str] = Field(default="Content", description="Tab name in backoffice")
    confidence: Optional[ConfidenceScore] = Field(default=None)


class ContentTypeDefinition(BaseModel):
    """
    Backend schema definition.
    Represents the Umbraco document type structure.
    """
    name: str = Field(..., description="Document type name (PascalCase)")
    alias: str = Field(..., description="Document type alias (camelCase)")
    description: Optional[str] = Field(default=None)
    icon: str = Field(default="icon-document", description="Backoffice icon")
    allow_at_root: bool = Field(default=False)
    is_element: bool = Field(default=False, description="Block element vs document type")
    properties: List[PropertyDefinition] = Field(default_factory=list)
    compositions: List[str] = Field(default_factory=list, description="Inherited compositions")
    allowed_child_types: List[str] = Field(default_factory=list)


# ============================================================
# Visual Structure
# ============================================================

class VisualRegion(BaseModel):
    """Visual region/section identified in design"""
    name: str = Field(..., description="Region name (e.g., 'header', 'hero', 'footer')")
    semantic_role: str = Field(..., description="Semantic purpose")
    bounding_box: Optional[Dict[str, int]] = Field(
        default=None,
        description="Coordinates {x, y, width, height}"
    )
    z_index: int = Field(default=0, description="Stacking order")
    contains_regions: List[str] = Field(default_factory=list, description="Nested region names")
    ui_patterns: List[str] = Field(
        default_factory=list,
        description="Detected patterns (e.g., 'card', 'button', 'form')"
    )


class VisualStructureDefinition(BaseModel):
    """
    Visual structure extracted from design images.
    Layout, regions, hierarchy.
    """
    regions: List[VisualRegion] = Field(default_factory=list)
    layout_type: str = Field(..., description="E.g., 'single-column', 'two-column', 'grid'")
    responsive_breakpoints: Dict[str, int] = Field(
        default_factory=dict,
        description="Breakpoints {mobile: 768, tablet: 1024, desktop: 1440}"
    )
    design_tokens: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted colors, fonts, spacing, etc."
    )
    desktop_image_path: Optional[str] = Field(default=None)
    mobile_image_path: Optional[str] = Field(default=None)


# ============================================================
# Functionality / Interactions
# ============================================================

class InteractionDefinition(BaseModel):
    """UI interaction definition"""
    type: InteractionType = Field(..., description="Interaction type")
    trigger: str = Field(..., description="What triggers it (e.g., 'button click')")
    target: str = Field(..., description="What it affects")
    behavior: str = Field(..., description="What happens")
    confidence: Optional[ConfidenceScore] = Field(default=None)


class FunctionalityDefinition(BaseModel):
    """
    Derived functionality from visual analysis.
    Interactions, behaviors, state management needs.
    """
    interactions: List[InteractionDefinition] = Field(default_factory=list)
    state_requirements: List[str] = Field(
        default_factory=list,
        description="State needed (e.g., 'isOpen', 'currentSlide')"
    )
    accessibility_requirements: List[str] = Field(
        default_factory=list,
        description="ARIA labels, keyboard nav, etc."
    )
    performance_considerations: List[str] = Field(
        default_factory=list,
        description="Image lazy loading, code splitting, etc."
    )


# ============================================================
# Dependencies
# ============================================================

class ConverterRequirement(BaseModel):
    """Converter requirement for a property"""
    property_alias: str = Field(..., description="Property needing converter")
    editor_alias: str = Field(..., description="Editor type")
    converter_type: ConverterType = Field(..., description="Type of converter")
    converter_class: Optional[str] = Field(
        default=None,
        description="Specific converter class if known"
    )
    project: Optional[str] = Field(
        default=None,
        description="Seed.Core or Seed.Backoffice.Extensions"
    )
    needs_custom_implementation: bool = Field(
        default=False,
        description="If true, custom converter must be written"
    )


class DependenciesDefinition(BaseModel):
    """
    Dependencies for component generation.
    Converters, child types, external packages.
    """
    converters: List[ConverterRequirement] = Field(default_factory=list)
    child_content_types: List[str] = Field(
        default_factory=list,
        description="Block list/grid element types"
    )
    npm_packages: List[str] = Field(
        default_factory=list,
        description="Additional npm dependencies"
    )
    compositions: List[str] = Field(
        default_factory=list,
        description="Umbraco compositions to inherit"
    )


# ============================================================
# Validation Results
# ============================================================

class ValidationGate(BaseModel):
    """Single validation gate result"""
    gate_name: str = Field(..., description="Gate 1-4 name")
    status: GateStatus = Field(default=GateStatus.PENDING)
    score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    passed_at: Optional[datetime] = Field(default=None)
    details: Dict[str, Any] = Field(default_factory=dict)


class ValidationResults(BaseModel):
    """
    Validation gate results.
    Tracks Gate 1-4 outcomes.
    """
    gate_1_structural: Optional[ValidationGate] = Field(
        default=None,
        description="TypeScript compiles, component renders, fields mapped"
    )
    gate_2_layout: Optional[ValidationGate] = Field(
        default=None,
        description="Screenshot similarity > 70%, responsive breakpoints"
    )
    gate_3_visual: Optional[ValidationGate] = Field(
        default=None,
        description="Screenshot similarity > 85%, iterative refinement"
    )
    gate_4_functional: Optional[ValidationGate] = Field(
        default=None,
        description="Interactions work, accessibility passes"
    )
    iteration_count: int = Field(default=0, description="Number of refinement iterations")
    all_gates_passed: bool = Field(default=False)

    def update_all_gates_status(self):
        """Check if all gates passed"""
        gates = [
            self.gate_1_structural,
            self.gate_2_layout,
            self.gate_3_visual,
            self.gate_4_functional
        ]
        self.all_gates_passed = all(
            gate and gate.status == GateStatus.PASSED
            for gate in gates
        )


# ============================================================
# Component Contract (Main Model)
# ============================================================

class ComponentContract(BaseModel):
    """
    Component Contract - Central artifact for multi-agent workflow.

    Single source of truth for all agents (Vision, Backend, TypeScript, Style).
    Maintains context across agent executions and validation gates.

    Version: 1.0.0
    """
    version: str = Field(default="1.0.0", description="Schema version (semver)")
    component_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique component identifier"
    )
    metadata: ComponentMetadata = Field(default_factory=ComponentMetadata)

    # Core definitions
    content_type: Optional[ContentTypeDefinition] = Field(
        default=None,
        description="Backend schema (document type)"
    )
    visual_structure: Optional[VisualStructureDefinition] = Field(
        default=None,
        description="Layout and regions from design"
    )
    functionality: Optional[FunctionalityDefinition] = Field(
        default=None,
        description="Interactions and behaviors"
    )
    dependencies: Optional[DependenciesDefinition] = Field(
        default=None,
        description="Converters, child types, packages"
    )
    validation_results: Optional[ValidationResults] = Field(
        default=None,
        description="Validation gate outcomes"
    )

    # Confidence tracking
    confidence_scores: List[ConfidenceScore] = Field(
        default_factory=list,
        description="All confidence scores from agents"
    )

    # Generated artifacts (file paths)
    artifacts: Dict[str, str] = Field(
        default_factory=dict,
        description="Generated files {type: path}"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "version": "1.0.0",
                "component_id": "550e8400-e29b-41d4-a716-446655440000",
                "metadata": {
                    "created": "2026-01-07T12:00:00Z",
                    "operator_approved": False,
                    "confidence_score": 0.92
                },
                "content_type": {
                    "name": "HeroSection",
                    "alias": "heroSection",
                    "properties": []
                }
            }
        }

    def to_json_file(self, file_path: str) -> None:
        """Save contract to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.model_dump(mode='json'), f, indent=2, default=str)

    @classmethod
    def from_json_file(cls, file_path: str) -> 'ComponentContract':
        """Load contract from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)

    def add_confidence_score(self, decision: str, score: float, reasoning: str) -> None:
        """Add a confidence score for tracking"""
        confidence = ConfidenceScore(
            decision=decision,
            score=score,
            reasoning=reasoning
        )
        self.confidence_scores.append(confidence)

        # Update overall metadata confidence (weighted average)
        if self.confidence_scores:
            avg_score = sum(c.score for c in self.confidence_scores) / len(self.confidence_scores)
            self.metadata.confidence_score = avg_score

    def needs_operator_review(self) -> bool:
        """Check if any decisions require operator review"""
        return any(score.requires_review for score in self.confidence_scores)

    def get_low_confidence_decisions(self) -> List[ConfidenceScore]:
        """Get all decisions that need review (< 0.75)"""
        return [score for score in self.confidence_scores if score.requires_review]

    def update_timestamp(self) -> None:
        """Update last_modified timestamp"""
        self.metadata.last_modified = datetime.utcnow()

    def mark_operator_approved(self, notes: Optional[str] = None) -> None:
        """Mark as approved by operator"""
        self.metadata.operator_approved = True
        if notes:
            self.metadata.notes = notes
        self.update_timestamp()
