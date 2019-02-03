import os
from pathlib import Path

CWD = Path(os.getcwd())

if CWD.stem == "tests":
    SAMPLE_SIM = CWD / "sample" / "sample.sim"
else:
    SAMPLE_SIM = CWD / "tests" / "sample" / "sample.sim"
