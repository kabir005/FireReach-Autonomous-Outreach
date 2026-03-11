# 🚀 FireReach Deployment Guide

Complete step-by-step guide to deploy FireReach on Vercel (Frontend + Backend).

## Prerequisites

- GitHub account (✅ Done - your repo is live)
- Vercel account (free) - Sign up at https://vercel.com
- Your API keys ready:
  - GROQ_API_KEY
  - TAVILY_API_KEY
  - GMAIL_EMAIL
  - GMAIL_APP_PASSWORD

---

## 🎨 Part 1: Deploy Frontend to Vercel

### Step 1: Sign in to Vercel
1. Go to https://vercel.com
2. Click "Sign Up" or "Log In"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub account

### Step 2: Import Your Repository
1. Click "Add New..." → "Project"
2. Find and select `FireReach-Autonomous-Outreach` from your repositories
3. Click "Import"

### Step 3: Configure Frontend Deployment
1. **Root Directory**: Click "Edit" and set to `frontend`
2. **Framework Preset**: Should auto-detect as "Vite" (if not, select it manually)
3. **Build Command**: `npm run build` (should be auto-filled)
4. **Output Directory**: `dist` (should be auto-filled)
5. **Install Command**: `npm install` (should be auto-filled)

### Step 4: Add Environment Variables
Click "Environment Variables" and add:

| Name | Value |
|------|-------|
| `VITE_API_URL` | Leave empty for now (we'll update after backend deployment) |

### Step 5: Deploy Frontend
1. Click "Deploy"
2. Wait 2-3 minutes for build to complete
3. You'll get a URL like: `https://fire-reach-autonomous-outreach.vercel.app`
4. **Save this URL** - you'll need it!

---

## ⚙️ Part 2: Deploy Backend to Vercel

### Step 1: Create New Project for Backend
1. Go back to Vercel dashboard
2. Click "Add New..." → "Project"
3. Select `FireReach-Autonomous-Outreach` again (yes, same repo)
4. Click "Import"

### Step 2: Configure Backend Deployment
1. **Root Directory**: Click "Edit" and set to `backend`
2. **Framework Preset**: Select "Other"
3. Leave build settings as default

### Step 3: Add Environment Variables (IMPORTANT!)
Click "Environment Variables" and add ALL of these:

| Name | Value | Example |
|------|-------|---------|
| `GROQ_API_KEY` | Your Groq API key | `gsk_...` |
| `TAVILY_API_KEY` | Your Tavily API key | `tvly-...` |
| `GMAIL_EMAIL` | Your Gmail address | `your_email@gmail.com` |
| `GMAIL_APP_PASSWORD` | Your Gmail app password | `abcd efgh ijkl mnop` |
| `FROM_NAME` | FireReach by Rabbitt AI | `FireReach by Rabbitt AI` |

**Important**: Make sure to add these to "Production", "Preview", and "Development" environments!

### Step 4: Deploy Backend
1. Click "Deploy"
2. Wait 2-3 minutes for build to complete
3. You'll get a URL like: `https://fire-reach-backend.vercel.app`
4. **Save this URL** - this is your API URL!

### Step 5: Test Backend
1. Visit: `https://your-backend-url.vercel.app/health`
2. You should see: `{"status":"healthy","configuration_errors":[]}`
3. If you see errors, check your environment variables

---

## 🔗 Part 3: Connect Frontend to Backend

### Step 1: Update Frontend Environment Variable
1. Go to Vercel dashboard
2. Select your **Frontend** project
3. Go to "Settings" → "Environment Variables"
4. Update `VITE_API_URL`:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.vercel.app` (your backend URL from Part 2)
5. Click "Save"

### Step 2: Redeploy Frontend
1. Go to "Deployments" tab
2. Click the three dots (...) on the latest deployment
3. Click "Redeploy"
4. Wait for redeployment to complete

---

## ✅ Part 4: Test Your Deployment

### Step 1: Visit Your Frontend
Go to your frontend URL: `https://your-frontend-url.vercel.app`

### Step 2: Test the Application
1. Fill in the form:
   - **ICP**: "We sell cybersecurity training to Series B startups"
   - **Company**: "Wiz"
   - **Email**: Your email address
2. Click "🚀 Launch FireReach"
3. Watch the agent work through all 3 steps
4. Check your email for the outreach message!

---

## 🎯 Quick Reference

### Your Deployment URLs

**Frontend**: `https://your-frontend-url.vercel.app`
**Backend**: `https://your-backend-url.vercel.app`
**API Docs**: `https://your-backend-url.vercel.app/docs`
**Health Check**: `https://your-backend-url.vercel.app/health`

### Environment Variables Checklist

**Frontend** (1 variable):
- ✅ VITE_API_URL

**Backend** (5 variables):
- ✅ GROQ_API_KEY
- ✅ TAVILY_API_KEY
- ✅ GMAIL_EMAIL
- ✅ GMAIL_APP_PASSWORD
- ✅ FROM_NAME

---

## 🐛 Troubleshooting

### Frontend Issues

**Problem**: "Failed to fetch" or CORS errors
**Solution**: 
1. Make sure VITE_API_URL is set correctly
2. Make sure it includes `https://` and NO trailing slash
3. Redeploy frontend after changing environment variables

**Problem**: Blank page
**Solution**:
1. Check browser console for errors
2. Make sure build completed successfully
3. Check Vercel deployment logs

### Backend Issues

**Problem**: "Configuration errors" in health check
**Solution**:
1. Verify all 5 environment variables are set
2. Check for typos in variable names
3. Make sure Gmail app password is correct (16 characters, no spaces)

**Problem**: "Email sending failed"
**Solution**:
1. Verify Gmail app password is correct
2. Make sure 2FA is enabled on Gmail
3. Check that GMAIL_EMAIL matches the account with app password

**Problem**: "Groq API error"
**Solution**:
1. Verify GROQ_API_KEY is valid
2. Check Groq console for rate limits
3. Make sure key has proper permissions

---

## 🔄 Updating Your Deployment

### When you make code changes:

1. **Commit and push to GitHub**:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

2. **Vercel auto-deploys**: Both frontend and backend will automatically redeploy when you push to GitHub!

### To manually redeploy:
1. Go to Vercel dashboard
2. Select your project
3. Go to "Deployments"
4. Click "Redeploy" on the latest deployment

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Professional frontend with modern UI
- ✅ Scalable backend API
- ✅ Automatic deployments on git push
- ✅ HTTPS enabled by default
- ✅ Global CDN distribution
- ✅ Free hosting (Vercel free tier)

Share your deployment URL and show off your autonomous outreach engine! 🔥

---

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **GitHub Issues**: https://github.com/kabir005/FireReach-Autonomous-Outreach/issues
- **Vercel Support**: https://vercel.com/support

---

**Built with 🔥 by Rabbitt AI**
