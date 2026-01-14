# Archive - Old Implementation

This folder contains the old static dataset approach that was replaced by the real-time scraping implementation.

## Archived Files:

### Static Data Files:
- `bundestag_complete_with_wahlkreis.csv` - Scraped data of 634 Bundestag members
- `plz_to_members.json` - 550 verified PLZ codes mapping
- `wahlkreis_list.json` - 295 Wahlkreise for city search

### Old Scripts:
- `create_accurate_plz_mapping.py` - Generated static PLZ mappings
- `scrape_bundestag.py` - Original bundestag.de scraper
- `scrape_abgeordnetenwatch_by_plz.py` - Standalone test script

### Old UI:
- `bundestag_finder.html` - Static data interface (no images)
- `abgeordnetenwatch_finder.html` - Test interface for scraper

## Why Archived?

The old approach had limitations:
- No member images
- Only 88% PLZ coverage (550 out of ~8200 PLZ codes)
- Static data that required manual updates
- City search fallback was not reliable

The new implementation uses real-time scraping from abgeordnetenwatch.de:
- ✅ Real-time data with member photos
- ✅ 100% PLZ coverage
- ✅ Handles multiple Wahlkreis options
- ✅ Always up-to-date

## Date Archived:
January 14, 2026
