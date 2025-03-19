import requests
import os
from dotenv import load_dotenv
load_dotenv()

groupMeToken = os.getenv("GROUPME_ACCESS_TOKEN")
groupId = os.getenv("GROUP_ID")
botId = os.getenv("BOT_ID")

groupMeUrl = "https://api.groupme.com/v3"
token = "?token="+groupMeToken
response = requests.get(groupMeUrl+"/groups"+token)



if response.status_code == 200: 
    data=response.json()
    # Extract group name and ID
    for group in data["response"]:
        print(f"Group Name: {group['name']}, Group ID: {group['id']}")
else:
    print(f"Error: {response.status_code}")

messages = requests.get(groupMeUrl+"/groups/"+groupId+"/messages"+token)
if messages.status_code == 200:
    data = messages.json()
    print(data)
    for message in data["response"]["messages"]:
        print(f"Sender: {message['name']}, Message: {message['text']}, ID: {message['id']}")
        if message['text'].find("tickets")!=-1: 
            delete = requests.delete(groupMeUrl+"/conversations/"+groupId+"/messages/"+message['id']+token)
            if delete.status_code == 204:
                print("Succesful deletion")
            else: 
                print(f"Error: {delete.status_code}")

else: 
    print(f"Error: {messages.status_code}")

"""
botData = {
    "bot": {
		"name": "AntiSpam",
		"group_id": ""+groupId,
        "callback_url": "https://web-production-5dfdf.up.railway.app/"
	} 
}
bot = requests.post(groupMeUrl+"/bots"+token, json=botData)
if bot.status_code == 201: 
    print("Bot Deployment Succesful!")
else: 
    print(f"Bot Deployment Failed! Error: {bot.status_code}")


index = requests.get(groupMeUrl+"/bots"+token)
if index.status_code == 200:
    data = index.json()
    print(data)
else :
    print(f"Error: {index.status_code}")

botMsg = {
    "bot_id": botId,
    "text": "Hello, I am here to auto delete spam/scam messages!"
}

send = requests.post(groupMeUrl+"/bots/post"+token, json = botMsg)
if send.status_code == 202:
    print("Success! Message sent!")
else: 
    print(f"Message failed. Error {send.status_code}")


botDelete = {"bot_id": botId}
delete = requests.post(groupMeUrl+"/bots/destroy"+token, json  = botDelete)
if delete.status_code == 200:
    print("Bot deleted succesfully!")
else:
    print(f"Error deleting bot {delete.status_code}")
"""