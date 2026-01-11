#!/usr/bin/env python3

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import pyperclip
except Exception:
    pyperclip = None  # We'll handle gracefully if missing

from icalendar import Calendar, Event
from pytz import timezone


def parse_prayer_times(text):
    prayers = {}
    lines = text.splitlines()
    current_prayer = None

    for line in lines:
        line = line.strip()

        # Match prayer name lines like "*Fajr Salah*" or with emojis
        # This regex handles emojis anywhere in the prayer name (before, after, or within)
        # Pattern: optional *, then any chars (including emojis), then word chars/spaces/@, then "Salah", then any chars (including emojis), optional *
        match_prayer = re.match(r"\*?([^\n]*?[\w\s@]+Salah[^\n]*?)\*?", line, re.IGNORECASE | re.UNICODE)
        if match_prayer:
            # Extract prayer name and clean it (remove asterisks, keep emojis if present)
            prayer_name = match_prayer.group(1).strip()
            # Remove asterisks but keep everything else including emojis
            prayer_name = re.sub(r'^\*+|\*+$', '', prayer_name).strip()
            current_prayer = prayer_name
            continue

        # Match time line, allow multiple times (e.g., "13:30 & 14:00")
        # This regex handles emojis before or after the time (like 🕧, ⚠️, etc.)
        # First check if line contains "Time:" pattern
        if re.search(r"Time[:：]", line, re.IGNORECASE) and current_prayer:
            # Filter out lines with ❌ (canceled prayers)
            if '❌' not in line:
                # Extract all time patterns (HH:MM) from the line, regardless of emojis
                # This handles cases like "Time: 🕧 12:30" or "Time: 12:30 ⚠️" or "Time: 13:30 & 14:00"
                time_matches = re.findall(r'\b(\d{1,2}:\d{2})\b', line)
                if time_matches:
                    # Remove duplicates while preserving order
                    seen = set()
                    unique_times = []
                    for t in time_matches:
                        if t not in seen:
                            seen.add(t)
                            unique_times.append(t)
                    if unique_times:
                        prayers.setdefault(current_prayer, []).extend(unique_times)
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

def ask_yes_no(prompt, default_yes=True):
    suffix = "[Y/n]" if default_yes else "[y/N]"
    resp = input(f"{prompt} {suffix} ").strip().lower()
    if not resp:
        return default_yes
    return resp in ("y", "yes")

def get_message_from_clipboard():
    if pyperclip is None:
        return None, "pyperclip not installed"
    try:
        txt = pyperclip.paste() or ""
        txt = txt.strip()
        if not txt:
            return None, "clipboard is empty"
        preview = (txt[:120] + "…") if len(txt) > 120 else txt
        if ask_yes_no(f"Clipboard has text:\n---\n{preview}\n---\nUse this?"):
            return txt, None
        return None, "user declined clipboard"
    except Exception as e:
        return None, f"clipboard error: {e}"

def get_message_from_file(path="msg.txt"):
    path = Path(path)
    if not path.exists():
        print("❌ File 'msg.txt' not found.")
        return None
    if not ask_yes_no(f"Read message from '{path}'?"):
        return None
    with path.open("r", encoding="utf-8") as f:
        return f.read()

# ---------- MAIN ----------
if __name__ == "__main__":
    # 1) Try clipboard
    message = None
    clip_reason = None
    message, clip_reason = get_message_from_clipboard()

    # 2) Otherwise, fallback to msg.txt (after confirmation)
    if message is None:
        if clip_reason:
            print(f"(Skipping clipboard: {clip_reason})")
        message = get_message_from_file("msg.txt")

    if not message or not message.strip():
        print("❌ No input message provided. Copy the WhatsApp text or create 'msg.txt'.")
        sys.exit(1)

    # Use today's date
    date_for_event = datetime.today().strftime("%Y-%m-%d")

    prayers = parse_prayer_times(message)
    if not prayers:
        print("⚠️ No valid prayer times found in the message.")
        sys.exit(1)

    cal = generate_calendar(prayers, date_for_event)
    out = "prayer_times.ics"
    save_calendar(cal, out)

    print(f"✅ Prayer times saved as '{out}'. Import it into your calendar app.")