"""Reference TMU values for common GSD and MTM motions.

TMU conversion:
1 TMU = 0.0006 minutes = 0.036 seconds.
"""

GSD_TMU = {
    "G01_GET_PART": 18,
    "G02_ALIGN_PLY": 26,
    "G03_START_STITCH": 20,
    "G04_GUIDE_SEAM_10CM": 80,
    "G05_BACK_TACK": 24,
    "G06_TRIM_THREAD": 16,
    "G07_STACK_OUTPUT": 22,
    "G08_LABEL_ATTACH": 60,
    "G09_REPOSITION": 28,
    "G10_INSPECTION": 35,
}

MTM_TMU = {
    "M01_REACH_SHORT": 10,
    "M02_GRASP": 8,
    "M03_MOVE_LIGHT_20CM": 16,
    "M04_POSITION_PRECISE": 22,
    "M05_RELEASE": 4,
    "M06_EYE_FOCUS": 6,
    "M07_MACHINE_PEDAL": 12,
    "M08_FOLD_PART": 30,
    "M09_ROTATE_PART": 18,
    "M10_CHECK_QUALITY": 28,
}

THREAD_FACTORS = {
    "301_lockstitch": 2.5,
    "401_chainstitch": 3.2,
    "504_overlock": 5.5,
    "516_safety": 6.0,
    "602_coverstitch": 4.0,
}


def get_codebook(standard: str) -> dict[str, int]:
    normalized = standard.lower().strip()
    if normalized == "gsd":
        return GSD_TMU
    if normalized == "mtm":
        return MTM_TMU
    raise ValueError("Unknown standard. Use 'GSD' or 'MTM'.")
