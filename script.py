import requests
import os
from dotenv import load_dotenv
load_dotenv()

groupMeToken = os.getenv("GROUPME_ACCESS_TOKEN")
groupId = os.getenv("GROUP_ID")

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
                print("Error: {delete.status_code}")

else: 
    print(f"Error: {messages.status_code}")
