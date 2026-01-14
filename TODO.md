# 📋 TODO - PLZ-to-MP Iran Solidarity

## 🧠 Project Purpose & Context

- [x] Add "Purpose" section to README
- [x] Add mission statement focused on Iran solidarity
- [x] Include links to current events / solidarity actions
- [x] Reference Bundestag's motion on "Solidarität mit den Menschen in Iran"
- [ ] Add context about ongoing demonstrations in Germany
- [ ] Link to human rights organizations (HÁWAR.help, FIM, etc.)

## 🧱 Backend Logic

- [x] Accept PLZ input
- [x] Fetch MPs from PLZ via scraping
- [x] Normalize MP data with:
  - [x] Full name
  - [ ] Gender (for email salutation)
  - [x] Party
  - [x] Constituency (city/region)
  - [x] Profile URL
  - [x] MP photo URL
- [ ] Add caching layer for recent results (24h TTL)
- [ ] Keep browser instance alive between requests
- [ ] Add rate limiting / request throttling

## 🌐 Website UI

### Home / Landing
- [ ] Add mission statement banner
- [ ] Brief explanation of Iran context
- [ ] Quote: "Frau, Leben, Freiheit" - Woman, Life, Freedom
- [ ] Link to current Bundestag debates
- [x] PLZ search input
- [ ] Instructions: "Enter your postal code to find your MPs"

### Results Page
- [x] Display MPs with photo
- [x] Show name, party, constituency
- [x] "View Profile" button
- [ ] Add "Contact for Iran Solidarity" call-to-action
- [ ] Show MP contact page links more prominently

### MP Contact Page (Future)
- [ ] Prefill email template
- [ ] Generate correct salutation (Herr / Frau based on gender)
- [ ] Include MP city / constituency in email body
- [ ] Show direct link to MP contact form
- [ ] Add copy-to-clipboard button for email

## 📩 Email Template Logic

- [x] German version (in README)
- [x] English version (in README)
- [ ] Dynamic MP name insertion
- [ ] Dynamic constituency/city insertion
- [ ] Gender-aware salutation (Sehr geehrte Frau / Sehr geehrter Herr)
- [ ] Optional: User customization fields

## 📄 Content & Copywriting

### Website Text
- [ ] Clear mission statement on homepage
- [ ] Explanation of Iran protests ("Frau, Leben, Freiheit")
- [ ] Why international solidarity matters
- [ ] References to human rights violations
- [ ] Links to humanitarian organizations (optional)
- [ ] Testimonials or impact stories (future)

### Email Template
- [x] Emotional appeal
- [x] Clear ask (support motion, acknowledge human rights)
- [x] Dynamic fields (MP name & constituency)
- [x] Respectful, non-partisan language
- [ ] Multiple language versions (DE, EN, FA - Persian)

## 📊 Quality, Governance, Ethics

- [x] Validate PLZ input (5-digit format)
- [ ] Add comprehensive error handling
- [ ] Cache recent scraping results
- [x] Respect abgeordnetenwatch.de robots.txt
- [x] Include disclaimer about respectful communication
- [x] Add Code of Conduct
- [ ] Privacy policy (if collecting any data)
- [ ] Terms of use
- [ ] Accessibility improvements (WCAG compliance)

## 🚀 Deployment

- [ ] Choose hosting platform (Vercel / Netlify / Cloud)
- [ ] Set up environment variables
- [ ] Add CI/CD pipeline
- [ ] Configure domain name
- [ ] Add SSL certificate
- [ ] Set up monitoring / logging
- [ ] Add analytics (optional, privacy-friendly)
- [ ] Performance optimization

## 📖 Documentation

- [x] Complete README with Iran solidarity focus
- [x] Quick start guide
- [x] API documentation
- [x] Email templates
- [x] Code of conduct
- [ ] Contributing guidelines
- [ ] FAQ section
- [ ] Troubleshooting guide
- [ ] German translation of documentation

## 🔧 Technical Improvements

### Performance
- [ ] Implement Redis caching
- [ ] Connection pooling for Firefox instances
- [ ] Async request handling
- [ ] CDN for static assets
- [ ] Image optimization

### Features
- [ ] Multi-language support (German, English, Persian)
- [ ] MP gender detection for salutations
- [ ] Email preview before sending
- [ ] Success confirmation page
- [ ] Social media sharing buttons
- [ ] Print-friendly MP list

### Security
- [ ] Input sanitization
- [ ] Rate limiting
- [ ] CAPTCHA for automated abuse prevention
- [ ] Security headers (CSP, HSTS)
- [ ] Dependency vulnerability scanning

## 🌍 Outreach & Impact

- [ ] Share on social media
- [ ] Contact solidarity organizations
- [ ] Reach out to German-Iranian communities
- [ ] Promote at demonstrations / events
- [ ] Create multilingual flyers
- [ ] Measure impact (number of MPs contacted)
- [ ] Gather user feedback
- [ ] Case studies / success stories

## 📱 Mobile & Accessibility

- [x] Responsive design (current)
- [ ] Mobile app (PWA)
- [ ] Offline support
- [ ] Screen reader optimization
- [ ] Keyboard navigation
- [ ] High contrast mode
- [ ] Font size controls

## 🔮 Future Features

- [ ] Email tracking (did MP respond?)
- [ ] MP voting history on Iran issues
- [ ] Bundestag session alerts
- [ ] Petition integration
- [ ] Community forum / discussion
- [ ] Event calendar (protests, debates)
- [ ] Success metrics dashboard
- [ ] Automated MP response analysis

## ✅ Immediate Priorities (Next Sprint)

1. **Add gender field** to MP data for proper salutations
2. **Homepage mission banner** with Iran context
3. **Caching layer** to improve performance
4. **Deploy to production** (choose hosting)
5. **Create flyers** for sharing at events

---

**Last Updated:** January 14, 2026  
**Status:** Active Development  
**Focus:** Iran Solidarity Civic Tech
