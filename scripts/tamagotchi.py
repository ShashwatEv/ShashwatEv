import json
import os
import sys
from datetime import datetime

STATE_PATH = "data/tamagotchi_state.json"
SVG_PATH = "assets/tamagotchi.svg"

def load_state():
    if not os.path.exists(STATE_PATH):
        return {
            "name": "BitByte", "hunger": 80, "energy": 80,
            "happiness": 80, "level": 1, "last_interacted_by": "none",
            "status": "Chilling"
        }
    with open(STATE_PATH, "r") as f:
        return json.load(f)

def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

def clamp(val):
    return max(0, min(100, val))

def handle_tick(state):
    state["hunger"] = clamp(state["hunger"] - 5)
    state["energy"] = clamp(state["energy"] - 4)
    state["happiness"] = clamp(state["happiness"] - 3)
    
    if state["hunger"] < 25:
        state["status"] = "Starving! Send code snippets..."
    elif state["energy"] < 20:
        state["status"] = "Exhausted... Needs coffee."
    else:
        state["status"] = "Idling peacefully."

def handle_action(state, action, username):
    state["last_interacted_by"] = username
    if action == "feed":
        state["hunger"] = clamp(state["hunger"] + 25)
        state["status"] = f"Fed by @{username}!"
    elif action == "coffee":
        state["energy"] = clamp(state["energy"] + 30)
        state["status"] = f"Caffeinated by @{username}!"
    elif action == "play":
        state["happiness"] = clamp(state["happiness"] + 20)
        state["energy"] = clamp(state["energy"] - 10)
        state["status"] = f"Played with @{username}!"
    elif action == "bugfix":
        state["happiness"] = clamp(state["happiness"] + 15)
        state["hunger"] = clamp(state["hunger"] + 10)
        state["level"] += 1
        state["status"] = f"Bug squashed by @{username}! Level up!"

def render_svg(state):
    os.makedirs(os.path.dirname(SVG_PATH), exist_ok=True)
    
    # ASCII Face based on mood
    avg = (state["hunger"] + state["energy"] + state["happiness"]) / 3
    if avg > 70:
        face = "( ^ _ ^ )"
        aura = "#4ade80"
    elif avg > 35:
        face = "( . _ . )"
        aura = "#facc15"
    else:
        face = "( x _ x )"
        aura = "#f87171"

    svg_content = f"""<svg width="450" height="200" viewBox="0 0 450 200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0d1117" rx="12" stroke="#30363d" stroke-width="2"/>
  <text x="25" y="35" fill="{aura}" font-family="monospace" font-size="16" font-weight="bold">◈ {state['name']} [Lv. {state['level']}]</text>
  <text x="25" y="55" fill="#8b949e" font-family="monospace" font-size="12">Last helped by: @{state['last_interacted_by']}</text>

  <!-- Creature Visual -->
  <rect x="25" y="75" width="100" height="100" rx="8" fill="#161b22" stroke="#30363d"/>
  <text x="75" y="132" fill="{aura}" font-family="monospace" font-size="18" text-anchor="middle" font-weight="bold">{face}</text>

  <!-- Meters -->
  <text x="145" y="85" fill="#e6edf3" font-family="monospace" font-size="12">Hunger:    {state['hunger']}%</text>
  <rect x="240" y="75" width="180" height="10" rx="4" fill="#21262d"/>
  <rect x="240" y="75" width="{int(state['hunger'] * 1.8)}" height="10" rx="4" fill="#38bdf8"/>

  <text x="145" y="115" fill="#e6edf3" font-family="monospace" font-size="12">Energy:    {state['energy']}%</text>
  <rect x="240" y="105" width="180" height="10" rx="4" fill="#21262d"/>
  <rect x="240" y="105" width="{int(state['energy'] * 1.8)}" height="10" rx="4" fill="#fbbf24"/>

  <text x="145" y="145" fill="#e6edf3" font-family="monospace" font-size="12">Happiness: {state['happiness']}%</text>
  <rect x="240" y="135" width="180" height="10" rx="4" fill="#21262d"/>
  <rect x="240" y="135" width="{int(state['happiness'] * 1.8)}" height="10" rx="4" fill="#ec4899"/>

  <text x="145" y="175" fill="#8b949e" font-family="monospace" font-size="11">Status: {state['status']}</text>
</svg>"""

    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "tick"
    state = load_state()

    if mode == "tick":
        handle_tick(state)
    elif mode == "action":
        action_name = sys.argv[2]
        user_name = sys.argv[3]
        handle_action(state, action_name, user_name)

    save_state(state)
    render_svg(state)
