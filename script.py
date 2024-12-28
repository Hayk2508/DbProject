import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8002"


def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def generate_random_words():
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt"

    response = requests.get(url=url)

    return response.text.splitlines()


def generate_bank_data(words):

    return {
        "name": random.choice(words),
        "address": random.choice(words),
        "attractiveness": round(random.uniform(1.0, 10.0), 2),
        "daily_income": round(random.uniform(10000, 500000), 2),
        "security_level": random.randint(1, 5)
    }


def post_data(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        print("Successfully added!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong {e}")
        return None


def populate_database(words):
    for _ in range(1050):
        bank_data = generate_bank_data(words)
        post_data("/banks/", bank_data)


if __name__ == "__main__":
    words = generate_random_words()
    populate_database(words)
