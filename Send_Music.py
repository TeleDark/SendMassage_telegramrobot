import requests

#token bot
token = "Your robot token"
# chanel or group id
chat_id = "Your chat id"  # chat id

with open('ahd.mp3','rb') as audio:
    payload = {
        'chat_id': "@chat or chanel id",
        'title': 'music title',
        'caption' : "caption file",
        'parse_mode': 'HTML'
        }
    files = {
        'audio' : audio.read(),
        }
    

resp = requests.post("https://api.telegram.org/bot{token}/sendAudio".format(token=token),data=payload,files=files).json()

