# 🔥 FireReach - Autonomous Outreach Engine

**By Rabbitt AI Ecosystem**

FireReach eliminates the manual "signal-to-email" bottleneck for SDR and GTM teams through autonomous AI-powered outreach with a stunning modern interface.

## ✨ What's New

- 🎨 **Professional Modern UI** - Dark theme with animated gradients, glowing effects, and smooth animations
- 🤖 **Groq AI Integration** - Lightning-fast email generation with Llama 3.3 70B
- 📧 **Gmail SMTP Support** - Direct email sending via Gmail
- 📊 **Real-time Metrics** - Live tracking of signals, briefs, and emails
- 🎯 **Enhanced Email Quality** - Elite B2B copywriting with 180-220 word structured emails

## What It Does

1. **Harvests** live buyer signals (funding, hiring, leadership changes) via Tavily API
2. **Generates** AI-powered 2-paragraph account briefs using Groq/Llama
3. **Sends** hyper-personalized outreach emails automatically via Gmail SMTP

**Zero-Template Policy**: Every email references real, specific signals. No generic templates.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Gmail account with App Password
- Groq API key (free tier available)
- Tavily API key (free tier available)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
```

Run the backend:
```bash
python run_dev.py
```

Backend will be available at http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:3000

## 🎨 UI Features

### Modern Design System
- **Dark Theme**: Deep space background (#0a0a0f) with animated gradient mesh
- **Fire Gradient**: Orange to amber accents (#ff4500 → #ff8c00)
- **Indigo Highlights**: AI/agent elements (#6366f1)
- **Inter Font**: Professional typography from Google Fonts

### Interactive Elements
- 🎯 **Mission Control Panel** - Streamlined input form with character counts and icons
- 📊 **Live Progress Tracker** - Animated progress bar with glowing state indicators
- 🔍 **Signal Filters** - Filter by Funding, Hiring, Leadership, Tech Stack, News
- 📧 **Gmail-Style Preview** - Professional email preview with copy functionality
- 📈 **Metrics Dashboard** - Real-time session statistics

### Animations & Effects
- Pulsing flame logo
- Shimmer effect on launch button
- Glowing borders on active cards
- Smooth fade-in transitions
- Custom scrollbar styling
- Hover lift effects

## 🏗️ Architecture

### Tech Stack
- **Backend**: Python FastAPI with async/await
- **AI Model**: Groq Llama 3.3 70B Versatile (free tier)
- **Frontend**: React + Vite + Tailwind CSS
- **Agent Framework**: LangGraph with ReAct pattern
- **Search API**: Tavily (live web signals)
- **Email**: Gmail SMTP

### Agent Flow
```
Signal Harvester → Research Analyst → Outreach Sender
     (Tavily)         (Groq/Llama)      (Gmail SMTP)
```

### 3-Tool Sequential Chain

1. **Signal Harvester** - Fetches live buyer intent signals
   - Input: company name, signal types
   - Output: structured signals with sources

2. **Research Analyst** - Generates account intelligence
   - Input: signals, ICP description
   - Output: 2-paragraph brief, pain points, strategic alignment

3. **Outreach Sender** - Drafts and sends personalized email
   - Input: brief, pain points, signals, recipient
   - Output: email subject, body, send status, message ID

## 📧 Email Generation Quality

### Elite B2B Copywriting Rules
- ✅ Specific subject lines referencing real signals
- ✅ Opening lines with concrete details (numbers, names, dates)
- ✅ Bridge paragraphs connecting signals to pain points
- ✅ Value propositions tied to specific context
- ✅ Soft CTAs offering specific value
- ✅ 180-220 word optimal length
- ✅ Confident, peer-to-peer tone
- ❌ No generic phrases ("hope this finds you well", "touching base", etc.)

## 🧪 The Rabbitt Challenge

Test with this exact scenario:
- **ICP**: "We sell high-end cybersecurity training to Series B startups."
- **Company**: "Wiz" (or any Series B startup)
- **Email**: Your email address
- **Result**: Agent finds real signals, generates brief, sends personalized email

## 📁 Project Structure

```
firereach/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── agent.py             # LangGraph agent orchestration
│   ├── models.py            # Pydantic schemas
│   ├── config.py            # Configuration management
│   ├── run_dev.py           # Development server
│   ├── tools/
│   │   ├── signal_harvester.py    # Tool 1: Fetch signals via Tavily
│   │   ├── research_analyst.py    # Tool 2: Generate brief via Groq
│   │   └── outreach_sender.py     # Tool 3: Draft & send via Gmail
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main dashboard component
│   │   ├── App.css          # Custom styles & animations
│   │   ├── index.css        # Global styles
│   │   └── main.jsx         # React entry point
│   ├── package.json
│   ├── tailwind.config.js   # Tailwind configuration
│   └── .env.example
└── README.md
```

## 🔑 API Keys Setup

### Groq API (Free)
1. Visit https://console.groq.com
2. Sign up for free account
3. Generate API key
4. Add to `.env`: `GROQ_API_KEY=gsk_...`

### Tavily API (Free)
1. Visit https://tavily.com
2. Sign up for free account
3. Generate API key
4. Add to `.env`: `TAVILY_API_KEY=tvly-...`

### Gmail SMTP
1. Enable 2-Factor Authentication on your Gmail account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Add to `.env`:
   ```
   GMAIL_EMAIL=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_16_char_app_password
   ```

## 🚀 Deployment

### Backend (Render.com)
```bash
# Use the included render.yaml
# Set environment variables in Render dashboard
```

### Frontend (Vercel)
```bash
# Use the included vercel.json
vercel --prod
```

## 📊 Features

- ✅ Real-time agent progress tracking
- ✅ Live signal harvesting from web
- ✅ AI-powered account intelligence
- ✅ Hyper-personalized email generation
- ✅ Automatic email sending
- ✅ Session metrics tracking
- ✅ Signal filtering by type
- ✅ Copy email functionality
- ✅ Message ID tracking
- ✅ Error handling & validation
- ✅ Mobile responsive design
- ✅ Dark mode optimized
- ✅ Smooth animations

## 🛠️ Development

### Backend
```bash
cd backend
python run_dev.py
# API docs: http://localhost:8000/docs
# Health check: http://localhost:8000/health
```

### Frontend
```bash
cd frontend
npm run dev
# Dashboard: http://localhost:3000
```

## 📝 License

Built for the Rabbitt AI ecosystem.

## 🤝 Contributing

This is a production-ready autonomous AI application. Feel free to fork and customize for your use case.

## 📧 Support

For issues or questions, please open a GitHub issue.

---

**🔥 FireReach - Autonomous Outreach. Zero Templates.**
