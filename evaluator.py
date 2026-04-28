import json
from datetime import datetime , UTC
from llm import get_llm_response
from metrics import relevance_score, correctness_score, hallucination_risk

PASS_THRESHOLD = 50


def evaluate_case(case):
    question = case["question"]
    expected = case["expected"]

    answer = get_llm_response(question)

    rel = relevance_score(question, answer)
    cor = correctness_score(expected, answer)
    final = round((rel + cor) / 2, 2)

    status = "PASS" if final >= PASS_THRESHOLD else "FAIL"
    hallucination = hallucination_risk(answer)

    return {
        "question": question,
        "answer": answer,
        "scores": {
            "relevance": rel,
            "correctness": cor,
            "final": final
        },
        "status": status,
        "hallucination_risk": hallucination,
        "timestamp": datetime.now(UTC).isoformat()
    }


def run():
    with open("dataset.json") as f:
        dataset = json.load(f)

    results = []

    for case in dataset:
        result = evaluate_case(case)
        results.append(result)

        print("\n---")
        print(f"Q: {result['question']}")
        print(f"A: {result['answer']}")
        print(f"Score: {result['scores']['final']} | {result['status']}")

    with open("results.jsonl", "a") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    run()