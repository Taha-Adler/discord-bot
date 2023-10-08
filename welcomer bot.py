import discord
from discord.ext import commands , tasks
from discord.utils import get
import jdatetime
import youtube_dl
import asyncio
import requests
import sqlite3

DATABASE = 'commands.db'
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
intents.voice_states = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="/",intents=intents)
TOKEN = "MTExMTcwOTQyNTc5MTY4NDY3OQ.GaSNck.8EPa_M1VCcnrKtDvMbp9HuoEP5vnLvm9xsNPes" 
user_data = {}


@bot.event
async def on_ready():
    print("start")
    
@bot.event
async def on_member_Join(member : discord.member):
    channel = bot.get_channel(1052242484924784721)
    await channel.send(f"Welcom||{member.mention}||")
#########################################################################################################################################################    
@bot.event
async def on_message(message):
    bad_words = ['koskesh',
'haromzade',
'madar jende',
'bi namos',
'be namos',
'haromi',
'kharkose',
'khar kose',
'lashi sag',
'lashi',
'sag',
'koni',
'konii',
'koniii',
'be sharaf',
'harami',
'lashex',
'be madar',
'bi madar',
'kos lis',
'koslis',
'jende',
'jande',
'janda',
'madar ghahve',
'madarghahve',
'خارکصه',
'خارکصده',
'مادر جنده ',
'حرومزاده',
'بیناموس',
'لاشکس',
'فانی بدبخت',
'فانی',
'بیشرف',
'کونی',
'کص پدر',
'کوص پدر',
'پدرسگ',
'مادرسگ',
'مادر به خطا',
'هول سگ',
'هول',
'لاشی',
'لاشگوشت',
'لاش گوشت',
'کونت میخواره',
'مادر حرومی',
'فقیر ',
'بدبخت',
'فقیر بدبخت',
'ای لاشی',
'کص ننت',
'کصمادرت',
'کص مادرت',
'کص پدر',
'کصپدر',
'لاپایی'
]
    
######################################################################################################################################################
    if any(word in message.content for word in bad_words):
         await message.delete()
         await message.channel.send("have bad words!!")
    

    
@bot.event   
async def on_message_commands(message):
    print(f"A message by {message.author} was deleted in channel {message.channel}.")
    
    
@bot.event
async def on_ready():
    zaman.start()
    print("Ready To Use")




@tasks.loop(minutes=10)
async def zaman():
    tarikh_channel = bot.get_channel(1115269545142259712)
    fa_date = jdatetime.date.today()
    t_banner = fa_date.strftime("%y %B %d")
    await tarikh_channel.edit(name = f"║¢{t_banner}¢║")
    
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await increase_points(message.author.id, 1)
    
    await cheak_level_up(message.author)
    
    await bot.process_commands(message)
    
async def increase_points(user_id , points):
        if user_id not in user_data:
            user_data[user_id] = {'points' : 0, 'level' : 0}
            
        user_data[user_id]['points'] += points
            
    
async def cheak_level_up(user):
    user_id = user.id
    points = user_data[user_id]['points']
    level = user_data[user_id]['level']
    
    if points >= (level + 1) * 10 :
       user_data[user_id]['level'] += 1
       await user.send(f'🥳╠══Afarin be level{level + 1} residi══╣🥳')
       
@bot.command()
async def profile(ctx):
   if ctx.message.content == '/profile':
        user_id = ctx.author.id
    
        if user_id in user_data:
            points = user_data[user_id]['points']
            level = user_data[user_id]['level']
            await ctx.send(f'emtiaz shoma : {points}\n level shoma : {level}')
        else:
            await ctx.send('shoma hich emtiazi')
        
#####voice############################################################################################################################################################################        
@bot.command(name='play')
async def play(ctx, *, query):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send('You must be in a voice channel to use this command.')
        return

    try:
        await voice_channel.connect()
    except discord.ClientException:
        pass

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'auto',
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)['entries'][0]
        except Exception:
            await ctx.send("Sorry, I couldn't find that song.")
            return

        url2 = info['formats'][0]['url']
        voice_client = ctx.voice_client
        voice_client.play(discord.FFmpegPCMAudio(url2))

        await ctx.send(f"Now playing: {info['title']}")

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('Playback stopped.')

@bot.command(name='disconnect')
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected from voice channel.')   

#####voice-end###################################################################################################################################################################################        
@bot.command()
@commands.has_permissions(administrator = True)
async def delet_channels(ctx):
    if ctx.message.content == '/delete_all_channels':
        channels = ctx.guild.channels
    
    
        voice_channels = [channel for channel in channels if isinstance(channel, discord.VoiceChannel)]
        await ctx.send(f'Deleting {len(voice_channels)} voice channels...')
        for channel in voice_channels:
            await channel.delete()
        
    
        await ctx.send('Deleting all channels...')
        for channel in channels:
            await channel.delete()

    @delete_all_channels_error
    async def delete_all_channels_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('😐-You dont have the permissions to run this command.')
        
   

@bot.command()
@commands.has_role('Helper')
async def clear_channel(ctx):
    if ctx.message.content == '/clear_channel':
        channel = ctx.message.channel

        if isinstance(channel, discord.TextChannel):
            await ctx.send('🧙‍♂️-Clearing channel...')
            await channel.purge()
        else:
            await ctx.send('This command is only available for text channels.')
##########################################################################################################################################################
@bot.command()
@commands.has_role('Helper')
async def createchannel(ctx, channel_name):
    guild = ctx.guild
    await guild.create_text_channel(channel_name)
    await ctx.send(f'Text channel "||{channel_name}||" created successfully.')

@bot.command()
@commands.has_role('Helper')
async def createvoice(ctx, channel_name):
    guild = ctx.guild
    await guild.create_voice_channel(channel_name)
    await ctx.send(f'Voice channel "||{channel_name}||" created successfully.')

@createchannel.error
async def createchannel_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have the role to use this command.")

@createvoice.error
async def createvoice_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have the  role to use this command.")


@bot.command()
@commands.has_role('Helper')
async def createrole(ctx, role_name):
    guild = ctx.guild
    role = await guild.create_role(name=role_name)
    await ctx.send(f'Role "||{role.name}||" created successfully.')


    
################start-log####################################################################################################################################################   

log_channel_id = 1114241536608174120

@bot.command()
@commands.has_role('Helper')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(f'User "||{member.name}||"||#{member.discriminator}|| has been kicked.')

@bot.command()
@commands.has_role('Helper')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(f'User "||{member.name}||"||#{member.discriminator}|| has been banned.')

@bot.command()
@commands.has_role('Helper')
async def log(ctx):
    log_channel = bot.get_channel(log_channel_id)
    messages = []
    async for message in log_channel.history(limit=None):
        messages.append(message)

    for message in messages:
        content = f'{message.author.name}#{message.author.discriminator}: {message.content}'
        user = await bot.fetch_user(ctx.author.id)
        await user.send(content)

    await ctx.send('Log has been sent to your DM.')
    
    
GUILD_ID = 1001811427885056001

@bot.command()
@commands.has_role('Helper')
async def delete_roles(ctx):
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        await ctx.send('The server could not be found')
    else:
        for role in guild.roles:
            try:
                await role.delete()
                print(f'remove the roll {role.name} ({role.id})')
            except discord.Forbidden:
                print('fLack of access to delete the roll : {role.name} ({role.id})')
            except discord.HTTPException:
                print(f'Error deleting roll : {role.name} ({role.id})')
        await ctx.send('All rolls have been removed successfully!!')
    
##########finish-ban and kick##############################################################################################################################
cursor.execute('''
    CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command TEXT
    )
''')
connection.commit()

@bot.command()
async def save_command(ctx, *, command):
    cursor.execute('INSERT INTO commands (command) VALUES (?)', (command,))
    connection.commit()
    await ctx.send(f'Command "{command}" saved successfully!')

@bot.command()
async def show_commands(ctx):
    cursor.execute('SELECT command FROM commands')
    commands = cursor.fetchall()
    if commands:
        command_list = '\n'.join([command[0] for command in commands])
        await ctx.send(f'Commands:\n{command_list}')
    else:
        await ctx.send('No commands found!')
####################nuke_Area###########################################################################################################################################

@bot.command()
@commands.has_role('347632057023423')
async def create_locked_channels(ctx, channel_name):
    for i in range(1000):
        asyncio.create_task(create_locked_channel(ctx.guild, channel_name))
    await ctx.send(f'Creating 1000 locked channels with name "{channel_name}"...')

async def create_locked_channel(guild, channel_name):
    channel = await guild.create_text_channel(channel_name)
    await channel.set_permissions(guild.default_role, send_messages=False)

@bot.command()
@commands.has_role('347632057023423')
async def create_locked_voice_channels(ctx, channel_name):
    for i in range(1000):
        asyncio.create_task(create_locked_voice_channel(ctx.guild, channel_name))
    await ctx.send(f'Creating 1000 locked voice channels with name "{channel_name}"...')

async def create_locked_voice_channel(guild, channel_name):
    channel = await guild.create_voice_channel(channel_name)
    await channel.set_permissions(guild.default_role, connect=False)
    
@bot.command()
@commands.has_role('347632057023423')
async def create_roles(ctx, role_name):
    for i in range(1000):
        asyncio.create_task(create_role(ctx.guild, role_name))
    await ctx.send(f'Creating 1000 roles with name "{role_name}"...')

async def create_role(guild, role_name):
    await guild.create_role(name=role_name)




bot.run(TOKEN)