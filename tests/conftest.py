# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Velascat
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Venv guard — tests must run inside the repo's .venv, not a foreign environment.
_EXPECTED_VENV = Path(__file__).resolve().parents[1] / ".venv"
if not sys.prefix.startswith(str(_EXPECTED_VENV)):
    warnings.warn(
        f"Tests running outside expected venv.\n"
        f"  active  : {sys.prefix}\n"
        f"  expected: {_EXPECTED_VENV}\n"
        "Activate the repo venv: source .venv/bin/activate",
        stacklevel=1,
    )
