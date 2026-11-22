"""GENERATED SYNTHETIC records for public demonstration; never sourced from wells.

Scores, labels and well histories here are fabricated solely to exercise UI.
They are not the reported historical-validation dataset and must not be used as evidence.
"""
import numpy as np
import pandas as pd


def generate_synthetic_demo(n_wells=110, seed=2026):
    rng=np.random.default_rng(seed)
    weeks=pd.date_range('2026-06-07',periods=18,freq='W-SUN')
    wells=[f'DEMO-WELL-{i:03d}' for i in range(1,n_wells+1)]
    per_well_base=rng.beta(1.6,7,n_wells)
    records=[]
    for k,week in enumerate(weeks):
        for i,well in enumerate(wells):
            disruption=rng.random()<0.06
            score=np.clip(per_well_base[i]+rng.normal(0,.065)+.18*disruption,.002,.95)
            oil_rate=max(0,rng.normal(11,3)-2.8*disruption)
            downtime=min(1,max(0,rng.beta(1.3,9)+.4*disruption))
            records.append({'uwi':well,'week_end':week,'relative_risk_score':score,
                'target_14d':int(rng.random()<score*.12),
                'down_fraction_2w':downtime,'downtime_hours_2w':downtime*168,
                'oil_daily_avg_2w':oil_rate,'lost_per_week_2w':max(0,oil_rate*downtime*7),
                'rpm_avg_2w':max(0,rng.normal(190,45)),'eff_avg_2w':rng.uniform(.4,.93),
                'torque_avg_2w':rng.uniform(100,900),'current_avg_2w':rng.uniform(4,15),
                'driver_1':rng.choice(['rpm_avg_2w','down_fraction_2w','watercut_2w']),
                'driver_2':rng.choice(['oil_daily_avg_2w','eff_avg_2w']),
                'driver_3':rng.choice(['torque_avg_2w','current_avg_2w'])})
    return pd.DataFrame.from_records(records)
