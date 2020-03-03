import random
from asyncio import queues
import discord
import youtube_dl
import shutil
import os
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='.')


def __init__(self, bot):
    self.bot = bot


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print("Current Working Dir: {}" .format(os.getcwd()))
    # lines = inspect.getsource(youtube_dl)
    # print(lines)         youtube_dl commandlerini printler


@bot.command(pass_contex=True)
async def connect(ctx):
    global voice
    channel = ctx.message.author.voice.channel  # Gets the channel whom message sent
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        print(f"Connected to 1 {voice}")
        await voice.move_to(channel)
    else:
        print(f"Connected to 2 {voice}")
        voice = await channel.connect()

    print(f"Connected to 3 {voice}")
    await voice.disconnect()

    if voice and voice.is_connected():
        print(f"Connected to 4 {voice}")
        await voice.move_to(channel)
        print(f"Connected to {voice}")
    else:
        print(f"Connected to 5 {voice}")
        voice = await channel.connect()
        print(f"Bot is connected to {channel}")

    await ctx.send(f"Joined 6{channel}")


@bot.command(pass_contect=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.channel.send(f'Left {channel}')


@bot.command(pass_contex=True)
async def connect_channel(ctx, *, channel):
    ctx.message.author = channel  # To move bot to different channel
    await channel.connect()


@bot.command(aliases=['p', 'pla'])
async def play(ctx, url: str):
    def check_queue():
        Queue_infile = os.path.isdir('./Queue')
        if Queue_infile is True:
            filedir = os.path.abspath(os.path.realpath('Queue'))
            length = len(os.listdir(filedir))
            still_q = length - 1
            try:
                first_file = os.listdir(filedir)[0]
            except:
                print('No more queued sond(s)\r\n')
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
            if length != 0:
                print('Song done, playing next queued\n')
                print(f'Songs still in queue: {still_q}')
                if song_there:
                    os.remove('song.mp3')
                shutil.move(song_path, main_location)
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print('No Songs were queued befor ending of the last Song\n')

    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
            queues.clear()
            print('Remove old song file')
    except PermissionError:
        print('Trying to delete Song file')
        await ctx.channel.send('ERROR: Music playing')
        return

    Queue_infile = os.path.isdir('./Queue')
    try:
        Queue_folder = './Queue'
        if Queue_infile is True:
            print('Remove old Queue Folder')
            shutil.rmtree(Queue_folder)
    except:
        print('No old Queue folder')

    await ctx.channel.send('Getting everything Ready now')

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quit': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now\n')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed File: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    name = name.rsplit('-', 2)
    await ctx.channel.send(f'Playing: {name[0]}')
    print('playing\n')


@bot.command(pass_contex=True)
async def pause(ctx):
    vc = ctx.guild.voice_client
    vc.pause()


@bot.command()
async def clear(ctx, amount=5):
    amount += 1
    await ctx.channel.purge(limit=amount)


@bot.command(pass_contex=True)
async def resume(ctx):
    vc = ctx.guild.voice_client
    vc.resume()


@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping of Bot: {round(bot.latency * 1000)}ms')


@bot.command(aliases=['nasılsın', 'merhaba'])
async def naber(ctx):
    await ctx.send('nebıyon kodumun')


@bot.command()
async def nereyebakıyon(ctx):
    await ctx.send('Nereye Bakıyon? Oğğlum Nereye bakıyon?')


@bot.command()
async def çay(message, *, isim):
    await message.channel.send(f'{message.author} kodumun {isim} şahısına çay söyledi. İç de kendine gel hararetini alır flamein kalmaz.  ')


@bot.command()
async def komutlar(ctx):
    komut_listesi = ".naber\n.ping\n.komutlar\n.ask_olcer (isim)\n"
    await ctx.send(komut_listesi)


@bot.command()
async def ask_olcer(message, *, isim):
    number = random.randint(45, 100)
    if (isim == 'aleyna' and message.author == "SAYK#1710") or (isim == 'Aleyna' and message.author == "SAYK#1710"):
        await message.channel.send(f'{isim} ile {message.author} aranızdaki Aşk %95 siz olmuşsunuz!!')
    elif isim == 'Abdulkafi' or isim == 'abdulkafi':
        await message.channel.send(f'{isim} ile {message.author} aranızdaki Aşk %!#0')
    elif (isim == 'aleyna' and message.author == "#1675") or (isim == 'Aleyna' and message.author == "#1675"):
        await message.channel.send(f'{isim} ile {message.author} aranızdaki Aşk %0')
    else:
        await message.channel.send(f'{isim} ile {message.author} aranızdaki Aşk %{number}')

"""
@bot.command()
async def play(ctx, url):
    server = ctx.message.server
    VoiceChannel.connect()
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
"""
"""
@client.command()
async def clear(message):
"""
bot.run('NTQwOTM4NTAxODk4NjMzMjc0.XK49LQ.-2Reah2ci5EtvIBrs3v1acJf7DA')
