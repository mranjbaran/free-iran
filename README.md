# 🇮🇷 PLZ-to-MP Iran Solidarity

**A civic-tech tool helping residents of Germany contact their Bundestag representatives to express solidarity with the people of Iran.**

## 🧭 Project Mission

The people of Iran continue to face brutal repression and human rights violations as they protest for freedom, equality, dignity, and fundamental rights. International solidarity — especially from democracies like Germany — plays a crucial role in keeping political pressure on the Iranian regime and supporting activists on the ground.

This project helps ordinary residents in Germany express their voices to their elected representatives, urging them to:

- 🗣️ Publicly acknowledge and support the Iranian people
- ⚖️ Adopt stronger human rights and diplomatic pressure
- 🤝 Work for humanitarian aid and international solidarity

Germany's Bundestag has discussed motions on **"Solidarität mit den Menschen in Iran"** and human rights, showing that this issue is actively part of parliamentary debate.

### Why This Matters

Mass protests inside Iran — including those demanding women's rights under the slogan **"Frau, Leben, Freiheit" (Woman, Life, Freedom)** — have drawn broad international attention and solidarity actions across German cities. Demonstrations in Berlin and other regions show public readiness to support these movements.

Germany, as a key EU partner, has influence on sanctions, diplomatic pressure, and humanitarian policy towards Iran — and **your voice can be part of that democratic input**.

## ✨ Features

- 🏠 **PLZ Lookup** - Enter your German postal code to find your Bundestag MPs
- 👤 **MP Profiles** - View photos, names, parties, and constituencies
- 📍 **100% Coverage** - All German postal codes supported via real-time scraping
- 🔄 **Always Current** - Real-time data from abgeordnetenwatch.de
- ✉️ **Contact Ready** - Direct links to MP profiles for advocacy outreach
- 🗺️ **Multiple Wahlkreis** - Handles PLZ codes spanning multiple districts

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Firefox browser (for web scraping)
- Git (optional, for cloning)

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install flask flask-cors selenium
```

### 2. Install Firefox

The app uses Firefox for web scraping. Download from: https://www.mozilla.org/firefox/

### 3. Start the Application

**Terminal 1 - Backend (Flask):**
```bash
python abgeordnetenwatch_server.py
```

**Terminal 2 - Frontend (HTTP Server):**
```bash
python start_server.py
```

### 4. Open in Browser

Navigate to: **http://localhost:8000/index.html**

## 📂 Project Structure

```
free.iran/
├── abgeordnetenwatch_server.py    # Flask backend (scraping)
├── index.html                      # Main user interface
├── start_server.py                # HTTP server for frontend
├── requirements.txt               # Python dependencies
├── archive/                       # Old static dataset approach
│   ├── bundestag_complete_with_wahlkreis.csv
│   ├── plz_to_members.json
│   └── ... (archived files)
└── README.md
```

## 🎯 How It Works

### User Flow:
1. 🏠 **Enter your PLZ** on the home page
2. 🔍 **View your MPs** - The app shows your Bundestag representatives
3. 👤 **Click an MP's profile** - Direct link to their page on abgeordnetenwatch.de
4. ✉️ **Contact them** - Use their profile to send a respectful email expressing support for Iran solidarity

### Technical Flow:
1. User enters PLZ in the search box
2. Flask backend launches headless Firefox browser
3. Selenium scrapes abgeordnetenwatch.de in real-time
4. Results displayed with photos, party, constituency, and profile links

### Special Cases:
- **Single Wahlkreis**: Shows MPs directly
- **Multiple Wahlkreis**: Shows selection interface (e.g., PLZ 10787 has 3 options)
- **No results**: Clear message displayed

## 🔧 API Endpoints

### Health Check
```bash
GET http://localhost:5000/health
```

### Search by PLZ
```bash
GET http://localhost:5000/api/search?plz=10961
```

**Response (Single Wahlkreis):**
```json
{
  "plz": "10961",
  "type": "members",
  "count": 1,
  "members": [
    {
      "name": "Pascal Meiser",
      "party": "Die Linke",
      "constituency": "Berlin-Friedrichshain-Kreuzberg – Prenzlauer Berg Ost",
      "profile_url": "https://www.abgeordnetenwatch.de/profile/...",
      "image_url": "https://www.abgeordnetenwatch.de/sites/default/files/..."
    }
  ]
}
```

**Response (Multiple Wahlkreis):**
```json
{
  "plz": "10787",
  "type": "multiple_wahlkreis",
  "message": "PLZ 10787 gehört zu mehreren Wahlkreisen",
  "options": [
    {
      "title": "Ansbacher Straße, Bayreuther Straße, Keithstraße",
      "url": "https://www.abgeordnetenwatch.de/bundestag/abgeordnete?..."
    }
  ]
}
```

## 🧪 Test PLZ Codes

- **10961** - Single result (Berlin-Friedrichshain-Kreuzberg)
- **33098** - Multiple results (Paderborn)
- **10787** - Multiple Wahlkreis options (Berlin Tiergarten area)
- **72213** - Multiple results (Altensteig)
- **30163** - Multiple results (Hannover)

## ⚙️ Technical Details

### Backend (Flask + Selenium)
- Headless Firefox browser
- CSS selector-based scraping
- CORS enabled for local development
- 3-5 second response time per search

### Frontend (HTML + Vanilla JavaScript)
- Pure JavaScript (no frameworks)
- Fetch API for backend communication
- Loading spinner during scraping
- Responsive design
- Hover effects on cards

## 🗂️ Archive

Old static dataset approach moved to `archive/` folder:
- CSV with 634 members (no images)
- JSON with 550 verified PLZ codes
- 88% coverage with city search fallback

See [archive/README.md](archive/README.md) for details.

## ⚠️ Performance Note

Scraping takes **3-5 seconds per PLZ** because:
1. Firefox browser launches (headless)
2. Page loads from abgeordnetenwatch.de
3. ✉️ Suggested Email Template (German)

When contacting your MP through their profile page, consider using this respectful template:

**Betreff:** Solidarität mit den mutigen Menschen im Iran – Menschenrechte schützen

**Text:**
```
Sehr geehrte(r) Frau/Herr [MP_LastName],

als Bürger*in Deutschlands und Bewohner*in von [Your_City] liegt mir die aktuelle 
Lage im Iran sehr am Herzen. Viele Menschen dort protestieren friedlich für 
Freiheit, Menschenrechte und Demokratie, doch werden sie mit brutaler Gewalt 
und Repression konfrontiert.

Ich bitte Sie, sich im Deutschen Bundestag klar für die Menschen im Iran 
auszusprechen und sich für politische Maßnahmen zur Unterstützung und zum 
Schutz der Zivilbevölkerung einzusetzen.

Mit freundlichen Grüßen,
[Your_Name]
```

### English Version:
**Subject:** Solidarity with the brave people of Iran – Protecting human rights

**Text:**
```
Dear Mr./Ms. [MP_LastName],

As a resident of [Your_City] in Germany, I am deeply concerned about the current 
situation in Iran. Many people there are peacefully protesting for freedom, human 
rights, and democracy, but are facing brutal violence and repression.

I ask you to clearly stand up for the people of Iran in the German Bundestag 
and advocate for political measures to support and protect the civilian population.

Sincerely,
[Your_Name]
```

## 📜 Code of Conduct

This project promotes **respectful, non-violent civic engagement** with elected officials. All communication should:

- ✅ Encourage constructive dialogue
- ✅ Focus on human rights advocacy
- ✅ Maintain respectful tone
- ❌ Avoid insults or partisan attacks
- ❌ Not be automated or mass-sent

## 📌 Disclaimer

This tool:
- ❗ Does **not** send emails automatically
- 📝 Provides MP information for **you** to contact them
- 🔓 Is **not affiliated** with any political party or organization
- 🤝 Encourages **constructive communication** on human rights issues
- 📊 Sources public data from [abgeordnetenwatch.de](https://www.abgeordnetenwatch.de/)

## 🌍 Context & Resources

### Current Events:
- [Bundestag Debate on Iran Solidarity](https://www.bundestag.de/)
- [Human Rights Watch - Iran](https://www.hrw.org/middle-east/north-africa/iran)
- [Amnesty International - Iran](https://www.amnesty.org/en/location/middle-east-and-north-africa/iran/)

### Solidarity Organizations:
- [HÁWAR.help](https://hawar.help/) - Emergency aid for activists
- [FIM - Frauenrecht ist Menschenrecht](https://www.fim-frauenrecht.de/)
- [Stop Femicide Iran](https://www.stop-femicide-iran.com/)

## 📝 License

This project is for educational and civic engagement purposes. All data sourced from public sources.

**MIT License** - Free to use, modify, and distribute for advocacy purposes.

## 👨‍💻 Development

**Purpose:** Supporting Iran solidarity advocacy through civic tech  
**Date:** January 2026  
**Tech Stack:** Python, Flask, Selenium, HTML, JavaScript  
**Motto:** "Frau, Leben, Freiheit" - Woman, Life, Freedom
This project is for educational purposes. Data sourced from [abgeordnetenwatch.de](https://www.abgeordnetenwatch.de/).

## 👨‍💻 Development

**Author:** Created for finding German Bundestag representatives  
**Date:** January 2026  
**Tech Stack:** Python, Flask, Selenium, HTML, JavaScript
