#!/usr/bin/env python3
"""SMV and thread consumption calculator using GSD/MTM codes."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

TMU_PER_MINUTE = 2000.0

GSD_CODES: Dict[str, float] = {
    "GSD_PICK_PLACE_LIGHT": 24,
    "GSD_ALIGN_FABRIC": 18,
    "GSD_SEW_STRAIGHT_10CM": 78,
    "GSD_TURN_PANEL": 30,
    "GSD_TRIM_THREAD": 12,
}

MTM_CODES: Dict[str, float] = {
    "MTM_REACH_GRASP": 22,
    "MTM_POSITION_PART": 28,
    "MTM_SEW_LOCKSTITCH_15CM": 96,
    "MTM_UNDERTRIM": 14,
    "MTM_STACK_OUTPUT": 20,
}


@dataclass
class OperationInput:
    name: str
    system: str
    code: str
    repetitions: int = 1
    seam_length_cm: float | None = None
    spi: float | None = None
    thread_mm_per_stitch: float = 6.0


@dataclass
class OperationResult:
    name: str
    system: str
    code: str
    repetitions: int
    unit_tmu: float
    total_tmu: float
    base_minutes: float
    thread_meters: float


@dataclass
class CalculationSummary:
    operations: List[OperationResult]
    total_tmu: float
    base_smv: float
    allowance_pct: float
    smv_with_allowance: float
    total_thread_meters: float


def tmu_to_minutes(tmu: float) -> float:
    return tmu / TMU_PER_MINUTE


def get_code_tmu(system: str, code: str) -> float:
    system_upper = system.upper()
    if system_upper == "GSD":
        mapping = GSD_CODES
    elif system_upper == "MTM":
        mapping = MTM_CODES
    else:
        raise ValueError(f"Unsupported system '{system}'. Use GSD or MTM.")

    if code not in mapping:
        available = ", ".join(sorted(mapping.keys()))
        raise ValueError(f"Code '{code}' not found for {system_upper}. Available: {available}")

    return mapping[code]


def estimate_thread_meters(
    seam_length_cm: float | None,
    spi: float | None,
    thread_mm_per_stitch: float,
    repetitions: int,
) -> float:
    if seam_length_cm is None or spi is None:
        return 0.0

    seam_length_in = seam_length_cm / 2.54
    stitches = seam_length_in * spi
    thread_mm = stitches * thread_mm_per_stitch * repetitions
    return thread_mm / 1000.0


def calculate(
    operations: Iterable[OperationInput],
    allowance_pct: float = 0.0,
) -> CalculationSummary:
    op_results: List[OperationResult] = []
    total_tmu = 0.0
    total_thread = 0.0

    for op in operations:
        unit_tmu = get_code_tmu(op.system, op.code)
        total_op_tmu = unit_tmu * op.repetitions
        base_minutes = tmu_to_minutes(total_op_tmu)
        thread_m = estimate_thread_meters(
            seam_length_cm=op.seam_length_cm,
            spi=op.spi,
            thread_mm_per_stitch=op.thread_mm_per_stitch,
            repetitions=op.repetitions,
        )

        result = OperationResult(
            name=op.name,
            system=op.system.upper(),
            code=op.code,
            repetitions=op.repetitions,
            unit_tmu=unit_tmu,
            total_tmu=total_op_tmu,
            base_minutes=base_minutes,
            thread_meters=thread_m,
        )
        op_results.append(result)
        total_tmu += total_op_tmu
        total_thread += thread_m

    base_smv = tmu_to_minutes(total_tmu)
    smv_with_allowance = base_smv * (1 + allowance_pct / 100.0)

    return CalculationSummary(
        operations=op_results,
        total_tmu=total_tmu,
        base_smv=base_smv,
        allowance_pct=allowance_pct,
        smv_with_allowance=smv_with_allowance,
        total_thread_meters=total_thread,
    )


def load_operations(path: str) -> List[OperationInput]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    operations: List[OperationInput] = []
    for entry in raw:
        operations.append(OperationInput(**entry))
    return operations


def format_report(summary: CalculationSummary) -> str:
    lines = []
    lines.append("Operation Breakdown")
    lines.append("-" * 90)
    lines.append(
        f"{'Operation':20} {'Sys':4} {'Code':28} {'Rep':>4} {'TMU':>8} {'Min':>8} {'Thread(m)':>10}"
    )
    lines.append("-" * 90)

    for op in summary.operations:
        lines.append(
            f"{op.name[:20]:20} {op.system:4} {op.code[:28]:28} {op.repetitions:>4} "
            f"{op.total_tmu:>8.2f} {op.base_minutes:>8.4f} {op.thread_meters:>10.4f}"
        )

    lines.append("-" * 90)
    lines.append(f"Total TMU           : {summary.total_tmu:.2f}")
    lines.append(f"Base SMV (minutes)  : {summary.base_smv:.4f}")
    lines.append(f"Allowance (%)       : {summary.allowance_pct:.2f}")
    lines.append(f"Final SMV (minutes) : {summary.smv_with_allowance:.4f}")
    lines.append(f"Total Thread (m)    : {summary.total_thread_meters:.4f}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate SMV, operation breakdown, and thread consumption using GSD/MTM codes."
    )
    parser.add_argument("input", help="Path to operations JSON file")
    parser.add_argument(
        "--allowance",
        type=float,
        default=0.0,
        help="Allowance percentage to apply on base SMV",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    operations = load_operations(args.input)
    summary = calculate(operations, allowance_pct=args.allowance)
    print(format_report(summary))


if __name__ == "__main__":
    main()
