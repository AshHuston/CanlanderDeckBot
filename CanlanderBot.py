import database
import os
import discord
from discord.ext import commands
import moxfieldDecklist
import canlanderPoints
from datetime import date
import time

decklistDatabase = database.database('canlanderDecksDB', ['deckName', 'colors', 'tags', 'user', 'points', 'url', 'decklist', 'submission date', 'region', 'price'])

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

def findDeckByUrl(url):
    foundDeck = decklistDatabase.getRowNumbers('url', url)
    foundDeckRowID = -1
    if foundDeck != []:
        foundDeckRowID = foundDeck
    return foundDeckRowID

def findDecksBy(criterion, value):
    foundDeckRowIDs = decklistDatabase.getRowNumbers(criterion, value)
    return foundDeckRowIDs

def updateDatabaseEntry(rowID, deckData):
    try:
        if len(deckData['tags'])<1:
            tags = decklistDatabase.getValue(rowID, 'tags')
            deckData['tags'] = tags
        if deckData['region'] == "Online":
            region = decklistDatabase.getValue(rowID, 'region')
            deckData['region'] = region
        decklistDatabase.updateRow(rowID, str(deckData))
        return True
    except:
        return False

def addNewDatabaseEntry(deckData):
    try:
        decklistDatabase.addRow(deckData)
        return True
    except:
        return False

def getCurrentDate():
    return str(date.today())


# ----------------------------------MOD_COMMANDS------------------------------------- #
@bot.command()
async def updateDecks(ctx):
    # Goes though deck database. If any decks have changed on moxfield, update them.
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
async def saveDeck(ctx, moxfieldLink, region='Online', *tags):
    loadingMessage = await ctx.send("Uploading to database...")
    moxfieldDeckInfo = moxfieldDecklist.getDeckInfo(moxfieldLink)
    deckData = {
        "deckName": moxfieldDeckInfo['deckName'], 
        "colors": moxfieldDeckInfo['colors'], 
        "tags": f"{tags}", 
        "user": f"{ctx.author}", 
        "points": getPoints(moxfieldDeckInfo['decklist']), 
        "url": moxfieldLink, 
        "decklist": moxfieldDeckInfo['decklist'], 
        "submission date": getCurrentDate(), 
        "region": region,
        "price": moxfieldDeckInfo['price']
        }

    deckID = findDeckByUrl(deckData['url'])
    if deckID != -1:
        if updateDatabaseEntry(deckID, deckData):
            msg = 'Your entry has been updated!'
        else:
            msg = 'There was an issue with your update. Wait a moment and try again. If you still have issues please contact AshTheHorse.'
        originalAuthor = decklistDatabase.getValue(deckID, 'user')
        if originalAuthor != ctx.author.name:
            msg = f'Sorry, this list has already been submitted by {originalAuthor} at storage ID {deckID}.'

    else:
        if addNewDatabaseEntry(deckData):
            msg = 'Your entry has been added to the database!'
        else:
            msg = 'There was an issue with your entry. Wait a moment and try again. If you still have issues please contact AshTheHorse.'
    await loadingMessage.delete()
    response = await ctx.send(msg)
    time.sleep(5)
    await response.delete()
    
@bot.command()
async def searchDecks(ctx, **criteria): ## --------------------------Look inot **kwargs more!
    loadingMessage = await ctx.send("Searching database...")
    allResultIDs = []
    for criterion in criteria:
        resultsForThis = findDecksBy(criterion, criteria[criterion])
        allResultIDs.append(resultsForThis)
    
    fullMatches = set()
    for each in allResultIDs:
        if allResultIDs.count(each) == len(criteria):
            fullMatches.add(each)
    
    outputLines = ""
    for unique in fullMatches:
        deckID = unique
        deckName = decklistDatabase.getValue(unique, 'deckName')
        url = decklistDatabase.getValue(unique, 'url')
        outputLines.append(f'ID: {deckID} - [{deckName}] - {url}')
    
    await loadingMessage.delete()
    if outputLines == "":
        await ctx.send('Sorry, no decks found.')
    else:
        await ctx.send(outputLines)
    #embed = discord.Embed()
    #embed.description = outputLines
    #await ctx.send(embed=embed)


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