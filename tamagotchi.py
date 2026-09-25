import json
import os
import sys
from datetime import datetime

STATE_FILE = "state.json"
README_FILE = "README.md"

SPRITES = {
    "Happy": r"""
      /\_/\  
     ( o.o )  *purrs*
      > ^ <   [Mood: Content]
    """,
    "Hungry": r"""
      /\_/\  
     ( -.- )  *stomach growls*
      > v <   [Mood: Starving!]
    """,
    "Sleeping": r"""
      /\_/\  
     ( -.- ) zZz...
      > - <   [Mood: Recharging]
    """
}

def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def progress_bar(val, max_val=100, length=10):
    val = max(0, min(val, max_val))
    filled = int((val / max_val) * length)
    return "█" * filled + "░" * (length - filled)

def render_readme(state):
    mood = state["status"]
    sprite = SPRITES.get(mood, SPRITES["Happy"])
    
    pet_block = f"""<!-- TAMAGOTCHI:START -->
```text
{sprite}
Name: {state['name']} | Level: {state['level']}
Hunger:    [{progress_bar(state['hunger'])}] {state['hunger']}%
Energy:    [{progress_bar(state['energy'])}] {state['energy']}%
Happiness: [{progress_bar(state['happiness'])}] {state['happiness']}%
Last cared for by: @{state['last_fed_by']}
