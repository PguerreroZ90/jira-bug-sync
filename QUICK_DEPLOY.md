# Deploy to Render.com in 5 Minutes

## Step 1: Prepare Files (DONE ✅)

All files are ready in this folder:
```
✅ app.py
✅ requirements.txt
✅ templates/index.html
✅ render.yaml
✅ .gitignore
```

## Step 2: Push to GitHub (2 min)

### Option A: Use GitHub Web UI (Easiest)

1. Go to https://github.com/new
2. Create repo: `jira-bug-sync`
3. Clone locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/jira-bug-sync.git
   cd jira-bug-sync
   ```
4. Copy all files from `jira_sync_middleware/` into this folder
5. Push:
   ```bash
   git add .
   git commit -m "Initial commit: JIRA bug sync middleware"
   git push
   ```

### Option B: GitHub CLI (If you have it)

```bash
cd jira_sync_middleware
gh repo create jira-bug-sync --public --source=. --remote=origin --push
```

---

## Step 3: Deploy to Render (2 min)

### Option 1: Via Render Dashboard (Recommended)

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Select **"GitHub"** (it will ask to connect)
4. Search for & select your `jira-bug-sync` repo
5. **Configure:**
   - **Name:** `jira-bug-sync`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free
6. Click **"Create Web Service"**
7. Wait ~2-3 minutes for build
8. You'll get a URL like: `https://jira-bug-sync.onrender.com`

### Option 2: Via render.yaml (Automated)

If you use `render.yaml`:
1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Select **"GitHub"** → your repo
3. Render will auto-detect `render.yaml` and use those settings
4. Click **"Create Web Service"**
5. Wait for deploy

---

## Step 4: Test Your Deployment (1 min)

1. Go to your new URL: `https://jira-bug-sync.onrender.com`
2. Enter bug key: `ANAPLAN-824` (or create a new one in ANAPLAN)
3. Click **"Sync to GFDH"**
4. Watch it sync!

---

## Verification Checklist

- [ ] GitHub repo created
- [ ] All files pushed to GitHub
- [ ] Render service created
- [ ] Build succeeded (green checkmark in Render dashboard)
- [ ] Service is running (status shows "Live")
- [ ] URL is accessible
- [ ] Test sync works (see new bug in GFDH)

---

## Troubleshooting

### Deploy fails with "build error"
→ Check Render's build log (Dashboard → service → Logs)
→ Most likely: missing dependencies (check `requirements.txt`)

### Service keeps timing out
→ Free tier might be sleeping
→ Click sync button again to wake it up
→ Should work after ~5 sec cold start

### Sync button doesn't work
→ Check browser console (F12 → Console tab)
→ Check Render service logs
→ Verify tokens are correct in render.yaml

### Bug created in GFDH but links failed
→ That's OK! Bug still synced
→ Check sync history logs on web page
→ Manual linking is always an option

---

## What Happens Next

### If sync works ✅
- You're ready for UAT!
- Keep using the web button to sync bugs
- Logs show all history

### Once Martin approves webhooks ✅
- I'll deploy v2.0 with full automation
- No button needed
- Same URL, auto-syncs on bug creation

---

## Live URL

Once deployed, your middleware will be at:

**`https://jira-bug-sync.onrender.com`**

Bookmark this for easy access during UAT!

---

## Questions?

If deploy fails:
1. Check Render logs
2. Share the error message
3. I can help troubleshoot

Ready to deploy? Let me know once you push to GitHub!

