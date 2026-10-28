# JIRA Cross-Instance Bug Sync Middleware
## Deployment & Setup Guide

---

## What This Does

Creates bugs in GFDH automatically when you sync from ANAPLAN:

```
User clicks "Sync to GFDH" button
    ↓
Middleware reads ANAPLAN bug details:
  - Title
  - Description
  - Priority
  - Issue Type (Bug)
    ↓
Middleware creates EXACT MATCH bug in GFDH:
  - Same title, description, priority
  - Assigned to: marina.segala@zurich.com
  - Labeled with: sync-from-ANAPLAN-XXX
    ↓
Middleware creates bidirectional links:
  - ANAPLAN bug → GFDH bug
  - GFDH bug → ANAPLAN bug
    ↓
Result: User sees confirmation with both bug keys
```

---

## Quick Start (Local Testing)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python app.py
```

Open: **http://localhost:5000**

### 3. Test It

1. Enter: `ANAPLAN-824`
2. Click "Sync to GFDH"
3. Wait for confirmation
4. Check GFDH for new bug

---

## Deploy to Render.com (FREE)

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up (free tier)
3. Connect GitHub (optional for auto-deploy) or use CLI

### Step 2: Create Web Service

**Via Dashboard:**
1. Click **"New +"** → **"Web Service"**
2. Choose **"Public Git repository"**
3. Paste repo URL (if using GitHub) or skip to manual deploy

**Manual Deploy:**
1. Install Render CLI: `npm install -g @render-platform/cli`
2. Or use the Render dashboard "Upload" option

### Step 3: Configure Service

**Settings:**
- **Name:** `jira-bug-sync`
- **Runtime:** `Python 3.11`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

**Environment Variables:**
```
ANAPLAN_TOKEN=<your-anaplan-token>
GFDH_TOKEN=<your-gfdh-token>
```
(Set these in Render dashboard → Environment)

### Step 4: Deploy

Click **"Deploy"** and wait ~2-3 minutes

You'll get a URL like: `https://jira-bug-sync.onrender.com`

### Step 5: Test Live

1. Go to: `https://jira-bug-sync.onrender.com`
2. Enter bug key and sync
3. Done!

---

## How to Use

### Simple Flow

**Every time you create a bug in ANAPLAN:**

1. Go to your bookmark: `https://jira-bug-sync.onrender.com`
2. Enter bug key (e.g., `ANAPLAN-824` or just `824`)
3. Click "Sync to GFDH"
4. Wait for success confirmation
5. New bug appears in GFDH with all fields

### View Sync History

1. Click "View Logs" on the web page
2. See all past syncs with timestamps
3. Check success/failure for each

---

## Future Enhancement: Auto-Webhook

Once you get admin access from Martin Rocha:

1. I'll reconfigure to use ANAPLAN webhooks
2. No more manual button clicks
3. Bugs sync automatically when created
4. Same middleware, just triggered differently

---

## Troubleshooting

### Issue: "Could not fetch ANAPLAN bug"
- **Check:** Is the bug key correct? (e.g., ANAPLAN-824, not ANAPLAN824)
- **Check:** Does the bug exist in ANAPLAN?
- **Check:** Can you access it in ANAPLAN UI?

### Issue: "Could not create GFDH bug"
- **Check:** Are you a user in GFDH?
- **Check:** Do you have permission to create bugs?
- **Contact:** Ask GFDH admin

### Issue: "Links failed"
- Bug is still created, just not linked
- You can manually link in UI as backup
- Log entry shows which link failed

### Issue: "Marina not assigned"
- Email might not exist in GFDH
- Check: marina.segala@zurich.com is in GFDH
- If not, contact GFDH admin to add her

---

## Configuration

### Change Assignee

Edit line 26 in `app.py`:
```python
GFDH_ASSIGNEE = "new.email@zurich.com"
```

Then redeploy.

### Change Label

Edit line in `create_gfdh_bug()`:
```python
"labels": [f"sync-from-{anaplan_bug.get('key')}", "your-label-here"]
```

---

## Security Notes

⚠️ **Tokens are embedded in environment variables on Render**

- They're NOT in the repo
- They're NOT in the code
- They're only in Render's secure vault

**After UAT is done:** Revoke both tokens and regenerate.

---

## Support

If something breaks:

1. Check the logs on the web page
2. Check Render's build/deploy logs
3. Contact me with the error message

---

## Timeline

- **Today:** Manual button deployed and tested locally
- **Once Martin approves webhook access:** Switch to full automation
- **UAT phase:** Use as-is (manual button is fine)
- **Post-UAT:** Archive or upgrade to webhook-based

