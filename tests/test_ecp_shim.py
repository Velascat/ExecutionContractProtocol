"""Tests for the temporary `ecp` → `cxrp` compatibility shim."""

from __future__ import annotations

import importlib
import warnings


def _reimport(*module_names: str) -> None:
    """Drop cached imports so the deprecation warning fires on next import."""
    import sys

    for name in module_names:
        sys.modules.pop(name, None)


def test_ecp_top_level_import_emits_deprecation_warning():
    _reimport("ecp", "ecp.contracts", "ecp.validation", "ecp.vocabulary")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        importlib.import_module("ecp")
    deprecations = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert deprecations, "importing `ecp` must emit a DeprecationWarning"
    assert "cxrp" in str(deprecations[0].message)


def test_ecp_contracts_reexports_cxrp_symbols():
    _reimport("ecp", "ecp.contracts")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from cxrp.contracts import LaneDecision as CxrpLaneDecision
        from ecp.contracts import (
            Artifact,
            ExecutionLimits,
            ExecutionRequest,
            ExecutionResult,
            LaneAlternative,
            LaneDecision,
            TaskProposal,
        )
    # The shim must not duplicate definitions — it imports from cxrp.
    assert LaneDecision is CxrpLaneDecision
    assert Artifact is not None
    assert ExecutionLimits is not None
    assert ExecutionRequest is not None
    assert ExecutionResult is not None
    assert LaneAlternative is not None
    assert TaskProposal is not None


def test_ecp_validation_json_schema_reexports_helpers():
    _reimport("ecp.validation.json_schema")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from cxrp.validation.json_schema import validate_contract as cxrp_validate
        from ecp.validation.json_schema import (
            SCHEMA_FILE_MAP,
            load_schema,
            validate_contract,
            validate_payload,
        )
    assert validate_contract is cxrp_validate
    assert "lane_decision" in SCHEMA_FILE_MAP
    assert load_schema is not None
    assert validate_payload is not None


def test_ecp_vocabulary_lane_reexports_lane_type():
    _reimport("ecp.vocabulary.lane")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from cxrp.vocabulary.lane import LaneType as CxrpLaneType
        from ecp.vocabulary.lane import LaneType
    assert LaneType is CxrpLaneType


def test_ecp_vocabulary_status_reexports_execution_status():
    _reimport("ecp.vocabulary.status")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from cxrp.vocabulary.status import ExecutionStatus as CxrpExecutionStatus
        from ecp.vocabulary.status import ExecutionStatus
    assert ExecutionStatus is CxrpExecutionStatus


def test_ecp_vocabulary_artifact_reexports_artifact_kind():
    _reimport("ecp.vocabulary.artifact")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from cxrp.vocabulary.artifact import ArtifactKind as CxrpArtifactKind
        from ecp.vocabulary.artifact import ArtifactKind
    assert ArtifactKind is CxrpArtifactKind


def test_ecp_lane_decision_construction_via_shim_runs_cxrp_validators():
    """Round-trip: construct LaneDecision via the shim, confirm cxrp's
    confidence-bounds check still fires."""
    _reimport("ecp.contracts")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from ecp.contracts import LaneDecision

    import pytest

    with pytest.raises(ValueError, match="confidence must be between 0.0 and 1.0"):
        LaneDecision(confidence=1.5)
