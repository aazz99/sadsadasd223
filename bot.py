from rubika import Bot
from json import load , dump
import time
import numpy as np

bot = Bot("zhnlcocfvtuxciwyhjcpuyrmzipwagsi")
target = "g0CX4C50c1f13d1305474e7676936ad3"





def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
			
def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData
	
# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "گذاشتن لینک در گروه ممنوع میباشد!\n\n"

	if coun == 1:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (1/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !!!")
	elif coun == 2:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (2/3) اخطار دریافت کرده اید ⚠️.")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 کاربر [ @"+user+" ] \n (3/3) اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .")
		bot.banGroupMember(target, guid)


while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

						elif msg.get("text") == "!stop" or msg.get("text") == "/stop" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "✅ ربات اکنون خاموش است", message_id=msg.get("message_id"))
							except:
								print("err off bot")
								
						elif msg.get("text") == "!restart" or msg.get("text") == "/restart" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "در حال راه اندازی مجدد . . .", message_id=msg.get("message_id"))
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت مجددا راه اندازی شد !", message_id=msg.get("message_id"))
							except:
								print("err Restart bot")
								
						elif msg.get("text").startswith("حذف") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +" پیام اخیر با موفقیت حذف شد", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "✅ پیام با موفقیت حذف شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("/ban") and msg.get("author_object_guid") in admins :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "کاربر  {user} به دلیل رعایت نکردن قوانین\nازگروه اخراج شد✅", message_id=msg.get("message_id"))
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("افزودن") or msg.get("text").startswith("/add") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ کاربر محدود میباشد", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "/panel":
							try:
								rules = open("help.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "ادمین":
							try:
								rules = open("admen.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت ادمین") and msg.get("author_object_guid") in admins:
							try:
								rules = open("admen.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت ادمین")))
								bot.sendMessage(target, "✅  ادمین ها آپدیت شد", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg["text"].startswith("بپرس"):
							try:
								adad=np.random.randint(1,129)
								bot.sendMessage(target, str(adad), msg["message_id"])
							except:
								print("err dastorat")
								
						elif msg.get("text") == "لینک":
							try:
								rules = open("leink.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت لینک") and msg.get("author_object_guid") in admins:
							try:
								rules = open("leink.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت لینک")))
								bot.sendMessage(target, "✅  لینک گروه آپدیت شد ", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
						
						elif msg.get("text") == "منو":
							try:
								rules = open("mno.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "!ins":
							try:
								rules = open("Insta.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "!boo":
							try:
								rules = open("boo.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "/panel":
							try:
								rules = open("balad.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "!anlaen":
							try:
								rules = open("anlaen.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "/bot":
							try:
								rules = open("bot.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "درباره گروه":
							try:
								rules = open("help.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت درباره") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت درباره")))
								bot.sendMessage(target, "درباره گروه آپدیت شد", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))						
								
						elif msg.get("text") == "/del" and msg.get("author_object_guid") in admins :
							try:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "پیام مورد نظر پاک شد...", message_id=msg.get("message_id"))
							except:
								print("err pak")
								
						elif msg.get("text").startswith("/cal") or msg.get("text").startswith("حساب"):
							msd = msg.get("text")
							if plus == True:
								try:
									call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
									if call[1] == "+":
										try:
											am = float(call[0]) + float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
											plus = False
										except:
											print("err answer +")
										
									elif call[1] == "-":
										try:
											am = float(call[0]) - float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer -")
										
									elif call[1] == "*":
										try:
											am = float(call[0]) * float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer *")
										
									elif call[1] == "/":
										try:
											am = float(call[0]) / float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer /")
											
								except IndexError:
									bot.sendMessage(target, "متاسفانه دستور شما اشتباه میباشد!" ,message_id=msg.get("message_id"))
									plus= True
						
						elif hasInsult(msg.get("text"))[0] and not msg.get("author_object_guid") in admins :
							try:
								print("yek ahmagh fohsh dad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("fohsh pak shod")
							except:
								print("err del fohsh Bug")
								
						elif msg.get("text").startswith("سلام") or msg.get("text").startswith("سلم") or msg.get("text").startswith("صلام") or msg.get("text").startswith("صلم") or msg.get("text").startswith("سیلام") or msg.get("text").startswith("صیلام"):
							try:
								bot.sendMessage(target,'چطوری گلم' ,message_id=msg.get("message_id"))
							except:
								print("err hello")

						elif msg.get("text").startswith("ربات") or msg.get("text").startswith("بات") or msg.get("text").startswith("بلکترون") or msg.get("text").startswith("روبات") or msg.get("text").startswith("belectron") or msg.get("text").startswith("Belectron"):
							try:
								bot.sendMessage(target,'جانم' ,message_id=msg.get("message_id"))
							except:
								print("err robot")

						elif msg.get("text").startswith("خوبی") or msg.get("text").startswith("text"):
							try:
					  			bot.sendMessage(target, "تا وقتی کونت مال من باشه من حالم خوبه خوبهههههه💜", message_id=msg.get("message_id"))
							except:
								print("err luagh")
								
						elif msg.get("text") == "🤣🤣🤣":
							try:
								bot.sendMessage(target, "جون تو فقط بخند🤤", message_id=msg.get("message_id"))
							except:
								print("err poker answer")

						elif msg.get("text") == "/bomber":
							try:
								bot.sendMessage(target, "💣 Bomber PaneL \n📍 این دستور توسط سازنده ربات برای کاربرانی که از نسخه رایگان ربات استفاده میکنند متوقف شده است . برای خرید این دستور لطفا به پیوی زیر مراجعه کنید.\n #Admin --> @T_NEFRAT_T", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
		
						elif msg.get("text") == "سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.pin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "پیام مورد نظر با موفقیت سنجاق شد!", message_id=msg.get("message_id"))
							except:
								print("err pin")
								
						elif msg.get("text") == "برداشتن سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.unpin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "پیام مورد نظر از سنجاق برداشته شد!", message_id=msg.get("message_id"))
							except:
								print("err unpin")						
						
						elif msg.get("text") == "قوانین":
							try:
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
								
						elif msg.get("text") == "/gj1":
							try:
								rules = open("grat1.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
								
						elif msg.get("text") == "/gj2":
							try:
								rules = open("grat2.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
								
						elif msg.get("text") == "/smf":
							try:
								rules = open("smf.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
								
						elif msg.get("text") == "/games":
							try:
								rules = open("byb.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
							
						elif msg.get("text") == "حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))
								
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "!speak" or msg.get("text") == "/speak" or msg.get("text") == "Speak" or msg.get("text") == "بگو":
							try:
								if msg.get('reply_to_message_id') != None:
									msg_reply_info = bot.getMessagesInfo(target, [msg.get('reply_to_message_id')])[0]
									if msg_reply_info['text'] != None:
										text = msg_reply_info['text']
										speech = gTTS(text)
										changed_voice = io.BytesIO()
										speech.write_to_fp(changed_voice)
										b2 = changed_voice.getvalue()
										changed_voice.seek(0)
										audio = MP3(changed_voice)
										dur = audio.info.length
										dur = dur * 1000
										f = open('sound.ogg','wb')
										f.write(b2)
										f.close()
										bot.sendVoice(target , 'sound.ogg', dur,message_id=msg["message_id"])
										os.remove('sound.ogg')
										print('sended voice')
								else:
									bot.sendMessage(target, 'پیام شما متن یا کپشن ندارد',message_id=msg["message_id"])
							except:
								print('server gtts bug')
							
						elif msg.get("text") == "برداشتن حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "لطفا دستور رو صحیح وارد کنید!", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))



						elif msg.get("text") == "/lock" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 گروه قفل شد", message_id=msg.get("message_id"))
							except:
								print("err lock GP")

						elif msg.get("text") == "بازکردن گروه" or msg.get("text") == "/unlock" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 گروه اکنون باز است", message_id=msg.get("message_id"))
							except:
								print("err unlock GP")

					else:
						if msg.get("text") == "!start" or msg.get("text") == "/start" and msg.get("author_object_guid") in admins :
							try:
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت روشن شد!", message_id=msg.get("message_id"))
							except:
								print("err on bot")
								
				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"تق خارکسه {user}", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err rm member answer")
					
					elif data["type"]=="AddedGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hey {user} 🍒 !\nWelcome to {name} 🏖\n\n📑 To get information about robot commands, send a /panel command !\n🔗 ChanneL; rubika.ir/BeLectron_bot", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err add member answer")
					
					elif data["type"]=="LeaveGroup":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"کون لقت {user}", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Leave member Answer")
							
					elif data["type"]=="JoinedGroupByLink":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hey {user} 🍒 !\nWelcome to {name} 🏖\n\n📑 To get information about robot commands, send a /panel command !\n🔗 ChanneL; rubika.ir/BeLectron_bot", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Joined member Answer")
							
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
