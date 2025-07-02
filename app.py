from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

# Connect to MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["github_events"]
    collection = db["events"]
    client.admin.command('ping')
    print("✅ MongoDB connection successful")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def github_webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    print("📬 Webhook received")
    print("Event Type:", event_type)

    try:
        if event_type == "push":
            author = payload['pusher']['name']
            to_branch = payload['ref'].split('/')[-1]
            timestamp = datetime.utcnow().replace(tzinfo=pytz.UTC)
            msg = f"{author} pushed to {to_branch} on {timestamp.strftime('%d %B %Y - %I:%M %p UTC')}"
        
        elif event_type == "pull_request":
            action = payload['action']
            if action == 'opened':
                author = payload['pull_request']['user']['login']
                from_branch = payload['pull_request']['head']['ref']
                to_branch = payload['pull_request']['base']['ref']
                timestamp = datetime.strptime(payload['pull_request']['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                msg = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp.strftime('%d %B %Y - %I:%M %p UTC')}"
            
            elif action == 'closed' and payload['pull_request']['merged']:
                author = payload['pull_request']['user']['login']
                from_branch = payload['pull_request']['head']['ref']
                to_branch = payload['pull_request']['base']['ref']
                timestamp = datetime.utcnow().replace(tzinfo=pytz.UTC)
                msg = f"{author} merged branch {from_branch} to {to_branch} on {timestamp.strftime('%d %B %Y - %I:%M %p UTC')}"
            else:
                return "Ignored pull request action", 200
        
        else:
            return "Event not tracked", 200

        print("📦 Storing to MongoDB:", msg)
        result = collection.insert_one({
            "message": msg,
            "timestamp": timestamp
        })
        print("✅ Inserted with ID:", result.inserted_id)

        return "Event processed", 200

    except Exception as e:
        print("❌ Error processing event:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    data = list(collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(10))
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
