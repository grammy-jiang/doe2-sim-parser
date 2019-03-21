import os
from pathlib import Path

CWD = Path(os.getcwd())

if CWD.stem == "tests":
    SAMPLE_SIM = CWD / "sample" / "sample.sim"
    SAMPLE_SIM_BEPS = CWD / "sample" / "sample - BEPS.sim"
    SAMPLE_SIM_BEPU = CWD / "sample" / "sample - BEPU.sim"
    SAMPLE_SIM_ES_D = CWD / "sample" / "sample - ES-D.sim"
    SAMPLE_SIM_LV_M = CWD / "sample" / "sample - LV-M.sim"
    SAMPLE_SIM_PS_E = CWD / "sample" / "sample - PS-E.sim"
    SAMPLE_SIM_HOURLY_REPORT = CWD / "sample" / "01-baseline-000 - hourly report.sim"
else:
    SAMPLE_SIM = CWD / "tests" / "sample" / "sample.sim"
    SAMPLE_SIM_BEPS = CWD / "tests" / "sample" / "sample - BEPS.sim"
    SAMPLE_SIM_BEPU = CWD / "tests" / "sample" / "sample - BEPU.sim"
    SAMPLE_SIM_ES_D = CWD / "tests" / "sample" / "sample - ES-D.sim"
    SAMPLE_SIM_LV_M = CWD / "tests" / "sample" / "sample - LV-M.sim"
    SAMPLE_SIM_PS_E = CWD / "tests" / "sample" / "sample - PS-E.sim"
    SAMPLE_SIM_HOURLY_REPORT = CWD / "tests" / "sample" / "01-baseline-000 - hourly report.sim"
