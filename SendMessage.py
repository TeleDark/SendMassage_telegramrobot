import requests
import re
from bs4 import BeautifulSoup


#token bot
bot_token = "Your robot token"
# chanel or group id
chanel_id = "Your chat id"  # chat id

def normalize(digit):
    arabic = '٠١٢٣٤٥٦٧٨٩'
    persian = '۰۱۲۳۴۵۶۷۸۹'
    for i in range(len(arabic)):
        digit = digit.replace(arabic[i], persian[i])
    return digit


# receive data from api
req = requests.get("https://www.azangoo.ir/owghat/irn/%D9%85%D8%A7%D8%B1%D8%A7%D9%86%D8%AF%DB%8C%D8%B2-(%D8%B1%D9%88%D8%B3%D8%AA%D8%A7).html")
soup = BeautifulSoup(req.text, 'html.parser')
data = soup.find('div', class_='container bc2 p1')

# find data with css class
data_religious = data.find('table', class_='rooz')
data_re = data_religious.find_all('tr')
#normalize and split data with regex
regex = r'..:..:..'
times = []
for i in range(3, 9):
    text = normalize(data_re[i].text)
    times.append(re.search(regex, text).group())
data_date= normalize(data.find('td', class_='date1').text)

output = ("""
سلام اعضای محترم کانال صبحتون بخیر

🕌اوقات شرعی {}🕌
    ‏———————————————
    به افق 
    ‏———————————————
    اوقات شرعی امروز
    🏙 اذان صبح {}
    🌅 طلوع آفتاب {}
    ☀️ اذان ظهر {}
    🌄 غروب افتاب {}
    🌃 اذان مغرب {}
    🌘 نیمه شب {}
    @
""".format(data_date, times[0], times[1], times[2], times[3], times[4], times[5]))

#send message
requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, chanel_id, output))