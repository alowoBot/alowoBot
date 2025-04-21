import requests
import credentials

PERSPECTIVE_API_KEY = credentials.get_perspectiveKey()

API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

ALL_ATTRIBUTES = ["TOXICITY", "SEVERE_TOXICITY", "THREAT", "IDENTITY_ATTACK", "INSULT", "PROFANITY"]
HATE_RELATED_LABELS = {"identity_attack", "severe_toxicity", "threat"}

def timeout_test(message: str, threshold: float = 0.7):
    if not PERSPECTIVE_API_KEY:
        print("Perspective API key not set!")
        return False, None, 0.0

    payload = {
        "comment": {"text": message},
        "languages": ["en"],
        "requestedAttributes": {attr: {} for attr in ALL_ATTRIBUTES}
    }

    try:
        response = requests.post(
            API_URL,
            params={"key": PERSPECTIVE_API_KEY},
            json=payload
        )

        if response.status_code != 200:
            print(f"Perspective API error {response.status_code}: {response.text}")
            return False, None, 0.0

        result = response.json()

        for attr in HATE_RELATED_LABELS:
            score = result["attributeScores"][attr.upper()]["summaryScore"]["value"]
            if score >= threshold:
                return True, attr.lower(), score

    except Exception as e:
        print(f"Error contacting Perspective API: {e}")

    return False, None, 0.0
