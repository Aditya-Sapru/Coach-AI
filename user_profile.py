import json
import os

PROFILE_PATH = 'user_profile.json'

def user_profile_exists():
    return os.path.exists(PROFILE_PATH) and os.path.getsize(PROFILE_PATH) > 0

def save_user_profile(data):
    with open(PROFILE_PATH, 'w') as f:
        json.dump(data, f)

def load_user_profile():
    if user_profile_exists():
        with open(PROFILE_PATH, 'r') as f:
            return json.load(f)
    return {}
