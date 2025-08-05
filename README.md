
# 🕌 Prayer Times Extractor & Google Calendar Importer

This tool extracts daily prayer times from a pasted WhatsApp message (via `msg.txt`) and generates a `.ics` calendar file that can be imported into Google Calendar, or synced directly via the Google Calendar API.

---

## 📦 Features

- Parse flexible WhatsApp prayer time formats
- Handle missing or canceled prayers (`❌`)
- Support for multiple Jumu'ah times (`&`)
- Generate `.ics` file or sync events directly to Google Calendar
- Easy-to-edit and customize

---

## 📂 Folder Structure

```
prayer_times_extractor/
├── main.py                    # Generate .ics file from WhatsApp message
├── prayer_google_sync.py # Optional: sync directly to Google Calendar
├── msg.txt                   # Paste WhatsApp message here
├── prayer_times.ics          # Output calendar file
├── credentials.json          # Google OAuth credentials
└── token.json                # Generated after first OAuth login
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
pip install icalendar pytz google-api-python-client google-auth google-auth-oauthlib
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

### 2. Generate `.ics` calendar file

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

## 📅 Option A: Import `.ics` into Google Calendar

1. Go to [Google Calendar](https://calendar.google.com).
2. Click the **gear icon (⚙)** → **Settings** → **Import & export**.
3. Under **“Import”**, choose:
   - **File**: `prayer_times.ics`
   - **Calendar**: your personal calendar or create a new one (e.g., "Prayer Times").
4. Click **Import**.

---

## 🌐 Option B: Sync Directly to Google Calendar (API)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable the **Google Calendar API**
3. Create an **OAuth 2.0 Client ID** (type: Desktop)
4. Download the `credentials.json` file to your project folder
5. Run:

```bash
python sync_to_google_calendar.py
```

✅ The script will open a browser, ask you to log in and authorize access.
Prayer times will be added directly to your Google Calendar.

---


## 🛠 Future Improvements
- [x] Google Calendar API integration for automatic syncing
- [ ] Export multiple days or a full month
- [ ] GUI or web version (e.g., with Streamlit)
<!-- - [ ] Auto-detect date from WhatsApp header -->
---

## 🙏 Contributing

Feel free to fork, modify, and submit PRs! Suggestions and improvements are welcome.
