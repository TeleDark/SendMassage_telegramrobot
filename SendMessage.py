import requests
import requests_random_user_agent
import re
from bs4 import BeautifulSoup

s = requests.Session()
headers = s.headers

# token bot
bot_token = ""
# channel or group id
chanel_id = "@example-channel"  # chat id
weather_status_text = {'light rain': 'ﺎﺤﺘﻣﺎﻟ ﺏﺍﺮﺷ🌤 ',
                       'sky is clear': 'ﺂﺴﻣﺎﻧ ﺹﺎﻓ☀️',
                       'clear sky': 'ﺂﺴﻣﺎﻧ ﺹﺎﻓ☀️',
                       'overcast clouds': 'ﺎﺑﺮﯾ🌤 ',
                       'moderate rain': 'ﺏﺍﺭﺎﻨﯾ🌧 ',
                       'scattered clouds': 'ﺎﺑﺮﻫﺎﯾ ﭖﺭﺎﮑﻧﺪﻫ☁️',
                       'broken clouds': 'ﺎﺑﺮﻫﺎﯾ ﭖﺭﺎﮑﻧﺪﻫ☁️',
                       'rain and snow': 'ﺏﺍﺭﺎﻧ ﻭ ﺏﺮﻓ🌨 ',
                       'few clouds': 'ﮏﻤﯾ ﺎﺑﺮﯾ🌤 ',
                       'light snow': 'ﺏﺮﻔﯾ❄️',
                       'snow':  'ﺏﺮﻔﯾ❄️',
                       'heavy intensity rain': "ﺏﺍﺭﺎﻧ ﺵﺪﯾﺩ⛈ "
                       }
week_day_zekr = {
    "ﺶﻨﺒﻫ": "ﯼﺍ ﺮﺑ ﺎﻠﻋﺎﻠﻤﯿﻧ",
    "ﯽﮑﺸﻨﺒﻫ": "ﯼﺍ ﺫﺍﺎﻠﺟﻼﻟ ﻭ ﺍﻼﮐﺭﺎﻣ",
    "ﺩﻮﺸﻨﺒﻫ": "ﯼﺍ ﻕﺎﻀﯾ ﺎﻠﺣﺎﺟﺎﺗ",
    "ﺲﻫ ﺶﻨﺒﻫ": "ﯼﺍ ﺍﺮﺤﻣ ﺎﻟﺭﺎﺤﻤﯿﻧ",
    "ﭻﻫﺍﺮﺸﻨﺒﻫ": "ﯼﺍ ﺢﯾ ﯼﺍ ﻖﯾﻮﻣ",
    "ﭗﻨﺟ ﺶﻨﺒﻫ": "ﻻ ﺎﻠﻫ ﺍﻻ ﺎﻠﻠﻫ ﺎﻠﻤﻠﮐ ﺎﻠﺤﻗ ﺎﻠﻤﺒﯿﻧ",
    "ﺞﻤﻌﻫ": "ﺎﻠﻠﻬﻣ ﺺﻟ ﻊﻠﯾ ﻢﺤﻣﺩ ﻭ ﺂﻟ ﻢﺤﻣﺩ"
}
def normalize_en(digit):
    arabic = '0123456789'
    persian = '۰۱۲۳۴۵۶۷۸۹'
    for i in range(len(arabic)):
        digit = digit.replace(arabic[i], persian[i])
    return digit


def normalize(digit):
    arabic = '٠١٢٣٤٥٦٧٨٩'
    persian = '۰۱۲۳۴۵۶۷۸۹'
    for i in range(len(arabic)):
        digit = digit.replace(arabic[i], persian[i])
    return digit


# receive data from api weather
req = requests.get(
    "https://he.weather.town/fa/forecast/iran/ostan-e-khorasan-e-razavi/marandiz/", headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')
# find data with css class
data = soup.find(
    'div', class_='informer-main-page__container fleft right-container')
weather = data.find_all('div', class_='forecast-day__item')

# receive data from api
req2 = requests.get(
        "https://www.azangoo.ir/owghat/irn/ﻡﺍﺭﺎﻧﺪﯾﺯ-(ﺭﻮﺴﺗﺍ).html", headers=headers)
soup2 = BeautifulSoup(req2.text, 'html.parser')
data2 = soup2.find('div', class_='container bc2 p1')

quote_from = soup2.find('div',class_='6u 12u(xsmall) bc-c').h5.text.strip()
quote_text = soup2.find('div',class_='6u 12u(xsmall) bc-c').span.text.strip()
occasion_day = "\n\t\t\t\t" + soup2.select_one('div.bc-b div.row div span').get_text(strip=True)
if 'ﻢﻧﺎﺴﺒﺘﯾ ﻮﺟﻭﺩ ﻥﺩﺍﺭﺩ' in occasion_day:
    occasion_day = ''


# find data with css class
data_religious = data2.find('table', class_='rooz')
data_re = data_religious.find_all('tr')
# normalize and split data with regex
regex = r'..:..:..'
times = []
for i in range(3, 9):
    text = normalize(data_re[i].text)
    times.append(re.search(regex, text).group())
data_date = normalize(data2.find('td', class_='date1').text)

week_day = re.search("^(\w*\s?\w*)\s\d", data_date).group(1)
zekr = week_day_zekr.get(week_day)

# normalize and split data with regex
date = []
temperature = []
weather_status = soup.find('div', class_='informer-top').i['title'].strip()

try:
    weather_status = weather_status_text[weather_status]
except KeyError:
    weather_status = 'ﻥﺎﭘﺎﯾﺩﺍﺭ'

for i in range(0, 4):
    temperature.append(normalize_en(weather[i].find(
        'div', class_='temperature').text.replace('°C', '')).replace("+", "%2B").strip())
    date.append(normalize_en(weather[i].find(
        'div', class_='date').text.strip()))

output = ("""
ﺱﻼﻣ ﺎﻌﺿﺎﯾ ﻢﺤﺗﺮﻣ ﮎﺎﻧﺎﻟ ﻡﺮﻧﺪﯾﺯ ﺺﺒﺤﺗﻮﻧ ﺐﺨﯾﺭ

    🗓  {} 
    📌 ﺬﮐﺭ ﺭﻭﺯ: {} {}
    <200f>———————————————
    🕌ﺍﻮﻗﺎﺗ ﺵﺮﻌﯾ
    🏙  ﺍﺫﺎﻧ ﺺﺒﺣ ⇽ {}
    🌅 ﻂﻟﻮﻋ ﺂﻔﺗﺎﺑ ⇽ {}
    ☀️ ﺍﺫﺎﻧ ﻆﻫﺭ ⇽ {}
    🌄 ﻍﺭﻮﺑ ﺎﻔﺗﺎﺑ ⇽ {}
    🌃 ﺍﺫﺎﻧ ﻢﻏﺮﺑ ⇽ {}
    🌘 ﻦﯿﻤﻫ ﺶﺑ ⇽ {}
    <200f>———————————————
    ﻮﻀﻌﯿﺗ ﺂﺑ ﻭ ﻩﻭﺍ: {}
    🌡 ﺪﻣﺍ
    🌅 {} ➜ {}
    ☀️ {} ➜ {}
    🌄 {} ➜ {}
    🌘 {} ➜ {}
    <200f>———————————————
    🔖{}:
{}

    {}
""".format(data_date, zekr, occasion_day, times[0], times[1], times[2], times[3], times[4], times[5], weather_status, date[0], temperature[0], date[1], temperature[1], date[2], temperature[2], date[3], temperature[3],quote_from,quote_text, chanel_id))

# send message
requests.post(
    'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, chanel_id, output))
