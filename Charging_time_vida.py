import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Vida VX2 Plus Charging Reminder",
    layout="centered"
)

# ---------------- DARK UI ----------------
st.markdown("""
<style>
body, .stApp {
    background-color: #0e1117;
    color: white;
}
div[data-testid="stProgress"] > div > div > div {
    background-color: #00ff99;
}
</style>
""", unsafe_allow_html=True)

st.title("🔋 Vida VX2 Plus Charging Reminder")
st.caption("Battery: 3.4 kWh | Charging Speed: 1% = 3.4 min")

st.divider()

# ---------------- INPUTS ----------------
current = st.number_input(
    "🔹 Current Battery Level (%)",
    min_value=0, max_value=100, value=20
)

target = st.number_input(
    "🔹 Target Battery Level (%)",
    min_value=0, max_value=100, value=80
)

notify_before = st.number_input(
    "⏰ Notify Before Completion (minutes)",
    min_value=0, max_value=120, value=5
)

start_btn = st.button("▶ Start Charging & Reminder")

# ---------------- LOGIC ----------------
if start_btn:
    if target <= current:
        st.error("❌ Target must be greater than current level")
        st.stop()

    required_percent = target - current
    total_minutes = required_percent * 3.4
    total_seconds = int(total_minutes * 60)

    ist = ZoneInfo("Asia/Kolkata")
    start_time = datetime.now(ist)
    end_time = start_time + timedelta(seconds=total_seconds)
    reminder_time = end_time - timedelta(minutes=notify_before)

    st.success("⚡ Charging Started")

    st.write(f"🕒 **Start Time:** {start_time.strftime('%I:%M:%S %p')}")
    st.write(f"⏰ **Reminder Time:** {reminder_time.strftime('%I:%M:%S %p')}")
    st.write(f"✅ **Completion Time:** {end_time.strftime('%I:%M:%S %p')}")

    progress_bar = st.progress(0)
    time_box = st.empty()
    percent_box = st.empty()

    reminder_sent = False

    for elapsed in range(total_seconds + 1):
        now = datetime.now(ist)
        remaining = total_seconds - elapsed

        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        secs = remaining % 60

        time_box.markdown(
            f"### ⏳ Remaining Time: **{hrs:02d}:{mins:02d}:{secs:02d}**"
        )

        charged_percent = current + (elapsed / total_seconds) * required_percent
        percent_box.markdown(
            f"### 🔋 Charging Level: **{charged_percent:.1f}%**"
        )

        progress_bar.progress(elapsed / total_seconds)

        # ---------- REMINDER ----------
        if not reminder_sent and now >= reminder_time:
            reminder_sent = True
            st.warning("🔔 Charging Almost Done!")

            st.markdown("""
            <script>
            alert("🔔 Vida VX2 Alert: Charging almost complete!");
            </script>
            """, unsafe_allow_html=True)

        time.sleep(1)

    # ---------- COMPLETION ALERT ----------
    st.markdown("""
    <script>
    alert("✅ Vida VX2 Charging Completed!");
    var audio = new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg");
    audio.play();
    </script>
    """, unsafe_allow_html=True)

    st.success("✅ Charging Target Reached!")
    st.balloons()
