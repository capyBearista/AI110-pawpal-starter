import streamlit as st  # type: ignore[import-not-found]
import pawpal_system as ps
from datetime import date, time as time_type

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Time available (minutes)", value=60)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, value=3)
weight = st.number_input("Pet weight (lbs)", min_value=0.1, value=10.0)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = ps.Scheduler(
        owner=ps.Owner(name=owner_name, available_minutes=int(available_minutes)),
        pets_involved=[ps.Pet(name=pet_name, age=int(age), weight=float(weight), species=species)],
    )

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_time = st.time_input("Start time", value=time_type(8, 0))

PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}
PRIORITY_LABEL = {1: "high", 2: "medium", 3: "low"}

if st.button("Add task"):
    new_task = ps.Task(
        title=task_title,
        priority=PRIORITY_MAP[priority],
        duration_in_minutes=int(duration),
        date=date.today(),
        time=task_time,
    )
    st.session_state.scheduler.add_task(new_task)

if st.session_state.scheduler.tasks:
    st.session_state.scheduler.sort_by_time()
    conflicts = st.session_state.scheduler.detect_conflicts()

    st.write("Current tasks (sorted by time):")
    st.table([
        {
            "Task": t.title,
            "Time": t.time.strftime("%H:%M"),
            "Duration (min)": t.duration_in_minutes,
            "Priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
        }
        for t in st.session_state.scheduler.tasks
    ])

    if conflicts:
        st.markdown("#### Schedule Conflicts")
        for msg in conflicts:
            st.warning(msg)
    else:
        st.success("No scheduling conflicts detected.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    schedule = st.session_state.scheduler.build_schedule()
    if schedule:
        st.write("Scheduled tasks:")
        st.table([{"title": t.title, "priority": t.priority, "duration_in_minutes": t.duration_in_minutes} for t in schedule])
    else:
        st.info("No schedule generated yet. Implement build_schedule() in pawpal_system.py!")