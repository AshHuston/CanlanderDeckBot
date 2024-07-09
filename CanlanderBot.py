import database
import os
import discord
from discord.ext import commands
import moxfieldDecklist

botAuthToken = 'MTI1ODUwMjkzNTc4NTI0MjY2NQ.G5Sxwg.eFvhLii4x1nz8FOO5uUto4dUZOi8mSKR8k_95A'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)    

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#----------------------------------COMMANDS-----------------------------------------#
@bot.command()
async def deckColors(ctx, url):
    print("test")
    await ctx.send("Checking...")
    deckInfo = moxfieldDecklist.getDeckInfo(url)
    await ctx.send(deckInfo["colors"])

@bot.command()
async def saveDeck(ctx, url):
    await ctx.send("Uploading to database...")
    user = 
    pass

# properties of a deck
    # Name
    # Colors (derivable)
    # Tags
    # User who submitted (derivable)
    # Points (derivable)
    # Link
    # Decklist
    # Database ID (derivable)
    # Submission date  (derivable)
    # Region



"""
data = {"name": 'Ash Huston', 'color': 'blue', 'flavor': 'delicious'}
mydb.addRow(data)
data = {'name': 'Grace Huston', 'color': 'blue', 'flavor': 'delicious'}
mydb.addRow(data)
data = {'name': 'Sprinkle Huston', 'color': 'pink', 'flavor': 'strawberry'}
mydb.addRow(data)
data = {'name': 'Dexter Morgan', 'color': 'red', 'flavor': 'metallic'}
mydb.addRow(data)


print(mydb.encryptionKey)
print(mydb.getValuesFromRows('name', 'color', 'red'))
mydb.updateRow(1, "{'name': 'Ash Huston', 'color': 'red', 'flavor': 'manly'}")
print(mydb.getValuesFromRows('name', 'color', 'red'))
mydb.updateValue(1, 'color', 'blue')
print(mydb.getValuesFromRows('name', 'color', 'red'))
print(mydb.getRowNumbers('color', 'red'))
"""

# ---------- Discord bs. Don't touch it. ----------
try:
    token = botAuthToken or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e