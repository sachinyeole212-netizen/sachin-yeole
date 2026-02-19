import unittest

from smv_calculator import OperationInput, calculate, estimate_thread_meters, get_code_tmu, tmu_to_minutes


class TestSmvCalculator(unittest.TestCase):
    def test_tmu_conversion(self):
        self.assertAlmostEqual(tmu_to_minutes(2000), 1.0)

    def test_get_code_tmu(self):
        self.assertEqual(get_code_tmu("GSD", "GSD_ALIGN_FABRIC"), 18)
        self.assertEqual(get_code_tmu("mtm", "MTM_STACK_OUTPUT"), 20)

    def test_thread_estimation(self):
        meters = estimate_thread_meters(seam_length_cm=25, spi=10, thread_mm_per_stitch=6.5, repetitions=2)
        self.assertGreater(meters, 1.2)
        self.assertLess(meters, 1.4)

    def test_calculate_summary(self):
        ops = [
            OperationInput(
                name="Shoulder Join",
                system="GSD",
                code="GSD_SEW_STRAIGHT_10CM",
                repetitions=2,
                seam_length_cm=25,
                spi=10,
                thread_mm_per_stitch=6.5,
            ),
            OperationInput(
                name="Side Seam",
                system="MTM",
                code="MTM_SEW_LOCKSTITCH_15CM",
                repetitions=2,
                seam_length_cm=60,
                spi=11,
                thread_mm_per_stitch=7.0,
            ),
        ]
        summary = calculate(ops, allowance_pct=15)
        self.assertAlmostEqual(summary.total_tmu, (78 * 2) + (96 * 2))
        self.assertGreater(summary.smv_with_allowance, summary.base_smv)
        self.assertGreater(summary.total_thread_meters, 0)


if __name__ == "__main__":
    unittest.main()
