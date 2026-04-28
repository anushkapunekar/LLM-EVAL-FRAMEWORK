import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean(text):
    return re.sub(r'[^a-z0-9\s]', '', text.lower())


def relevance_score(question, answer):
    vec = CountVectorizer().fit_transform([question, answer])
    sim = cosine_similarity(vec.toarray())[0][1]
    return round(sim * 100, 2)


def correctness_score(expected, answer):
    expected = set(clean(expected).split())
    answer = set(clean(answer).split())

    if not expected:
        return 0

    common = expected & answer

    # weighted scoring
    precision = len(common) / len(answer) if answer else 0
    recall = len(common) / len(expected)

    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

    return round(f1 * 100, 2)


def hallucination_risk(answer):
    if "not sure" in answer.lower():
        return "HIGH"
    return "LOW"