# Source verification and release checks

The competition Parquet files were used locally to regenerate the full model, the operating-only comparison, and the seven-day input-delay sensitivity. The release verifier compares the two published aggregate JSON files with regenerated outputs. Model dependencies are pinned for reproduction. The withheld sample contains 22,580 well-weeks and 643 distinct eligible events.

Use the README commands to repeat source verification. Private outputs contain restricted identifiers and must remain local. The synthetic Streamlit logic smoke and unit suite are independent of the raw data. The final release media uses AI narration with recorded synthetic app visuals.
