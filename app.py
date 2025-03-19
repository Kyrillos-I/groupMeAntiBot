from flask import Flask, request, jsonify
import requests
import os 
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

groupMeToken = os.getenv("GROUPME_ACCESS_TOKEN")
groupId = os.getenv("GROUP_ID")
botId = os.getenv("BOT_ID")

groupMeUrl = "https://api.groupme.com/v3"
token = "?token="+groupMeToken
PORT = int(os.getenv("PORT", 5000))  # Railway assigns a port dynamically

GROUPME_POST_URL = groupMeUrl+"/bots/post"

@app.route("/", methods=["POST"])
def groupme_callback():
    """Handle incoming messages from GroupMe."""
    data = request.get_json()

    if data:
        sender_name = data.get("name", "Unknown")
        sender_id = data.get("sender_id")
        message_id = data.get("id")
        message_text = data.get("text", "")
        print(f"@{sender_name}, you said: {message_text}")
        if message_text.find("tickets")!=-1: 
                delete = requests.delete(groupMeUrl+"/conversations/"+groupId+"/messages/"+message_id+token)
                if delete.status_code == 204:
                    print("Succesful deletion")
                else: 
                    print(f"Error: {delete.status_code}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)