# SMV, Operation Breakdown, and Thread Consumption Calculator

This project provides a small software tool for garment engineering teams to calculate:

- **SMV** (Standard Minute Value)
- **Operation-wise time breakdown**
- **Thread consumption**

It supports both **GSD** and **MTM** code systems.

## Features

- Built-in GSD and MTM motion code libraries (editable in code)
- Operation-level calculation with repetitions
- Optional seam-based thread consumption estimation
- Adjustable allowance percent for personal/fatigue/delay
- CLI that reads operations from JSON and prints a detailed report

## How it works

1. Each operation references either a GSD or MTM code.
2. The code maps to a TMU value.
3. TMU is converted to minutes (`minutes = TMU / 2000`).
4. Allowances are applied to calculate final SMV.
5. If seam information is given, thread consumption is estimated from:
   - seam length
   - stitches per inch (SPI)
   - thread usage per stitch

## Usage

```bash
python smv_calculator.py sample_operations.json --allowance 15
```

## Input format

`sample_operations.json`:

```json
[
  {
    "name": "Shoulder Join",
    "system": "GSD",
    "code": "GSD_SEW_STRAIGHT_10CM",
    "repetitions": 2,
    "seam_length_cm": 25,
    "spi": 10,
    "thread_mm_per_stitch": 6.5
  },
  {
    "name": "Side Seam",
    "system": "MTM",
    "code": "MTM_SEW_LOCKSTITCH_15CM",
    "repetitions": 2,
    "seam_length_cm": 60,
    "spi": 11,
    "thread_mm_per_stitch": 7.0
  }
]
```

## Run tests

```bash
python -m unittest discover -s tests
```
