import time
from slack_sdk import WebClient

SLACK_BOT_TOKEN = 'xoxb-2152601087-1222293976343-Zu2DhXIjaosdGCaLHb3HZonD'
SOURCE_CHANNEL_ID = 'C0959QX9MMH'  # techhops_slack_test1
TARGET_CHANNEL_ID = 'C095EP3QJN6'  # techhops_slack_test2

client = WebClient(token=SLACK_BOT_TOKEN)

latest_ts = None

while True:
    # Fetch latest messages
    response = client.conversations_history(channel=SOURCE_CHANNEL_ID, oldest=latest_ts)
    messages = response['messages']
    messages = [m for m in messages if not m.get('bot_id')]  # Ignore bot messages

    # Post new messages to target channel
    for message in reversed(messages):  # Oldest first
        text = message['text']
        client.chat_postMessage(channel=TARGET_CHANNEL_ID, text=text)
        latest_ts = message['ts']

    time.sleep(5)  # Poll every 5 seconds