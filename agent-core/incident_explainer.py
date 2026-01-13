import json
import subprocess

INCIDENT_FILE = "../backend/src/main/resources/data/incidents.json"


def load_latest_incident():
    with open(INCIDENT_FILE, "r") as f:
        incidents = json.load(f)
    return incidents[-1]


def build_prompt(incident):
    return f"""
You are a senior production support engineer.

Explain the following incident clearly and professionally:

Short Description:
{incident['short_description']}

Category: {incident['category']}
Priority: {incident['priority']}

Work Notes:
{incident['work_notes']}

Provide:
1. What likely happened
2. Why it happened
3. What should be checked next
"""


def explain_incident(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        encoding="utf-8",
        errors="replace"
    )
    return result.stdout


def main():
    incident = load_latest_incident()
    prompt = build_prompt(incident)
    explanation = explain_incident(prompt)

    print("\nAI INCIDENT EXPLANATION:\n")
    print(explanation)


if __name__ == "__main__":
    main()
