import os
import json
from datetime import datetime

HISTORY_DIR = 'user_history'
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

def save_workout_plan(user_name, plan):
    """Save workout plan to history"""
    filename = os.path.join(HISTORY_DIR, f'workout_history_{user_name}.json')
    
    # Load existing history or create new
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    # Add new plan with timestamp
    history.append({
        'timestamp': datetime.now().isoformat(),
        'plan': plan
    })
    
    # Save updated history
    with open(filename, 'w') as f:
        json.dump(history, f, indent=2)

def save_meal_plan(user_name, plan):
    """Save meal plan to history"""
    filename = os.path.join(HISTORY_DIR, f'meal_history_{user_name}.json')
    
    # Load existing history or create new
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    # Add new plan with timestamp
    history.append({
        'timestamp': datetime.now().isoformat(),
        'plan': plan
    })
    
    # Save updated history
    with open(filename, 'w') as f:
        json.dump(history, f, indent=2)

def get_workout_history(user_name):
    """Get workout plan history for a user"""
    filename = os.path.join(HISTORY_DIR, f'workout_history_{user_name}.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def get_meal_history(user_name):
    """Get meal plan history for a user"""
    filename = os.path.join(HISTORY_DIR, f'meal_history_{user_name}.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def get_latest_workout_plan(user_name):
    """Get the most recent workout plan for a user"""
    history = get_workout_history(user_name)
    if history:
        return history[-1]['plan']
    return None

def get_latest_meal_plan(user_name):
    """Get the most recent meal plan for a user"""
    history = get_meal_history(user_name)
    if history:
        return history[-1]['plan']
    return None 