# 🚀 FireReach Quick Start Guide

Get FireReach running locally in 5 minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+
- API Keys (see below)

## Step 1: Get API Keys

You'll need at least 3 API keys:

1. **Anthropic API** (Required): https://console.anthropic.com/
2. **Search API** (Choose one):
   - SerpAPI: https://serpapi.com/ (Recommended)
   - Tavily: https://tavily.com/
3. **Email API** (Choose one):
   - SendGrid: https://sendgrid.com/ (Recommended)
   - Resend: https://resend.com/

## Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Run the server
uvicorn main:app --reload
```

Backend will be running at: http://localhost:8000

Test it: http://localhost:8000/health

## Step 3: Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000)

# Run the dev server
npm run dev
```

Frontend will be running at: http://localhost:3000

## Step 4: Test the Challenge Scenario

1. Open http://localhost:3000 in your browser
2. Fill in the form:
   - **ICP**: "We sell high-end cybersecurity training to Series B startups."
   - **Company**: "Wiz" (or another Series B startup)
   - **Email**: Your test email address
3. Click "Launch FireReach"
4. Watch the agent work through the 3 steps
5. Check your email for the personalized outreach

## Troubleshooting

### Backend won't start
- Check that all required API keys are in `.env`
- Run `python -c "from config import config; print(config.validate())"` to see what's missing

### Frontend can't connect to backend
- Verify backend is running at http://localhost:8000
- Check `VITE_API_URL` in `frontend/.env`
- Look for CORS errors in browser console

### No signals found
- Verify your search API key (SERPAPI_KEY or TAVILY_API_KEY) is valid
- Try a well-known company name like "Stripe" or "Notion"

### Email not sending
- Verify your email API key (SENDGRID_API_KEY or RESEND_API_KEY) is valid
- Check that FROM_EMAIL is configured correctly
- For SendGrid, verify your sender email is authenticated

## Next Steps

- Read [DOCS.md](./DOCS.md) for complete technical documentation
- Deploy to production (see Deployment section in DOCS.md)
- Customize the agent prompts in `backend/tools/`
- Adjust the UI styling in `frontend/src/App.jsx`

## Architecture Overview

```
┌─────────────┐
│   React     │  Frontend (Port 3000)
│  Dashboard  │  • Input form
└──────┬──────┘  • Live progress tracker
       │         • Results display
       │ HTTP
       ▼
┌─────────────┐
│   FastAPI   │  Backend (Port 8000)
│   Server    │  • /api/firereach endpoint
└──────┬──────┘  • CORS enabled
       │
       ▼
┌─────────────┐
│  LangGraph  │  Agent Orchestration
│    Agent    │  • ReAct pattern
└──────┬──────┘  • Sequential tool chain
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Signal   │      │ Research │      │ Outreach │
│Harvester │      │ Analyst  │      │  Sender  │
└────┬─────┘      └────┬─────┘      └────┬─────┘
     │                 │                 │
     ▼                 ▼                 ▼
  SerpAPI          Claude AI         SendGrid
  /Tavily          (Anthropic)       /Resend
```

## Support

For issues or questions:
- Check [DOCS.md](./DOCS.md) for detailed documentation
- Review the agent logs in the dashboard
- Inspect backend logs in the terminal

---

**Built for the Rabbitt AI Ecosystem** 🔥
