# 🚀 FireReach Deployment Guide

Complete guide for deploying FireReach to production.

## Overview

- **Backend**: Deploy to Render.com (or any Python hosting)
- **Frontend**: Deploy to Vercel (or any static hosting)
- **Estimated Time**: 15-20 minutes

---

## Backend Deployment (Render.com)

### Prerequisites
- GitHub account
- Render.com account (free tier available)
- All API keys ready

### Step 1: Prepare Repository

Ensure your code is pushed to GitHub:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Create Render Service

1. Go to https://render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `firereach-api`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables

In Render dashboard, add these environment variables:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
SERPAPI_KEY=your_serpapi_key
SENDGRID_API_KEY=SG.your_sendgrid_key
FROM_EMAIL=noreply@yourdomain.com
FROM_NAME=FireReach by Rabbitt AI
```

**Important**: Use the "Secret File" option for sensitive keys if available.

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for build to complete (2-3 minutes)
3. Note your backend URL: `https://firereach-api.onrender.com`

### Step 5: Test Backend

```bash
curl https://firereach-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "configuration_errors": []
}
```

---

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- Backend URL from previous step

### Step 1: Update Environment Variable

In `frontend/.env`:
```bash
VITE_API_URL=https://firereach-api.onrender.com
```

Commit and push:
```bash
git add frontend/.env
git commit -m "Update API URL for production"
git push origin main
```

### Step 2: Create Vercel Project

1. Go to https://vercel.com/
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 3: Add Environment Variable

In Vercel project settings:
- Go to "Settings" → "Environment Variables"
- Add: `VITE_API_URL` = `https://firereach-api.onrender.com`

### Step 4: Deploy

1. Click "Deploy"
2. Wait for build to complete (1-2 minutes)
3. Note your frontend URL: `https://firereach.vercel.app`

### Step 5: Test Frontend

1. Visit your Vercel URL
2. Fill in the form with test data
3. Click "Launch FireReach"
4. Verify all 3 steps complete successfully

---

## Alternative Deployment Options

### Backend Alternatives

#### Railway.app
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

#### Docker (Self-Hosted)
```bash
cd backend
docker build -t firereach-api .
docker run -p 8000:8000 --env-file .env firereach-api
```

### Frontend Alternatives

#### Netlify
1. Connect GitHub repo
2. Build command: `npm run build`
3. Publish directory: `frontend/dist`
4. Add environment variable: `VITE_API_URL`

#### Cloudflare Pages
1. Connect GitHub repo
2. Framework preset: Vite
3. Build command: `npm run build`
4. Build output: `dist`

---

## Post-Deployment Configuration

### 1. Update CORS Settings

If your frontend is on a different domain, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://firereach.vercel.app",  # Your frontend URL
        "http://localhost:3000"  # Keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Configure Custom Domain (Optional)

#### Backend (Render)
1. Go to Render dashboard → Settings
2. Add custom domain: `api.yourdomain.com`
3. Update DNS records as instructed

#### Frontend (Vercel)
1. Go to Vercel dashboard → Settings → Domains
2. Add custom domain: `firereach.yourdomain.com`
3. Update DNS records as instructed

### 3. Set Up Monitoring

#### Backend Health Checks
Configure Render to ping `/health` every 5 minutes:
- Go to Settings → Health Check Path
- Set to `/health`

#### Error Tracking (Optional)
Add Sentry for error tracking:

```bash
pip install sentry-sdk[fastapi]
```

In `main.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

---

## Environment-Specific Configuration

### Development
```bash
# backend/.env
ANTHROPIC_API_KEY=sk-ant-...
SERPAPI_KEY=test_key
SENDGRID_API_KEY=test_key

# frontend/.env
VITE_API_URL=http://localhost:8000
```

### Staging
```bash
# backend/.env (Render)
ANTHROPIC_API_KEY=sk-ant-...
SERPAPI_KEY=staging_key
SENDGRID_API_KEY=staging_key

# frontend/.env (Vercel)
VITE_API_URL=https://firereach-staging.onrender.com
```

### Production
```bash
# backend/.env (Render)
ANTHROPIC_API_KEY=sk-ant-...
SERPAPI_KEY=production_key
SENDGRID_API_KEY=production_key
FROM_EMAIL=noreply@yourdomain.com

# frontend/.env (Vercel)
VITE_API_URL=https://api.yourdomain.com
```

---

## Security Checklist

Before going to production:

- [ ] All API keys are stored as environment variables (not in code)
- [ ] CORS is configured to allow only your frontend domain
- [ ] HTTPS is enabled on both frontend and backend
- [ ] Rate limiting is configured (if needed)
- [ ] Error messages don't expose sensitive information
- [ ] FROM_EMAIL is verified with your email provider
- [ ] Test with real data to ensure no PII leaks

---

## Performance Optimization

### Backend
1. **Enable Caching**: Cache company signals for 24 hours
2. **Connection Pooling**: Use httpx connection pools
3. **Async All The Way**: Ensure all I/O is async

### Frontend
1. **Code Splitting**: Already handled by Vite
2. **Image Optimization**: Use WebP format for any images
3. **CDN**: Vercel automatically uses CDN

---

## Monitoring & Maintenance

### Key Metrics to Track
- API response time (should be < 20 seconds)
- Error rate (should be < 1%)
- Email delivery rate (should be > 95%)
- Signal harvesting success rate

### Regular Maintenance
- Monitor API key usage and credits
- Check for API deprecations
- Update dependencies monthly
- Review error logs weekly

---

## Troubleshooting

### Backend Won't Start
- Check Render logs for errors
- Verify all environment variables are set
- Test `/health` endpoint

### Frontend Can't Connect
- Verify `VITE_API_URL` is correct
- Check CORS settings in backend
- Look for errors in browser console

### Emails Not Sending
- Verify SendGrid/Resend API key
- Check sender email is verified
- Review email provider logs

### Slow Performance
- Check API rate limits
- Monitor Render resource usage
- Consider upgrading to paid tier

---

## Rollback Procedure

If deployment fails:

### Backend (Render)
1. Go to Render dashboard
2. Click "Manual Deploy" → Select previous commit
3. Deploy

### Frontend (Vercel)
1. Go to Vercel dashboard → Deployments
2. Find previous successful deployment
3. Click "..." → "Promote to Production"

---

## Cost Estimates

### Free Tier (Development)
- Render: Free (with sleep after inactivity)
- Vercel: Free (100GB bandwidth)
- Anthropic: $5 free credit
- SerpAPI: 100 free searches/month
- SendGrid: 100 free emails/day
- **Total**: ~$0/month (within free limits)

### Production (Low Volume)
- Render: $7/month (Starter plan)
- Vercel: Free (within limits)
- Anthropic: ~$10/month (100 requests)
- SerpAPI: $50/month (5,000 searches)
- SendGrid: $15/month (up to 40,000 emails)
- **Total**: ~$82/month

### Production (High Volume)
- Render: $25/month (Standard plan)
- Vercel: $20/month (Pro plan)
- Anthropic: ~$100/month (1,000 requests)
- SerpAPI: $150/month (20,000 searches)
- SendGrid: $90/month (up to 100,000 emails)
- **Total**: ~$385/month

---

## Support

For deployment issues:
- Check [DOCS.md](./DOCS.md) for configuration
- Review [TESTING.md](./TESTING.md) for validation
- Check Render/Vercel logs for errors

---

**Ready to deploy!** 🚀
