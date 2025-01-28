import json
import requests
import hashlib

# URL of your JSON file in the repo
REPO_JSON_URL = "https://raw.githubusercontent.com/santhoshriha/daily_gk/main/data/questions.json"
# URL of my daily questions (replace with your Gist/API)
DAILY_JSON_URL = "https://gist.githubusercontent.com/{username}/{gist-id}/raw/daily_questions.json"

def update_questions():
    # Fetch existing questions from your repo
    response = requests.get(REPO_JSON_URL)
    existing_data = response.json()
    existing_hashes = {q["id"] for q in existing_data["questions"]}

    # Fetch new daily questions
    new_questions = requests.get(DAILY_JSON_URL).json()

    # Generate unique ID using question text hash
    for q in new_questions:
        q_hash = hashlib.md5(q["question"].encode()).hexdigest()
        if q_hash not in existing_hashes:
            q["id"] = q_hash
            existing_data["questions"].append(q)

    # Save updated JSON locally (GitHub Actions will commit this)
    with open("data/questions.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_questions()
