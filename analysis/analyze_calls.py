import json
import os
from prompt_evaluator import evaluate_agent_response

TRANSCRIPT_FOLDER = "../transcripts"
VERDICTS_FILE = "../verdicts.json"


def load_verdicts():
    with open(VERDICTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_agent_messages(data):

    agent_messages = []

    if "messages" in data:
        for m in data["messages"]:
            if m.get("role") == "agent":
                agent_messages.append(m.get("content", ""))

    elif "turns" in data:
        for t in data["turns"]:
            if t.get("speaker") == "agent":
                agent_messages.append(t.get("text", ""))

    elif "transcript" in data:
        for t in data["transcript"]:
            if t.get("speaker") == "agent":
                agent_messages.append(t.get("text", ""))

    return agent_messages


def analyze_transcripts():

    verdicts = load_verdicts()
    results = []

    for file in os.listdir(TRANSCRIPT_FOLDER):

        if not file.endswith(".json"):
            continue

        path = os.path.join(TRANSCRIPT_FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        agent_messages = extract_agent_messages(data)

        evaluation = evaluate_agent_response(agent_messages)

        results.append({
            "call_file": file,
            "evaluation": evaluation,
            "expected_verdict": verdicts.get(file)
        })

    return results


def save_results(results):

    with open("../analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":

    results = analyze_transcripts()

    save_results(results)

    print("Analysis complete.")