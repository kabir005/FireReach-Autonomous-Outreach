# 🧪 FireReach Testing Guide

This guide helps you test and validate the FireReach agent.

## Quick Test

Run the automated test script:

```bash
cd backend
python test_firereach.py
```

This will:
1. Validate your configuration
2. Run the agent with the Rabbitt Challenge scenario
3. Display the full execution log
4. Show all results (signals, brief, email)

## Manual Testing via API

### 1. Start the Backend

```bash
cd backend
uvicorn main:app --reload
```

### 2. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "configuration_errors": []
}
```

### 3. Test FireReach Endpoint

```bash
curl -X POST http://localhost:8000/api/firereach \
  -H "Content-Type: application/json" \
  -d '{
    "icp_description": "We sell high-end cybersecurity training to Series B startups.",
    "company_name": "Wiz",
    "recipient_email": "your-test-email@example.com"
  }'
```

### 4. Verify Response

Check that the response includes:
- `"status": "success"`
- `"send_status": "sent"`
- Non-empty `signals` array
- 2-paragraph `account_brief`
- `email_subject` and `email_body` that reference specific signals
- Valid `message_id`

## Testing via Frontend

### 1. Start Both Servers

Terminal 1:
```bash
cd backend
uvicorn main:app --reload
```

Terminal 2:
```bash
cd frontend
npm run dev
```

### 2. Open Dashboard

Navigate to http://localhost:3000

### 3. Fill Form

- **ICP**: "We sell high-end cybersecurity training to Series B startups."
- **Company**: "Wiz" (or another well-known Series B startup)
- **Email**: Your test email address

### 4. Launch Agent

Click "Launch FireReach" and watch the progress tracker:
1. 🔍 Harvesting Signals (should complete in 5-10 seconds)
2. 📊 Generating Brief (should complete in 3-5 seconds)
3. ✉️ Sending Outreach (should complete in 2-3 seconds)

### 5. Verify Results

Check that the dashboard shows:
- Green checkmarks for all 3 steps
- Signals card with multiple signals
- Account Brief card with 2 paragraphs
- Email Preview card with "Sent ✓" badge
- Email body that mentions at least 2 specific signals

### 6. Check Your Email

Verify that you received the email and it:
- Has a personalized subject line
- References specific signals about the company
- Feels human and conversational
- Is under 150 words
- Ends with a question

## Test Cases

### Test Case 1: The Rabbitt Challenge (Primary)

**Input:**
- ICP: "We sell high-end cybersecurity training to Series B startups."
- Company: "Wiz"
- Email: test@example.com

**Expected:**
- Finds funding signals (Series D, $300M+)
- Finds hiring signals (security engineers)
- Brief connects growth to training needs
- Email mentions both funding and hiring

**Pass Criteria:**
- ✅ All 3 tools execute successfully
- ✅ Email references 2+ specific signals
- ✅ Email is sent (status = "sent")
- ✅ Email feels personalized, not templated

---

### Test Case 2: Different Company

**Input:**
- ICP: "We provide DevOps automation tools for fast-growing SaaS companies."
- Company: "Notion"
- Email: test@example.com

**Expected:**
- Finds relevant signals for Notion
- Brief connects signals to DevOps needs
- Email is personalized to Notion's situation

**Pass Criteria:**
- ✅ Signals are relevant to Notion (not Wiz or other companies)
- ✅ Email doesn't use generic templates
- ✅ Email references Notion-specific signals

---

### Test Case 3: Limited Signals

**Input:**
- ICP: "We sell enterprise software."
- Company: "SmallStartupXYZ123" (non-existent company)
- Email: test@example.com

**Expected:**
- Agent completes even with few/no signals
- Brief acknowledges limited data
- Email is still sent but may be more generic

**Pass Criteria:**
- ✅ Agent doesn't crash
- ✅ Returns partial results
- ✅ Logs indicate limited signal availability

---

### Test Case 4: Error Handling

**Input:**
- ICP: "Test"
- Company: "Test"
- Email: invalid-email (invalid format)

**Expected:**
- Validation error before agent runs
- Clear error message returned

**Pass Criteria:**
- ✅ Returns 422 validation error
- ✅ Error message indicates email format issue

## Debugging

### Backend Logs

Watch the backend terminal for:
- `[REASONING]` - Agent's thought process
- `[ACTION]` - Tool executions
- `[OBSERVATION]` - Tool outputs
- `[ERROR]` - Any failures

### Frontend Console

Open browser DevTools (F12) and check:
- Network tab for API calls
- Console for any JavaScript errors
- Response payloads from `/api/firereach`

### Common Issues

#### No Signals Found
- **Cause**: Search API key invalid or rate limited
- **Fix**: Verify SERPAPI_KEY or TAVILY_API_KEY in .env
- **Test**: Try a well-known company like "Stripe"

#### Email Not Sending
- **Cause**: Email API key invalid or sender not verified
- **Fix**: 
  - Verify SENDGRID_API_KEY or RESEND_API_KEY
  - For SendGrid, verify sender email in SendGrid dashboard
  - Check FROM_EMAIL is configured correctly

#### Agent Timeout
- **Cause**: Search API taking too long
- **Fix**: Check your internet connection and API status

#### Generic Email
- **Cause**: Not enough signals or poor signal quality
- **Fix**: 
  - Try a different company with more public information
  - Check that signals are being harvested correctly
  - Review the agent log to see what signals were found

## Performance Benchmarks

Expected execution times:
- Signal Harvesting: 5-10 seconds
- Research Analysis: 3-5 seconds
- Email Drafting & Sending: 2-3 seconds
- **Total**: 10-18 seconds end-to-end

If significantly slower:
- Check API response times
- Verify network connectivity
- Consider API rate limits

## Validation Checklist

Use this checklist to validate a complete FireReach execution:

- [ ] Configuration validated (no errors in /health)
- [ ] Agent executes all 3 tools in order
- [ ] Signals array contains real data (not empty)
- [ ] Account brief is exactly 2 paragraphs
- [ ] Pain points array has 2-4 items
- [ ] Email subject is 6-10 words
- [ ] Email body is under 150 words
- [ ] Email references at least 2 specific signals
- [ ] Email tone is conversational, not corporate
- [ ] Email ends with a question
- [ ] Send status is "sent"
- [ ] Message ID is returned
- [ ] Agent log shows reasoning at each step
- [ ] No errors in agent log
- [ ] Email actually arrives in inbox

## Load Testing

For production readiness, test with multiple concurrent requests:

```bash
# Install Apache Bench
# macOS: brew install httpd
# Ubuntu: apt-get install apache2-utils

# Run 10 requests with 2 concurrent
ab -n 10 -c 2 -p test_payload.json -T application/json \
  http://localhost:8000/api/firereach
```

Create `test_payload.json`:
```json
{
  "icp_description": "We sell high-end cybersecurity training to Series B startups.",
  "company_name": "Wiz",
  "recipient_email": "test@example.com"
}
```

Expected:
- All requests complete successfully
- Average response time < 20 seconds
- No 500 errors

## CI/CD Testing

For automated testing in CI/CD pipelines:

```bash
# Set environment variables
export ANTHROPIC_API_KEY=your_key
export SERPAPI_KEY=your_key
export SENDGRID_API_KEY=your_key

# Run test script
cd backend
python test_firereach.py

# Check exit code
if [ $? -eq 0 ]; then
  echo "✅ Tests passed"
else
  echo "❌ Tests failed"
  exit 1
fi
```

## Support

If tests fail:
1. Check [DOCS.md](./DOCS.md) for configuration details
2. Review agent logs for specific errors
3. Verify all API keys are valid and have sufficient credits
4. Try the test script first before manual testing

---

**Happy Testing!** 🔥
