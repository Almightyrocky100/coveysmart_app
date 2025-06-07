import streamlit as st
import json
import os

# Load goals from JSON file with error handling
def load_goals():
    if os.path.exists("goals.json"):
        try:
            with open("goals.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    st.warning("The goals.json file is empty. Starting with an empty goal list.")
                    return []
                return json.loads(content)
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON: {e}")
            return []
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return []
    else:
        st.info("goals.json file not found. Starting with an empty goal list.")
        return []

# Save goals to JSON file
def save_goals(goals):
    try:
        with open("goals.json", "w", encoding="utf-8") as f:
            json.dump(goals, f, indent=4)
    except Exception as e:
        st.error(f"An error occurred while saving the goals: {e}")

# Main application
def main():
    st.title("🌟 CoveySMART Goal Tracker")

    goals = load_goals()

    for idx, goal in enumerate(goals):
        st.header(f"{goal.get('title', 'Untitled Goal')} ({goal.get('duration_years', 'N/A')} Years)")
        phases = goal.get("phases", [])
        for phase in phases:
            year = phase.get("year", "N/A")
            objective = phase.get("objective", "No Objective")
            target = phase.get("target", 0)
            achieved = phase.get("achieved", 0)

            st.subheader(f"Year {year}: {objective}")
            progress = achieved / target if target else 0
            st.progress(progress)
            st.write(f"Achieved: {achieved} / {target} {goal.get('unit', '')}")

            # Update achieved value
            new_achieved = st.number_input(
                f"Update Achieved for Year {year}",
                min_value=0,
                max_value=target,
                value=achieved,
                key=f"{idx}_{year}"
            )
            phase["achieved"] = new_achieved

    # Save updates
    if st.button("Save Progress"):
        save_goals(goals)
        st.success("Progress saved successfully!")

if __name__ == "__main__":
    main()
