# 🗺️ FireReach Project Map

Visual guide to navigating the FireReach codebase.

---

## Quick Navigation

```
┌─────────────────────────────────────────────────────────────────┐
│                    FIREREACH PROJECT MAP                         │
└─────────────────────────────────────────────────────────────────┘

📚 DOCUMENTATION (Start Here)
├─ 🚀 GETTING_STARTED.md    → New users start here
├─ ⚡ QUICKSTART.md          → 5-minute setup
├─ 📖 DOCS.md                → Complete technical reference
├─ 🏗️ ARCHITECTURE.md        → System design
├─ 🔄 WORKFLOW.md            → Visual workflows
├─ 🧪 TESTING.md             → Testing guide
├─ 🚢 DEPLOYMENT.md          → Production deployment
├─ ✅ CHECKLIST.md           → 200+ validation points
├─ 📋 PROJECT_SUMMARY.md     → High-level overview
├─ 🎉 PROJECT_COMPLETE.md    → Completion report
├─ 📚 INDEX.md               → Documentation index
└─ 📄 README.md              → Project overview

💻 BACKEND (Python FastAPI)
├─ main.py                   → API endpoints
├─ agent.py                  → LangGraph orchestration
├─ models.py                 → Pydantic schemas
├─ config.py                 → Configuration
├─ tools/
│  ├─ signal_harvester.py   → Tool 1: Fetch signals
│  ├─ research_analyst.py   → Tool 2: Generate brief
│  └─ outreach_sender.py    → Tool 3: Draft & send
├─ run_dev.py                → Development server
├─ test_firereach.py         → Test script
├─ requirements.txt          → Dependencies
├─ Dockerfile                → Container config
├─ render.yaml               → Render deployment
└─ .env.example              → Environment template

🎨 FRONTEND (React + Vite)
├─ src/
│  ├─ App.jsx                → Main dashboard
│  ├─ main.jsx               → React entry
│  └─ index.css              → Tailwind imports
├─ index.html                → HTML template
├─ package.json              → Dependencies
├─ vite.config.js            → Vite config
├─ tailwind.config.js        → Tailwind config
├─ vercel.json               → Vercel deployment
└─ .env.example              → Environment template

⚙️ CONFIGURATION
├─ .gitignore                → Git ignore rules
└─ LICENSE                   → MIT License
```

---

## By Task

### "I want to get started"
```
1. Read: GETTING_STARTED.md
2. Setup: backend/.env.example → backend/.env
3. Setup: frontend/.env.example → frontend/.env
4. Run: backend/run_dev.py
5. Run: frontend/npm run dev
6. Test: Open http://localhost:3000
```

### "I want to understand the code"
```
1. Read: ARCHITECTURE.md (system design)
2. Read: WORKFLOW.md (data flow)
3. Explore: backend/agent.py (agent logic)
4. Explore: backend/tools/ (tool implementations)
5. Explore: frontend/src/App.jsx (UI)
```

### "I want to test it"
```
1. Read: TESTING.md
2. Run: backend/test_firereach.py
3. Check: CHECKLIST.md
4. Verify: All 200+ points
```

### "I want to deploy it"
```
1. Read: DEPLOYMENT.md
2. Configure: backend/render.yaml
3. Configure: frontend/vercel.json
4. Deploy: Backend to Render
5. Deploy: Frontend to Vercel
```

### "I want to customize it"
```
1. Prompts: backend/tools/research_analyst.py
2. Prompts: backend/tools/outreach_sender.py
3. UI: frontend/src/App.jsx
4. Styling: frontend/tailwind.config.js
```

---

## By Role

### Developer
```
Priority Files:
1. GETTING_STARTED.md    → Setup
2. ARCHITECTURE.md       → Design
3. backend/agent.py      → Agent logic
4. backend/tools/        → Tool implementations
5. frontend/src/App.jsx  → UI code
```

### DevOps/SRE
```
Priority Files:
1. DEPLOYMENT.md         → Deployment guide
2. backend/Dockerfile    → Container
3. backend/render.yaml   → Backend config
4. frontend/vercel.json  → Frontend config
5. CHECKLIST.md          → Security checklist
```

### Product Manager
```
Priority Files:
1. README.md             → Overview
2. PROJECT_SUMMARY.md    → Features
3. WORKFLOW.md           → User journey
4. DOCS.md               → Capabilities
5. PROJECT_COMPLETE.md   → Status
```

### QA/Tester
```
Priority Files:
1. TESTING.md            → Test guide
2. CHECKLIST.md          → Validation
3. backend/test_firereach.py → Test script
4. GETTING_STARTED.md    → Setup
5. WORKFLOW.md           → Expected behavior
```

---

## Code Organization

### Backend Structure
```
backend/
├─ Entry Point
│  └─ main.py (80 lines)
│     ├─ FastAPI app
│     ├─ CORS middleware
│     ├─ /api/firereach endpoint
│     ├─ /health endpoint
│     └─ / endpoint
│
├─ Agent Orchestration
│  └─ agent.py (200 lines)
│     ├─ GraphState definition
│     ├─ signal_harvester_node()
│     ├─ research_analyst_node()
│     ├─ outreach_sender_node()
│     ├─ should_continue()
│     ├─ create_firereach_graph()
│     └─ run_firereach_agent()
│
├─ Data Models
│  └─ models.py (120 lines)
│     ├─ Signal
│     ├─ SignalHarvesterInput/Output
│     ├─ ResearchAnalystInput/Output
│     ├─ OutreachSenderInput/Output
│     ├─ FireReachRequest
│     ├─ FireReachResponse
│     ├─ AgentState
│     └─ GraphState
│
├─ Configuration
│  └─ config.py (50 lines)
│     ├─ Config class
│     ├─ Environment variables
│     └─ validate()
│
└─ Tools
   ├─ signal_harvester.py (150 lines)
   │  ├─ search_serpapi()
   │  ├─ search_tavily()
   │  ├─ parse_search_results()
   │  └─ tool_signal_harvester()
   │
   ├─ research_analyst.py (120 lines)
   │  ├─ RESEARCH_ANALYST_PROMPT
   │  └─ tool_research_analyst()
   │
   └─ outreach_sender.py (180 lines)
      ├─ EMAIL_DRAFTING_PROMPT
      ├─ draft_email_with_claude()
      ├─ send_email_sendgrid()
      ├─ send_email_resend()
      └─ tool_outreach_automated_sender()
```

### Frontend Structure
```
frontend/
├─ Entry Point
│  ├─ index.html (15 lines)
│  └─ src/main.jsx (10 lines)
│
├─ Main Application
│  └─ src/App.jsx (400 lines)
│     ├─ State management (useState)
│     ├─ Form handling (handleSubmit)
│     ├─ Progress tracking (getStepStatus)
│     ├─ StepIndicator component
│     ├─ ResultCard component
│     └─ Main render
│
├─ Styling
│  ├─ src/index.css (15 lines)
│  ├─ src/App.css (5 lines)
│  └─ tailwind.config.js (25 lines)
│
└─ Configuration
   ├─ vite.config.js (10 lines)
   ├─ postcss.config.js (7 lines)
   └─ package.json (30 lines)
```

---

## Data Flow Map

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                │
└─────────────────────────────────────────────────────────────────┘

USER INPUT (Frontend)
├─ icp_description: string
├─ company_name: string
└─ recipient_email: string
    │
    ▼ HTTP POST /api/firereach
    │
FASTAPI (main.py)
├─ Validate with Pydantic (models.py)
└─ Call run_firereach_agent()
    │
    ▼
AGENT (agent.py)
├─ Initialize GraphState
├─ Execute signal_harvester_node()
│  └─ Call tool_signal_harvester() (tools/signal_harvester.py)
│     └─ Returns: signals[]
├─ Execute research_analyst_node()
│  └─ Call tool_research_analyst() (tools/research_analyst.py)
│     └─ Returns: account_brief, pain_points[], alignment
└─ Execute outreach_sender_node()
   └─ Call tool_outreach_automated_sender() (tools/outreach_sender.py)
      └─ Returns: email_subject, email_body, send_status, message_id
    │
    ▼
RESPONSE (main.py)
├─ Assemble FireReachResponse (models.py)
└─ Return JSON
    │
    ▼ HTTP Response
    │
FRONTEND (App.jsx)
├─ Update state with result
├─ Render progress tracker
├─ Render signals card
├─ Render account brief card
└─ Render email preview card
```

---

## Integration Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                         │
└─────────────────────────────────────────────────────────────────┘

FIREREACH BACKEND
    │
    ├─ SerpAPI / Tavily
    │  ├─ Used by: tools/signal_harvester.py
    │  ├─ Purpose: Web search for signals
    │  ├─ Calls: 5 per execution
    │  └─ Config: SERPAPI_KEY or TAVILY_API_KEY
    │
    ├─ Anthropic Claude
    │  ├─ Used by: tools/research_analyst.py
    │  │           tools/outreach_sender.py
    │  ├─ Purpose: Generate brief and email
    │  ├─ Calls: 2 per execution
    │  ├─ Model: claude-sonnet-4-20250514
    │  └─ Config: ANTHROPIC_API_KEY
    │
    └─ SendGrid / Resend
       ├─ Used by: tools/outreach_sender.py
       ├─ Purpose: Send email
       ├─ Calls: 1 per execution
       └─ Config: SENDGRID_API_KEY or RESEND_API_KEY

FIREREACH FRONTEND
    │
    └─ Backend API
       ├─ Endpoint: POST /api/firereach
       ├─ Protocol: HTTPS
       ├─ Format: JSON
       └─ Config: VITE_API_URL
```

---

## File Size Reference

```
Total Files: 42
Total Size: ~185 KB

Breakdown:
├─ Backend Code: ~50 KB
├─ Frontend Code: ~30 KB
├─ Documentation: ~100 KB
└─ Configuration: ~5 KB
```

---

## Dependency Map

### Backend Dependencies
```
fastapi==0.109.0
├─ uvicorn[standard]==0.27.0
├─ pydantic==2.6.0
└─ python-multipart==0.0.6

anthropic==0.18.1
└─ httpx==0.26.0

langchain==0.1.6
└─ langgraph==0.0.20

sendgrid==6.11.0
python-dotenv==1.0.0
```

### Frontend Dependencies
```
react==18.2.0
└─ react-dom==18.2.0

vite==5.0.11
└─ @vitejs/plugin-react==4.2.1

tailwindcss==3.4.1
├─ autoprefixer==10.4.17
└─ postcss==8.4.33

axios==1.6.5
```

---

## Quick Commands Reference

### Development
```bash
# Backend
cd backend
python run_dev.py                # Start dev server
python test_firereach.py         # Run tests

# Frontend
cd frontend
npm run dev                      # Start dev server
npm run build                    # Build for production
```

### Testing
```bash
# Health check
curl http://localhost:8000/health

# Test API
curl -X POST http://localhost:8000/api/firereach \
  -H "Content-Type: application/json" \
  -d '{"icp_description":"...","company_name":"...","recipient_email":"..."}'
```

### Deployment
```bash
# Backend (Docker)
cd backend
docker build -t firereach-api .
docker run -p 8000:8000 --env-file .env firereach-api

# Frontend (Build)
cd frontend
npm run build
# Deploy dist/ folder to Vercel
```

---

## Color-Coded Priority

🔴 **Critical** - Must read/understand
🟡 **Important** - Should read/understand
🟢 **Optional** - Nice to have

### For Getting Started
🔴 GETTING_STARTED.md
🔴 backend/.env.example
🔴 frontend/.env.example
🟡 QUICKSTART.md
🟢 README.md

### For Development
🔴 ARCHITECTURE.md
🔴 backend/agent.py
🔴 backend/tools/
🟡 WORKFLOW.md
🟡 frontend/src/App.jsx

### For Testing
🔴 TESTING.md
🔴 CHECKLIST.md
🟡 backend/test_firereach.py
🟢 WORKFLOW.md

### For Deployment
🔴 DEPLOYMENT.md
🔴 backend/render.yaml
🔴 frontend/vercel.json
🟡 CHECKLIST.md (security section)
🟢 ARCHITECTURE.md (infrastructure section)

---

**Use this map to navigate the FireReach project efficiently!** 🗺️
