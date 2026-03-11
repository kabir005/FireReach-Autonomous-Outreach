# 🚀 Easy Deployment Guide - Step by Step

Follow these exact steps to deploy FireReach in 15 minutes.

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- ✅ GitHub account (you already have this)
- ✅ Your API keys ready (get them from your `.env` file):
  - `GROQ_API_KEY`: Your Groq API key (starts with `gsk_`)
  - `TAVILY_API_KEY`: Your Tavily API key (starts with `tvly-`)
  - `GMAIL_EMAIL`: Your Gmail address
  - `GMAIL_APP_PASSWORD`: Your Gmail app password (16 characters)

---

## 🎯 Part 1: Deploy Backend to Render (5 minutes)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click **"Get Started"** (top right)
3. Click **"Sign in with GitHub"**
4. Authorize Render to access your GitHub account
5. You'll be redirected to Render dashboard

### Step 2: Create New Web Service
1. On Render dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and click **"FireReach-Autonomous-Outreach"**
5. Click **"Connect"**

### Step 3: Configure Web Service

Fill in these EXACT settings:

| Field | Value |
|-------|-------|
| **Name** | `firereach-api` (or any name you like) |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section and click **"Add Environment Variable"**.

Add these ONE BY ONE:

**Variable 1:**
- Key: `GROQ_API_KEY`
- Value: `[Your Groq API key from .env file]`

**Variable 2:**
- Key: `TAVILY_API_KEY`
- Value: `[Your Tavily API key from .env file]`

**Variable 3:**
- Key: `GMAIL_EMAIL`
- Value: `[Your Gmail address from .env file]`

**Variable 4:**
- Key: `GMAIL_APP_PASSWORD`
- Value: `[Your Gmail app password from .env file]`

**Variable 5:**
- Key: `FROM_NAME`
- Value: `FireReach by Rabbitt AI`

### Step 5: Deploy Backend
1. Click **"Create Web Service"** button at the bottom
2. Wait 3-5 minutes for deployment (you'll see logs scrolling)
3. Look for: `✅ Build successful` and `✅ Deploy live`
4. Your backend URL will appear at the top (e.g., `https://firereach-api.onrender.com`)
5. **COPY THIS URL** - you'll need it for frontend!

### Step 6: Test Backend
1. Click on your backend URL
2. Add `/health` to the end: `https://firereach-api.onrender.com/health`
3. You should see: `{"status":"healthy","configuration_errors":[]}`
4. If you see this, backend is working! ✅

**Troubleshooting:**
- If you see errors, check the "Logs" tab
- Make sure all 5 environment variables are set correctly
- Check for typos in the values

---

## 🎨 Part 2: Deploy Frontend to Vercel (5 minutes)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Click **"Sign Up"** (top right)
3. Click **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub account
5. You'll be redirected to Vercel dashboard

### Step 2: Import Project
1. Click **"Add New..."** button (top right)
2. Select **"Project"**
3. You'll see a list of your GitHub repositories
4. Find **"FireReach-Autonomous-Outreach"**
5. Click **"Import"** button next to it

### Step 3: Configure Project

Fill in these EXACT settings:

| Field | Value |
|-------|-------|
| **Framework Preset** | `Vite` (should auto-detect) |
| **Root Directory** | Click "Edit" → Type `frontend` → Click "Continue" |
| **Build Command** | `npm run build` (auto-filled) |
| **Output Directory** | `dist` (auto-filled) |
| **Install Command** | `npm install` (auto-filled) |

### Step 4: Add Environment Variable

1. Click **"Environment Variables"** dropdown (expand it)
2. Add this variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.onrender.com` (paste your Render URL from Part 1, Step 5)
   - **IMPORTANT**: Remove any trailing slash from the URL!

Example:
- ✅ Correct: `https://firereach-api.onrender.com`
- ❌ Wrong: `https://firereach-api.onrender.com/`

3. Make sure it's added to all environments (Production, Preview, Development)

### Step 5: Deploy Frontend
1. Click **"Deploy"** button
2. Wait 2-3 minutes for build (you'll see progress)
3. Look for: `✅ Build Completed` and confetti animation 🎉
4. Your frontend URL will appear (e.g., `https://fire-reach-autonomous-outreach.vercel.app`)
5. Click **"Visit"** to open your deployed app

### Step 6: Test Full Application
1. Open your frontend URL
2. Fill in the form:
   - **ICP**: "We sell cybersecurity training to Series B startups"
   - **Company**: "Wiz"
   - **Email**: Your email address
3. Click **"🚀 Launch FireReach"**
4. Watch the agent work through all 3 steps
5. Check your email inbox for the outreach message!

**If it works, you're done! 🎉**

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: "Application failed to respond"**
- Solution: Check Render logs for errors
- Make sure all environment variables are set
- Verify `uvicorn main:app --host 0.0.0.0 --port $PORT` is the start command

**Problem: "Configuration errors" in /health**
- Solution: Double-check all 5 environment variables
- Make sure there are no extra spaces in the values
- Verify Gmail app password is correct (16 characters)

**Problem: "Build failed"**
- Solution: Check if `requirements.txt` is in the `backend` folder
- Make sure Root Directory is set to `backend`
- Check build logs for specific error messages

### Frontend Issues

**Problem: "Failed to fetch" or CORS errors**
- Solution: Make sure `VITE_API_URL` is set correctly
- Verify the URL has `https://` and NO trailing slash
- Redeploy frontend after changing environment variables

**Problem: Blank page**
- Solution: Check browser console (F12) for errors
- Make sure Root Directory is set to `frontend`
- Verify build completed successfully

**Problem: "Cannot connect to backend"**
- Solution: Test backend URL directly: `https://your-backend-url.onrender.com/health`
- If backend is down, check Render dashboard
- Free tier backends sleep after 15 minutes of inactivity (first request wakes it up)

---

## 🎯 Quick Reference

### Your Deployment URLs

**Backend (Render):**
- Dashboard: https://dashboard.render.com
- API URL: `https://your-backend-url.onrender.com`
- Health Check: `https://your-backend-url.onrender.com/health`
- API Docs: `https://your-backend-url.onrender.com/docs`

**Frontend (Vercel):**
- Dashboard: https://vercel.com/dashboard
- App URL: `https://your-frontend-url.vercel.app`

### Environment Variables Summary

**Backend (Render) - 5 variables:**
1. `GROQ_API_KEY`
2. `TAVILY_API_KEY`
3. `GMAIL_EMAIL`
4. `GMAIL_APP_PASSWORD`
5. `FROM_NAME`

**Frontend (Vercel) - 1 variable:**
1. `VITE_API_URL` (your Render backend URL)

---

## 🔄 How to Update Your Deployment

### When you make code changes:

**Option 1: Automatic (Recommended)**
1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
2. Both Render and Vercel will automatically redeploy! ✨

**Option 2: Manual**
1. **Render**: Go to dashboard → Select service → Click "Manual Deploy" → Select "main" branch
2. **Vercel**: Go to dashboard → Select project → Go to "Deployments" → Click "Redeploy"

---

## ⚠️ Important Notes

### Render Free Tier Limitations
- Backend sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for testing)
- To keep it always on, upgrade to paid plan ($7/month)

### Vercel Free Tier Limitations
- 100 GB bandwidth/month
- Unlimited deployments
- Custom domains supported
- More than enough for testing and demos

---

## ✅ Success Checklist

After deployment, verify:
- [ ] Backend health check returns `{"status":"healthy"}`
- [ ] Frontend loads without errors
- [ ] Can fill in the form and submit
- [ ] Agent progresses through all 3 steps
- [ ] Email is received in inbox
- [ ] No console errors in browser (F12)

---

## 🎉 You're Done!

Your FireReach application is now live and accessible from anywhere!

**Share your deployment:**
- Frontend URL: `https://your-app.vercel.app`
- GitHub Repo: https://github.com/kabir005/FireReach-Autonomous-Outreach

**For your interview:**
- Show the live demo
- Walk through the code on GitHub
- Explain the architecture using the README
- Discuss challenges using PROJECT_DESCRIPTION.md

---

## 📞 Need Help?

If you get stuck:
1. Check the troubleshooting section above
2. Look at deployment logs (Render/Vercel dashboards)
3. Test each component separately (backend health, frontend load)
4. Verify all environment variables are set correctly

**Common Issues:**
- 90% of issues are due to incorrect environment variables
- 5% are due to wrong Root Directory settings
- 5% are due to API rate limits or network issues

---

**Good luck with your interview! 🚀**

Built with 🔥 by Kabir Malhotra
