# What to do after the practice run
1. Choose ONE track with your team: intent, sentiment, or limited semantic parsing. Tell the organisers your choice before large-scale annotation.
2. Confirm your primary language and an independent competent reviewer. Read TRACKS.md.
3. Open taxonomy.csv for intents/semantic actions, or sentiment_guidelines.md for sentiment. Read NATURAL_DATA.md.
4. Copy data/template.csv (or semantic_template.csv) to data/contribution.csv. Add 30 human-checked sample records; include every selected label.
5. Complete DATA_PLAN.md and source/permission details. Keep uncleared data private.
6. Have a reviewer check the sample. Agree label boundaries before scaling up.
7. Meet your track target: intent 250; sentiment 300; semantic 250 with at least 100 slot-bearing examples. Use the split minima in TRACKS.md. Independent review is required for every test example.
8. Run validate.py with --track YOUR_TRACK; fix errors. It cannot judge fluency or real consent.
9. Train and inspect development results. Freeze choices, then evaluate the test set once.
10. Inspect per_label_report.csv and test_predictions.csv, analyse up to five actual errors; report all if there are fewer, and complete the documentation.
11. Adapt the Streamlit app or a mobile UI. Show real model predictions and failure cases. No live action is necessary.
12. Commit and tag your own GitHub repo. Preserve the SHA and ZIP. Use the final NLP Hub repository process when it is announced.

## Example: sentiment track, own data
python validate.py --track sentiment --data data/contribution.csv
python train.py --track sentiment --data data/contribution.csv
python evaluate.py --track sentiment --data data/contribution.csv
python -m streamlit run app.py

For English teaching runs, add --practice and use the matching practice CSV from data/. Intent is the default if --track is omitted. A run needs no minimum F1 to be honestly reported.

