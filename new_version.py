import discord
from discord.ext import commands
import importlib.util
import sys
import os
from yt_dlp import YoutubeDL
import requests
import json
import random
import subprocess
import sys
import asyncio
from replit import db
from keep_alive import keep_alive
import pymongo


############# ses paketini indirme kodu ######################

def CheckModules():
	packages = ["discord.py[voice]","PyNaCl"]
	for package in packages:
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
		if package in sys.modules:
			print(f"{package!r} already in sys.modules")
		elif (spec := importlib.util.find_spec(package)) is not None:
			# If you choose to perform the actual import ...
			module = importlib.util.module_from_spec(spec)
			sys.modules[package] = module
			spec.loader.exec_module(module)
			print(f"{package!r} has been imported")
		else:
			print(f"can't find the {package!r} module")	


############################################################3#
#region MUSIC BOT PART

#region Music queue #####################
class SongQueue(asyncio.Queue):
	def __getitem__(self, item):
		if isinstance(item, slice):
			return list(itertools.islice(self._queue, item.start, item.stop, item.step))
		else:
			return self._queue[item]

	def __iter__(self):
		return self._queue.__iter__()

	def __len__(self):
		return self.qsize()

	def clear(self):
		self._queue.clear()

	def shuffle(self):
		random.shuffle(self._queue)

	def remove(self, index: int):
		del self._queue[index]
########################################





# Bot bir voice_channel a bağlı mı check için bir veriable
isConnectedtoVoiceChannel = False

client = commands.Bot(command_prefix="$")

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

def search(arg):
	with YoutubeDL(YDL_OPTIONS) as ydl:
		try:
			get(arg) 
		except:
			video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
		else:
			video = ydl.extract_info(arg, download=False)
	print("--------------",video.get("webpage_url"),"--------------")

	return video.get("webpage_url")

@client.command()
async def play(ctx, url : str):
	global isConnectedtoVoiceChannel
	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
	except PermissionError:
		await ctx.send("Wait for the current playing music to end or use the 'stop' command")
		return

	voiceChannel = ctx.author.voice.channel

	if isConnectedtoVoiceChannel == False:
		await voiceChannel.connect()
		isConnectedtoVoiceChannel = True
	
	
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}


	with YoutubeDL(ydl_opts) as ydl:
		if not "http" in url:
			ydl.download([search(ctx.message.content.replace("$play ",""))])
		else:
			ydl.download([url])
			

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")
	voice.play(discord.FFmpegPCMAudio("song.mp3"))
	

@client.command()
async def leave(ctx):
	global isConnectedtoVoiceChannel
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	isConnectedtoVoiceChannel = False
	if voice.is_connected():
		await voice.disconnect()
	else:
		await ctx.send("The bot is not connected to a voice channel.")



# Hüsamettin Demirtaş 3.12.2021 13.16
@client.command()
async def writeToErMeydani(ctx):
	channelIDofErMeydani = client.get_channel(485549819339997205)
	message = ctx.message.content.split("$writeToErMeydani ")[1]
	await channelIDofErMeydani.send(message)
# Hüsamettin Demirtaş 3.12.2021 13.16

@client.command()
async def pause(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
	else:
		await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_paused():
		voice.resume()
	else:
		await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	voice.stop()
#endregion

curse_words = []

default_reacts = []

# if there is no any attribute that checks bot's responding, creates one
if "responding" not in db.keys():
	db["responding"] = True

# if there is no any attribute that check's bot's curse filter, creates one
if "cursefilter" not in db.keys():
	db["cursefilter"] = True


def get_quote():
	response = requests.get("7110b89c-9585-42f0-b8e2-b69fd607d734")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return (quote)


#region BOT REACT
# This part is related to the answer that bot's react to the curse words
def update_reacts(react_message):
	if "reacts" in db.keys():
		reacts = db["reacts"]
		reacts.append(react_message)
		db["reacts"] = reacts
	else:
		db["reacts"] = [react_message]


def delete_reacts(index):
	reacts = db["reacts"]
	if len(reacts) > index:
		del reacts[index]
		db["reacts"] = reacts
#endregion


#region BOT REACT TO
# This part is related to the curse words that bot's react to
def update_curses(new_curse):
	if "curses" in db.keys():
		curses = db["curses"]
		curses.append(new_curse)
		db["curses"] = curses
	else:
		db["curses"] = [new_curse]


def delete_curses(index):
	curses = db["curses"]
	if len(curses) > index:
		del curses[index]
		db["curses"] = curses
#endregion

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_spam(message):
	await play(message, atmasikik_Url)

############################## ON MESSAGE #########################
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	# mesajın içeriğini alıp küçültüyorum ki büyük küçük farkı olmasın
	# im lowercasing the message's content due to prevent problems
	msg = message.content.lower()
	

	# this line uses the get_quote method to type random
	# inspiration message that returned from api
	if msg.startswith('$inspire'):
		quote = get_quote()
		await message.channel.send(quote)

	# allah kurtarsın kardeşim kodu
	if any("allah kurtarsın kardeşim" in msg for word in msg):
		await play(message, allahKurtarsinKardesim_url)    

	if any("niye öyle diyorsunuz beyefendi" in msg for word in msg):
		await play(message, niyeoylediyorsunuzbeyefendi_url)

	# If bot's responding mode is activated those lines work
	if not str(message.author) == "Mr.Ironstone#9317":
		if db["responding"]:
			options = default_reacts
			if "reacts" in db.keys():
				options.extend(db["reacts"])

				if "curses" in db.keys():
					curses = db["curses"]
					curses.extend(curse_words)

				if any(word in msg for word in curses):
					# await message.delete()
					# await message.channel.send(message.author.mention + " " + random.choice(options))
					# await message.reply(message.author.mention + " " + random.choice(options))
					await message.reply(message.author.mention + " " + random.choice(options))

#region ADDING, DELETING and LISTING REACTS
	if msg.startswith("$newreact"):
		react_message = msg.split("$newreact ", 1)[1]
		update_reacts(react_message)
		await message.channel.send("New react message added.")

	if msg.startswith("$delreact"):
		reacts = []
		if "reacts" in db.keys():
			index = int(msg.split("$delreact ", 1)[1])
			delete_reacts(index)
			reacts = db["reacts"]
		await message.channel.send(reacts)

	if msg.startswith("$listreacts"):
		reacts = []
		if "reacts" in db.keys():
			reacts = db["reacts"]
		await message.channel.send(reacts)

	if msg.startswith("$clearreacts"):
		if "reacts" in db.keys():
			reacts = db["reacts"]
			if not len(reacts) == 0:
				reacts.clear()
				db["reacts"] = reacts
				await message.channel.send(
					"Reacts' container is successfully cleared")
			else:
				await message.channel.send("Reacts' container is already empty" )
		else:
			await message.channel.send("This database is not existed")

#endregion

#region ADDING, DELETING and LISTING CURSES
	if msg.startswith("$newcurse"):
		curse_message = msg.split("$newcurse ", 1)[1]
		update_curses(curse_message)
		await message.channel.send("New curse message added.")

	if msg.startswith("$delcurse"):
		curses = []
		if "curses" in db.keys():
			index = int(msg.split("$delcurse ", 1)[1])
			delete_curses(index)
			curses = db["curses"]
		await message.channel.send(curses)

	if msg.startswith("$listcurses"):
		curses = []
		if "curses" in db.keys():
			curses = db["curses"]
		await message.channel.send(curses)

	if msg.startswith("$clearcurses"):
		if "curses" in db.keys():
			curses = db["curses"]
			if not len(curses) == 0:
				curses.clear()
				db["curses"] = curses
				await message.channel.send(
					"Curses' container is successfully cleared")
			else:
				await message.channel.send("Curses' container is already empty")
		else:
			await message.channel.send("This database is not existed")
#endregion

#region ACTIVATING AND DEACTIVATING THE RESPONDING OF BOT
	if msg.startswith("$responding"):
		value = msg.split("$responding ", 1)[1]

		if value.lower() == "on":
			db["responding"] = True
			await message.channel.send("Responding is on.")
		else:
			db["responding"] = False
			await message.channel.send("Responding is off.")
#endregion

#region ACTIVATING AND DEACTIVATING THE CURSE FILTER OF BOT
	if msg.startswith("$cursefilter"):
		value = msg.split("$cursefilter ", 1)[1]

		if value.lower() == "on":
			db["cursefilter"] = True
			await message.channel.send("Profinity Filter is on.")
		else:
			db["cursefilter"] = False
			await message.channel.send("Profinity Filter is off.")

	await client.process_commands(message)
#endregion


keep_alive()
client.run(os.getenv('TOKEN'))

