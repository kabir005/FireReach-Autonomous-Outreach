# 🚀 DEPLOY NOW - 5 Minutes to Live App

## Forget Render - Use Vercel for EVERYTHING

### Step 1: Go to Vercel (2 minutes)

1. Open: https://vercel.com
2. Click "Sign Up" → "Continue with GitHub"
3. Authorize Vercel

### Step 2: Deploy Backend (2 minutes)

1. Click "Add New..." → "Project"
2. Select "FireReach-Autonomous-Outreach"
3. Click "Import"
4. **Root Directory**: Leave as `.` (root)
5. **Framework**: Other
6. Click "Environment Variables"
7. Add these:

```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
FROM_NAME=FireReach by Rabbitt AI
```

8. Click "Deploy"
9. Wait 2 minutes
10. DONE! ✅

### Step 3: Test It

Your app will be at: `https://your-project.vercel.app`

Test backend: `https://your-project.vercel.app/health`
Test frontend: `https://your-project.vercel.app`

## That's It!

Both frontend and backend deployed together on Vercel.

No Render. No complexity. Just works.

---

## Alternative: Deploy Separately

If you want backend and frontend separate:

### Backend Only:
1. Vercel → New Project → Select repo
2. Root Directory: `backend`
3. Add environment variables
4. Deploy

### Frontend Only:
1. Vercel → New Project → Select repo  
2. Root Directory: `frontend`
3. Add: `VITE_API_URL=https://your-backend-url.vercel.app`
4. Deploy

---

## Your Interview Tomorrow

Just show them:
- Live URL: `https://your-project.vercel.app`
- GitHub: https://github.com/kabir005/FireReach-Autonomous-Outreach
- Say: "I built a production-ready AI agent that autonomously harvests signals, generates briefs, and sends personalized emails"

Done. 🔥
