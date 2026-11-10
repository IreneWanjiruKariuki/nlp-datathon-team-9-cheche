"""Team 9 Cheche - Kiswahili sentiment demo (Track B). Adapted from Strathmore NLP Hub starter kit v2.0."""
import json
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

TRACK = 'sentiment'
ART = Path('artifacts') / TRACK
MODEL_PATH = ART / 'model.joblib'
CONTRIB_PATH = Path('data') / 'contribution.csv'
LABELS = ['positive', 'negative', 'neutral']

# One-line Kiswahili + English summary per label (Kiswahili wording to be checked by our fluent reviewer).
SUMMARY = {
    'positive': ('Maoni chanya: mwandishi ameridhika na huduma.', 'Positive opinion: the writer is satisfied with the service.'),
    'negative': ('Maoni hasi: mwandishi hajaridhika na huduma.', 'Negative opinion: the writer is dissatisfied with the service.'),
    'neutral': ('Kauli ya kawaida: taarifa isiyo na mtazamo wa wazi.', 'Neutral: a factual statement without a clear opinion.'),
}

# PLACEHOLDERS - replace with real rows from artifacts/sentiment/test_predictions.csv after the final test run.
EXAMPLES = {
    'correct': [
        {'text': '[test sentence 1]', 'gold': 'positive', 'predicted': 'positive', 'why': '[why the model got it right]'},
        {'text': '[test sentence 2]', 'gold': 'negative', 'predicted': 'negative', 'why': '[why the model got it right]'},
        {'text': '[test sentence 3]', 'gold': 'neutral', 'predicted': 'neutral', 'why': '[why the model got it right]'},
    ],
    'wrong': [
        {'text': '[test sentence 4]', 'gold': '[gold]', 'predicted': '[predicted]', 'why': '[likely cause, e.g. negation or unseen word]'},
        {'text': '[test sentence 5]', 'gold': '[gold]', 'predicted': '[predicted]', 'why': '[likely cause]'},
    ],
}

st.set_page_config(page_title='Team 9 Cheche - Kiswahili Sentiment', page_icon='💬')
st.title('Team 9 Cheche · Kiswahili · Track B Sentiment · Prototype')
st.info('This detects opinion polarity in feedback. It is not emotion or mental-state detection.')

if not MODEL_PATH.exists():
    st.error('No sentiment model found. Run train.py --track sentiment first; see NEXT_STEPS.md.')
    st.stop()
pack = joblib.load(MODEL_PATH)  # Only load model files you created and trust.
model = pack['model']
if pack.get('practice'):
    st.warning('PRACTICE MODEL: trained on the English teaching fixtures. Kiswahili input will not be handled well '
               'until we retrain on data/contribution.csv. Scores below are teaching results, not a benchmark.')
st.caption(f"Model language: {pack.get('language', 'unknown')}")

# --- Prediction ---
st.header('Try it')
text = st.text_area('Andika maoni kwa Kiswahili / Enter Kiswahili feedback',
                    placeholder='Mfano: Huduma ilikuwa nzuri sana.')
if st.button('Predict / Tabiri'):
    if not text.strip():
        st.info('Enter text first.')
    else:
        label = model.predict([text])[0]
        proba = model.predict_proba([text])[0]
        sw, en = SUMMARY.get(label, (label, label))
        st.subheader(f'Predicted label: {label}')
        st.write(f'**Kiswahili:** {sw}')
        st.write(f'**English:** {en}')
        st.write(f'Model probability (uncalibrated): {max(proba):.1%}')
        st.caption('Uncalibrated: this is not the chance the label is correct. '
                   'The model always picks one of the three labels, even for unrelated input.')

# --- Examples ---
st.header('Examples')
for kind, title in [('correct', 'Correct predictions (3)'), ('wrong', 'Wrong predictions (2)')]:
    st.subheader(title)
    for ex in EXAMPLES[kind]:
        st.markdown(f"> {ex['text']}  \nGold: **{ex['gold']}** · Predicted: **{ex['predicted']}**  \n_{ex['why']}_")

# --- Results ---
st.header('Results')


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else None


test = load_json(ART / 'test_metrics.json')
dev = load_json(ART / 'dev_metrics.json')
if test is None:
    st.info('No test_metrics.json yet. Run evaluate.py --track sentiment.')
else:
    m, base = test['model'], test['majority_baseline']
    if test.get('practice'):
        st.caption('Metrics come from the practice run (teaching data, not a benchmark).')
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Test accuracy', f"{m['accuracy']:.3f}")
    c2.metric('Test macro-F1', f"{m['macro_f1']:.3f}")
    c3.metric('Majority baseline macro-F1', f"{base['macro_f1']:.3f}")
    c4.metric('Dev macro-F1', f"{dev['model']['macro_f1']:.3f}" if dev else 'n/a')
    st.caption(f"Test examples: {test.get('test_size', 'n/a')}")

    order = m['label_order']
    st.subheader('Per-class F1 (test)')
    st.dataframe(pd.DataFrame(
        [{'label': l, 'precision': m['report'][l]['precision'], 'recall': m['report'][l]['recall'],
          'F1': m['report'][l]['f1-score'], 'support': int(m['report'][l]['support'])} for l in order]
    ).set_index('label').round(3))

    st.subheader('Confusion matrix (test)')
    st.dataframe(pd.DataFrame(m['confusion_matrix'],
                              index=[f'gold: {l}' for l in order], columns=[f'pred: {l}' for l in order]))

st.subheader('Dataset summary (data/contribution.csv)')
if CONTRIB_PATH.exists():
    df = pd.read_csv(CONTRIB_PATH)
    if df.empty:
        st.info('data/contribution.csv exists but has no rows yet.')
    else:
        counts = pd.crosstab(df['label'], df['split'], margins=True, margins_name='total')
        st.dataframe(counts)
        st.caption('Track B minimum: 300 rows; per label 60 train, 20 dev, 20 test.')
else:
    st.info('data/contribution.csv not found yet. Copy data/template.csv to data/contribution.csv and add our Kiswahili data.')
