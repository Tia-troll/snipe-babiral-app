import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

TARGET_USER_ID = 898947797699666010
CHANNEL_ID = 1308366869161578530
MESSAGE = "{user} getting sniped by a self made auto farm bot is crazy asl ngl"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

last_status = None


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def test(ctx):
    user = ctx.guild.get_member(TARGET_USER_ID)
    if not user:
        return await ctx.send("User not found in server.")
    await ctx.send(MESSAGE.format(user=user.mention))


@bot.event
async def on_presence_update(before, after):
    global last_status

    if before is None or after is None:
        return

    if after.id != TARGET_USER_ID:
        return

    if before.status == after.status:
        return

    if after.status in [discord.Status.online, discord.Status.idle]:

        if last_status == after.status:
            return

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(MESSAGE.format(user=after.mention))

        last_status = after.status

    else:
        last_status = after.status


bot.run(TOKEN)
