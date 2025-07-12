import time
import base64
import requests

# --- Securely store and decode sensitive info ---
ENCODED_SOURCE_CHANNEL = 'dGVjaGhvcHNfc2xhY2tfdGVzdDE='
ENCODED_DEST_CHANNEL = 'dGVjaGhvcHNfc2xhY2tfdGVzdDI='
ENCODED_TOKEN = 'eG94Yi0yMTUyNjAxMDg3LTEyMjIyOTM5NzYzNDMtWnUyRGhYSWphb3NkR0NhTEhiM0hab25E'

SOURCE_CHANNEL = base64.b64decode(ENCODED_SOURCE_CHANNEL).decode()
DEST_CHANNEL = base64.b64decode(ENCODED_DEST_CHANNEL).decode()
SLACK_TOKEN = base64.b64decode(ENCODED_TOKEN).decode()

def get_channel_id(channel_name):
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    params = {"limit": 1000}
    response = requests.get(url, headers=headers, params=params).json()
    if not response.get("ok"):
        print("Error fetching channel list:", response)
        return None
    for ch in response["channels"]:
        if ch["name"] == channel_name.lstrip("#_"):
            return ch["id"]
    print(f"Channel {channel_name} not found.")
    return None

def get_latest_messages(channel_id, latest_ts=None):
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    params = {"channel": channel_id}
    if latest_ts:
        params["oldest"] = latest_ts
    response = requests.get(url, headers=headers, params=params).json()
    if not response.get("ok"):
        print("Error fetching messages:", response)
        return []
    return response.get("messages", [])

def post_message(channel_id, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"channel": channel_id, "text": text}
    response = requests.post(url, headers=headers, json=payload).json()
    if not response.get("ok"):
        print("Error posting message:", response)

def list_all_channels():
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    params = {"limit": 1000, "types": "public_channel,private_channel"}
    response = requests.get(url, headers=headers, params=params).json()
    if not response.get("ok"):
        print("Error fetching channel list:", response)
        return
    print("Channels your bot can see:")
    for ch in response["channels"]:
        print(f"Name: {ch['name']}, ID: {ch['id']}, is_private: {ch.get('is_private', False)}")

if __name__ == "__main__":
    list_all_channels()
    print("Resolving channel IDs...")
    source_id = get_channel_id(SOURCE_CHANNEL)
    dest_id = get_channel_id(DEST_CHANNEL)
    if not source_id or not dest_id:
        print("Could not resolve channel IDs. Exiting.")
        exit(1)

    print(f"Relaying messages from {SOURCE_CHANNEL} to {DEST_CHANNEL}...")
    last_ts = None
    while True:
        messages = get_latest_messages(source_id, latest_ts=last_ts)
        # Sort oldest to newest
        messages = sorted(messages, key=lambda x: x['ts'])
        for msg in messages:
            if 'subtype' not in msg and 'text' in msg:
                post_message(dest_id, msg['text'])
                last_ts = msg['ts']
        time.sleep(5)

    import base64
    print(base64.b64encode(b'techhops_slack_test1').decode())
    print(base64.b64encode(b'techhops_slack_test2').decode())
