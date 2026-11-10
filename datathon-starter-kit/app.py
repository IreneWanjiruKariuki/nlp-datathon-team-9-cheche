from pathlib import Path
import joblib
import streamlit as st
from core import FRIENDLY,extract
st.set_page_config(page_title='African-language NLP Demo',page_icon='🌍')
st.title('African-language NLP Demo')
track=st.selectbox('Task',['intent','sentiment','semantic'])
path=Path('artifacts')/track/'model.joblib'
if not path.exists():st.info('Train this task first; see NEXT_STEPS.md.');st.stop()
pack=joblib.load(path) # Only load model files you created and trust.
if pack['practice']:st.warning('PRACTICE MODE: constructed English teaching examples. Scores do not establish real-world quality.')
st.write('Language:',pack['language'])
text=st.text_area('Enter text in the model language')
if st.button('Predict'):
    if not text.strip():st.info('Enter text first.');st.stop()
    label=pack['model'].predict([text])[0]
    st.subheader(('The sentiment is: ' if track=='sentiment' else 'The intention of the user is: ')+FRIENDLY.get(label,label))
    proba=pack['model'].predict_proba([text])[0];st.write(f"Model probability (uncalibrated): {max(proba):.1%}")
    st.caption('This score is not a guarantee of correctness. The model chooses a known label even for unsupported input.')
    if track=='semantic':
        st.json({'intent':label,'slots':extract(text,pack['slot_memory'])})
        st.caption('Training-only surface-value matcher: unseen slot values may be missed; no date/time normalisation or real action is executed.')
    elif track=='intent':st.info('Simulated route only. No calendar, music, weather or other external action has been executed.')
    else:st.info('Sentence-level opinion label only; this is not emotion detection, sarcasm understanding or a diagnosis.')

