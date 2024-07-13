import database
import os
import discord
from discord.ext import commands
import moxfieldDecklist
import canlanderPoints
from datetime import date
import time
from thefuzz import fuzz

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


def getColorsDict(value):
    outputColors = {'white': 'false', 'blue': 'false', 'black': 'false', 'red': 'false', 'green': 'false', 'exactColorsOnly': 'false'}
    wubrg = {
        'w': ['white'],
        'u': ['blue'],
        'b': ['black'],
        'r': ['red'],
        'g': ['green']
        }
    
    colorDictionary= {
        'abzan': ['white', 'black', 'green'],
        'naya': ['white', 'red', 'green'],
        'sultai': ['blue', 'black', 'green'],
        'jund': ['red', 'black', 'green'],
        'jeskai': ['white', 'blue', 'red'],
        'grixis': ['blue', 'black', 'red'],
        'mardu': ['white', 'black', 'red'],
        'temur': ['blue', 'green', 'red'],
        'esper': ['blue', 'black', 'white'],
        'bant': ['blue', 'white', 'green'],
        'azorius': ['white', 'blue'],
        'boros': ['white', 'red'],
        'dimir': ['blue', 'black'],
        'golgari': ['black', 'green'],
        'rakdos': ['black', 'red'],
        'selesnya': ['green', 'white'],
        'orzhov': ['white', 'black'],
        'gruul': ['green', 'red'],
        'izzet': ['blue', 'red'],
        'simic': ['blue', 'green'],
    }
    for colorName in colorDictionary:
        if colorName in value:
            for each in colorDictionary[colorName]:
                outputColors[each] = 'True'
    if outputColors == {'white': 'false', 'blue': 'false', 'black': 'false', 'red': 'false', 'green': 'false', 'exactColorsOnly': 'false'}:
        for colorName in wubrg:
            if colorName in value:
                for each in wubrg[colorName]:
                    outputColors[each] = 'True'
    if "*" in value:
        outputColors['exactColorsOnly'] = 'True'
    return str(outputColors)


def findUser(username):
    foundDeckRowIDs = []
    stillFindingRows = True
    i = 1
    perfectMatch = None
    while stillFindingRows:
        rowData = decklistDatabase.getRows('row', i)
        if rowData != []:
            matchPercent = fuzz.ratio(username, rowData['user'])
            if matchPercent == 100:
                perfectMatch = rowData["user"]
            if matchPercent >= 70:
                foundDeckRowIDs.append(rowData['row'])
        else:
            stillFindingRows = False
        i += 1
    
    if perfectMatch:
        i = len(foundDeckRowIDs)-1
        while i>=0:
            rowUser = decklistDatabase.getRows('row', foundDeckRowIDs[i])["user"]
            if rowUser != perfectMatch:
                del foundDeckRowIDs[i]
            i -= 1
    return foundDeckRowIDs


def getCurrentDate():
    return str(date.today())


def findDecksAfterDate(value):
    currentDate = getCurrentDate()
    date = currentDate.replace('/', '-').replace('.', '-')
    years = date[0]
    months = date[1]
    days = date[2]
    currentDateTotalDays = days + (months*30) + (years*365)

    try: # look for X days/weeks/months ago and newer.
        split = value.lower().split(" ")
        quantity = split[0]
        unit = split[1]
        match unit:
            case 'day':
                quantity = quantity
            case 'week':
                quantity *= 7
            case 'month':
                quantity *= 30
            case 'year':
                quantity *= 365
            case 'days':
                quantity = quantity
            case 'weeks':
                quantity *= 7
            case 'months':
                quantity *= 30
            case 'years':
                quantity *= 365
            case _:
                raise Exception
        inputTotalDays = currentDateTotalDays - quantity
    except: # look for all newer than the date given by value. Date given in YYYY-MM-DD format.
        date = value.replace('/', '-').replace('.', '-')
        years = date[0]
        months = date[1]
        days = date[2]
        inputTotalDays = days + (months*30) + (years*365)

    foundDeckRowIDs = []
    stillFindingRows = True
    i = 1
    while stillFindingRows:
        rowData = decklistDatabase.getRows('row', i)
        if rowData != []:
            rowDate = rowData['submission date']
            rowDate = rowDate.replace('/', '-').replace('.', '-')
            years = rowDate[0]
            months = rowDate[1]
            days = rowDate[2]
            rowDateTotalDays = days + (months*30) + (years*365)
            if inputTotalDays <= rowDateTotalDays:
                foundDeckRowIDs.append(rowData['row'])
        else:
            stillFindingRows = False
        i += 1
    return foundDeckRowIDs


def getEntriesByColor(key, enteredColors):
    enteredColorDict = eval(enteredColors)
    exactColorsOnly = enteredColorDict['exactColorsOnly']
    del enteredColorDict['exactColorsOnly']
    foundDeckRowIDs = decklistDatabase.getRowNumbers(key, enteredColorDict)
    if type(foundDeckRowIDs) != list:
            foundDeckRowIDs = [foundDeckRowIDs]

    if exactColorsOnly == 'false':
        i = 1
        while i>0:
            try:
                rowColors = decklistDatabase.getValue(i, 'colors')
            except:
                i = -1
                continue
            dontAdd = False
            for each in enteredColorDict:
                if enteredColorDict[each] == 'True' and rowColors[each] == 'False':
                    dontAdd = True
            if dontAdd == False:
                foundDeckRowIDs.append(i)
            i += 1

        unique = []
        for each in foundDeckRowIDs:
            if each not in unique:
                unique.append(each)
        foundDeckRowIDs = unique


    return foundDeckRowIDs


def findDecksUnderBudget(budget):
    foundDeckRowIDs = []
    if "$" in budget:
        budgetFloat = float(budget.replace("$",""))
    i = 1
    while i>0:
            try:
                rowPrice = decklistDatabase.getValue(i, 'price')
                if "$" in rowPrice:
                    rowPrice = float(rowPrice.replace("$","").replace(",",""))
            except:
                print("error in findDecksUnderBudget()")
                i = -1
                continue
            dontAdd = True
            if budgetFloat > rowPrice:
                dontAdd = False
            if dontAdd == False:
                foundDeckRowIDs.append(i)
            i += 1

    return foundDeckRowIDs


def findDecksWithCards(cards):
    foundDeckRowIDs = []
    cardsList = cards.lower().split("/")
    i = 1
    while i>0:
            try:
                fullDeckList = decklistDatabase.getValue(i, 'decklist').lower()
            except:
                i = -1
                continue
            dontAdd = False
            for each in cardsList:
                if fullDeckList.count(each) < 1:
                    dontAdd = True
            if dontAdd == False:
                foundDeckRowIDs.append(i)
            i += 1

    return foundDeckRowIDs


def findDecksBy(criterion, value):
    print(f'findDecksBy(): {criterion} - {value}')
    foundDeckRowIDs = -1
    key = criterion.lower()
    match key:
        case 'link':
            key = 'url'
        case 'color':
            key = 'colors'
        case 'date':
            key = 'submission date'
        case 'meta':
            key = 'region'
        case 'budget':
            key = 'price'
        case 'deckname':
            key = 'deckName'
        case 'deck name':
            key = 'deckName'
        case 'name':
            key = 'deckName'
        case 'archetype':
            key = 'archetype'
        case 'card':
            key = 'cards'
        case 'author':
            key = 'user'

    match key:
        case 'deckName':
            foundDeckRowIDs = decklistDatabase.getRowNumbers(key, value, True)
        case 'colors':
            foundDeckRowIDs = getEntriesByColor(key, getColorsDict(value))
        case 'tags':
            foundDeckRowIDs = decklistDatabase.getRowNumbers(key, value, True)
        case 'user':
            foundDeckRowIDs = findUser(value)
        case 'points':
            foundDeckRowIDs = decklistDatabase.getRowNumbers(key, value, True)
        case 'submission date':
            foundDeckRowIDs = findDecksAfterDate(value)
        case 'price':
            foundDeckRowIDs = findDecksUnderBudget(value)
        case 'url':
            foundDeckRowIDs = decklistDatabase.getRowNumbers(key, value)
        case 'region':
            foundDeckRowIDs = decklistDatabase.getRowNumbers(key, value)
        case 'cards':
            foundDeckRowIDs = findDecksWithCards(value)
        case 'archetype':
            foundDeckRowIDs = set()
            tagMatches = decklistDatabase.getRowNumbers('tags', value, True)
            nameMatches = decklistDatabase.getRowNumbers('deckName', value, True)
            if type(tagMatches) == list:
                for each in tagMatches:
                    foundDeckRowIDs.add(each)
            else:
                foundDeckRowIDs.add(tagMatches)
            if type(nameMatches) == list:
                for each in nameMatches:
                    foundDeckRowIDs.add(each)
            else:
                foundDeckRowIDs.add(nameMatches)
            unique = []
            for each in foundDeckRowIDs:
                if each not in unique:
                    unique.append(each)
            foundDeckRowIDs = unique

    print(f'Found rows: {foundDeckRowIDs}')
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


# ----------------------------------MOD_COMMANDS------------------------------------- #
@bot.command()
async def updateDecks(ctx):
    # Goes though deck database. If any decks have changed on moxfield, update them.
    pass
    
# ----------------------------------COMMANDS----------------------------------------- #
@bot.command(aliases=['pointscheck'])
async def pointsCheck(ctx, url):
    loadingMessage = await ctx.send("Checking...")
    deckInfo = moxfieldDecklist.getDeckInfo(url)
    points = getPoints(deckInfo["decklist"])
    await loadingMessage.delete()
    await ctx.send(points)
    
@bot.command(aliases=['submitDeck', 'submitdeck', 'savedeck'])
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
    
@bot.command(aliases=['listDecks', 'findDecks', 'finddecks', 'listdecks', 'searchdecks', 'listDeck', 'findDeck', 'finddeck', 'listdeck', 'searchdeck', 'searchDeck'])
async def searchDecks(ctx, *args):
    embed = discord.Embed()
    criteria = {}
    for each in args:
        pair = each.split("=")
        key = pair[0]
        value = pair[1]
        criteria.update({key: value})

    loadingMessage = await ctx.send("Searching database...")
    allResultIDs = []
    for criterion in criteria:
        resultsForThis = findDecksBy(criterion, criteria[criterion])
        if type(resultsForThis) != list:
            allResultIDs.append(resultsForThis)
        else:
            allResultIDs.extend(resultsForThis)
    
    fullMatches = set()
    for each in allResultIDs:
        if allResultIDs.count(each) == len(criteria):
            fullMatches.add(each)
    
    outputLines = ""
    for unique in fullMatches:
        deckID = unique
        deckName = decklistDatabase.getValue(unique, 'deckName')
        subDate = decklistDatabase.getValue(unique, 'submission date')
        url = decklistDatabase.getValue(unique, 'url')
        outputLines += f'ID: {deckID} - {subDate} - [{deckName}]({url})\n'

    await loadingMessage.delete()
    if outputLines == "":
        await ctx.send('Sorry, no decks found.')
    else:
        embed.description = outputLines
        await ctx.send(embed=embed)

@bot.command(aliases=['deckinfo', 'getDeckInfo', 'getdeckinfo'])
async def deckInfo(ctx, id):
    deckName = decklistDatabase.getValue(id, 'deckName')
    subDate = decklistDatabase.getValue(id, 'submission date')
    url = decklistDatabase.getValue(id, 'url')
    colorsDict = decklistDatabase.getValue(id, 'colors')
    colors = ""
    if colorsDict['white'] == 'True':
        colors += 'W'
    if colorsDict['blue'] == 'True':
        colors += 'U'
    if colorsDict['black'] == 'True':
        colors += 'B'
    if colorsDict['red'] == 'True':
        colors += 'R'
    if colorsDict['green'] == 'True':
        colors += 'G'
    tagsList = eval(decklistDatabase.getValue(id, 'tags'))
    tags = ""
    for tag in tagsList:
        tags += f'{tag}, '
    user = decklistDatabase.getValue(id, 'user')
    points = decklistDatabase.getValue(id, 'points')
    region = decklistDatabase.getValue(id, 'region')
    price = decklistDatabase.getValue(id, 'price')
    embed = discord.Embed()
    embed.description = f'{subDate}  -  User: {user}  -  [{deckName}]({url})\nColors: {colors}  -  Region: {region}  -  {price}\nTags:{tags}\nPoints:\n{points}'
    await ctx.send(embed=embed)
    
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