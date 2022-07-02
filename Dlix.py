from email import message
from click import command
from telebot import *
import socket
import json, os
import pafy
from urllib.request import urlopen
import re
import requests
import random
import hashlib
import shutil
from bs4 import BeautifulSoup as bes

# pip install pytelegrambotapi
# pip install youtube_dl
# pip install requests
# pip install instaloader
# pip install beautifulsoup4

# Note : edit file backend_youtube_dl.py in 
# line 53 and 54, 
# change to self._likes = self._ydl_info.get('like_count',0) 
# And self._dislikes = self._ydl_info.get('dislike_count',0)
        
# Acc Instagram
ig_log = "username_ig"
ig_pw  = "password_ig"

# Acc Telegram
id = 12345678
username_owner = "username_tele"

api = "Token API"
bot = TeleBot(api)

sapa = ['Hai Juga', 'Hallo Juga', 'Hi Juga', 'Aloo Juga']
nama = ['Nama Saya adalah DliX Bot\nYang di ciptakan oleh Tuan Adli ']

@bot.message_handler(commands=['start'])
def start_message(message):
    
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if message.from_user.id == id and message.from_user.username == username_owner:
        bot.reply_to(message, 'Hallo, senang bertemu anda kembali. Tuan, apakah ada yang bisa saya bantu?')
    else:
        bot.reply_to(message, 'Hi, apa kabar {} {}? Ada yang bisa saya bantu? Jika ada ketik \n/help'.format(first_name,last_name))
    markup = types.ReplyKeyboardMarkup()
    item4 = types.KeyboardButton('/help')
    item5 = types.KeyboardButton('/cek_id')
    markup.row(item5, item4)
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
    
@bot.message_handler(commands=['help'])
def menu(message):
    
    bot.reply_to(message, 'Apakah Ada Yang bisa saya bantu? \nPilih menu di bawah ini tuan >///<')
    markup = types.ReplyKeyboardMarkup()
    item4 = types.KeyboardButton('/start')
    item5 = types.KeyboardButton('/cek_id')
    markup.row(item5, item4)
    bot.reply_to(message, ''' -= TOOLS MENU =-


Check ID:
/cek_id — Digunakan untuk mengecek ID Telegram anda, cara penggunaan nya.
ex = /cek_id 

Tanya Wiki:
/apa_itu — Digunakan untuk mencaritahu sesuatu, dan mendapatkan jawaban dari wikipeadia, contoh.
ex = /apa_itu cahaya
ex2 = /apa_itu Google LLC

YT Vidmate Download:
/yt_vidmate — Digunakan untuk download musik youtube, berupa link download, cara penggunaan.
ex = /yt_vidmate https://youtube/gcJVgFQwnpc

YT Audio Download:
/yt_audio — Digunakan untuk download musik youtube, dapat mendownload secara otomatis, dan di kirim otomatis ke telegram, cara penggunaan.
ex = /yt_audio https://youtube/gcJVgFQwnpc

Instagram Download:
/ig_download — Digunakan untuk download postingan instagram, caranya.
ex = /ig_download https://www.instagram.com/p/CfVZMhxrLmA/?utm_source=ig_web_copy_link

Domain To IP:
/domain_to_ip — Digunakan mengubah dari domain ke IP, cara penggunaan nya.
ex = /domain_to_ip example.com

MD5:
/md5 — Digunakan untuk mengubah kalimat / huruf ke hash MD5, cara penggunaan nya.
ex = /md5 example

SHA1:
/sha1 — Digunakan untuk mengubah kalimat / huruf ke hash sha1, cara penggunaan nya.
ex = /sha1 example

IP Geolocation:
/ip_geo — Digunakan untuk mengetahui informasi tentang IP, mulai dari nama negara hingga ke lokasi IP tersebut, cara penggunaan nya.
ex = /ip_geo 8.8.8.8

Password Hash:
/pw_hash — Digunakan untuk mengencripsi password ke hash md5 hingga hash sha512, cara penggunaan nya.
ex = /pw_hash yourPass123

Random Quotes:
/random_quotes — Digunakan untuk memunculkan kata kata keren dan memotivasi, cara penggunaan nya.
ex = /random_quotes

ClickJacking Tester
/cj_tester — Digunakan untuk mengecek sebuah website apakah website tersebut vuln terhadap clickjacking atau tidak, cara penggunaan nya.
ex = /cj_tester https://example.com''')


# BAGIAN TOOLS


    
@bot.message_handler(commands=['domain_to_ip'])
def domain_to_ip(message):
    
    text = message.text.replace("/domain_to_ip ", "")
    
    if text:
        bot.reply_to(message, "Cek Domain {}".format(text))
        bot.reply_to(message, "IP {} Adalah {}".format(text, socket.gethostbyname(text)))
        
@bot.message_handler(commands=['md5'])
def hashmd5(message):
    
    text = message.text.replace("/md5 ", "")
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    bot.reply_to(message, '''nilai asli : {} 
nilai hash md5 : {}'''.format(text, md5.hexdigest()))

@bot.message_handler(commands=['sha1'])
def hashsha(message):
    
    text = message.text.replace("/sha1 ", "")
    sha = hashlib.sha1()
    sha.update(text.encode("utf-8"))
    bot.reply_to(message, '''nilai asli : {} 
nilai hash sha1 : {}'''.format(text, sha.hexdigest()))
        
@bot.message_handler(commands=['ip_geo'])
def ipgeo(message):
    
    ipaddr = message.text.replace("/ip_geo ", "")
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
    
    text = message.text.replace("/pw_hash ", "")
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
    bot.reply_to(message, f'''Note: Password tidak boleh menggunakan spasi ( )

Password hash sha1 :  {sha1.hexdigest()}

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
        
@bot.message_handler(commands=['cj_tester'])
def ClickjackingTester(message):
    
    def check(url):

        try:
            if "http" not in url: url = "http://" + url

            data = urlopen(url)
            headers = data.info()

            if not "X-Frame-Options" in headers: return True

        except: return False


    def code_html(url):

        code = f"""
<html>
    <head><title>Clickjack test page</title></head>
    <body>
        <p>Website is vulnerable to clickjacking!</p>
        <iframe src="{url}" width="500" height="500" ></iframe>
    </body>
</html>
        """
        return code

    site = message.text.replace("/cj_tester ", "")

        
    bot.reply_to(message, f"[*] Checking {site}")
    status = check(site)

    if status:
        bot.reply_to(message, f" [+] Website is vulnerable! \n[*] Copy This Code and Try This \n{code_html(site)}")
    elif not status: 
        bot.reply_to(message, " [-] Website is not vulnerable!")
    else: 
        bot.reply_to(message, "ERROR")
        
@bot.message_handler(commands=['apa_itu'])
def wiki(message):
    
    text = message.text.replace("/apa_itu ", "")
    if text:
        try:
            dpt = f'https://id.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={text}'
            hasil = requests.get(dpt).json()
            filter = hasil['query']['pages']
            d = re.findall(r'(\d+)', str(filter))
            result = filter[d[0]]['extract']
            bot.reply_to(message, f'''Pertanyaan : {text}

Jawaban : {result}''')
        except Exception as e:
            print(e)
            bot.reply_to(message, f'Maaf, Yang anda cari "{text}" tidak bisa ditemukan di wikipedia!')
            
@bot.message_handler(commands=['yt_vidmate'])
def ytAudio(message):
    
    text = message.text.replace("/yt_vidmate ", "")
    if text:
        try:
            url = text.replace('[','').replace(']','')
            ytAudio = requests.post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':url,'q_auto':'0','ajax':'1'}).json()
            find = bes(ytAudio['result'], 'html.parser').findAll('td')
            ukuran = find[len(find)-10].text
            id = re.findall('var k__id = "(.*?)"', ytAudio['result'])
            judul = bes(ytAudio['result'], 'html.parser').find('b').text
            link_download = bes(requests.post('https://www.y2mate.com/mates/en60/convert',data={'type':url.split('/')[2],'_id':id[0],'v_id':url.split('/')[3],'ajax':'1','token':'','ftype':'mp3','fquality':'128'}).json()['result'],'html.parser').find('a')['href']
            bot.reply_to(message, f'''Judul : {judul}
Ukuran : {ukuran}
Download link : {link_download}''')
        except Exception as e:
            print(e)
            bot.reply_to(message, "Maaf sepertinya link ini telah error")

@bot.message_handler(commands=['yt_audio'])
def ytAudio(message):
    try:
        filter = message.text.replace("/yt_audio ", "")
        url = pafy.new(filter)
        bot.reply_to(message, f'''Note : versi k2 dalam proses pengembangan, maaf jika ada error

Judul : {url.title}
Thumbnail : {url.thumb}
Durasi : {url.duration}

Sedang Mendownload Mohon Tunggu Sesaat
estimasi download [3 menit jika sinyal lancar]

''')
        result = url.getbestaudio()
        result.download(f'{url.title} {message.from_user.id}.mp3')
        
        for i in os.listdir():
            if i.endswith(f"{message.from_user.id}.mp3"):
                print(i)
                bot.send_audio(message.chat.id, open(i, 'rb'))
                os.remove(i)
    except:
        bot.reply_to(message, "Maaf, Ada Kesalahan Silahkan Masukkan Kembali Link Dengan Benar")
        
@bot.message_handler(commands=['ig_download'])
def ig_download(message):
    try:
        isi = message.text.replace("/ig_download ", "").replace("https://www.instagram.com/reel/", "").replace("/?utm_source=ig_web_copy_link", "").replace("https://www.instagram.com/p/","").replace("/?igshid=YmMyMTA2M2Y=", "")
        bot.reply_to(message, "Download Sedang di proses Silahkan menunggu, Download mungkin agak lama.....")
        os.system(f"instaloader --login={ig_log} --password={ig_pw} -- -{isi}")
        
        for i in os.listdir(f'-{isi}'):
            print(i)
            if i.endswith(".jpg"):
                print("anjay")
                bot.send_photo(message.chat.id, open(f'-{isi}/{i}', 'rb'))
            elif i.endswith(".mp4"):
                print("anjass")
                bot.send_video(message.chat.id, open(f'-{isi}/{i}', 'rb'))
        shutil.rmtree(f"-{isi}")
    except:
        bot.reply_to(message, '''Maaf, Ada Kesalahan Silahkan Masukkan Kembali Link Dengan Benar''')
            
# @bot.message_handler(commands=['story_horror'])
# def story(message):
    
#     texts = message.text.split()
#     filter = texts[1]
#     text = filter.replace("_", " ")
#     if text == "judul":
#         query = "select judul_cerita from cerita"
#         sql.execute(query)
#         result = sql.fetchall()
#         pesan = ''
#         for data in result:
#             pesan = pesan + 'Judul : ' + str(data).replace("'", "").replace("(", "").replace(")", "").replace(",", "")  + '\nCara Akses : /story_horror ' + str(data).replace(" ", "_").replace("'", "").replace("(", "").replace(")", "").replace(",", "") + '\n\n'
#         bot.reply_to(message, pesan)
#     else:
#         query = f"select isi_cerita from cerita where judul_cerita = '{text}'"
#         sql.execute(query)
#         result = sql.fetchall()
#         pesan = ''
#         for data in result:
#             pesan = pesan + str(data) + '\n'
#             if len(str(data)) > 4096:
#                 text = "Cerita Gagal Terkirim"
#                 pesan = f"Maaf, cerita ini tidak dapat terkitim karena melebihi 4096 karakter/batas karakter chat di telegram. \ncerita ini memiliki {len(str(data))} karakter"
#         bot.reply_to(message, f'''{text}

# {pesan.replace("'", "").replace("(", "").replace(")", "")}''')
        
@bot.message_handler(commands=['add_story'])
def add_story(message):
    if message.from_user.id == id and message.from_user.username == username_owner:
        bot.reply_to(message, "Cerita Anda Segera Kami Proses")
    else:
        bot.reply_to(message, "Sorry, just owner can use this commands")
    
    
@bot.message_handler(commands=['tes_inp'])
def tes_inp(message):
    text = message.text.replace("/tes_inp ", "")
    bot.reply_to(message, text)
    
while True:
    try:
        bot.polling()
    except:
        pass