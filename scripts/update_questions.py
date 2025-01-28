import json
import hashlib
import requests

def main():
    # Load existing questions
    with open("data/malayalam_gk.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    existing_questions = {q["id"] for q in data["questions"]}

    # Fetch new questions (URL example)
    response = requests.get("https://gist.githubusercontent.com/{your_gist_id}/raw/daily_gk.json")
    new_questions = response.json()

    # Add new questions with unique IDs
    for q in new_questions:
        q_id = hashlib.md5(q["question"].encode()).hexdigest()  # Generate unique ID
        if q_id not in existing_questions:
            q["id"] = q_id
            data["questions"].append(q)

    # Save updated JSON
    with open("data/malayalam_gk.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
