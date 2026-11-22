import unittest
import pandas as pd
from core.scheduling import rank_week,schedule_inspections,event_recall,break_even_success_rate

class TestScheduling(unittest.TestCase):
 def test_ties_are_stable(self):
  f=pd.DataFrame({'uwi':['B','A','C'],'relative_risk_score':[.8,.8,.6]})
  self.assertEqual(rank_week(f,capacity=2).uwi.tolist(),['A','B'])
 def test_cooldown_prevents_consecutive_selection(self):
  f=pd.DataFrame({'uwi':['A','B','A','B','A','B'],'week_end':pd.to_datetime(['2026-06-07']*2+['2026-06-14']*2+['2026-06-21']*2),'relative_risk_score':[.9,.8,.9,.8,.9,.8]})
  out=schedule_inspections(f,capacity=1,cooldown_weeks=1)
  self.assertEqual(out.uwi.tolist(),['A','B','A'])
  no=schedule_inspections(f,capacity=1)
  self.assertEqual(no.uwi.tolist(),['A','A','A'])
 def test_cannot_see_future(self):
  f=pd.DataFrame({'uwi':['A','B'],'week_end':pd.to_datetime(['2026-06-07','2026-06-14']),'relative_risk_score':[.2,.99]})
  o=schedule_inspections(f,capacity=1,through_date='2026-06-07')
  self.assertEqual(o.uwi.tolist(),['A'])
 def test_event_eligibility(self):
  d=pd.DataFrame({'uwi':['A','B'],'week_end':pd.to_datetime(['2026-06-07']*2)})
  f=pd.DataFrame({'uwi':['A','B','B'],'failure_start_date':['2026-06-13','2026-06-20','2026-06-02']})
  res=event_recall(d,d.iloc[:1],f)
  self.assertEqual((res['eligible_events'],res['caught_events']),(2,1))
 def test_break_even(self):
  self.assertEqual(break_even_success_rate(flagged_events_per_week=4,fraction_addressable=.5,volume_per_event_m3=10,value_cad_per_m3=100,inspections_per_week=20,cost_cad_per_inspection=50),.5)
 def test_bad_capacity(self):
  with self.assertRaises(ValueError): rank_week(pd.DataFrame({'uwi':['A'],'relative_risk_score':[.5]}),capacity=0)

if __name__=='__main__': unittest.main()
