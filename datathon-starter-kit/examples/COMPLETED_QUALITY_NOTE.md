# Completed teaching quality note
Corpus:kit v2.0 sentiment practice set;120 constructed examples.
Structural checks:run validate.py in practice mode. That mode deliberately skips final contribution/review thresholds.
Independent language review:no claim is made; P1/P2 are tutorial placeholders.
Excluded records: none in this authored fixture. For real work,log exclusions and reasons.
Semantic duplicate risk:practice uses repeated templates. Group IDs prevent same class/service families crossing splits, but templates still repeat. It is not a generalisation benchmark.
Metrics:run the commands in README; the actual outputs go to artifacts/sentiment/test_metrics.json and per_label_report.csv. Do not invent values or copy scores from another run.
Failure analysis example:if 'The help was not good' is predicted positive,check negation and label coverage; do not edit the held-out test label just to improve a score.
Real submission:record genuine disagreements, corrections, source exclusions and up to five actual errors (report all if there are fewer).

