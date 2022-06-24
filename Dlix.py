from email import message
from telebot import *
import socket
import json
import re
import requests
import random
import hashlib

api = "5528549523:AAHqzEl53rhrUQIGLFsQMWF42Joeyu09AtE"
bot = TeleBot(api)

sapa = ['Hai Juga', 'Hallo Juga', 'Hi Juga', 'Aloo Juga']
nama = ['Nama Saya adalah DliX Bot\nYang di ciptakan oleh Tuan Adli ']


# Bagian Menu


@bot.message_handler(commands=['start'])
def start_message(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    bot.reply_to(message, 'Hi, apa kabar {} {}? Ada yang bisa saya bantu?'.format(first_name,last_name))
    markup = types.ReplyKeyboardMarkup()
    item3 = types.KeyboardButton('/menu')
    item4 = types.KeyboardButton('/bantuan')
    item5 = types.KeyboardButton('/cek_id')
    markup.row(item3, item4)
    markup.row(item5)
    chatid = message.chat.id
    bot.send_message(chatid, 'Silahkan pilih', reply_markup=markup)
    
@bot.message_handler(commands=['bantuan'])
def bantuan(message):
    bot.reply_to(message, 'Apakah Ada Yang bisa saya bantu? \nPilih menu di bawah ini tuan >///<\n\n ')
    markup = types.ReplyKeyboardMarkup()
    item3 = types.KeyboardButton('/menu')
    item4 = types.KeyboardButton('/start')
    item5 = types.KeyboardButton('/cek_id')
    markup.row(item3, item4)
    markup.row(item5)
    chatid = message.chat.id
    bot.send_message(chatid, 'Silahkan pilih', reply_markup=markup)

@bot.message_handler(commands=['cek_id'])
def action_id(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    id_telegram = message.from_user.id
    username = message.from_user.username
    bot.reply_to(message, '''
Hi, ini ID Telegram kamu
Nama = {} {}
Username = {}
ID = {}
'''.format(first_name,last_name, username, id_telegram))    
    
@bot.message_handler(commands=['menu'])
def menu(message):
    bot.reply_to(message, ''' -= TOOLS MENU =-


Check ID:
ex = /cek_id

Domain To IP:
ex = /domain_to_ip website.com

MD5:
ex = /md5 string

SHA1:
ex = /sha1 string

IP Geolocation:
ex = /ip_geo 8.8.8.8 (your ip)

Password Hash:
ex = /pw_hash yourpw

Random Quotes:
ex = /random_quotes''')


# BAGIAN TOOLS


    
@bot.message_handler(commands=['domain_to_ip'])
def domain_to_ip(message):
    bot.reply_to(message, "Tutorial : \n\nEx = /domain_to_ip google.com")
    texts = message.text.split()
    text = texts[1]
    
    if text:
        bot.reply_to(message, "Cek Domain {}".format(text))
        bot.reply_to(message, "IP {} Adalah {}".format(text, socket.gethostbyname(text)))
        
@bot.message_handler(commands=['md5'])
def hashmd5(message):
    texts = message.text.split()
    text = texts[1]
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    bot.reply_to(message, " nilai hash md5 : {}".format(md5.hexdigest()))

@bot.message_handler(commands=['sha1'])
def hashsha(message):
    texts = message.text.split()
    text = texts[1]
    sha = hashlib.sha1()
    sha.update(text.encode("utf-8"))
    bot.reply_to(message, " nilai hash sha1 : {}".format(sha.hexdigest()))
        
@bot.message_handler(commands=['ip_geo'])
def ipgeo(message):
    texts = message.text.split()
    ipaddr = texts[1]
    ipreq = requests.get(f"http://ip-api.com/json/{ipaddr}")

    if ipreq.status_code == 200:
        ipdata = json.loads(ipreq.text)

        if ipdata["status"] == "success":
            for key in ipdata:
                bot.reply_to(message, f"{key.capitalize()} : {ipdata[key]}")
                
                if key == "lon":
                    lat = ipdata["lat"]
                    lon = ipdata["lon"]
                    maps = f"https://www.google.com/maps/@{lat},{lon},9z"
                    bot.reply_to(message, f" Maps : {maps}")
        
@bot.message_handler(commands=['pw_hash'])
def pw_hash(message):
    texts = message.text.split()
    text = texts[1]
    sha1 = hashlib.sha1()
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    sha384 = hashlib.sha384()
    sha512 = hashlib.sha512()

    sha1.update(text.encode("utf-8"))
    md5.update(text.encode("utf-8"))
    sha256.update(text.encode("utf-8"))
    sha384.update(text.encode("utf-8"))
    sha512.update(text.encode("utf-8"))
    bot.reply_to(message, f'''Password hash sha1 :  {sha1.hexdigest()}

Password hash md5 :  {md5.hexdigest()}

Password hash sha256 :  {sha256.hexdigest()}

Password hash sha384 :  {sha384.hexdigest()}

Password hash sha512 :  {sha512.hexdigest()}''')
        
@bot.message_handler(commands=['random_quotes'])
def random_quotes(message):
    file = open('q.json','r').read()
    sl = json.loads(file)
    js = random.choice(sl)
    bot.reply_to(message, f'{js["quote"]} \n\nby {js["nama"]}')
        
while True:
    try:
        bot.polling()
    except:
        pass