import json
import requests
import sys

REPO_JSON_URL = "https://raw.githubusercontent.com/santhoshriha/daily_gk/main/data/questions.json"
DAILY_JSON_URL = "https://gist.githubusercontent.com/santhoshriha/2d042e91048e3657bc5c7bd9abc4d5e3/raw/questions.json"

def update_questions():
    try:
        # Fetch existing questions
        repo_response = requests.get(REPO_JSON_URL)
        repo_response.raise_for_status()
        existing_data = repo_response.json()
        existing_questions = {q["question"] for q in existing_data["questions"]}

        # Fetch new questions
        daily_response = requests.get(DAILY_JSON_URL)
        daily_response.raise_for_status()
        new_questions = daily_response.json()

        # Merge new questions
        last_id = max(q["id"] for q in existing_data["questions"]) if existing_data["questions"] else 0
        new_entries = []
        for q in new_questions:
            if q["question"] not in existing_questions:
                last_id += 1
                q["id"] = last_id
                new_entries.append(q)
        
        if new_entries:
            existing_data["questions"].extend(new_entries)
            # Save updated data
            with open("data/questions.json", "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            print(f"Added {len(new_entries)} new questions.")
        else:
            print("No new questions to add.")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    update_questions()
