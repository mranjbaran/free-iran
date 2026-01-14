# Bundestag Abgeordnete Finder

## 📋 Overview
A simple web application that allows users to find their Bundestag representatives by entering their PLZ (postal code), city name, or Wahlkreis (electoral district).

## 🎯 Features
- **Search by PLZ, City, or Wahlkreis**: Type any city name or district to find representatives
- **Real-time Search**: Results update as you type
- **Party Affiliation**: Shows each member's political party with color coding
- **Direct Contact**: Links to official contact forms for each representative
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Files Created

### Data Files:
1. **bundestag_complete.csv** / **.json** - Complete list of 634 Bundestag members
   - Name, mdbId, Fraktion (party), Contact URL

2. **wahlkreis_data.json** - Wahlkreis information with cities and members
   - 10 Wahlkreis entries with associated cities

3. **members_with_wahlkreis.csv** / **.json** - Enriched member data
   - Members linked to their Wahlkreis and cities

### Web Application:
4. **bundestag_finder.html** - Interactive web page for searching representatives

## 🚀 How to Use

### Option 1: Direct File Access
Simply open `bundestag_finder.html` in your web browser.

### Option 2: Local Server (Recommended)
For better performance, run a local web server:

```powershell
# Using Python
python -m http.server 8000

# Then open: http://localhost:8000/bundestag_finder.html
```

## 🔍 Search Examples
- **City**: "Berlin", "München", "Aachen"
- **Wahlkreis**: "074", "Berlin-Mitte"
- **Region**: "Rhein-Neckar", "Bamberg"

## 📊 Data Coverage
- **634 Bundestag members** (21st Wahlperiode)
- **10 Wahlkreis** districts with detailed city information
- **All major parties**: SPD, CDU/CSU, Bündnis 90/Die Grünen, AfD, Die Linke, Fraktionslos

## 🎨 Party Color Coding
- **SPD**: Red
- **CDU/CSU**: Black
- **Bündnis 90/Die Grünen**: Green
- **FDP**: Yellow
- **AfD**: Blue
- **Die Linke**: Magenta

## 🔗 Contact URLs
Each member has a direct link to their official contact form:
`https://www.bundestag.de/services/formular/contactform?mdbId={mdbId}`

## 📝 Notes
- The current version includes 10 Wahlkreis districts from the sample data
- To get complete PLZ coverage, you would need to scrape all 299 Wahlkreise
- The webpage works offline once loaded (all data is embedded in JSON files)

## 🛠️ Technical Details
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Format**: JSON
- **No Backend Required**: Static files only
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Edge, Safari)

## 📈 Future Enhancements
- Add all 299 Wahlkreise
- Complete PLZ to Wahlkreis mapping
- Member photos and biographies
- Voting records and statistics
- Advanced filtering options (party, state, mandate type)

---

Created: January 10, 2026
