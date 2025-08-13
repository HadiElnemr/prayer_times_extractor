import streamlit as st
import re
from datetime import datetime, timedelta
from pathlib import Path
from icalendar import Calendar, Event
from pytz import timezone

# ------------------ Logic Functions ------------------ #

def parse_prayer_times(text):
    prayers = {}
    lines = text.splitlines()
    current_prayer = None

    for line in lines:
        line = line.strip()

        # Match prayer name lines like "*Fajr Salah*"
        match_prayer = re.match(r"\*?([\w\s@]+Salah)[^\n]*\*?", line, re.IGNORECASE)
        if match_prayer:
            current_prayer = match_prayer.group(1).strip()
            continue

        # Match time line, allow multiple times (e.g., "13:30 & 14:00")
        match_time = re.search(r"Time[:：]?\s*([\d: &]+)", line)
        if match_time and current_prayer:
            if '❌' not in line:
                time_str = match_time.group(1)
                time_entries = [t.strip() for t in time_str.split("&") if t.strip()]
                prayers.setdefault(current_prayer, []).extend(time_entries)
            current_prayer = None

    return prayers

def generate_calendar(prayers, date_str, location="ÖZ", tz="Europe/Berlin"):
    cal = Calendar()
    tzinfo = timezone(tz)

    for prayer, times in prayers.items():
        for time_str in times:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            dt = tzinfo.localize(dt)

            event = Event()
            event.add('summary', prayer)
            event.add('dtstart', dt)
            event.add('dtend', dt + timedelta(minutes=10))
            event.add('location', location)
            event.add('description', f"{prayer} time")
            cal.add_component(event)

    return cal

def save_calendar(cal, filename):
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

# ------------------ Streamlit UI ------------------ #

st.title("🕌 Prayer Times to Calendar")

st.write("Paste your WhatsApp prayer times message below or upload a `.txt` file:")

# Option 1: Paste text
message_text = st.text_area("Prayer times message", height=200)

# Option 2: Upload file
uploaded_file = st.file_uploader("...or upload a message text file", type=["txt"])
if uploaded_file and not message_text.strip():
    message_text = uploaded_file.read().decode("utf-8")

# Date selector
date_for_event = st.write(f"#### 🗓️ Date:  {datetime.today().strftime('%Y-%m-%d')}")

# Location and timezone
date_for_event = st.write(f"#### 📍 Event Location: ÖZ")
date_for_event = st.write(f"#### 🌎 Timezone: Europe/Berlin")


if st.button("Generate Calendar"):
    if not message_text.strip():
        st.error("❌ No message provided. Please paste or upload the prayer times.")
    else:
        prayers = parse_prayer_times(message_text)
        if not prayers:
            st.warning("⚠️ No valid prayer times found in the message.")
        else:
            cal = generate_calendar(prayers, date_for_event, location, tz)
            out_filename = "prayer_times.ics"
            save_calendar(cal, out_filename)

            st.success(f"✅ Prayer times saved as '{out_filename}'.")
            with open(out_filename, "rb") as f:
                st.download_button(
                    label="📥 Download Calendar File",
                    data=f,
                    file_name=out_filename,
                    mime="text/calendar"
                )

            st.subheader("Parsed Prayer Times")
            st.json(prayers)
