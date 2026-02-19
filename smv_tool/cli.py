"""CLI entrypoint for SMV and thread calculator."""

import argparse
import csv
import json
from pathlib import Path

from .calculator import OperationInput, calculate_smv


TABLE_HEADERS = [
    "Operation",
    "Std",
    "Code",
    "Repeats",
    "Total TMU",
    "SMV min (incl allowance)",
    "Thread cm",
]



def _load_operations(path: Path) -> list[OperationInput]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)

    operations = [OperationInput(**row) for row in payload["operations"]]
    return operations



def _print_breakdown(result) -> None:
    rows = []
    for op in result.operations:
        rows.append(
            [
                op.name,
                op.standard,
                op.code,
                str(op.repeats),
                f"{op.total_tmu:.0f}",
                f"{op.smv_minutes:.4f}",
                f"{op.thread_cm:.2f}",
            ]
        )

    widths = [len(h) for h in TABLE_HEADERS]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(TABLE_HEADERS))
    sep = "-+-".join("-" * widths[i] for i in range(len(widths)))

    print(line)
    print(sep)
    for row in rows:
        print(" | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))

    print("\nTotals")
    print(f"- Net SMV (minutes): {result.net_smv_minutes:.4f}")
    print(f"- Allowance (minutes): {result.allowance_minutes:.4f}")
    print(f"- Final SMV (minutes): {result.final_smv_minutes:.4f}")
    print(f"- Total thread (cm): {result.total_thread_cm:.2f}")



def _export_csv(result, output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(TABLE_HEADERS)
        for op in result.operations:
            writer.writerow(
                [
                    op.name,
                    op.standard,
                    op.code,
                    op.repeats,
                    f"{op.total_tmu:.0f}",
                    f"{op.smv_minutes:.4f}",
                    f"{op.thread_cm:.2f}",
                ]
            )
        writer.writerow([])
        writer.writerow(["Net SMV (minutes)", f"{result.net_smv_minutes:.4f}"])
        writer.writerow(["Allowance (minutes)", f"{result.allowance_minutes:.4f}"])
        writer.writerow(["Final SMV (minutes)", f"{result.final_smv_minutes:.4f}"])
        writer.writerow(["Total thread (cm)", f"{result.total_thread_cm:.2f}"])



def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate SMV, operation breakdown, and thread consumption from GSD/MTM operations."
    )
    parser.add_argument("input", type=Path, help="Path to JSON input file")
    parser.add_argument("--csv", type=Path, help="Optional path to export operation breakdown CSV")
    args = parser.parse_args()

    operations = _load_operations(args.input)
    result = calculate_smv(operations)
    _print_breakdown(result)

    if args.csv:
        _export_csv(result, args.csv)
        print(f"\nExported CSV report to: {args.csv}")


if __name__ == "__main__":
    main()
