from google_verify import google_search, extract_evidence, verify_claim
from explain import generate_explanation, impact_analysis, plausibility_check

import streamlit as st
import re
import joblib
import nltk
import wikipedia
import requests

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Fake News Detection", layout="centered")

# 👇 ADD CSS HERE
st.markdown("""
<style>

/* Page background */
.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
}

/* Main container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 950px;
}

/* Headings */
h1 {
    text-align:center;
    font-weight:700;
}

h2, h3 {
    margin-top:10px;
}

/* Card container */
.card {
    background:#1e293b;
    padding:20px;
    border-radius:12px;
    border:1px solid #334155;
    margin-bottom:20px;
    box-shadow:0px 4px 20px rgba(0,0,0,0.3);
}

/* Text area */
textarea {
    background:#1e293b !important;
    color:white !important;
    border-radius:10px !important;
}

/* Buttons */
button[kind="secondary"] {
    border-radius:10px !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-image: linear-gradient(90deg,#3b82f6,#22c55e);
}

/* Metric card look */
[data-testid="metric-container"] {
    background:#1e293b;
    border-radius:10px;
    padding:10px;
    border:1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
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

# ---------- NEWS API ----------
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

def get_news_articles(query):

    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    data = response.json()

    articles = []

    if "articles" in data:
        for a in data["articles"][:5]:
            articles.append({
                "title": a["title"],
                "source": a["source"]["name"],
                "url": a["url"]
            })

    return articles

# ---------- USER INPUT ----------
user_input = st.text_area("Enter News Title or Content")


# ---------- DETECT BUTTON ----------
if st.button("Detect"):

    if user_input.strip() == "":
        st.warning("Please enter some news text.")

    else:

        # ---------- CLEAN TEXT ----------
        cleaned = clean_text(user_input)

        # ---------- VECTORIZE ----------
        X = vectorizer.transform([cleaned])

        # ---------- MODEL PREDICTION ----------
        prediction = model.predict(X)[0]
        confidence = model.predict_proba(X).max() * 100

        # ---------- FINAL LABEL ----------
        final_label = "Real News" if prediction == 1 else "Fake News"

        # ---------- RESULT ----------
        st.subheader("🧾 Prediction Result")

        if final_label == "Real News":
            st.success(f"✅ Real News ({confidence:.2f}% confidence)")
        else:
            st.error(f"❌ Fake News ({confidence:.2f}% confidence)")

        st.progress(int(confidence))


        # ---------- CLAIM PLAUSIBILITY ----------
        st.subheader("🔍 Claim Plausibility Analysis")

        plausibility = plausibility_check(user_input)

        for p in plausibility:
            st.write(f"• {p}")

        st.subheader("📚 Wikipedia Context")

        try:
            summary = wikipedia.summary(user_input, sentences=2)
            st.write(summary)
        except:
            st.write("No Wikipedia information found for this claim.")


        # ---------- AI FACT CHECK ANALYSIS ----------
        analysis = generate_explanation(user_input, final_label)

        st.subheader("🧠 AI Fact-Check Analysis")

        for point in analysis["analysis"]:
            st.write(f"• {point}")

        st.subheader("📊 Overall Assessment")
        st.info(analysis["summary"])


        # ---------- IMPACT ANALYSIS ----------
        st.subheader("🌍 Potential Impact of This News")

        impacts = impact_analysis(user_input)

        for impact in impacts:
            st.write(f"• {impact}")


        # ---------- WEB VERIFICATION ----------
        if 60 < confidence < 85:

            st.subheader("🔎 Web Verification Result")
            st.warning("Low confidence prediction — verifying using trusted sources.")

            search_query = user_input
            search_data = google_search(search_query)

            evidence = extract_evidence(search_data)
            verdict = verify_claim(user_input, evidence)

            st.info(verdict)

            if evidence:
                st.subheader("🧾 Evidence from Trusted Sources")

                for e in evidence[:3]:
                    st.write(f"• **{e['title']}**")
                    st.write(e["link"])

        else:
            st.info("ℹ️ High confidence — web verification not required.")

        # ---------- NEWS COVERAGE ----------
        st.subheader("📰 Related News Coverage")

        articles = get_news_articles(user_input)

        if articles:
            for article in articles:
                st.write(f"**{article['title']}**")
                st.write(f"Source: {article['source']}")
                st.write(article["url"])
        else:
            st.write("No major news coverage found for this claim.")

        # ---------- MISINFORMATION PREVENTION ----------
        st.markdown("---")
        st.subheader("🛑 Prevent the Spread of Misinformation")

        if final_label == "Fake News" and confidence > 80:
            st.error("🚨 Warning: This news is likely misinformation. Sharing it may spread false information.")

        if final_label == "Fake News":
            st.subheader("🤔 Think Before You Share")
            st.write(
                "Before sharing this information, consider verifying it with reliable sources. "
                "Spreading misinformation can cause public confusion and harm."
            )

        st.subheader("🔎 Verify Using Trusted Sources")
        st.write("• World Health Organization (WHO)")
        st.write("• Government Press Releases")
        st.write("• Reuters Fact Check")
        st.write("• BBC News")

        # ---------- RISK METER ----------
        st.subheader("⚠️ Misinformation Risk Level")

        risk_score = int(confidence)
        st.progress(risk_score)

        if risk_score > 80:
            st.error("High risk of misinformation spreading.")
        elif risk_score > 60:
            st.warning("Moderate misinformation risk.")
        else:
            st.success("Low misinformation risk.")


        # ---------- SPREAD SIMULATION ----------
        if final_label == "Fake News":

            st.subheader("📈 Potential Spread Simulation")
            st.write("Estimated Spread Pattern:")
            st.write("• 1 hour → ~500 shares")
            st.write("• 5 hours → ~10,000 shares")
            st.write("• 24 hours → ~100,000 views")


        # ---------- FACT CHECK SUMMARY ----------
        st.subheader("📋 Fact-Check Summary")

        st.info(
            "Our system suggests this claim may contain misinformation. "
            "Users are encouraged to verify information with trusted sources before sharing."
        )


# ---------- FOOTER ----------
st.markdown("---")
st.caption(
    "Note: This system uses AI-based language analysis. "
    "For low-confidence cases, it performs web-based verification using trusted news sources."
)

