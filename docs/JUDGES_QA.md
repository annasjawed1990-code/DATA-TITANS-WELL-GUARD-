# DATA TITANS — Finalist judges' questions and answers

**Q1: Why LightGBM?**  
The dataset mixes missing numerical measurements with non-linear operating signals; LightGBM can handle missing numerical features and complex interactions. We compare against simple recent-downtime and prior-failure baselines. More complex architectures are not justified unless they beat these under the same time-aware test.

**Q2: Did the model actually prevent any failures?**  
No. This was retrospective. We demonstrated higher ranking quality and identified eligible historical events ahead of their recorded start dates. Prevention or savings require a prospective trial.

**Q3: What is average precision (AP)?**  
A threshold-independent summary of the precision–recall relationship. Test base prevalence was 4.5%; the model achieved 16.4% AP while a stronger continuous failure-recency baseline achieved 10.3%. AP should not be called 'accuracy'.

**Q4: Why did you use a chronological split?**  
Because random splits permit information from later periods, including shifts in equipment or reporting regimes, to leak into model selection. Our validation and test periods were later than training and separated by at least a target-horizon gap.

**Q5: Does 0.805 ROC-AUC mean 80.5% accuracy?**  
No. ROC-AUC measures ranking discrimination over thresholds, not classification accuracy or probability calibration.

**Q6: What about missing failure records in 2021–2024?**  
We explicitly avoid training on those years as if they were failure-free. The observed 2025 logging shift remains a limitation even after restricting training to later records.

**Q7: Why are failures and maintenance jobs recorded on the same day?**  
That may reflect actual repair timing, documentation workflows, or target creation. We exclude future maintenance jobs from model features, but reporting-process confounding remains and should be investigated with the data provider.

**Q8: Do you include every well?**  
No. Scoring covers eligible producing well-week snapshots with enough observed data. Rankings must not be interpreted as fleet-wide or suitable for injection wells.

**Q9: Can you explain an alert?**  
We show model-feature attributions for the private replay and measured production evidence. Attributions describe the mathematical score, not a mechanical root cause; field experts still verify equipment diagnosis.

**Q10: How did you calculate financial impact?**  
Only with an explicit assumption-based sensitivity calculator. Real savings cannot be derived from the historical aggregate loss number; the calculator makes all assumed effectiveness, volume, price and cost values visible.

**Q11: What is innovative?**  
A capacity-constrained risk queue integrated with evidence checks, transparency about reporting bias and a financial sensitivity model rather than a black-box score. A local-LLM explanation is optional and flagged unverified.

**Q12: How would you deploy it?**  
Start with an access-controlled pilot, scheduled feature computation, source-record lineage, standardized operator notes, drift monitoring, and a shadow evaluation before production changes.

**Q13: Have team members verified all claims?**  
The coding assistant reproduced the model metrics using its intermediate data and ran unit tests. Registered team members must independently execute on raw Parquet, verify the private app, and approve the final slides before submission. Do not say 'yes' until they have.

**Q14: Why isn't Canary used?**  
Canary is optional for overall competition entry. We prioritized reproducibility and operational reasoning; there is no verified Canary integration in this version.

**Q15: Why does the no-repeat policy flag 142 events? Is that proven?**  
No. The 1-week cooldown was considered after inspecting the original holdout; its 142/643 result is a post-hoc sensitivity analysis, not an independent result. We would pre-register the scheduling rule and test on future weeks.

**Q16: How is the queue deterministic?**  
We sort by relative risk and resolve ties by the well identifier. A recency score replaces the mostly tied binary history flag. A cooldown only uses earlier scheduled selections, never hidden future event labels.

**Q17: What does the confidence interval mean?**  
750 resamples of 18 entire weeks gave an AP difference of 0.061 with a descriptive 95% range of 0.044–0.077. It does not account fully for repeated wells and is not prospective confidence.

**Q18: Have you verified the live source pipeline?**  
The model was reproduced from private intermediate weekly features and the synthetic web dashboard was browser-tested. A registered teammate must still run original Parquet with PyArrow and Streamlit on an authorized computer; we will not claim that check is completed until it is.
