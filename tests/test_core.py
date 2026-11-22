import unittest
from core.decision import scenario_weekly_gross_exposure,investigator_report,format_measure
from core.demo_data import generate_synthetic_demo

class CoreTests(unittest.TestCase):
    def test_scenario(self):
        s=scenario_weekly_gross_exposure(20,10,.4,.5,500,25,100)
        self.assertAlmostEqual(s['hypothetical_oil_m3'],40)
        self.assertAlmostEqual(s['hypothetical_net_cad'],17500)
    def test_invalid_fraction(self):
        with self.assertRaises(ValueError):
            scenario_weekly_gross_exposure(1,1,1.5,.1,1,1,1)
    def test_missing_values(self):
        self.assertEqual(format_measure(float('nan')),'not recorded')
    def test_evidence_is_cautious(self):
        text=investigator_report({'uwi':'DEMO-WELL-001','rpm_avg_2w':150},1)
        self.assertIn('not a failure diagnosis',text)
        self.assertIn('not recorded',text)
    def test_demo_reproducible(self):
        a=generate_synthetic_demo(8,10); b=generate_synthetic_demo(8,10)
        self.assertEqual(len(a),144)
        self.assertTrue(a.equals(b))
        self.assertTrue(a.uwi.str.startswith('DEMO').all())

if __name__=='__main__':unittest.main()
