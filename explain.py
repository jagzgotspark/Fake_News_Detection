import random

def generate_explanation(text, prediction):

    fake_reasons = [
        "The article uses sensational or exaggerated language.",
        "No credible sources are cited in the content.",
        "The claims resemble patterns commonly found in misinformation.",
        "The wording is highly emotional and intended to provoke reactions."
    ]

    real_reasons = [
        "The article uses neutral and factual language.",
        "Credible sources are referenced.",
        "The writing style matches patterns seen in verified journalism.",
        "The claims align with known factual information."
    ]

    if prediction == "Fake":
        reason = random.choice(fake_reasons)
        return f"This article is likely fake because {reason}"
    else:
        reason = random.choice(real_reasons)
        return f"This article appears credible because {reason}"