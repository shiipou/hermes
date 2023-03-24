import requests

class TwitchApi:

    url:str
    client_id:str
    token:str

    def __init__(self, clientid, token, url='https://api.twitch.tv/helix'):
        self.url = url
        self.client_id = clientid
        self.token = token
    
    def channel_info(self, channel):
        response=requests.get(f'{self.url}/users?login=Captain_Marty_', headers= {"Authorization": f"Bearer {self.token}","Client-ID": self.client_id})
        return response.json()
    
    def stream_info(self, channel):
        response=requests.get(f'{self.url}/streams?user_login=Captain_Marty_', headers= {"Authorization": f"Bearer {self.token}","Client-ID": self.client_id})
        return response.json()