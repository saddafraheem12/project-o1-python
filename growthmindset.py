gitimport streamlit as st
import pandas as pd
from datetime import date

# Initialize session state for 4 weeks
if 'progress' not in st.session_state:
    st.session_state.progress = {week: {} for week in range(1, 5)}
if 'reflections' not in st.session_state:
    st.session_state.reflections = {}

# Surah list with verse counts
surahs = {
    "Al-Hujurat": 18,
    "Yaseen": 83,
    "Al-Waqiah": 96,
    "An-Nisa": 176,
    "An-Noor": 64,
    "Yusuf": 111
}

# App header
st.title("📖 Dura Quran Memorization Tracker")
st.subheader("4-Week Growth Mindset Challenge")
st.write("Embrace the journey of learning - every verse memorized is a step towards growth!")

# Week selection
current_week = st.selectbox("Select Current Week", [1, 2, 3, 4])

# Progress tracking
st.header(f"Week {current_week} Progress")
for surah, verses in surahs.items():
    st.subheader(surah)
    col1, col2 = st.columns(2)

    with col1:
        memorized = st.slider(
            f"Verses memorized ({verses} total)",
            0, verses,
            value=st.session_state.progress[current_week].get(surah, 0),
            key=f"{surah}_week{current_week}"
        )
        st.session_state.progress[current_week][surah] = memorized

    with col2:
        progress_percent = memorized / verses
        st.metric("Completion", f"{progress_percent:.0%}")
        st.progress(progress_percent)

# Growth mindset features
st.header("Growth Mindset Tools")

# Progress visualization
st.subheader("Overall Progress")
total_progress = {
    surah: sum(st.session_state.progress[week].get(surah, 0) for week in range(1, 5))
    for surah in surahs
}
progress_data = {
    "Surah": list(surahs.keys()),
    "Memorized (%)": [
        total_progress[surah] / surahs[surah] for surah in surahs
    ]
}
st.bar_chart(pd.DataFrame(progress_data))

# Daily reflection
st.subheader("Daily Reflection Journal")
reflection = st.text_area(
    "What did you learn today? What challenges did you overcome?",
    help="Practice growth mindset by reflecting on your daily progress"
)
st.session_state.reflections[current_week] = reflection

# Motivational messages
total_memorized = sum(total_progress.values())
total_verses = sum(surahs.values())
achievement_level = total_memorized / total_verses

if achievement_level < 0.25:
    st.warning("🌟 Every beginning is challenging - you're building momentum!")
elif achievement_level < 0.5:
    st.info("💪 You're making progress! Remember: consistent effort beats perfection")
elif achievement_level < 0.75:
    st.success("Amazing focus! Keep up the strategic work")
else:
    st.balloons()
    st.success("You're almost there! Maintain your consistent practice")

# Save functionality
if st.button("Save Progress"):
    save_data = {
        "date": str(date.today()),
        "week": current_week,
        "progress": st.session_state.progress[current_week],
        "reflection": st.session_state.reflections.get(current_week, "")
    }
    st.success("Progress saved! Your future self will thank you for this consistency!")
    st.json(save_data)  # Optional: Show saved data
    import csv
# Inside the 'Save Progress' block
with open("progress_log.csv", mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        date.today(),
        current_week,
        surah,
        memorized,
        reflection
    ])
    import json
with open("progress_data.json", "w") as f:
    json.dump(st.session_state.progress, f)
    st.subheader("View Past Progress")
week_to_view = st.selectbox("Select week to view", [1, 2, 3, 4])
st.write(st.session_state.progress.get(week_to_view, {}))
import io

if st.button("Download Weekly Report"):
    report = f"Week {current_week} - Reflection: {reflection}\n\nProgress:\n"
    for surah, v in st.session_state.progress[current_week].items():
        report += f"{surah}: {v} verses\n"
    st.download_button("Download Report", report, file_name="weekly_report.txt")