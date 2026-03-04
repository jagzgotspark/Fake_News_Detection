from google_verify import google_search, extract_evidence, verify_claim

import streamlit as st
import re
import pandas as pd
import joblib
import nltk
from explain import generate_explanation, impact_analysis, plausibility_check

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Fake News Detection", layout="centered")
st.title("📰 AI-Based Fake News Detection System")
st.write("Detect fake news using AI and verify claims using trusted sources.")

# ---------- NLTK SETUP ----------
@st.cache_resource
def load_nltk():
    nltk.download("punkt")
    nltk.download("stopwords")

load_nltk()

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# ---------- TEXT CLEANING ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z ]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---------- USER INPUT ----------
user_input = st.text_area("Enter News Title or Content")

# ---------- BUTTON ----------
if st.button("Detect"):

    if user_input.strip() == "":
        st.warning("Please enter some news text.")
    else:
        cleaned = clean_text(user_input)
        X = vectorizer.transform([cleaned])

        prediction = model.predict(X)[0]
        confidence = model.predict_proba(X).max() * 100

        # Conservative decision for low confidence
        if confidence < 60:
            final_label = "Fake News"
        else:
            final_label = "Real News" if prediction == 1 else "Fake News"


        # ---------- ML RESULT ----------
        if final_label == "Real News":
            st.success(f"✅ Real News ({confidence:.2f}% confidence)")
        else:
            st.error(f"❌ Fake News ({confidence:.2f}% confidence)")

        # ---------- CLAIM PLAUSIBILITY CHECK ----------

        st.subheader("🔍 Claim Plausibility Analysis")

        plausibility = plausibility_check(user_input)

        for p in plausibility:
            st.write(f"• {p}")

       # ---------- AI FACT CHECK ANALYSIS ----------
        analysis = generate_explanation(user_input, final_label)

        st.subheader("🧠 AI Fact-Check Analysis")

        for point in analysis["analysis"]:
            st.write(f"• {point}")

        st.subheader("📊 Overall Assessment")
        st.info(analysis["summary"])


        #---------- IMPACT ANALYSIS ----------
        st.subheader("🌍 Potential Impact of This News")

        impacts = impact_analysis(user_input)

        for impact in impacts:
            st.write(f"• {impact}")

        # ---------- UNCERTAINTY HANDLING ----------
        if confidence < 85 and confidence > 60:
            st.warning("⚠️ Low confidence prediction — verifying using trusted sources.")

            # ---------- GOOGLE VERIFICATION ----------
            from google_verify import google_search, extract_evidence, verify_claim

            search_query = "RBI interest rates unchanged inflation"
            search_data = google_search(search_query)

            evidence = extract_evidence(search_data)
            verdict = verify_claim(user_input, evidence)

            st.subheader("🔎 Web Verification Result")
            st.info(verdict)

            if evidence:
                st.subheader("🧾 Evidence from Trusted Sources")
                for e in evidence[:3]:
                    st.write(f"• **{e['title']}**")
                    st.write(e["link"])
            

        else:
            st.info("ℹ️ High confidence — web verification not required.")

# ---------- FOOTER ----------
st.markdown("---")
st.caption(
    "Note: This system uses AI-based language analysis. "
    "For low-confidence cases, it performs web-based verification using trusted news sources."
)

