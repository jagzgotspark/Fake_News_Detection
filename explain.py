import re

KNOWN_PEOPLE = ["tom cruise","elon musk","barack obama","narendra modi"]

DEATH_KEYWORDS = ["died","dead","passed away","killed"]

def generate_explanation(text, prediction):

    text_lower = text.lower()
    analysis = []

    # ---------- claim detection ----------
    for person in KNOWN_PEOPLE:
        if person in text_lower:
            if any(word in text_lower for word in DEATH_KEYWORDS):

                analysis.append(
                    f"The claim states that {person.title()} has died."
                )

                analysis.append(
                    f"{person.title()} is a widely known public figure and there are no credible reports confirming this claim."
                )

                analysis.append(
                    "Celebrity death hoaxes are a common form of viral misinformation."
                )

    # ---------- lack of evidence ----------
    if not re.search(r"(report|according|official|news|confirmed)", text_lower):
        analysis.append(
            "The statement does not reference any credible source, official report, or news organization."
        )

    # ---------- logical structure ----------
    if len(text.split()) < 10:
        analysis.append(
            "The claim is very short and lacks contextual details such as date, location, or evidence."
        )

    if not analysis:
        analysis.append(
            "The text does not show strong indicators of misinformation but further verification is recommended."
        )

    # ---------- summary ----------
    if prediction == "Fake News":
        summary = (
            "Multiple credibility indicators suggest that the claim may be misinformation "
            "or an unverified statement."
        )
    else:
        summary = (
            "The claim does not strongly match patterns commonly seen in fake news."
        )

    return {
        "analysis": analysis,
        "summary": summary
    }

def impact_analysis(text):

    text = text.lower()
    impacts = []

    if "died" in text or "passed away" in text:
        impacts.append(
            "False reports about celebrity deaths can spread extremely quickly on social media and create unnecessary panic or emotional distress."
        )

        impacts.append(
            "Repeated celebrity death hoaxes reduce public trust in online news sources."
        )

    if "government" in text or "election" in text:
        impacts.append(
            "Political misinformation can influence voter perception and distort democratic discourse."
        )

    if "vaccine" in text or "virus" in text:
        impacts.append(
            "Health misinformation can discourage people from following verified medical advice."
        )

    if not impacts:
        impacts.append(
            "Even small pieces of misinformation can spread rapidly online and contribute to public confusion."
        )

    return impacts

def plausibility_check(text):

    text = text.lower()
    analysis = []

    # extraordinary events
    extraordinary_words = [
        "aliens","sky","planet","earth","meteor","superpower",
        "immortal","invisible","teleport","time travel"
    ]

    # prediction patterns
    prediction_words = ["will","tomorrow","next year","soon"]

    # check extraordinary claims
    if any(word in text for word in extraordinary_words):
        analysis.append(
            "The claim describes an unusual or extraordinary event that would normally require strong scientific or factual evidence."
        )

    # predictive statements
    if any(word in text for word in prediction_words):
        analysis.append(
            "The statement makes a prediction about the future without referencing evidence or credible forecasting sources."
        )

    # missing source
    if not any(word in text for word in ["report","according","research","study","official"]):
        analysis.append(
            "No credible source or supporting evidence is mentioned in the statement."
        )

    # short claims
    if len(text.split()) < 7:
        analysis.append(
            "The claim is very brief and lacks contextual details such as location, date, or evidence."
        )

    if not analysis:
        analysis.append(
            "The claim appears linguistically plausible but should still be verified using trusted sources."
        )

    return analysis