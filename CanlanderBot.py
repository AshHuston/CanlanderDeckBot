import database
import discord
from discord.ext import commands
import moxfieldDecklist
import canlanderPoints
from datetime import date
import time
from thefuzz import fuzz
import validators

databaseUpdating = False # Will use to disable everything else during the update.    NEW_PLAN = Maybe it's better to make a thread, make a copy of the DB, update all those entries, then replace the old with the new.
decklistDatabase = database.database('canlanderDecksDB', ['deckName', 'colors', 'tags', 'user', 'points', 'url', 'decklist', 'last updated', 'region', 'price'])
botAuthToken = "bot_token"

intents = discord.Intents.default()
intents.message_content = True
helpCommand = commands.DefaultHelpCommand(no_category = 'Commands', dm_help = True)
bot = commands.Bot(command_prefix='/', intents=intents, help_command=helpCommand)    

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    print(error)

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

def formatDate(inputDate):
    split = inputDate.replace('-', ' ').replace('/', ' ').split()
    year = split[0]
    month = split[1]
    day = split[2]
    formatted = f'{month}/{day}/{year}'
    return formatted

def getCurrentDate():
    return formatDate(str(date.today()))

def getUpdateDate(inputDate):
    return inputDate.split(',')[0]

def findDecksAfterDate(value):
    date = value.replace('/', '-').replace('.', '-').split('-')
    months = date[0]
    days = date[1]
    years = date[2]
    inputTotalDays = days + (months*30) + (years*365)

    foundDeckRowIDs = []
    stillFindingRows = True
    i = 1
    while stillFindingRows:
        rowData = decklistDatabase.getRows('row', i)
        if rowData != []:
            rowDate = rowData['last updated']
            rowDate = rowDate.replace('/', '-').replace('.', '-').split('-')
            months = rowDate[0]
            days = rowDate[1]
            years = rowDate[2]
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
                fullDeckList = decklistDatabase.getValue(i, 'decklist').lower().replace("/", " ")
            except:
                i = -1
                continue
            dontAdd = False
            for each in cardsList:
                if fullDeckList.count(each.strip()) < 1:
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
            key = 'last updated'
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
        case 'last updated':
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
@bot.command(hidden=True, aliases=['updatedecks'])
async def updateDecks(ctx):
    isMod = False
    for each in ctx.author.roles:
        if each.name.lower() == 'moderator':
            isMod = True

    if isMod:
        loadingMessage = await ctx.send('Updating database. This may take a while.')
        databaseUpdating = True
        start = time.time()
        oldDB = open('db_canlanderDecksDB.txt', 'r')
        oldDB_text = oldDB.read()
        oldDB.close()
        currentDate = getCurrentDate().replace('/', '-')
        backupDBName = f'dbBackup_{currentDate}'
        
        try:
                backup = open(f'{backupDBName}.txt', 'x')
        except:
            i = 1
            while True:
                try:
                    backup = open(f'{backupDBName}({i}).txt', 'x')
                    break
                except:
                    i += 1
            
        backup.write(oldDB_text)
        backup.close()
        i = 1
        while i>0:
            oldData = decklistDatabase.getRows('row', i)
            if len(oldData) == 0:
                break
            moxfieldLink = oldData['url']
            moxfieldDeckInfo = await moxfieldDecklist.getDeckInfo(moxfieldLink)
            deckData = {
                "deckName": moxfieldDeckInfo['deckName'].replace('\'', ''), 
                "colors": moxfieldDeckInfo['colors'], 
                "tags": f"{oldData['tags']}", 
                "user": f"{oldData['user']}", 
                "points": getPoints(moxfieldDeckInfo['decklist']), 
                "url": moxfieldLink, 
                "decklist": moxfieldDeckInfo['decklist'].replace("'", "").replace("/", " ").replace(",", "").replace(".", ""), 
                "last updated": getUpdateDate(moxfieldDeckInfo['lastUpdated']).lstrip("0"), 
                "region": decklistDatabase.getValue(i, 'region'),
                "price": moxfieldDeckInfo['price']
                }
            try:
                decklistDatabase.updateRow(i, str(deckData))
            except:
                response = await ctx.send(f"error at db row {i}")
            i += 1
        databaseUpdating = False
        file = discord.File("db_canlanderDecksDB.txt")
        await ctx.send(file=file, content="New backup:")
        end = time.time()
        response = await ctx.send(f"Database finished updating in {round(end-start, 1)} seconds.")
    else:
        response = await ctx.send(f"Sorry! You do not have the required permissions to use this command.")
    time.sleep(5)
    await loadingMessage.delete()
    await response.delete()
    

   # ------------------------------------------------------------------------------------------------------ DB cant see the file i guess? its not reading anything so like idk... ------------------------------# 


# ----------------------------------CLIENT_COMMANDS----------------------------------------- #
@bot.command(aliases=['pointscheck', 'points'])
async def pointsCheck(ctx, url):
    """Get points from a moxfield link

    Args:
        url: The link to check

    Raises:
        commands.UserInputError: Entered an invalid url
    """
    if not validators.url(url):
        raise commands.UserInputError
    loadingMessage = await ctx.send("Checking...")
    deckInfo = await moxfieldDecklist.getDeckInfo(url)
    points = getPoints(deckInfo["decklist"])
    await loadingMessage.delete()
    await ctx.send(points)
@pointsCheck.error
async def pointsCheckError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        msg = f'Missing required argument.\nCorrect syntax: /{ctx.invoked_with} moxfield_link'
    if isinstance(error, commands.UserInputError):
        msg = f'There was an input error.\nCorrect syntax: /{ctx.invoked_with} moxfield_link'
    response = await ctx.send(msg)
    time.sleep(15)
    await response.delete().error

@bot.command(aliases=['uploadDeck', 'uploaddeck', 'submitDeck', 'submitdeck', 'savedeck', 'addDeck', 'adddeck'])
async def saveDeck(ctx, moxfieldLink, region='Online', *tags):
    """Upload a deck to the database

    Args:
        moxfieldLink: The decklist link from moxfield
        region (optional): The geographical region that the deck is played in. Defaults to 'Online'.
        tags (optional): *Must enter region before tags.* Any number of tags to help with searching.

    Raises:
        commands.UserInputError: Entered an invalid URL
    """
    if not validators.url(moxfieldLink):
        raise commands.UserInputError
    loadingMessage = await ctx.send("Uploading to database...")
    moxfieldDeckInfo = await moxfieldDecklist.getDeckInfo(moxfieldLink)
    deckData = {
        "deckName": moxfieldDeckInfo['deckName'].replace('\'', ''), 
        "colors": moxfieldDeckInfo['colors'], 
        "tags": f"{tags}", 
        "user": f"{ctx.author}", 
        "points": getPoints(moxfieldDeckInfo['decklist']), 
        "url": moxfieldLink, 
        "decklist": moxfieldDeckInfo['decklist'].replace("'", "").replace("/", " ").replace(",", "").replace(".", ""), 
        "last updated": getUpdateDate(moxfieldDeckInfo['lastUpdated']).lstrip("0"), 
        "region": region,
        "price": moxfieldDeckInfo['price']
        }

    deckID = findDeckByUrl(deckData['url'])
    if deckID != -1:
        originalAuthor = decklistDatabase.getValue(deckID, 'user')
        if originalAuthor != ctx.author.name:
            msg = f'Sorry, this list has already been submitted by {originalAuthor} at storage ID {deckID}.'
        else:
            if updateDatabaseEntry(deckID, deckData):
                msg = 'Your entry has been updated!'
            else:
                msg = 'There was an issue with your update. Wait a moment and try again. If you still have issues please contact AshTheHorse.'
        

    else:
        if addNewDatabaseEntry(deckData):
            msg = 'Your entry has been added to the database!'
        else:
            msg = 'There was an issue with your entry. Wait a moment and try again. If you still have issues please contact AshTheHorse.'
    await loadingMessage.delete()
    response = await ctx.send(msg)
    time.sleep(5)
    await response.delete()
@saveDeck.error
async def saveDeckError(ctx, error):
    msg = f'Unknown error in /{ctx.invoked_with}'
    if isinstance(error, commands.MissingRequiredArgument):
        msg = f'Missing required argument.\nCorrect syntax: /{ctx.invoked_with} moxfield_link region tag1 tag2...'
    if isinstance(error, commands.UserInputError):
        msg = f'There was an input error.\nCorrect syntax: /{ctx.invoked_with} moxfield_link region tag1 tag2...'
    
    response = await ctx.send(msg)
    time.sleep(15)
    await response.delete()

@bot.command(aliases=['listDecks', 'findDecks', 'finddecks', 'listdecks', 'searchdecks', 'listDeck', 'findDeck', 'finddeck', 'listdeck', 'searchdeck', 'searchDeck'], help="Search the database by any number of filters")
async def searchDecks(ctx, *args):
    """Search the database for decks matching any number of criteria. valid criteria include:
    url: The moxfield link.
    colors: wubrg, guilds, shards, or wedges. Colors will return decks with at minimum these colors. If you wish to search exact colors, include an asterisk "*" in the request. (colors=*rg)
    date: The longest ago that results will have been updated.
    meta: The region to search for. "Online" is a valid option.
    budget: The highest pricepoint (tcgplayer low) to find decks.
    deckname: Searches decks that contain the entered text in their name.
    archetype: Searches tags and deckname for the entered text.
    cards: Searches for decks with al listed cards. Separate cards by /. If there are spaces, you must wrap the whole critera in quotes like so "cards=force of will"
    author: the discord user to search for submissions by.
    tags: Searc for decks whos tags include all listed tags exactly. Multiple tags should be (in parenthsis, and, comma separated)

    Args:
        filters: Any number of filters, separated by spaces. Should be formatted like so: critera=value. e.g. colors=wu. 
                  If a value contains spaces, such as "cards=lightning bolt/brainstorm", you must surround that entire criterion in quotes as shown here.

    """
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
        subDate = decklistDatabase.getValue(unique, 'last updated')
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
    """Get database entry by ID#

    Args:
        id: The ID# of the entry to fetch.
    """
    deckName = decklistDatabase.getValue(id, 'deckName')
    subDate = decklistDatabase.getValue(id, 'last updated')
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
@deckInfo.error
async def deckInfoError(ctx, error):
    msg = 'An unknown error occured. Try again or contact AshTheHorse.'
    if isinstance(error, commands.MissingRequiredArgument):
        msg = f'Missing required argument.\nCorrect syntax: /{ctx.invoked_with} deckID#'
    response = await ctx.send(msg)
    time.sleep(15)
    await response.delete()    

@bot.command(aliases=['howmanydecks', 'howManyDecks', 'deckcount'])
async def deckCount(ctx):
    """Says how many decks are in the database
    """
    i = 0
    while True:
        i += 1
        row = decklistDatabase.getRows('row', i)
        if row == []:
            break
    await ctx.send(f'There are currently {i} decks in the database.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.strip().startswith('https://www.moxfield.com'):
        link = message.content.split()[0]
        if findDecksBy('url', link) == []:
            msg = await message.channel.send('Looks like you just shared a Moxfield link that isn\'t in the database.\nWe\'d appreicaite if you add it with "/saveDeck MOXFIELD_LINK".')
                                       #Would you like to add it to the database? (respond "yes" or "no". Or ignore for 10 econds.)')
            start = time.time()
            while True:
                current = time.time()
                if current - start >=10:
                    await msg.delete()
                    break
        
      #  waitingOnUser = message.author #Eventually use this to make an easy "yes id like to add this to the DB" response withot making the user call /addDeck
      #  waitingForResponse = True
      #  startWait = time.time
      #  while waitingForResponse:
      #      pass
    await bot.process_commands(message)

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