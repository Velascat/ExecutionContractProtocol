from enum import Enum


class ArtifactKind(str, Enum):
    """Canonical artifact-kind vocabulary for ExecutionResult payloads.

    Artifact.kind on the wire is an open string — consumers may register
    their own kinds. These values are the well-known canonical kinds CxRP
    guarantees universal meaning for.
    """

    INPUT = "input"
    OUTPUT = "output"
    LOG = "log"
    DIAGNOSTIC = "diagnostic"
