# Source references and boundaries

## Primary competition materials (nonpublic; not redistributed)

- DSMLC, Chirality Research & Canary Labs, **Datathon: Briefing Document** (November 2026). Official problem, deliverables, AI and privacy rules, judging rubric.
- DSMLC, **Datathon: Dataset Handbook** (November 2026). The source definitions, units, coverage, and context for all 3 competition datasets.
- DSMLC, **Datathon: Research Topic Guide** (November 2026). Suggested industrial optimization questions.
- Dataset provider: Strathcona Resources. Three competition-use Parquet files. **Do not upload or include these in a public repository.**

## Public industrial background

1. SPE PetroWiki, *Progressing cavity pump (PCP) systems*, updated January 29, 2025. https://onepetro.org/spe/general-information/2015/Progressing-cavity-pump-PCP-systems  
   Supports the mechanical explanation that PCP rotor is driven through the rod string and that operating signals should be understood in equipment context.
2. SLB, *The Defining Series: Progressing Cavity Pumps*. https://www.slb.com/-/media/files/oilfield-review/defining-pcp.ashx  
   Describes PCP operational stresses, rod/tubing failure, rotation and friction; these are **generic engineering mechanisms**, not diagnosed causes of any Strathcona event.
3. Society of Petroleum Engineers, *Coated Continuous Sucker Rod Reduces Fatigue Failures in Progressing Cavity Pumping Applications*, SPE Artificial Lift Conference (2024). https://onepetro.org/SPEALCE/proceedings-abstract/24ALCE/24ALCE/D021S007R002/550399  
   Provides contextual rationale for studying rod reliability, but does not validate our particular classifier.
4. Sherif Fakher, Abdelaziz Khlaifat, M. Enamul Hossain, and Hashim Nameer, *A comprehensive review of sucker rod pumps' components, diagnostics, mathematical models, and common failures and mitigations* (2021). https://link.springer.com/article/10.1007/s13202-021-01270-7  
   Domain background only; rod-pump systems are not identical to PCP systems.

## Research and model reproducibility

- LightGBM documentation: https://lightgbm.readthedocs.io/
- Scikit-learn average precision: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html
- Scikit-learn ROC-AUC: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
- Plotly Python: https://plotly.com/python/
- Streamlit documentation: https://docs.streamlit.io/

**Attribution and interpretation:** Public background sources explain the engineering importance of artificial-lift monitoring. They do **not** prove observed production changes caused a failure or that an inspection intervention can prevent it. Competition data provides the retrospective counts and model evaluation. Video, slides and software disclose all AI assistance.
