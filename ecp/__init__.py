"""Compatibility shim — `ecp` was renamed to `cxrp`.

Importing from ``ecp`` still works during the transition window, but
emits a ``DeprecationWarning``. Update imports to ``cxrp.*``.

The shim re-exports from ``cxrp`` and intentionally does not duplicate
any model definitions.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "The `ecp` package has been renamed to `cxrp`. Update imports to "
    "`from cxrp.contracts import ...` etc. The `ecp` shim will be "
    "removed in a future release.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["contracts", "validation", "vocabulary"]
