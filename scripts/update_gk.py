import json
import requests
import hashlib

REPO_JSON_URL = "https://raw.githubusercontent.com/santhoshriha/daily_gk/main/data/questions.json"
DAILY_JSON_URL = "https://gist.githubusercontent.com/santhoshriha/f7bafc57b24f0923b359b5c305c08f0a/raw/questions.json"  # REPLACE THIS


def update_questions():
    try:
        # Fetch existing questions
        repo_response = requests.get(REPO_JSON_URL)
        repo_response.raise_for_status()
        existing_data = repo_response.json()
        existing_questions = {q["question"] for q in existing_data["questions"]}  # Avoid duplicates by question text

        # Fetch new questions
        daily_response = requests.get(DAILY_JSON_URL)
        daily_response.raise_for_status()
        new_questions = daily_response.json()

        # Generate numeric IDs (assuming existing IDs are integers)
        last_id = max(q["id"] for q in existing_data["questions"]) if existing_data["questions"] else 0
        new_entries = []
        for q in new_questions:
            if q["question"] not in existing_questions:
                last_id += 1
                q["id"] = last_id
                new_entries.append(q)

        # Append new entries
        existing_data["questions"].extend(new_entries)

        # Save updated JSON
        with open("data/questions.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    update_questions()
