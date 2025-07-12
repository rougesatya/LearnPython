import requests


# slack_link = os.environ['slack_link']
slack_link='https://slack.com/api/'
# slack_token_debugChannel = os.environ['slack_token']
slack_token_debugChannel='xoxb-2152601087-1222293976343-Zu2DhXIjaosdGCaLHb3HZonD'
# slack_debugChannel = f"#{os.environ['slack_test_channel']}"
slack_debugChannel='test_p1_alert'

class slackHandler:

    def __init__(self, token=slack_token_debugChannel):
        self.__token = token

    def postMessage(self, message, channel=slack_debugChannel):
        url = f'{slack_link}chat.postMessage'
        payload = {
            "text": message,
            "channel": channel
        }
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'link_names': '1',
            'Authorization': f'Bearer {self.__token}'
        }
        return requests.request("POST", url, headers=headers, json=payload)

    def postFile(self, fileName, channel):
        url = "https://slack.com/api/files.upload"
        headers = {
            "Authorization": f"Bearer {slack_token_debugChannel}", }
        payload = {"channels": channel}

        file_upload = {
            "file": (fileName,
                     open(fileName, 'rb'), 'text/plain')
        }

        response = requests.post(url, headers=headers, files=file_upload, data=payload)

        print(response.json())


    def deleteSlackMsg(self,ts,channel):
        url = f'{slack_link}chat.delete'
        headers = {'Authorization': f'Bearer {self.__token}'}
        payload = {
            "ts": ts,
            "channel": channel
        }
        return requests.post(url=url, json=payload, headers=headers).json()

    def getLatestMsgsFromChannelByUser(self,user,channel,type='user'):
        method = 'conversations.history'
        params = {'channel': channel}
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        res = requests.get(url=f'{slack_link}{method}', headers=headers, params=params).json()
        msgs = []
        for msg in res['messages']:
            if type == 'bot_message':
                if msg.get('subtype',None) == type and msg.get('bot_id',None) == user:
                    msgs.append(msg)
            else:
                if msg['user'] == user:
                    msgs.append(msg)
        return msgs

