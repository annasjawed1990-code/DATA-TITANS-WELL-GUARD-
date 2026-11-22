# Mandatory final review — DATA TITANS

## Registered-team responsibilities

- [ ] Verify registered team membership and replace the README name placeholder.
- [ ] Each registered contributor reviews code, output, and AI-assisted claims.
- [ ] Run tests: `python -m unittest discover -s tests -v (expect 19 passing tests)`.
- [ ] On permitted local computer, run full **original Parquet** audit, training/replay, and private history enrichment.
- [ ] Check `aggregate_model_metrics.json` against displayed AP, ROC-AUC, event recall and sample sizes.
- [ ] Launch Streamlit and click each tab in private and synthetic modes.
- [ ] Review already browser-tested offline HTML (capacity 25/50, cooldown, as-of inspector charts, simulator sliders, synthetic CSV export); repeat locally for approval.
- [ ] Validate dates, units, data dictionary assumptions, source labels and missingness treatment.
- [ ] Check model disclosure: only **historical** relative ranking; not calibrated probability, causal prevention or production uplift.
- [ ] Audit public files and screenshots for prohibited raw competition records and real well identifiers.
- [ ] In a **clean public copy**, run `python scripts/04_publication_preflight.py`; inspect GitHub staging before publishing.
- [ ] Read/approve `AI_ASSISTANCE_DISCLOSURE.md`, `docs/REFERENCES.md`, `docs/MODEL_CARD.md`.
- [ ] Correct any AI-narrated video mispronunciations or timing; ideally substitute team voice and actual synthetic-app walkthrough.
- [ ] Confirm MP4 is approximately 5 minutes, readable and audible, and hosted via an accessible link.
- [ ] Confirm presentation deck contains no unsupported return-on-investment or causal claims.
- [ ] Create public GitHub repository and link the MP4, PDF/PPTX, source code and documentation.
- [ ] Submit final **public repository URL** to Discord `#submissions` before **Sunday Nov 22 at 12:00 PM Calgary time**.
- [ ] All competing team members attend the mandatory Sunday in-person event; rehearse 10-minute presentation + 3-minute Q&A.

## Verified by assistant in revised build
- [x] Reproduced model training using original private weekly intermediate features.
- [x] Continuous failure-recency comparator AP 0.1030, event coverage 75/643 at 25 slots.
- [x] Stable tie-break, 0/1/2-week cooldown and as-of UI fix.
- [x] Resampling by test week with appropriately qualified uncertainty.
- [x] Automated unit tests and real-browser synthetic demo checks.
- [x] Real synthetic UI click-through incorporated in narrated video draft.
- [ ] PyArrow original-Parquet end-to-end run on team machine (not possible here).
- [ ] Streamlit private UI launched and checked by registered team (not possible here).
- [ ] Final confirmed roster, public repository, published video link, final team-approved narration, submission to Discord.

## Evidence and reproduction checks
- [ ] Original Parquet training passes and `python scripts/06_verify_reproduction.py --out-dir outputs` reports PASS.
- [ ] Actual Streamlit runs and every tab/queue/plot renders on authorized Windows machine.
- [ ] Authorized teammate inspects `outputs/source_quality_gate.json` for ambiguous efficiency units, conflicting duplicates, incomplete costs.
- [ ] Public media is watched fully: 299.4 seconds, updated slides, no white flash, synthetic UI only.
- [ ] Explain the seven-day input delay result: 66 model events versus 75 for lagged recency at 25 slots.
- [ ] Confirm official roster, genuine individual contributions, and AI-credit wording; do not invent roles.
- [ ] Confirm accessible hosted video URL and public repository URL in README, plus actual Discord submission before the deadline.
