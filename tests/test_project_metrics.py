import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AggregateMetrics(unittest.TestCase):
    def test_expected_holdout(self):
        d=json.loads((ROOT/'results/model_feasibility.json').read_text())
        self.assertEqual(d['data']['test_rows'],22580)
        self.assertEqual(d['data']['test_events'],1015)
        self.assertAlmostEqual(d['metrics']['LightGBM preliminary']['average_precision'],0.1636889203355008)
        self.assertGreater(d['metrics']['LightGBM preliminary']['average_precision'],d['metrics']['Recent failure (90 days)']['average_precision'])
    def test_event_recall_denominator(self):
        d=json.loads((ROOT/'results/robustness_summary.json').read_text())['event_coverage']
        self.assertEqual(d['eligible_events_with_active_lookback'],643)
        self.assertEqual(d['model_top25_events_caught'],116)
        self.assertAlmostEqual(d['model_top25_event_recall_eligible'],116/643)
if __name__=='__main__':unittest.main()
