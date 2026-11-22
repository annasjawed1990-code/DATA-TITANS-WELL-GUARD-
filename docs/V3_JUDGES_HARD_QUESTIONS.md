# Five tough questions we expect from judges — with evidence-based answers

**1. What happens if the input data arrive late?**
The full model achieved higher AP (0.1639 vs 0.1476) and better distinct-event recall at 50 and 100 slots. However, the operating-only alternative **does** lead narrowly at 25 slots, the headline business objective. We preserve the earlier full-model benchmark for consistency, disclose the trade-off, and propose evaluating both under a frozen prospective policy before selecting either for deployment. We cannot legitimately claim the full model wins every test.

**2. Why are there almost no failures recorded before 2025? Could this just be a maintenance-data artifact?**
Yes. Reporting coverage may have changed, and most failure records are temporally close to maintenance records. We restrict model training to later coverage and avoid future job data as features, but a field-owner label audit is needed. No claim of actual failure causation or operational readiness follows from this holdout alone.

**3. Is 0.164 average precision equal to 16.4% accuracy?**
No. Average precision summarizes precision–recall ranking across thresholds and depends on failure-label prevalence (4.5% in this holdout). ROC-AUC is 0.805, also not accuracy. The 25/week result is 116/643 **distinct eligible recorded events**, not 115 avoided breakdowns.

**4. How much money would the prototype save?**
We do not know. Actual maintenance final costs and validated intervention effectiveness are largely unavailable. The simulator makes all scenario assumptions editable and calculates break-even. A prospective controlled pilot is required for credible realized savings or avoided-downtime evidence.

**5. Did you run the original dataset and full app successfully?**
The original data were analyzed earlier, and the model was reproduced from verified private intermediate features. Source-to-PyArrow training and real Streamlit interaction have **not yet been independently completed in this execution environment**. Registered members must run the supplied private batch pipeline and launch all app tabs locally; until then, we describe a source-reproducible candidate rather than a fully validated deployed solution. The synthetic HTML interaction and code-level tab smoke test are separately documented.
