#Intégration chatGPT
import openai
import datetime

from datetime import timedelta

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
api_last_check : datetime.datetime
channel_info: dict

def generate_response(self, message, channel_settings):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[  {"role": "system", "content": self.personnality},
                        {"role": "system", "content": channel_settings},
                        {"role": "user", "content": message.content},
                ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=1.2,
            frequency_penalty=0,
            presence_penalty=0
        )
        response = completion.choices[0].message.content.strip()
        return response

async def event_message_gpt(self,message):
        api_last_check = None
        if api_last_check is None or api_last_check > timestamp(): 
            api_last_check = datetime.datetime.now() + timedelta(minutes=30)
            stream_info = self.twitchApi.stream_info('Captain_Marty_')
            game_name='offline'
            title='offline'
            try:
                    game_name = stream_info[0].game_name
                    title = stream_info[0].title
            except:
                    pass
            channel_info = {
                    'channel_name': 'Captain_Marty_',
                    'channel_stream_title': title,
                    'channel_stream_category': game_name
            }
        channel_settings = f'{self.channel_rules}'

        for k, v in channel_info.items():
                channel_settings = channel_settings.replace('{{' + k + '}}', str(v))

        # channel_info = await self.twitchApi.channel_info('Captain_Marty_')
        response = generate_response(self, message, channel_settings)
        print(timestamp, self.nick, ": ", response)
        await message.channel.send(f"{response}")

#FIN Intégration chatGPT