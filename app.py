"""
JIRA Cross-Instance Bug Sync Middleware
Syncs bugs from ANAPLAN (Cloud) to GFDH (Server)
"""

from flask import Flask, render_template, request, jsonify
import requests
import base64
import json
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
ANAPLAN_URL = "https://zurichinsurance.atlassian.net"
GFDH_URL = "https://jira.zurich.com"

ANAPLAN_EMAIL = "patricio.guerrero@zurich.com"
ANAPLAN_TOKEN = os.getenv("ANAPLAN_TOKEN")
GFDH_TOKEN = os.getenv("GFDH_TOKEN")

GFDH_ASSIGNEE = "marina.segala@zurich.com"

# Logging
SYNC_LOG_FILE = "sync_log.json"

def log_sync(anaplan_key, gfdh_key, status, message):
    """Log sync operation"""
    try:
        if os.path.exists(SYNC_LOG_FILE):
            with open(SYNC_LOG_FILE, 'r') as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append({
            "timestamp": datetime.now().isoformat(),
            "anaplan_key": anaplan_key,
            "gfdh_key": gfdh_key,
            "status": status,
            "message": message
        })

        with open(SYNC_LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Logging error: {e}")

def get_anaplan_headers():
    """Get ANAPLAN API headers with Basic Auth"""
    auth_string = f"{ANAPLAN_EMAIL}:{ANAPLAN_TOKEN}"
    auth_b64 = base64.b64encode(auth_string.encode()).decode()
    return {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json"
    }

def get_gfdh_headers():
    """Get GFDH API headers"""
    return {
        "Authorization": f"Bearer {GFDH_TOKEN}",
        "Content-Type": "application/json"
    }

def get_user_by_email_gfdh(email):
    """Find GFDH user by email to get account ID"""
    try:
        headers = get_gfdh_headers()
        resp = requests.get(
            f"{GFDH_URL}/rest/api/2/user/search?username={email}",
            headers=headers,
            timeout=10
        )

        if resp.status_code == 200:
            users = resp.json()
            if users:
                return users[0]  # Return first match
        return None
    except Exception as e:
        print(f"Error finding GFDH user: {e}")
        return None

def fetch_anaplan_bug(bug_key):
    """Fetch bug details from ANAPLAN"""
    try:
        headers = get_anaplan_headers()
        resp = requests.get(
            f"{ANAPLAN_URL}/rest/api/3/issue/{bug_key}",
            headers=headers,
            timeout=10
        )

        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"Status {resp.status_code}", "details": resp.text[:200]}
    except Exception as e:
        return {"error": str(e)}

def create_gfdh_bug(anaplan_bug):
    """Create bug in GFDH with same fields"""
    try:
        print(f"DEBUG: GFDH_TOKEN exists: {bool(GFDH_TOKEN)}, length: {len(GFDH_TOKEN) if GFDH_TOKEN else 0}")
        headers = get_gfdh_headers()
        print(f"DEBUG: headers = {headers}")

        fields = anaplan_bug.get('fields', {})

        # Prepare GFDH payload
        gfdh_payload = {
            "fields": {
                "project": {"key": "GFDH"},
                "summary": fields.get('summary', 'No title'),
                "description": fields.get('description', ''),
                "issuetype": {"name": "Task"},
                "priority": {"name": fields.get('priority', {}).get('name', 'Medium')},
                "labels": [f"sync-from-{anaplan_bug.get('key')}", "cross-instance"]
            }
        }


        resp = requests.post(
            f"{GFDH_URL}/rest/api/2/issue",
            headers=headers,
            json=gfdh_payload,
            timeout=10
        )

        if resp.status_code in [200, 201]:
            created_issue = resp.json()
            return created_issue
        else:
            return {"error": f"Status {resp.status_code}", "full_response": resp.text}
    except Exception as e:
        return {"error": str(e)}

def create_link_anaplan_to_gfdh(anaplan_key, gfdh_key):
    """Create link from ANAPLAN bug to GFDH bug"""
    try:
        headers = get_anaplan_headers()

        # Get available link types
        resp = requests.get(
            f"{ANAPLAN_URL}/rest/api/3/issueLinkType",
            headers=headers,
            timeout=10
        )

        if resp.status_code != 200:
            return {"error": f"Could not fetch link types: {resp.status_code}"}

        link_types = resp.json().get('issueLinkTypes', [])
        if not link_types:
            return {"error": "No link types available"}

        # Use first link type
        link_type_id = link_types[0].get('id')

        # Create link
        link_payload = {
            "type": {"id": link_type_id},
            "outwardIssue": {"key": anaplan_key},
            "inwardIssue": {"key": gfdh_key}
        }

        resp = requests.post(
            f"{ANAPLAN_URL}/rest/api/3/issueLink",
            headers=headers,
            json=link_payload,
            timeout=10
        )

        if resp.status_code in [201, 204]:
            return {"success": True}
        else:
            return {"error": f"Status {resp.status_code}", "details": resp.text[:200]}
    except Exception as e:
        return {"error": str(e)}

def create_link_gfdh_to_anaplan(gfdh_key, anaplan_key):
    """Create link from GFDH bug back to ANAPLAN bug"""
    try:
        headers = get_gfdh_headers()

        # Get available link types
        resp = requests.get(
            f"{GFDH_URL}/rest/api/2/issueLinkType",
            headers=headers,
            timeout=10
        )

        if resp.status_code != 200:
            return {"error": f"Could not fetch link types: {resp.status_code}"}

        link_types = resp.json().get('issueLinkTypes', [])
        if not link_types:
            return {"error": "No link types available"}

        # Use first link type
        link_type_id = link_types[0].get('id')

        # Create link
        link_payload = {
            "type": {"id": link_type_id},
            "outwardIssue": {"key": gfdh_key},
            "inwardIssue": {"key": anaplan_key}
        }

        resp = requests.post(
            f"{GFDH_URL}/rest/api/2/issueLink",
            headers=headers,
            json=link_payload,
            timeout=10
        )

        if resp.status_code in [201, 204]:
            return {"success": True}
        else:
            return {"error": f"Status {resp.status_code}", "details": resp.text[:200]}
    except Exception as e:
        return {"error": str(e)}

# Routes

@app.route('/')
def index():
    """Home page with sync form"""
    return render_template('index.html')

@app.route('/api/sync', methods=['POST'])
def sync_bug():
    """Sync bug from ANAPLAN to GFDH"""
    data = request.json
    anaplan_key = data.get('bug_key', '').upper()

    if not anaplan_key:
        return jsonify({"success": False, "error": "No bug key provided"}), 400

    # Step 1: Fetch ANAPLAN bug
    print(f"\n[1] Fetching ANAPLAN bug: {anaplan_key}")
    anaplan_bug = fetch_anaplan_bug(anaplan_key)

    if "error" in anaplan_bug:
        error_msg = f"Could not fetch ANAPLAN bug: {anaplan_bug.get('error')}"
        print(f"ERROR: {error_msg}")
        log_sync(anaplan_key, None, "FAILED", error_msg)
        return jsonify({"success": False, "error": error_msg}), 400

    print(f"✓ Found: {anaplan_bug.get('key')} - {anaplan_bug.get('fields', {}).get('summary', '')[:60]}")

    # Step 2: Create GFDH bug
    print(f"\n[2] Creating bug in GFDH...")
    gfdh_bug = create_gfdh_bug(anaplan_bug)

    if "error" in gfdh_bug:
        error_msg = f"Could not create GFDH bug: {gfdh_bug.get('error')}"
        print(f"ERROR: {error_msg}")
        log_sync(anaplan_key, None, "FAILED", error_msg)
        return jsonify({"success": False, "error": error_msg}), 500

    gfdh_key = gfdh_bug.get('key')
    print(f"✓ Created: {gfdh_key}")

    # Step 3: Create links
    print(f"\n[3] Creating bidirectional links...")

    link1 = create_link_anaplan_to_gfdh(anaplan_key, gfdh_key)
    if "error" in link1:
        print(f"Warning (link ANAPLAN→GFDH): {link1.get('error')}")
    else:
        print(f"✓ Linked ANAPLAN→GFDH")

    link2 = create_link_gfdh_to_anaplan(gfdh_key, anaplan_key)
    if "error" in link2:
        print(f"Warning (link GFDH→ANAPLAN): {link2.get('error')}")
    else:
        print(f"✓ Linked GFDH→ANAPLAN")

    # Log success
    success_msg = f"Bug synced successfully. ANAPLAN: {anaplan_key} → GFDH: {gfdh_key}"
    print(f"\n✓ {success_msg}")
    log_sync(anaplan_key, gfdh_key, "SUCCESS", success_msg)

    return jsonify({
        "success": True,
        "message": success_msg,
        "anaplan_key": anaplan_key,
        "gfdh_key": gfdh_key
    }), 200

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get sync history"""
    try:
        if os.path.exists(SYNC_LOG_FILE):
            with open(SYNC_LOG_FILE, 'r') as f:
                logs = json.load(f)
            return jsonify(logs), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
