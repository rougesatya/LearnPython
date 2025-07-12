import time
import win32com.client
from slack_sdk import WebClient

# Slack setup
SLACK_BOT_TOKEN = 'xoxb-2152601087-1222293976343-Zu2DhXIjaosdGCaLHb3HZonD'
TARGET_CHANNEL_ID = 'C0963KFRH08'  # your new Slack channel ID

client = WebClient(token=SLACK_BOT_TOKEN)
MY_EMAIL = "satya.prakash.das@walmart.com"

# Outlook setup
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox

last_processed_id = None

def email_matches_criteria(mail):
    to = mail.To or ""
    cc = mail.CC or ""
    # BCC is not directly accessible, but if you received the email, you are in at least one of To/CC/BCC
    return (MY_EMAIL.lower() in to.lower()) or (MY_EMAIL.lower() in cc.lower())

while True:
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)  # Newest first
    if messages.Count > 0:
        mail = messages[0]  # Only check the latest email
        entry_id = mail.EntryID
        if entry_id != last_processed_id:
            if email_matches_criteria(mail):
                subject = mail.Subject
                body = mail.Body
                slack_text = f"*Email to you!*\n*Subject:* {subject}\n*Body:*\n{body[:1000]}"  # Limit body length
                client.chat_postMessage(channel=TARGET_CHANNEL_ID, text=slack_text)
            last_processed_id = entry_id
    time.sleep(30)  # Check every 30 seconds