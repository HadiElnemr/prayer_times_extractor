
# 🕌 Prayer Times Extractor & Google Calendar Importer

This tool extracts daily prayer times from a pasted WhatsApp message (via `msg.txt`) and generates a `.ics` calendar file that can be imported into Google Calendar.

---

## 📦 Features

- Parse flexible WhatsApp prayer time formats
- Handle missing or canceled prayers (`❌`)
- Support for multiple Jumu'ah times (`&`)
- Generate `.ics` file for use with Google Calendar
- Easy-to-edit and customize

---

## 📂 Folder Structure

```
prayer_times_extractor/
├── prayer_to_calendar.py     # Main script
├── msg.txt                   # Paste WhatsApp message here
└── prayer_times.ics          # Output calendar file
```

---

## ⚙️ Installation

### 1. Clone the repository or download the files

```bash
git clone https://github.com/yourusername/prayer_times_extractor.git
cd prayer_times_extractor
```

### 2. Install dependencies

```bash
pip install icalendar pytz
```

---

## 📝 Usage

### 1. Paste your message

Paste the **full WhatsApp message** containing prayer times into `msg.txt`.
Example:

```
السلام عليكم ورحمة الله وبركاته

*Fajr Salah*
Time: 05:30 ⚠️

*Jumuaa Salah @ Vaihingen*
Time: 13:30 & 14:00

*Asr Salah*
Time: 17:45

*Maghrib Salah*
Time: 21:05 ⚠️

*Ishaa Salah*
Time: 23:10 ⚠️

Location: ÖZ
إن شاء الله
```

> ℹ️ The script **ignores times marked with ❌** and supports multiple times for Jumu'ah.

---

### 2. Run the script

```bash
python main.py
```
or run as an executable:
```bash
chmod +x main.py
./main.py
```

This will create a file named `prayer_times.ics`.

---

## 📅 How to Import `.ics` into Google Calendar

1. Go to [Google Calendar](https://calendar.google.com).
2. Click the **gear icon (⚙)** → **Settings** → **Import & export**.
3. Under **“Import”**, choose:
   - **File**: `prayer_times.ics`
   - **Calendar**: your personal calendar or create a new one (e.g., "Prayer Times").
4. Click **Import**.

> ✅ Events will now appear on your calendar for the date of the message.

---

## 🛠 Future Improvements

- Auto-detect date from WhatsApp header
- Export multiple days or a full month
- Google Calendar API integration for automatic syncing
- GUI or web version (e.g., with Streamlit)

---

## 🙏 Contributing

Feel free to fork, modify, and submit PRs! Suggestions and improvements are welcome.
