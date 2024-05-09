import requests, json
from flask import Flask, request

app = Flask(__name__)

FACEBOOK_APP_ID = '7477882075624318'
SECRET_APP_KEY = 'ab6d3dc4207581df83902c06ba1cb5cc'
PAGE_ACCESS_TOKEN = 'Working on it...'

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if request.args.get('hub.verify_token') == '200':
            return request.args.get('hub.challenge')
        else:
            return 'Verification token mismatch', 403
    else:
        return 'Invalid request', 400

@app.route('/', methods=['POST'])
def handle_messages():
    payload = request.get_json()
    for entry in payload['entry']:
        for messaging_event in entry['messaging']:
            if messaging_event.get('message'):
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                message_text = messaging_event['message']['text']
                send_message(sender_id, message_text)
    return 'ok'

def send_message(sender_id, message_text):
    url = f'https://graph.facebook.com/{sender_id}/messages'
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': message_text},
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {PAGE_ACCESS_TOKEN}',
    }
    requests.post(url, data=json.dumps(data), headers=headers)

if __name__ == '__main__':
    app.run()