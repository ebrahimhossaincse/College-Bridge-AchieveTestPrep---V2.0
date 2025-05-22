import json
import os
import re

import requests
import random
from pathlib import Path

# Constants
FAKER_API_URL = "https://fakerapi.it/api/v1/persons"
DEFAULT_QUANTITY = 1
DEFAULT_OUTPUT_FILE = "test_data/college_bridge_test_data.json"
PROGRAM_OPTIONS = ["LPN to RN/BSN", "Medical Assistant to RN", "Paramedic to RN", "No license yet"]


# Function to get the project root directory
def get_project_root():
    return Path(__file__).resolve().parent.parent


# Function to fetch fake user data from FakerAPI
def fetch_fake_users(quantity=1):
    response = requests.get(f"{FAKER_API_URL}?_quantity={quantity}")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from FakerAPI: {response.status_code}")

    users = response.json().get("data", [])
    formatted_users = []

    for user in users:
        email = f"{user['firstname'].lower()}.{user['lastname'].lower()}@noemail.com"
        formatted_users.append({
            "first_name": user["firstname"],
            "last_name": user["lastname"],
            "email": email,
            "phone_number": clean_phone_number(user["phone"]),
            "zip_code": user.get("zipcode", "19801"),  # fallback if not present
            "program_of_interest": random.choice(PROGRAM_OPTIONS)
        })

    return formatted_users


def clean_phone_number(raw_phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', raw_phone)

    # If it starts with country code (e.g., '1' for +1), remove it
    if len(digits) > 10 and digits.startswith("1"):
        digits = digits[1:]

    return digits[-10:]  # Return only the last 10 digits

# Function to save data to a JSON file
def save_to_json(data, filename=DEFAULT_OUTPUT_FILE):
    full_path = get_project_root() / filename
    os.makedirs(full_path.parent, exist_ok=True)

    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Data saved to: {full_path}")


# Main execution block
if __name__ == "__main__":
    num_entries = DEFAULT_QUANTITY  # or change to user input
    try:
        test_data = fetch_fake_users(num_entries)
        print(test_data)
        save_to_json(test_data)
    except Exception as e:
        print(f"❌ Error: {e}")
