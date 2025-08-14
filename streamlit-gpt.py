import streamlit as st
import re
from datetime import datetime, timedelta
from pathlib import Path
from icalendar import Calendar, Event
from pytz import timezone

# Optional clipboard support
try:
    import pyperclip
except ImportError:
    pyperclip = None


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

# Session state setup
if "message_text" not in st.session_state:
    st.session_state["message_text"] = ""

# --- Clipboard Support ---
clipboard_content = ""
max_lines_clipboard_preview = 3
if pyperclip is not None:
    try:
        clipboard_content = pyperclip.paste().strip()
        if clipboard_content:
            with st.container(horizontal=True):
                if st.button("📋 Use Clipboard Content"):
                    st.session_state["message_text"] = clipboard_content
                formatted_clipboard_content = "\n".join(clipboard_content.splitlines()[:max_lines_clipboard_preview]) + ("\n..." if len(clipboard_content.splitlines()) > max_lines_clipboard_preview else "")
                st.markdown(f"""> {formatted_clipboard_content}""", width=450)
        else:
            st.caption("📋 Clipboard is empty.")
    except Exception as e:
        st.caption(f"⚠️ Could not read clipboard: {e}")
else:
    st.caption("📋 Clipboard support not available — install `pyperclip` to enable.")

# --- File upload ---
uploaded_file = st.file_uploader("...or upload a message text file", type=["txt"])
if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    st.session_state["message_text"] = file_content

# --- Text area (always reflects current state) ---
st.text_area(
    "Prayer times message",
    height=200,
    key="message_text"  # This directly reads/writes session state
)

# Date selector
date_for_event = datetime.today().strftime('%Y-%m-%d')
st.write(f"#### 🗓️ Date:    {date_for_event}")

# Location and timezone
location = "ÖZ"
st.write(f"#### 📍 Event Location:  {location}")
tz = "Europe/Berlin"
st.write(f"#### 🌎 Timezone:    {tz}")

# Generate calendar button
if st.button("Generate Calendar"):
    if not st.session_state["message_text"].strip():
        st.error("❌ No message provided. Please paste, upload, or load from clipboard.")
    else:
        prayers = parse_prayer_times(st.session_state["message_text"])
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
