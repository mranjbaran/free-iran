# 🇮🇷 Iran Solidarity - Bundestag MP Contact Tool

**A web application helping German residents contact their Bundestag representatives about human rights violations in Iran.**

---

## 🚀 **Quick Start for Non-Technical Users**

**Just want to run the app? Follow these simple steps:**

### Step 1: Start the Backend Server
1. Open **PowerShell** or **Command Prompt**
2. Navigate to the project folder (where you cloned/downloaded the repo)
3. Copy and paste these commands:
   ```bash
   venv\Scripts\activate
   python abgeordnetenwatch_server.py
   ```
4. Wait until you see: `Running on http://127.0.0.1:5000`
4. **Keep this window open!** ✅

### Step 2: Start the React App
1. Open a **second** PowerShell/Command Prompt window
2. Navigate to the project folder, then:
   ```bash
   cd frontend
   npm run dev
   ```
3. Wait until you see: `Local: http://localhost:5173`

### Step 3: Open in Browser
1. Open your web browser (Chrome, Firefox, Edge)
2. Go to: **http://localhost:5173**
3. ✅ **The app is now running!**

> **Note:** You need both windows open for the app to work. To stop: Press `Ctrl+C` in both windows.

---

## 🎯 Purpose

This tool enables people living in Germany to:
1. Find their Bundestag representatives by postal code (PLZ)
2. Get personalized contact information with gender-aware salutations
3. Send solidarity messages about the Iran human rights crisis

> *"The people of Iran continue to face brutal repression. International solidarity from democracies like Germany is crucial."*

## 📁 Project Structure

```
free.iran/
├── frontend/                       # React/TypeScript Application
│   ├── components/
│   │   ├── Hero.tsx               # Hero section with language switcher
│   │   ├── SituationReport.tsx    # Iran crisis statistics & timeline
│   │   ├── ActionCenter.tsx       # PLZ search & MP selection
│   │   ├── MPList.tsx             # MP cards with email modal
│   │   └── Footer.tsx             # Attribution footer
│   ├── App.tsx                    # Main application
│   ├── translations.ts            # Multi-language support (EN/DE/FA)
│   ├── types.ts                   # TypeScript definitions
│   ├── vite.config.ts             # Vite configuration
│   └── package.json               # Frontend dependencies
│
├── data/
│   └── bundestag_contacts.csv     # 634 MPs with contact URLs
│
├── static/
│   └── index.html                 # Standalone HTML version (backup)
│
├── abgeordnetenwatch_server.py    # Flask API server
├── gender_data.py                 # 1037 gender mappings
├── requirements.txt               # Python dependencies
└── venv/                          # Python virtual environment
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.13+**
- **Node.js 18+**
- **Firefox** (for Selenium scraping)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mranjbaran/free-iran.git
cd free-iran

# 2. Create Python virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running the Application

**Terminal 1: Flask Backend (Required)**
```bash
# From project root directory
venv\Scripts\activate
python abgeordnetenwatch_server.py
```
✅ Backend: http://localhost:5000

**Terminal 2: React Frontend**
```bash
# From project root directory
cd frontend
npm run dev
```
✅ Frontend: http://localhost:5173

## 🛠️ Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.3 | UI framework |
| TypeScript | 5.8.2 | Type safety |
| Vite | 6.2.0 | Build tool & dev server |
| Tailwind CSS | CDN | Styling |
| Lucide React | 0.562.0 | Icons |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Flask | 3.1.0 | REST API server |
| Selenium | 4.27.1 | Web scraping |
| Flask-CORS | 5.0.0 | Cross-origin support |

### Data
- **634 Bundestag MPs** with official contact form URLs
- **1037 gender mappings** for personalized salutations
- Real-time scraping from abgeordnetenwatch.de

## 📡 API Documentation

### `GET /api/search?plz=<postal_code>`
Search for MPs by German postal code.

**Example Request:**
```bash
curl http://localhost:5000/api/search?plz=10961
```

**Response Type 1: Members Found**
```json
{
  "type": "members",
  "plz": "10961",
  "members": [
    {
      "name": "Angela Merkel",
      "party": "CDU",
      "constituency": "Berlin-Mitte",
      "image_url": "https://www.abgeordnetenwatch.de/...",
      "contact_url": "https://www.bundestag.de/services/formular/...",
      "gender": "female",
      "profile_url": "https://www.abgeordnetenwatch.de/..."
    }
  ]
}
```

**Response Type 2: Multiple Electoral Districts**
```json
{
  "type": "multiple_wahlkreis",
  "plz": "28195",
  "message": "Mehrere Wahlkreise gefunden",
  "options": [
    {
      "title": "Bremen I - Bremen",
      "url": "https://www.abgeordnetenwatch.de/bundestag/wahlkreis/bremen-i"
    }
  ]
}
```

### `GET /api/scrape-url?url=<wahlkreis_url>`
Scrape specific electoral district URL for MPs.

**Example:**
```bash
curl "http://localhost:5000/api/scrape-url?url=https://www.abgeordnetenwatch.de/bundestag/wahlkreis/bremen-i"
```

## ✨ Features

### 🌍 Multi-Language Interface
- **English** - Interface navigation
- **German** - Full support
- **Farsi (فارسی)** - Persian language with RTL support

**Note:** All email templates to MPs use German regardless of interface language.

### 🎭 Gender-Aware Salutations
Automatically generates appropriate German greetings:
- **Male MPs:** `"Sehr geehrter Herr [LastName]"`
- **Female MPs:** `"Sehr geehrte Frau [LastName]"`
- **Unknown:** `"Sehr geehrtes Mitglied des Deutschen Bundestages"`

**Detection Method:**
1. Exact match from 634 MP database
2. Fallback to ~210 common German first names
3. Handles titles: Dr., Prof., Dr. med.

### ⚡ Smart Features
- ✅ Real-time MP search with **3-5 second loading indicator**
- ✅ Profile images from abgeordnetenwatch.de
- ✅ Direct links to **official Bundestag contact forms**
- ✅ One-click **copy-to-clipboard** email templates
- ✅ Party color-coded badges:
  - SPD → Red
  - CDU/CSU → Black
  - Grüne → Green
  - FDP → Yellow
  - AfD → Blue
  - Linke → Pink

### 📧 Email Template Format
```
Betreff:
Solidarität mit den Menschen im Iran – Einsatz für Menschenrechte
////
Nachricht:

[SALUTATION],

als Bürgerin/Bürger Ihres Wahlkreises wende ich mich heute an Sie...
```

**Template Focus:**
- November 2024 Bundestag resolution
- Human rights violations since September 2022
- Calls for sanctions, investigations, and asylum protection

## 🔒 Privacy & Security

- ✅ **No data storage** - All searches are real-time
- ✅ **No tracking** - No analytics or cookies
- ✅ **External links only** - Direct to official forms
- ✅ **CORS enabled** - Safe cross-origin requests

## 🧪 Testing

Test the application with these PLZ codes:

| PLZ | Expected Result | Purpose |
|-----|----------------|---------|
| 10961 | Single district | Berlin - typical case |
| 28195 | Multiple districts | Bremen - district selection |
| 12345 | No results | Error handling |

## 🐛 Troubleshooting

### Backend Not Starting
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process and restart
Get-Process -Id <PID> | Stop-Process -Force
python abgeordnetenwatch_server.py
```

### Frontend Not Loading
```bash
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Clear cache and reinstall
cd frontend
Remove-Item node_modules, package-lock.json -Recurse -Force
npm install
npm run dev
```

### "Failed to fetch" Error
```bash
# Ensure backend is running
curl http://localhost:5000/api/search?plz=10961

# Check Flask CORS configuration
# abgeordnetenwatch_server.py should have:
# CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Selenium/Firefox Issues
```bash
# Install geckodriver
# Download from: https://github.com/mozilla/geckodriver/releases
# Add to PATH or place in project root
```

## 📊 Database Details

### Bundestag Contacts (`data/bundestag_contacts.csv`)
- **Format:** `"Last, First",mdbId,fraktion,wahlkreis_number,wahlkreis_name,contact_url`
- **Records:** 634 MPs
- **Source:** Official Bundestag member directory
- **Updated:** January 2026

### Gender Detection (`gender_data.py`)
- **Entries:** 1037 mappings
- **Coverage:** All 634 MPs in both name formats
- **Format:** `GENDER_LOOKUP = {'last, first': 'gender', 'first last': 'gender'}`
- **Accuracy:** ~95% with fallback patterns

## 🎨 Design System

### Color Palette
- **Background:** `zinc-950` (dark theme)
- **Accent:** `red-600` (solidarity color)
- **Text:** `white` / `zinc-400` (hierarchy)
- **Cards:** `zinc-800` / `zinc-900`

### Typography
- **Font:** Inter (Google Fonts)
- **Weights:** 400 (regular), 600 (semibold), 700 (bold), 900 (black)

### Components
- Responsive grid layouts
- Smooth scroll animations
- Loading spinners
- Modal overlays
- Copy-to-clipboard feedback

## 📦 Build & Deploy

### Production Build
```bash
cd frontend
npm run build
# Output: frontend/dist/
```

### Preview Production Build
```bash
npm run preview
# Runs on: http://localhost:4173
```

### Static HTML Alternative
For environments without Node.js:
```bash
# Use static/index.html
# Requires only Flask backend
# No build step needed
```

## 🤝 Contributing

This is an independent solidarity project. Improvements welcome:

**Priority Areas:**
1. 🎯 More accurate gender detection
2. 🌍 Additional language translations
3. ⚡ Performance optimizations
4. 📊 Updated MP database

**How to Contribute:**
1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

## 📝 License

This is an independent solidarity project. Not affiliated with any political party or organization.

**Purpose:** To support human rights advocacy and democratic participation.

## 📞 Support

### Debugging Steps
1. Check Flask server logs (Terminal 1)
2. Check browser console (F12 → Console)
3. Check network tab (F12 → Network)
4. Verify both servers are running

### Common Issues
| Issue | Solution |
|-------|----------|
| CORS error | Restart Flask backend |
| 404 on API call | Check Flask is on port 5000 |
| Images not loading | Check abgeordnetenwatch.de access |
| Gender wrong | Update gender_data.py |

---

**Project Status:** ✅ Production Ready  
**Last Updated:** January 14, 2026  
**Frontend:** http://localhost:5173  
**Backend:** http://localhost:5000  

**Made with ❤️ for human rights and democracy**
