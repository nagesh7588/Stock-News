# QA Testing Checklist - Stock News Application

## 1. Functional Testing

### Core Functionality
- [ ] Application starts successfully without errors
- [ ] Homepage loads within acceptable time (< 3 seconds)
- [ ] News articles are displayed correctly
- [ ] All news items are stock/market related (filtered correctly)
- [ ] News articles show within last 24 hours only
- [ ] Article titles are clickable and open correct URL
- [ ] External links open in new tab/window

### News Display
- [ ] Article title displays correctly
- [ ] Publication date/time shows properly
- [ ] Source name is visible and accurate
- [ ] Description/summary text appears correctly
- [ ] URL links are functional and not broken
- [ ] Articles are sorted by publication date (newest first)

### Data Filtering
- [ ] Keywords filter works (stock, stocks, share market, sensex, nifty, market, earnings, quarter results)
- [ ] Non-relevant articles are filtered out
- [ ] Case-insensitive keyword matching works
- [ ] Keywords in both title and description are detected

## 2. API Integration Testing

### NewsAPI Integration
- [ ] API key authentication works correctly
- [ ] API requests complete successfully
- [ ] Response data is parsed correctly
- [ ] Handles 200 OK responses
- [ ] Handles 401 Unauthorized (invalid API key)
- [ ] Handles 429 Too Many Requests (rate limiting)
- [ ] Handles 500 Internal Server Error
- [ ] Handles network timeout errors
- [ ] API parameters are correctly formatted:
  - [ ] Query string (`q` parameter)
  - [ ] Date range (`from` parameter)
  - [ ] Sort order (`sortBy=publishedAt`)
  - [ ] Language (`language=en`)
  - [ ] Page size (`pageSize=50`)

### Error Handling
- [ ] Missing API key shows appropriate error
- [ ] Invalid API key shows meaningful error message
- [ ] Network errors are handled gracefully
- [ ] Empty API response doesn't crash application
- [ ] Malformed JSON response is handled
- [ ] Missing article fields don't cause errors

## 3. Environment & Configuration

### Environment Variables
- [ ] NEWS_API_KEY environment variable loads correctly
- [ ] Missing NEWS_API_KEY raises ValueError with clear message
- [ ] Empty NEWS_API_KEY is rejected
- [ ] Environment variable persists across application restarts

### Configuration Files
- [ ] config.py loads without errors
- [ ] Configuration values are accessible
- [ ] No hardcoded credentials in code

## 4. UI/UX Testing

### Visual Design
- [ ] Page layout is clean and readable
- [ ] Container background color displays correctly (current: pink)
- [ ] H1 heading color is visible (current: yellow/red depending on branch)
- [ ] Text contrast is sufficient for readability
- [ ] Font sizes are appropriate
- [ ] Spacing and padding are consistent
- [ ] Border styling is correct (5px solid #0d67dd)

### Responsive Design
- [ ] Page displays correctly on desktop (1920x1080)
- [ ] Page displays correctly on laptop (1366x768)
- [ ] Page displays correctly on tablet (768x1024)
- [ ] Page displays correctly on mobile (375x667)
- [ ] Text remains readable at all screen sizes
- [ ] No horizontal scrolling on smaller screens

### User Experience
- [ ] Page loading indicator (if applicable)
- [ ] Clear visual hierarchy of content
- [ ] Easy to scan news items
- [ ] Links are clearly distinguishable
- [ ] Hover effects work on interactive elements

## 5. Performance Testing

### Load Time
- [ ] Initial page load < 3 seconds
- [ ] API response time < 2 seconds
- [ ] Total time to interactive < 5 seconds

### Resource Usage
- [ ] Memory usage is acceptable
- [ ] CPU usage is minimal
- [ ] No memory leaks during extended use
- [ ] Browser/tab doesn't freeze

### Scalability
- [ ] Handles 50 articles without performance degradation
- [ ] Handles empty results gracefully
- [ ] Multiple concurrent users supported

## 6. Security Testing

### API Security
- [ ] API key is not exposed in frontend code
- [ ] API key is stored as environment variable
- [ ] No API key in version control (check .gitignore)
- [ ] HTTPS used for API calls (NewsAPI uses HTTPS)

### Web Security
- [ ] No XSS vulnerabilities in article content
- [ ] External links are safe (target="_blank" with rel="noopener")
- [ ] No sensitive data logged to console
- [ ] Error messages don't expose system details

### Access Control
- [ ] Environment variables accessible only to application
- [ ] No unauthorized access to configuration files

## 7. Browser Compatibility

### Desktop Browsers
- [ ] Google Chrome (latest version)
- [ ] Mozilla Firefox (latest version)
- [ ] Microsoft Edge (latest version)
- [ ] Safari (macOS latest version)

### Mobile Browsers
- [ ] Chrome Mobile (Android)
- [ ] Safari (iOS)
- [ ] Firefox Mobile
- [ ] Samsung Internet

### JavaScript
- [ ] Works with JavaScript enabled
- [ ] Graceful degradation if JavaScript disabled

## 8. Data Validation

### Input Validation
- [ ] Date parameters are validated
- [ ] API responses are validated before processing
- [ ] Article data structure is validated

### Output Validation
- [ ] HTML is properly escaped
- [ ] No broken HTML tags
- [ ] Special characters display correctly
- [ ] Unicode characters render properly

## 9. Edge Cases & Boundary Testing

### Data Edge Cases
- [ ] Zero articles returned
- [ ] Exactly 1 article returned
- [ ] Maximum articles (50) returned
- [ ] Articles with missing titles
- [ ] Articles with missing descriptions
- [ ] Articles with missing source information
- [ ] Articles with null values
- [ ] Very long article titles (truncation?)
- [ ] Very long descriptions

### Date/Time Edge Cases
- [ ] Articles exactly 24 hours old
- [ ] Articles 23:59:59 old
- [ ] Articles from different timezones
- [ ] Future dated articles (shouldn't appear)

### Special Characters
- [ ] Articles with emojis
- [ ] Articles with special characters (&, <, >, ", ')
- [ ] Articles with non-English characters
- [ ] Articles with HTML entities

## 10. Deployment Testing

### Pre-Deployment
- [ ] All unit tests pass (14 tests)
- [ ] All integration tests pass (11 tests)
- [ ] No critical errors in logs
- [ ] Dependencies installed correctly
- [ ] requirements.txt is up to date

### Azure Deployment (if applicable)
- [ ] Application deploys successfully
- [ ] Environment variables configured in Azure
- [ ] Application runs in production mode
- [ ] Logs are accessible
- [ ] Application restarts correctly
- [ ] Health check endpoint works

### Post-Deployment
- [ ] Production URL is accessible
- [ ] News data loads in production
- [ ] No console errors in production
- [ ] Performance metrics are acceptable
- [ ] Error tracking is enabled

## 11. Accessibility Testing

### WCAG 2.1 Compliance
- [ ] Sufficient color contrast ratios (AA level minimum)
  - [ ] Text contrast >= 4.5:1
  - [ ] Large text contrast >= 3:1
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Alt text for images (if applicable)
- [ ] Semantic HTML structure
- [ ] Focus indicators visible
- [ ] No keyboard traps

### Assistive Technologies
- [ ] NVDA screen reader (Windows)
- [ ] JAWS screen reader (Windows)
- [ ] VoiceOver (macOS/iOS)
- [ ] TalkBack (Android)

## 12. Regression Testing

### After Code Changes
- [ ] All previous functionality still works
- [ ] No new errors introduced
- [ ] Performance hasn't degraded
- [ ] UI/UX unchanged (unless intentional)

### After Dependency Updates
- [ ] Flask update doesn't break functionality
- [ ] requests library update works correctly
- [ ] Python version compatibility maintained

## 13. Git & Version Control Testing

### Branch Testing
- [ ] `main` branch is stable
- [ ] `abc` branch styling reviewed (greenyellow/yellow issues)
- [ ] `def` branch identical to main
- [ ] `integration` branch has correct merges
- [ ] `production` branch is deployment-ready
- [ ] No merge conflicts exist
- [ ] All branches build successfully

### Merge Safety
- [ ] Cherry-picks don't introduce conflicts
- [ ] Merge commits are clean
- [ ] No conflict markers in code
- [ ] History is readable and logical

## 14. Monitoring & Logging

### Application Logs
- [ ] Logs are generated for key events
- [ ] Error logs include stack traces
- [ ] Log levels are appropriate
- [ ] Sensitive data not logged

### Monitoring
- [ ] Uptime monitoring configured
- [ ] Error rate tracking
- [ ] API call success/failure tracking
- [ ] Response time monitoring

## 15. Documentation Testing

### Code Documentation
- [ ] README.md is accurate and complete
- [ ] Code comments are clear
- [ ] API documentation exists
- [ ] Setup instructions work

### User Documentation
- [ ] Installation steps are correct
- [ ] Configuration guide is clear
- [ ] Troubleshooting section helpful
- [ ] Examples are working

## Test Execution Summary

### Critical Path Testing
Priority: **HIGH** - Must pass before deployment
- [ ] Application starts
- [ ] News fetching works
- [ ] Filtering works correctly
- [ ] UI displays properly
- [ ] No security vulnerabilities

### Test Environment
- **OS**: Windows 11
- **Python Version**: 3.12.3
- **Browser**: Chrome/Firefox/Edge latest
- **Test Date**: ___________
- **Tester**: ___________

### Sign-Off
- [ ] All critical tests passed
- [ ] All high-priority tests passed
- [ ] Known issues documented
- [ ] Ready for deployment

**QA Tester Signature**: ___________  
**Date**: ___________  
**Approved for Deployment**: [ ] Yes  [ ] No

---

## Notes & Issues Found

**Issue #1**:
- Description:
- Severity: [Critical/High/Medium/Low]
- Status: [Open/In Progress/Resolved]

**Issue #2**:
- Description:
- Severity:
- Status:

---

## Known Issues (Current)

1. **Accessibility Issue (abc branch)**: Yellow text on greenyellow background has poor contrast
   - Severity: High
   - Branch: abc
   - Status: Not merged to production

2. **Deprecation Warning**: `datetime.utcnow()` deprecated in news_service.py
   - Severity: Low
   - Impact: Will need update in future Python versions
   - Status: Documented

3. **Styling Issue (main/def branch)**: Red text on pink background has suboptimal contrast
   - Severity: Medium
   - Branch: main, def, production
   - Status: In production
