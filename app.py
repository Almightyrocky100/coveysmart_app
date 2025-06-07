import streamlit as st
import json
import os

# Load goals from JSON file
def load_goals():
    if os.path.exists("goals.json"):
        with open("goals.json", "r") as f:
            return json.load(f)
    else:
        return []

# Save goals to JSON file
def save_goals(goals):
    try:
        with open("goals.json", "w") as f:
            json.dump(goals, f, indent=4)
    except Exception as e:
        st.error(f"An error occurred while saving the goals: {e}")

# Main application
def main():
    st.title("🎯 CoveySMART Goal Tracker")

    goals = load_goals()

    for idx, goal in enumerate(goals):
        st.header(f"{goal['title']} ({goal['duration_years']} Years)")
        for phase in goal["phases"]:
            st.subheader(f"Year {phase['year']}: {phase['objective']}")
            progress = phase["achieved"] / phase["target"] if phase["target"] else 0
            st.progress(progress)
            st.write(f"Achieved: {phase['achieved']} / {phase['target']} {goal['unit']}")

            # Update achieved value
            new_achieved = st.number_input(
                f"Update Achieved for Year {phase['year']}",
                min_value=0,
                max_value=phase["target"],
                value=phase["achieved"],
                key=f"{idx}_{phase['year']}"
            )
            phase["achieved"] = new_achieved

    # Save updates
    if st.button("Save Progress"):
        save_goals(goals)
        st.success("Progress saved successfully!")

if __name__ == "__main__":
    main()
