import streamlit as st
import json
import os

GOALS_FILE = "goals.json"

def load_goals():
    if os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE, "r", encoding="utf-8") as f:
                data = f.read().strip()
                if not data:
                    st.warning("goals.json is empty – start by adding goals.")
                    return []
                return json.loads(data)
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {e}")
            return []
    else:
        st.info("goals.json not found; starting fresh.")
        return []

def save_goals(goals):
    try:
        with open(GOALS_FILE, "w", encoding="utf-8") as f:
            json.dump(goals, f, indent=4)
    except Exception as e:
        st.error(f"Error saving goals.json: {e}")

def main():
    st.title("🌟 CoveySMART Long-Term Goal Tracker")

    goals = load_goals()

    for idx, goal in enumerate(goals):
        if not isinstance(goal, dict):
            st.warning(f"Entry at index {idx} is not a JSON object – skipped.")
            continue

        title = goal.get("title")
        duration = goal.get("duration_years")
        phases = goal.get("phases")

        if not title or not isinstance(duration, int) or not isinstance(phases, list):
            st.warning(f"Goal at index {idx} missing fields – skipped.")
            continue

        st.header(f"{title} — {duration} years")
        updated = False

        for phase in phases:
            if all(k in phase for k in ("year","objective","target","achieved")):
                year = phase["year"]
                obj = phase["objective"]
                target = phase["target"]
                achieved = phase["achieved"]

                st.subheader(f"Year {year}: {obj}")
                progress = achieved / target if target > 0 else 0
                st.progress(progress)
                st.write(f"Completed: {achieved} / {target} {goal.get('unit','')}")

                new_achieved = st.number_input(
                    f"Update Year {year}",
                    min_value=0,
                    max_value=target,
                    value=achieved,
                    key=f"{idx}_{year}"
                )
                if new_achieved != achieved:
                    phase["achieved"] = new_achieved
                    updated = True
            else:
                st.warning(f"Invalid phase in goal {idx}: {phase}")

        if updated:
            save_goals(goals)
            st.success(f"Updated progress for '{title}'")

    if st.button("🗂 Add Example Goal"):
        example = {
            "title": "New 12-Year Goal",
            "duration_years": 12,
            "unit": "modules",
            "phases": [
                {"year": i+1,
                 "objective": f"Year {i+1} objective",
                 "target": 10, "achieved": 0}
                for i in range(12)
            ]
        }
        goals.append(example)
        save_goals(goals)
        st.success("Added example goal. Refresh to view it.")

if __name__ == "__main__":
    main()
