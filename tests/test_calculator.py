from smv_tool.calculator import OperationInput, calculate_smv


def test_calculate_smv_and_thread():
    operations = [
        OperationInput(
            name="Overlock side seam",
            standard="GSD",
            code="G04_GUIDE_SEAM_10CM",
            repeats=5,
            seam_length_cm=40,
            stitch_type="504_overlock",
            allowance_pct=10,
        ),
        OperationInput(
            name="Position part",
            standard="MTM",
            code="M04_POSITION_PRECISE",
            repeats=2,
            allowance_pct=5,
        ),
    ]

    result = calculate_smv(operations)

    # Net SMV = (80*5 + 22*2) * 0.0006 = 0.2664
    assert round(result.net_smv_minutes, 4) == 0.2664

    # Allowance = op1(10%) + op2(5%) => 0.0240 + 0.00132 = 0.02532
    assert round(result.allowance_minutes, 5) == 0.02532
    assert round(result.final_smv_minutes, 5) == 0.29172

    # Thread for op1 only = 40 * 5.5
    assert result.total_thread_cm == 220


def test_raises_for_unknown_code():
    operations = [
        OperationInput(name="Unknown", standard="GSD", code="BAD_CODE")
    ]

    try:
        calculate_smv(operations)
    except ValueError as exc:
        assert "not found" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown code")
