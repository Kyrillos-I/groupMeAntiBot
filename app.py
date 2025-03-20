from flask import Flask, request, jsonify
import requests
import os 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

bannedWords = [
    'tickets', 'ticket',
    'claim',
    'offer', 'promo', 'promotion',
    'lottery', 'cash',
    'bitcoin', 'crypto', 'cryptocurrency',
    'urgent', 'act now', 'guaranteed',
    'bonus', 'investment'
]

def send_deletion_email(deleted_message, bannedWord):
    # Email configuration: it's best to store these in environment variables for security.
    sender_email = os.environ.get('SENDER_EMAIL')  # e.g., 'your_email@example.com'
    receiver_email = os.environ.get('RECEIVER_EMAIL')  # e.g., 'notify_me@example.com'
    email_password = os.environ.get('EMAIL_PASSWORD')  # your email account password or app-specific password

    # Create the email container
    message = MIMEMultipart()
    message['Subject'] = 'GroupMe Message Deleted'
    message['From'] = sender_email
    message['To'] = f"{receiver_email}, {sender_email}"

    # Email body content: include details about the deleted message.
    body = f"This GroupMe message was deleted:\n\n{deleted_message}\n\n It was deleted for containing the word: \n\n{bannedWord}"
    message.attach(MIMEText(body, 'plain'))

    try:
        # Using Gmail's SMTP server.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, email_password)
            server.send_message(message)
        print("Notification email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route("/", methods=["POST"])
def groupme_callback():
    #Handle incoming messages from GroupMe.
    data = request.get_json()

    if data:
        sender_name = data.get("name", "Unknown")
        sender_id = data.get("sender_id")
        message_id = data.get("id")
        message_text = data.get("text", "")
        print(f"@{sender_name}, you said: {message_text}")
        for word in bannedWords:
            if message_text.lower().find(word)!=-1: 
                    delete = requests.delete(groupMeUrl+"/conversations/"+groupId+"/messages/"+message_id+token)
                    if delete.status_code == 204:
                        send_deletion_email(message_text, word)
                        print("Succesful deletion")
                    else:
                        send_deletion_email("ERROR: their was an error deleting the group me message: "+message_text, word ) 
                        print(f"Error: {delete.status_code}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)