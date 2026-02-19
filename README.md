# SMV + GSD/MTM Calculator

A lightweight Python tool to calculate:

- **SMV (Standard Minute Value)**
- **Operation breakdown** by GSD and MTM code
- **Thread consumption** from seam length and stitch type

## What it does

The tool maps each operation code to a TMU value, converts TMU to minutes, applies optional allowance %, and totals everything into a production-ready summary.

Formula used:

- `SMV minutes = TMU × 0.0006`
- `Final SMV = Net SMV + Allowance`
- `Thread consumption (cm) = seam_length_cm × stitch_factor`

## Quick start

```bash
python -m pip install -e .
smv-tool data/sample_operations.json --csv report.csv
```

## Input format

Provide a JSON file like this:

```json
{
  "operations": [
    {
      "name": "Join shoulder seam",
      "standard": "GSD",
      "code": "G04_GUIDE_SEAM_10CM",
      "repeats": 6,
      "seam_length_cm": 30,
      "stitch_type": "516_safety",
      "allowance_pct": 12
    }
  ]
}
```

### Operation fields

- `name`: operation name for reporting
- `standard`: `GSD` or `MTM`
- `code`: method code from built-in codebook
- `repeats`: how many times operation repeats
- `seam_length_cm`: seam length for thread calculation (optional)
- `stitch_type`: stitch type for thread factor (optional)
- `allowance_pct`: operation allowance % (optional)

## Built-in stitch factors

- `301_lockstitch`: 2.5
- `401_chainstitch`: 3.2
- `504_overlock`: 5.5
- `516_safety`: 6.0
- `602_coverstitch`: 4.0

## Running tests

```bash
python -m pytest
```
