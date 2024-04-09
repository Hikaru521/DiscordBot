import os.path
from discord.ext import commands
import discord
import youtube_dl

intents = discord.Intents.all()
client = discord.Bot(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.activity.Game(name="Anyáddal"),
                                 status=discord.Status.do_not_disturb)
    print(f'{client.user} bot has logged in!')

@client.slash_command(name="leave", description="Elmegyek a picsába")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.respond("Mentem testvérem!")
        await ctx.voice_client.disconnect()
    else:
        await ctx.respond("Bent se voltam he!")

@client.slash_command(name="join", description="Jövök hozzád parfümöt árulni")
async def join(ctx):
    channel = ctx.author.voice.channel
    await ctx.respond("Itt vagyok, érdekel olcsón parfüm?")
    voice = await channel.connect()

@client.slash_command(name="play", description="Lejátszom azt a zenét amit beadsz nekem he")
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.respond("Bent se vagy sehol cigány!")
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'retries':3,
        'outtmpl': 'song.%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ctx.voice_client.stop()
        if os.path.exists("song.mp3"):
            os.remove("song.mp3")
        await ctx.respond("Várjá tesó lopom le netről...")
        ydl.download([url])
        source = discord.FFmpegPCMAudio('song.mp3')
        print(source)
        ctx.voice_client.play(source)

client.run('Your Token')