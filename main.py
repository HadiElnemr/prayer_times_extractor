#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from pytz import timezone

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

def save_calendar(cal, filename="prayer_times.ics"):
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

# ---------- MAIN ----------
if __name__ == "__main__":
    try:
        with open("msg.txt", "r", encoding="utf-8") as f:
            message = f.read()
    except FileNotFoundError:
        print("❌ File 'msg.txt' not found. Please create it and paste the WhatsApp message inside.")
        exit(1)

    # Use today's date; you can change this to auto-detect from header if needed
    date_for_event = datetime.today().strftime("%Y-%m-%d")

    prayers = parse_prayer_times(message)
    if not prayers:
        print("⚠️ No valid prayer times found in the message.")
        exit(1)

    cal = generate_calendar(prayers, date_for_event)
    save_calendar(cal)

    print("✅ Prayer times saved as 'prayer_times.ics'. You can now import it into Google Calendar.")

