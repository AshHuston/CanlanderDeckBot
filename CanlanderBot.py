import database
import os
import discord
from discord.ext import commands
import moxfieldDecklist
import canlanderPoints

decklistDatabase = database.database('canlanderDecksDB', ['deckName', 'colors', 'tags', 'user', 'points', 'link', 'decklist', 'submission date', 'regions', 'price'])

botAuthToken = 'MTI1ODUwMjkzNTc4NTI0MjY2NQ.G5Sxwg.eFvhLii4x1nz8FOO5uUto4dUZOi8mSKR8k_95A'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)    

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# ----------------------------------FUNCTIONS---------------------------------------- #
def createDatabaseEntry(dataStruct):
    try:
        decklistDatabase.addRow(dataStruct)
        return True
    except:
        return False
    
def getPoints(decklist):
    decklist = decklist.split("\n")
    i = 0
    while i < len(decklist):
        text = decklist[i]
        if text == "" or text == 'SIDEBOARD:':
            decklist.pop(i)
            i -= 1
        i += 1

    for i in range(len(decklist)):
        originalString = decklist[i]
        noQuantity = originalString.split(" ", 1)[1]
        noSetID = noQuantity.split("(", 1)[0]
        decklist[i] = noSetID

    return canlanderPoints.listPointedCards(decklist)

def getCurrentDate():
    pass
# ----------------------------------MOD_COMMANDS------------------------------------- #
@bot.command()
async def modOnly(ctx):
    pass
    
# ----------------------------------COMMANDS----------------------------------------- #
@bot.command()
async def pointsCheck(ctx, url):
    loadingMessage = await ctx.send("Checking...")
    deckInfo = moxfieldDecklist.getDeckInfo(url)
    points = getPoints(deckInfo["decklist"])
    await loadingMessage.delete()
    await ctx.send(points)
    
@bot.command()
async def saveDeck(ctx, moxfieldLink, region, *tags):
    loadingMessage = await ctx.send("Uploading to database...")
    moxfieldDeckInfo = moxfieldDecklist.getDeckInfo(moxfieldLink)
    deckData = {
        'deckName': moxfieldDeckInfo['deckName'], 
        'colors': moxfieldDeckInfo['color'], 
        'tags': tags, 
        'user': ctx.author, 
        'points': getPoints(moxfieldDeckInfo['decklist']), 
        'link': moxfieldLink, 
        'decklist': moxfieldDeckInfo['decklist'], 
        'submission date': getCurrentDate(), 
        'region': region,
        'price': moxfieldDeckInfo['price']
        }

   


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

# ---------- Discord stuff. Don't touch it. ----------
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