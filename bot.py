import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

TARGET_USER_ID = 898947797699666010   # your friend
CHANNEL_ID = 1308366869161578530      # your server channel
MESSAGE = "@{user} getting sniped by a self made auto farm bot is crazy asl ngl"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# To prevent spam on same status
last_status = None


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def test(ctx):
    """Manual test ping"""
    user = ctx.guild.get_member(TARGET_USER_ID)
    if not user:
        return await ctx.send("User not found in server.")

    await ctx.send(MESSAGE.format(user=user.mention))


@bot.event
async def on_presence_update(before, after):
    global last_status

    # only track your target
    if after.id != TARGET_USER_ID:
        return

    # skip if status didn’t change
    if before.status == after.status:
        return

    # triggers on ONLINE or IDLE
    if after.status in [discord.Status.online, discord.Status.idle]:

        # ignore repeated identical triggers
        if last_status == after.status:
            return

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(MESSAGE.format(user=after.mention))

        last_status = after.status

    else:
        # store new status so the next transition fires
        last_status = after.status


bot.run(TOKEN)
