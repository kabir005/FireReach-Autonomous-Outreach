# 👋 Welcome to FireReach!

**You're in the right place.** This is your starting point.

---

## What is FireReach?

FireReach is an AI agent that automatically:
1. Finds live buyer signals about a company (funding, hiring, etc.)
2. Writes a strategic account brief
3. Sends a personalized outreach email

**No templates. Every email references real, specific signals.**

---

## I'm New Here - What Do I Do?

### Step 1: Understand What You're Building (2 minutes)

Read this quick overview:

**The Problem**: SDR teams waste hours manually researching companies and writing personalized emails.

**The Solution**: FireReach does it automatically in 15 seconds.

**How It Works**:
```
User inputs ICP + Company Name
    ↓
Agent searches web for signals
    ↓
AI generates account brief
    ↓
AI drafts personalized email
    ↓
Email sent automatically
```

**Example**:
- Input: "We sell cybersecurity training" + "Wiz"
- Agent finds: Wiz raised $300M, hiring 15 engineers
- Email says: "I noticed Wiz just raised $300M and is hiring 15 security engineers..."
- Result: Personalized, signal-based outreach

---

### Step 2: Get It Running (10 minutes)

Follow this guide: **[GETTING_STARTED.md](./GETTING_STARTED.md)**

You'll need:
- Python 3.11+
- Node.js 18+
- 3 API keys (all have free tiers)

The guide walks you through:
1. Getting API keys (5 min)
2. Setting up backend (3 min)
3. Setting up frontend (2 min)
4. Testing your first outreach (2 min)

**Start here**: [GETTING_STARTED.md](./GETTING_STARTED.md)

---

### Step 3: Explore the Docs (As Needed)

Once you're running, explore these docs based on what you need:

**Want to understand the code?**
→ [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
→ [WORKFLOW.md](./WORKFLOW.md) - Visual workflows

**Want to test thoroughly?**
→ [TESTING.md](./TESTING.md) - Testing guide
→ [CHECKLIST.md](./CHECKLIST.md) - 200+ validation points

**Want to deploy to production?**
→ [DEPLOYMENT.md](./DEPLOYMENT.md) - Step-by-step deployment

**Want complete technical reference?**
→ [DOCS.md](./DOCS.md) - Everything you need to know

**Want to see all docs?**
→ [INDEX.md](./INDEX.md) - Complete documentation index

---

## Quick Links

### 🚀 Getting Started
- [GETTING_STARTED.md](./GETTING_STARTED.md) - Complete setup guide
- [QUICKSTART.md](./QUICKSTART.md) - 5-minute quick start

### 📖 Understanding
- [README.md](./README.md) - Project overview
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
- [WORKFLOW.md](./WORKFLOW.md) - Visual workflows

### 🧪 Testing
- [TESTING.md](./TESTING.md) - Testing guide
- [CHECKLIST.md](./CHECKLIST.md) - Validation checklist

### 🚢 Deployment
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Production deployment

### 📚 Reference
- [DOCS.md](./DOCS.md) - Complete technical docs
- [INDEX.md](./INDEX.md) - Documentation index
- [PROJECT_MAP.md](./PROJECT_MAP.md) - Project navigation

---

## Project Structure

```
firereach/
├── 📚 Documentation (13 files)
│   └── START_HERE.md ← You are here
│
├── 💻 Backend (Python FastAPI)
│   ├── main.py - API endpoints
│   ├── agent.py - LangGraph agent
│   └── tools/ - 3 agent tools
│
└── 🎨 Frontend (React)
    └── src/App.jsx - Dashboard UI
```

---

## The Rabbitt Challenge

This project was built to pass this exact test:

**Input**:
- ICP: "We sell high-end cybersecurity training to Series B startups."
- Company: "Wiz"

**Expected Output**:
- Finds Wiz's Series D funding and security hiring
- Generates brief connecting growth to training needs
- Sends email mentioning both signals

**Result**: ✅ PASSED

---

## What Makes This Special?

1. **Real Signals**: No hallucination - all data from actual web searches
2. **Zero Templates**: Every email is unique and personalized
3. **Full Automation**: From signal to sent email in 15 seconds
4. **Production Ready**: Complete with docs, tests, and deployment configs
5. **Transparent**: See the agent's reasoning at every step

---

## Tech Stack

**Backend**: Python + FastAPI + Claude AI + LangGraph
**Frontend**: React + Vite + Tailwind CSS
**Agent**: ReAct pattern with 3-tool sequential chain

---

## Next Steps

1. **Read**: [GETTING_STARTED.md](./GETTING_STARTED.md)
2. **Setup**: Get your API keys
3. **Run**: Start backend and frontend
4. **Test**: Send your first outreach
5. **Explore**: Check out other docs as needed

---

## Need Help?

### Common Questions

**Q: What API keys do I need?**
A: Anthropic (Claude), SerpAPI or Tavily (search), SendGrid or Resend (email). All have free tiers.

**Q: How long does setup take?**
A: About 10 minutes following [GETTING_STARTED.md](./GETTING_STARTED.md)

**Q: Can I customize the emails?**
A: Yes! Edit the prompts in `backend/tools/outreach_sender.py`

**Q: How much does it cost to run?**
A: Free tier: $0/month. Production: ~$82/month. See [DEPLOYMENT.md](./DEPLOYMENT.md) for details.

**Q: Is it production ready?**
A: Yes! Complete with Docker, deployment configs, and comprehensive docs.

### Troubleshooting

If you run into issues:
1. Check [GETTING_STARTED.md](./GETTING_STARTED.md) troubleshooting section
2. Verify your API keys in `.env` files
3. Run the health check: `http://localhost:8000/health`
4. Review [TESTING.md](./TESTING.md) debugging guide

---

## Documentation Overview

We have 14 documentation files covering everything:

- **Getting Started**: Setup and quick start guides
- **Technical**: Architecture, workflows, and API reference
- **Testing**: Test cases and validation checklists
- **Deployment**: Production deployment guides
- **Reference**: Complete technical documentation

**See all docs**: [INDEX.md](./INDEX.md)

---

## Project Status

✅ **Complete** - All features implemented
✅ **Tested** - Passes all requirements
✅ **Documented** - 6,500+ lines of docs
✅ **Production Ready** - Deployment configs included
✅ **Rabbitt Challenge** - Passed successfully

---

## Ready to Start?

**Go to**: [GETTING_STARTED.md](./GETTING_STARTED.md)

It will walk you through everything step-by-step.

---

**Welcome to FireReach! Let's eliminate the signal-to-email bottleneck.** 🔥

**Questions?** Check [INDEX.md](./INDEX.md) for the complete documentation index.
