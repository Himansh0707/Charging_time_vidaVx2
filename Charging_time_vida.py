import streamlit as st
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="Vida VX2 Plus Charging",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- Dark Premium Styling ----
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.stApp {
    background-color: #0e1117;
}
h1, h2, h3, p, label {
    color: white !important;
}
div[data-testid="stProgress"] > div > div > div {
    background-color: #00ff99;
}
</style>
""", unsafe_allow_html=True)

st.title("🔋 Vida VX2 Plus Charging Tracker")
st.caption("Battery: 3.4 kWh | Charging Speed: 1% = 3.4 min")

st.divider()

current = st.number_input(
    "🔹 Current Battery Level (%)",
    min_value=0,
    max_value=100,
    value=40
)

target = st.number_input(
    "🔹 Target Battery Level (%)",
    min_value=0,
    max_value=100,
    value=80
)

start_btn = st.button("▶ Start Charging Calculation")

if start_btn:
    if target <= current:
        st.error("❌ Target level must be greater than current level")
    else:
        required_percent = target - current
        total_minutes = required_percent * 3.4
        total_seconds = int(total_minutes * 60)

        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=total_seconds)

        st.success("⚡ Charging Started")

        st.write(f"🕒 **Start Time:** {start_time.strftime('%I:%M:%S %p')}")
        st.write(f"✅ **Completion Time:** {end_time.strftime('%I:%M:%S %p')}")

        progress_bar = st.progress(0)
        countdown_placeholder = st.empty()
        percent_placeholder = st.empty()

        for elapsed in range(total_seconds + 1):
            remaining = total_seconds - elapsed

            hrs = remaining // 3600
            mins = (remaining % 3600) // 60
            secs = remaining % 60

            countdown_placeholder.markdown(
                f"### ⏳ Remaining Time: **{hrs:02d}:{mins:02d}:{secs:02d}**"
            )

            charged_percent = current + (elapsed / total_seconds) * required_percent
            percent_placeholder.markdown(
                f"### 🔋 Charging Level: **{charged_percent:.1f}%**"
            )

            progress = elapsed / total_seconds
            progress_bar.progress(min(progress, 1.0))

            time.sleep(1)

        st.balloons()
        st.success("✅ Charging Target Reached!")
