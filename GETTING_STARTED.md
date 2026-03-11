# 🚀 Getting Started with FireReach

Welcome to FireReach! This guide will get you from zero to running in under 10 minutes.

---

## What is FireReach?

FireReach is an autonomous AI agent that:
1. **Harvests** live buyer signals about a company (funding, hiring, etc.)
2. **Generates** an AI-powered account brief
3. **Sends** a hyper-personalized outreach email automatically

**Zero templates. Every email references real, specific signals.**

---

## Prerequisites

Before you start, make sure you have:

- [ ] Python 3.11 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] A code editor (VS Code recommended)
- [ ] A terminal/command prompt

Check your versions:
```bash
python --version  # Should be 3.11+
node --version    # Should be 18+
```

---

## Step 1: Get Your API Keys (5 minutes)

You need 3 API keys. All have free tiers:

### 1. Anthropic (Claude AI) - REQUIRED
- Go to: https://console.anthropic.com/
- Sign up for an account
- Navigate to "API Keys"
- Click "Create Key"
- Copy your key (starts with `sk-ant-api03-`)

### 2. Search API - REQUIRED (Choose One)

**Option A: SerpAPI (Recommended)**
- Go to: https://serpapi.com/
- Sign up for free account (100 searches/month)
- Copy your API key from dashboard

**Option B: Tavily**
- Go to: https://tavily.com/
- Sign up for free account
- Copy your API key

### 3. Email API - REQUIRED (Choose One)

**Option A: SendGrid (Recommended)**
- Go to: https://sendgrid.com/
- Sign up for free account (100 emails/day)
- Navigate to Settings → API Keys
- Create a new API key with "Mail Send" permissions
- Copy your key (starts with `SG.`)

**Important**: You must verify your sender email in SendGrid:
1. Go to Settings → Sender Authentication
2. Verify a single sender email
3. Use this email as `FROM_EMAIL` in your .env

**Option B: Resend**
- Go to: https://resend.com/
- Sign up for free account
- Copy your API key

---

## Step 2: Clone and Setup Backend (3 minutes)

```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create your environment file
cp .env.example .env
```

Now edit `backend/.env` with your API keys:

```bash
# Open .env in your editor
# On Windows: notepad .env
# On Mac/Linux: nano .env

# Add your keys:
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
SERPAPI_KEY=your_serpapi_key_here
SENDGRID_API_KEY=SG.your_sendgrid_key_here
FROM_EMAIL=your-verified-email@example.com
FROM_NAME=FireReach by Rabbitt AI
```

Save and close the file.

**Test your backend:**
```bash
python run_dev.py
```

You should see:
```
✅ Configuration validated successfully
🔥 Starting FireReach development server...
📍 Backend: http://localhost:8000
```

Open http://localhost:8000/health in your browser. You should see:
```json
{
  "status": "healthy",
  "configuration_errors": []
}
```

✅ Backend is working! Keep this terminal open.

---

## Step 3: Setup Frontend (2 minutes)

Open a NEW terminal window:

```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Create your environment file
cp .env.example .env
```

The default `.env` should work:
```bash
VITE_API_URL=http://localhost:8000
```

**Start the frontend:**
```bash
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:3000/
```

Open http://localhost:3000 in your browser.

✅ Frontend is working! You should see the FireReach dashboard.

---

## Step 4: Test Your First Outreach (2 minutes)

In the FireReach dashboard:

1. **ICP Field**: Paste this:
   ```
   We sell high-end cybersecurity training to Series B startups.
   ```

2. **Company Name**: Enter:
   ```
   Wiz
   ```

3. **Recipient Email**: Enter YOUR email address:
   ```
   your-email@example.com
   ```

4. Click **"🚀 Launch FireReach"**

Watch the magic happen:
- 🔍 Harvesting Signals (5-10 seconds)
- 📊 Generating Brief (3-5 seconds)
- ✉️ Sending Outreach (2-3 seconds)

You should see:
- Green checkmarks on all 3 steps
- Signals card showing funding, hiring, etc.
- Account Brief card with 2 paragraphs
- Email Preview card with "Sent ✓" badge

**Check your email!** You should receive a personalized outreach email that mentions specific signals about Wiz.

---

## Troubleshooting

### "Configuration errors" on startup

**Problem**: Missing or invalid API keys

**Solution**:
1. Check that `.env` file exists in `backend/`
2. Verify all API keys are correct (no extra spaces)
3. Make sure you copied the full key
4. For SendGrid, verify your sender email

### "No signals found"

**Problem**: Search API not working

**Solution**:
1. Verify your SERPAPI_KEY or TAVILY_API_KEY
2. Check you haven't exceeded free tier limits
3. Try a different company name (e.g., "Stripe", "Notion")

### "Email send failed"

**Problem**: Email API not configured

**Solution**:
1. Verify your SENDGRID_API_KEY or RESEND_API_KEY
2. For SendGrid: Make sure FROM_EMAIL is verified in SendGrid dashboard
3. Check API key has "Mail Send" permissions

### Frontend can't connect to backend

**Problem**: CORS or wrong URL

**Solution**:
1. Make sure backend is running on port 8000
2. Check `VITE_API_URL` in `frontend/.env`
3. Look for errors in browser console (F12)

### "Module not found" errors

**Problem**: Dependencies not installed

**Solution**:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## Next Steps

Now that you have FireReach running:

### Learn More
- Read [DOCS.md](./DOCS.md) for complete technical documentation
- Check [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Review [TESTING.md](./TESTING.md) for testing strategies

### Customize
- Modify prompts in `backend/tools/research_analyst.py`
- Adjust email style in `backend/tools/outreach_sender.py`
- Customize UI colors in `frontend/tailwind.config.js`

### Deploy
- Follow [DEPLOYMENT.md](./DEPLOYMENT.md) to deploy to production
- Backend → Render.com
- Frontend → Vercel

### Experiment
Try different scenarios:
- Different ICPs (DevOps tools, HR software, etc.)
- Different companies (Stripe, Notion, Figma)
- Different signal combinations

---

## Quick Reference

### Start Development Servers

**Backend:**
```bash
cd backend
python run_dev.py
# or: uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Run Tests

```bash
cd backend
python test_firereach.py
```

### Check Configuration

```bash
cd backend
python -c "from config import config; print(config.validate())"
```

### View API Documentation

Open http://localhost:8000/docs (when backend is running)

---

## Common Commands

```bash
# Backend
cd backend
pip install -r requirements.txt    # Install dependencies
python run_dev.py                  # Start dev server
python test_firereach.py           # Run tests

# Frontend
cd frontend
npm install                        # Install dependencies
npm run dev                        # Start dev server
npm run build                      # Build for production

# Both
git status                         # Check changes
git add .                          # Stage changes
git commit -m "message"            # Commit changes
git push                           # Push to GitHub
```

---

## Getting Help

If you're stuck:

1. **Check the docs**: Most answers are in [DOCS.md](./DOCS.md)
2. **Review logs**: Look at terminal output for errors
3. **Test health**: Visit http://localhost:8000/health
4. **Check API keys**: Verify they're correct in `.env`
5. **Try the test script**: `python test_firereach.py`

---

## Project Structure

```
firereach/
├── backend/           # Python FastAPI server
│   ├── main.py       # API endpoints
│   ├── agent.py      # LangGraph agent
│   ├── tools/        # 3 agent tools
│   └── .env          # Your API keys (create this)
├── frontend/         # React dashboard
│   ├── src/
│   │   └── App.jsx   # Main UI
│   └── .env          # API URL (create this)
└── docs/             # All the .md files
```

---

## Success Checklist

You're ready to go when:

- [x] Backend starts without errors
- [x] Frontend loads in browser
- [x] Health endpoint returns "healthy"
- [x] Test outreach completes all 3 steps
- [x] Email arrives in your inbox
- [x] Email mentions specific signals

---

**You're all set! Start building autonomous outreach campaigns.** 🔥

Questions? Check [DOCS.md](./DOCS.md) or [TESTING.md](./TESTING.md).
