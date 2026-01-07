"""
Component Contract Models

Pydantic models for the Component Contract schema.
The Component Contract is the central artifact that maintains context across all agents.
"""

from .component_contract import (
    ComponentContract,
    ComponentMetadata,
    ContentTypeDefinition,
    PropertyDefinition,
    DataTypeReference,
    VisualStructureDefinition,
    VisualRegion,
    FunctionalityDefinition,
    InteractionDefinition,
    DependenciesDefinition,
    ConverterRequirement,
    ValidationResults,
    ValidationGate,
    ConfidenceScore,
    # Enums
    GateStatus,
    ConverterType,
    InteractionType,
)

__all__ = [
    "ComponentContract",
    "ComponentMetadata",
    "ContentTypeDefinition",
    "PropertyDefinition",
    "DataTypeReference",
    "VisualStructureDefinition",
    "VisualRegion",
    "FunctionalityDefinition",
    "InteractionDefinition",
    "DependenciesDefinition",
    "ConverterRequirement",
    "ValidationResults",
    "ValidationGate",
    "ConfidenceScore",
    # Enums
    "GateStatus",
    "ConverterType",
    "InteractionType",
]
