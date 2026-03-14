#!/usr/bin/env python3
"""
SMS Policy - Ultra-minimal Flask app that serves the SMS compliance policy.
Deploy to Railway as a standalone service.
"""

import os
from pathlib import Path
from flask import Flask, send_file

app = Flask(__name__)

# Try to read SMS policy from the OPsKPI repo location
SMS_POLICY_FILE = Path(__file__).parent.parent / "OPsKPI" / ".streamlit" / "static" / "sms_policy.html"

# Fallback to current directory
if not SMS_POLICY_FILE.exists():
    SMS_POLICY_FILE = Path(__file__).parent / "sms_policy.html"

print(f"SMS Policy file: {SMS_POLICY_FILE}")
print(f"File exists: {SMS_POLICY_FILE.exists()}")


@app.route("/_stcore/static/sms_policy.html")
@app.route("/sms_policy.html")
@app.route("/public/sms_policy.html")
@app.route("/")
def serve_sms_policy():
    """Serve the SMS policy HTML file."""
    if SMS_POLICY_FILE.exists():
        return send_file(SMS_POLICY_FILE, mimetype="text/html")
    return "SMS Policy file not found", 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
