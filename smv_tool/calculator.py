"""Core calculation engine for SMV, operation breakdown, and thread consumption."""

from dataclasses import dataclass

from .codebooks import THREAD_FACTORS, get_codebook

TMU_TO_MINUTES = 0.0006


@dataclass(slots=True)
class OperationInput:
    name: str
    standard: str
    code: str
    repeats: int = 1
    seam_length_cm: float = 0.0
    stitch_type: str = "301_lockstitch"
    allowance_pct: float = 0.0


@dataclass(slots=True)
class OperationResult:
    name: str
    standard: str
    code: str
    repeats: int
    base_tmu: int
    total_tmu: float
    smv_minutes: float
    thread_cm: float


@dataclass(slots=True)
class CalculationResult:
    operations: list[OperationResult]
    net_smv_minutes: float
    allowance_minutes: float
    final_smv_minutes: float
    total_thread_cm: float



def _thread_consumption_cm(seam_length_cm: float, stitch_type: str) -> float:
    if seam_length_cm <= 0:
        return 0.0
    if stitch_type not in THREAD_FACTORS:
        known = ", ".join(sorted(THREAD_FACTORS))
        raise ValueError(f"Unknown stitch type '{stitch_type}'. Known: {known}")
    return seam_length_cm * THREAD_FACTORS[stitch_type]



def calculate_smv(operations: list[OperationInput]) -> CalculationResult:
    op_results: list[OperationResult] = []
    net_smv = 0.0
    allowance = 0.0
    total_thread = 0.0

    for op in operations:
        codebook = get_codebook(op.standard)
        if op.code not in codebook:
            known = ", ".join(sorted(codebook))
            raise ValueError(f"Code '{op.code}' not found in {op.standard.upper()} codebook. Known: {known}")
        if op.repeats < 1:
            raise ValueError("Repeats must be >= 1")

        base_tmu = codebook[op.code]
        total_tmu = base_tmu * op.repeats
        op_smv = total_tmu * TMU_TO_MINUTES
        op_allowance = op_smv * (op.allowance_pct / 100)
        thread_cm = _thread_consumption_cm(op.seam_length_cm, op.stitch_type)

        net_smv += op_smv
        allowance += op_allowance
        total_thread += thread_cm

        op_results.append(
            OperationResult(
                name=op.name,
                standard=op.standard.upper(),
                code=op.code,
                repeats=op.repeats,
                base_tmu=base_tmu,
                total_tmu=total_tmu,
                smv_minutes=op_smv + op_allowance,
                thread_cm=thread_cm,
            )
        )

    return CalculationResult(
        operations=op_results,
        net_smv_minutes=net_smv,
        allowance_minutes=allowance,
        final_smv_minutes=net_smv + allowance,
        total_thread_cm=total_thread,
    )
