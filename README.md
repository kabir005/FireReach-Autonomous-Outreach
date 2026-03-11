# 🔥 FireReach - Autonomous Outreach Engine

**By Rabbitt AI Ecosystem**

FireReach eliminates the manual "signal-to-email" bottleneck for SDR and GTM teams through autonomous AI-powered outreach.

**👋 New here? Start with [START_HERE.md](./START_HERE.md)**

## What It Does

1. **Harvests** live buyer signals (funding, hiring, leadership changes)
2. **Generates** AI-powered 2-paragraph account briefs
3. **Sends** hyper-personalized outreach emails automatically

**Zero-Template Policy**: Every email references real, specific signals. No generic templates.

## Quick Start

See [QUICKSTART.md](./QUICKSTART.md) for detailed setup instructions.

### TL;DR

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000 and launch your first autonomous outreach!

## Architecture

- **Backend**: Python FastAPI with Claude Sonnet 4.5
- **Frontend**: React + Vite + Tailwind CSS
- **Agent**: LangGraph ReAct pattern with 3-tool sequential chain
- **Tools**: Signal Harvester → Research Analyst → Outreach Sender

## The Rabbitt Challenge

Test with this exact scenario:
- **ICP**: "We sell high-end cybersecurity training to Series B startups."
- **Company**: "Wiz"
- **Result**: Agent finds real signals, generates brief, sends personalized email

## Documentation

**New to FireReach?** Start with [GETTING_STARTED.md](./GETTING_STARTED.md)

**Complete Documentation Index**: [INDEX.md](./INDEX.md)

Key documents:
- [GETTING_STARTED.md](./GETTING_STARTED.md) - Complete setup guide (10 minutes)
- [QUICKSTART.md](./QUICKSTART.md) - Quick reference (5 minutes)
- [DOCS.md](./DOCS.md) - Complete technical documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design and architecture
- [TESTING.md](./TESTING.md) - Testing guide with test cases
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Production deployment guide
- [CHECKLIST.md](./CHECKLIST.md) - 200+ validation points

## Project Structure

```
firereach/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── agent.py             # LangGraph agent orchestration
│   ├── models.py            # Pydantic schemas
│   ├── config.py            # Configuration management
│   ├── tools/
│   │   ├── signal_harvester.py    # Tool 1: Fetch signals
│   │   ├── research_analyst.py    # Tool 2: Generate brief
│   │   └── outreach_sender.py     # Tool 3: Draft & send
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main dashboard component
│   │   └── main.jsx
│   ├── package.json
│   └── .env.example
├── DOCS.md                  # Technical documentation
├── QUICKSTART.md            # Setup guide
└── README.md                # This file
```

## Deployment

- **Backend**: Deploy to Render.com (see `backend/render.yaml`)
- **Frontend**: Deploy to Vercel (see `frontend/vercel.json`)

## Requirements

- Python 3.11+
- Node.js 18+
- API Keys:
  - Anthropic (Claude)
  - SerpAPI or Tavily (search)
  - SendGrid or Resend (email)

## License

Built for the Rabbitt AI ecosystem.
