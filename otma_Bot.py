import discord
import asyncio
from discord.ext import commands

Token = 'MTIzNTkyMzAzOTEzMzI0MTM4NA.G6ceOX.JoZvRpZA1H3Xheh5X6u-o2_gS8sKyvAX3kIREc'
intents = discord.Intents.default()
intents.message_content = True

bot  = commands.Bot(command_prefix = "!" , intents = intents)
@bot.event
async def on_ready():
    print("Bot is running!!")

@bot.command()
@commands.has_role("ꜰᴏᴜɴᴅᴇʀ")
async def delete_messages(ctx):
    channel = ctx.channel
    await channel.purge()

@bot.command()
@commands.has_role("ꜰᴏᴜɴᴅᴇʀ")
@commands.has_role("ᴏᴛᴍᴀ-ᴛᴇᴀᴍ")
@commands.has_role("ᴀᴅᴍɪɴꜱ")
async def Move_All(ctx, *members: discord.Member):
    for member in members:
        await member.move_to(ctx.author.voice.channel)
        await ctx.send(f"{member.display_name} moved!!!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(word.startswith("http") for word in message.content.split()):
        await message.delete()
        await message.channel.send(f"{message.author.mention} , you cant sennd link!!")

    await bot.process_commands(message)


bot.run(Token)

