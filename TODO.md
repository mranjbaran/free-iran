# TODO List - Iran Solidarity Tool

## ✅ Completed

### Phase 1: Core Functionality
- [x] Flask API with real-time scraping
- [x] PLZ-to-MP search
- [x] 634 MP contact URLs loaded
- [x] Email templates with Iran solidarity message
- [x] Contact form integration

### Phase 2: Data & Intelligence
- [x] Gender database (1037 mappings)
- [x] Two-tier gender detection
- [x] Name normalization (Dr., Prof., etc.)
- [x] Gender-aware German salutations

### Phase 3: UX Improvements
- [x] Multiple Wahlkreis support
- [x] "3-5 seconds" loading message
- [x] Party color-coded badges
- [x] Copy-to-clipboard
- [x] Email modal with personalization

### Phase 4: React Frontend
- [x] React/TypeScript with Vite
- [x] Multi-language (EN/DE/FA)
- [x] Modern dark theme
- [x] All components implemented
- [x] Connected to Flask API

### Phase 5: Project Organization
- [x] Reorganized to frontend/ folder
- [x] Cleaned unnecessary files
- [x] Professional README
- [x] Updated TODO

### Phase 6: Reliability
- [x] PLZ input validation + 10s request timeout on frontend
- [x] User-facing no-results message

## 📋 Future Enhancements

### High Priority
- [ ] Automated MP database updates
- [ ] Enhanced gender detection
- [ ] Response caching (5 min)

### Medium Priority
- [ ] Privacy-preserving analytics
- [ ] Multiple email templates
- [ ] Additional MP data (Twitter, committees)

### Low Priority
- [ ] Accessibility improvements
- [ ] Unit & E2E tests
- [ ] Docker deployment

## 🐛 Known Issues

- [ ] Vite occasionally fails first start (restart fixes)
- [ ] Long names may overflow on mobile
- [ ] Selenium scrape depends on abgeordnetenwatch.de markup and Firefox/geckodriver availability

---

**Status:** Beta (local use)  
**Version:** 0.0.0  
**Updated:** January 16, 2026
