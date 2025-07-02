# GitHub Webhook Event Tracker

This project is part of the TechStaX assignment to demonstrate GitHub webhook integration using Python, Flask, and MongoDB.

## 📦 Features

- Receives GitHub webhook events (push, pull request, merge)
- Stores event messages in MongoDB
- Displays them in a clean UI
- Auto-refreshes every 15 seconds
- Light/Dark theme toggle

## ⚙️ Technologies Used

- Python + Flask
- HTML, CSS, JavaScript
- MongoDB (local)
- Ngrok (for webhook tunneling)

## 🚀 How to Run

1. Start MongoDB:


2. Start Flask:


3. Start Ngrok in a separate terminal:

4. Add the Ngrok URL + `/webhook` as a webhook to your `action-repo` on GitHub.

5. Open browser at:
