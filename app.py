from flask import Flask, request, jsonify
from collections import defaultdict
import os

app = Flask(__name__)

# Replace EMAIL with your actual logged-in email before deploying
API_KEY = "ak_7hie3n2wf2e2i71u4r2ixktw"
EMAIL = "claude-agent@anthropic.com"


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "*"
    return resp


@app.route("/analytics", methods=["POST", "OPTIONS"])
def analytics():
    if request.method == "OPTIONS":
        return "", 204

    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True, silent=True) or {}
    events = data.get("events", [])

    total_events = len(events)
    users = set()
    revenue = 0.0
    user_totals = defaultdict(float)

    for e in events:
        user = e.get("user")
        amount = e.get("amount", 0)
        users.add(user)
        if amount and amount > 0:
            revenue += amount
            user_totals[user] += amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None

    return jsonify({
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8003))
    app.run(host="0.0.0.0", port=port)
