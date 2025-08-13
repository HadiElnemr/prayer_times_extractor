
# 🕌 Prayer Times Extractor & Google Calendar Importer

This tool extracts daily prayer times from a pasted WhatsApp message (read from **clipboard** or `msg.txt`) and generates a `.ics` calendar file that can be imported into Google Calendar, or synced directly via the Google Calendar API.

---

## 📦 Features

- Reads message directly from clipboard (no paste required) or from msg.txt
- Parse flexible WhatsApp prayer time formats
- Handle missing or canceled prayers (`❌`)
- Support for multiple Jumu'ah times (`&`)
- Generate `.ics` file or sync events directly to Google Calendar
- Easy-to-edit and customize

---

## 📂 Folder Structure

```
prayer_times_extractor/
├── main.py                    # Generate .ics file from WhatsApp message (clipboard or file)
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
pip install icalendar pytz pyperclip google-api-python-client google-auth google-auth-oauthlib

# In case you got a message similar to this when running main.py: (Skipping clipboard: clipboard error: Pyperclip could not find a copy/paste mechanism for your system. For more information, please visit https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error. On Linux, you can run sudo apt-get install xclip or sudo apt-get install xselect to install a copy/paste mechanism.)
sudo apt install -y xclip

```

---

## 📝 Usage

### 0. Alternative quick way:

Add a function in your `.bashrc` or `.zshrc` file to run the script directly from the terminal:

```bash
function prayer_sync(){
  cd ~/dev/prayer_times_extractor
  ./main.py
  ./prayer_google_sync.py
}
```

Copy the message from WhatsApp (now it is in clipboard) and run:

```bash
prayer_sync
```

Just like that, you will have the prayer times in your Google Calendar after signing in.

### 1. Prepare your message

Option A (Recommended): Copy the WhatsApp prayer times message to your clipboard — the script will read it automatically.
Option B: Paste the message into `msg.txt`

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
Time: ❌❌

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
<!-- - [ ] Read Automatically from Whatsapp? Not possible -->
---

## 🙏 Contributing

Feel free to fork, modify, and submit PRs! Suggestions and improvements are welcome.
