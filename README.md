# JIRA Cross-Instance Bug Sync Middleware

**Status:** ✅ Ready to Deploy

## What You Have

A **simple web app** that creates bugs in GFDH automatically when you click a button in ANAPLAN.

```
Files created:
  ✅ app.py                    - Flask backend (bug sync logic)
  ✅ templates/index.html      - Web UI (form + logs)
  ✅ requirements.txt          - Python dependencies
  ✅ DEPLOYMENT_GUIDE.md       - Setup instructions
  ✅ README.md                 - This file
```

## Quick Start

### Local Testing (Right Now)

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python app.py

# Open browser
http://localhost:5000
```

### Deploy to Render.com (Free)

See **DEPLOYMENT_GUIDE.md** for step-by-step instructions.

**Cost:** FREE (Render free tier)  
**Wake Time:** Auto-wakes when you click sync button  
**Downtime:** Auto-sleeps after 15 min inactivity (fine for UAT)

## How to Use

1. **Create a bug in ANAPLAN** (e.g., ANAPLAN-824)
2. **Go to:** https://jira-bug-sync.onrender.com
3. **Enter bug key:** ANAPLAN-824 (or just 824)
4. **Click:** "Sync to GFDH"
5. **See confirmation:** Bug created in GFDH as GFDH-YYYY

## What Happens When You Sync

**ANAPLAN Bug:**
```
Title: "Login button not working"
Description: "Users can't click login..."
Priority: "High"
Type: "Bug"
```

**GFDH Bug (Auto-Created):**
```
Title: "Login button not working"          ← SAME
Description: "Users can't click login..."  ← SAME
Priority: "High"                           ← SAME
Type: "Bug"                                ← SAME
Assignee: marina.segala@zurich.com         ← AUTO-SET
Labels: sync-from-ANAPLAN-824              ← AUTO-TAGGED
```

**Links Created:**
- ANAPLAN-824 → GFDH-YYYY ✅
- GFDH-YYYY → ANAPLAN-824 ✅

## Next Steps

### Option 1: Test Locally First
```bash
pip install -r requirements.txt
python app.py
# Test with ANAPLAN-824 or another bug
```

### Option 2: Deploy to Render Now
Follow **DEPLOYMENT_GUIDE.md**

### Option 3: Wait for Martin's Approval
Once you get webhook admin access from Martin Rocha, I can:
- Remove manual button
- Auto-sync on ANAPLAN bug creation
- Same app, just triggered differently

---

## FAQ

**Q: Does this work on free Render tier?**  
A: Yes. It sleeps after 15 min but wakes instantly when you click sync.

**Q: What if sync fails?**  
A: Check the logs on the web page. Most common: bug key not found or Gfdh permission issue.

**Q: Can I change who gets assigned in GFDH?**  
A: Yes. Edit `GFDH_ASSIGNEE` in `app.py` and redeploy.

**Q: Is this secure?**  
A: Yes. Tokens live in Render's encrypted vault, not in code.

**Q: What happens when Martin approves webhooks?**  
A: This app becomes fully automatic. No button needed.

---

## Files Location

```
C:\Users\PATRICIO.GUERRERO\OneDrive - Zurich Insurance\Documents\Anaplan & EPM documents\jira_sync_middleware\
├── app.py                           (Flask backend)
├── requirements.txt                 (Dependencies)
├── templates/
│   └── index.html                   (Web UI)
├── DEPLOYMENT_GUIDE.md              (Setup instructions)
├── README.md                        (This file)
└── sync_log.json                    (Auto-created, stores history)
```

---

## Ready?

1. **Test locally:** `python app.py` → http://localhost:5000
2. **Or deploy to Render:** Follow DEPLOYMENT_GUIDE.md
3. **Or wait:** I can help with either when you're ready

Let me know! 👍

