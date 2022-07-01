import requests
import os

#token bot
token = "Your robot token"
# chanel or group id 
chat_id = "Your chat id" # chat id

#addr page number file
file_addr = './number.txt'
#open file for read page number
with open(file_addr,"r") as number:
    page_number = number.read()
#close file
number.close()

#write new page number and save it
new_page_number = str(int(page_number) + 1)
with open(file_addr,'w') as new_number:
    new_number.write(new_page_number)
#close file
new_number.close()


# addr image file
img_file = "./image/{}.jpg".format(page_number)

#system sleep for save data 
os.system("sleep 5")

#url send data to the telegram
url = f"https://api.telegram.org/bot{token}/sendPhoto"
files = {}
#paylod file for send ...
files["photo"] = open(img_file, "rb")
payload = {'caption' : """
بسم الله الرحمن الرحیم
📗 #روزی_یک_صفحه_قرآن
#صفحه_{} 
{}
""".format(page_number,chat_id)}
#send image to the telegram chanel
requests.get(url, params={"chat_id": chat_id}, files=files,data=payload)