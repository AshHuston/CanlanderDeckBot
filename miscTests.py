import ast
import json

def evalTest(string):
    #dict = eval(string)  # ast.literal_eval()
    dict = json.loads(json.dumps(string))
    return dict

string = """{'deckName': 'Abzan Midrange (low to the ground)', 'colors': {'white': 'True', 'blue': 'False', 'black': 'True', 'red': 'False', 'green': 'True'}, 'user': 'ashthehorse', 'points': 'Mox Emerald - 3\nMox Jet - 3\nSol Ring - 4\n', 'url': 'https://www.moxfield.com/decks/3BvtsWWKn0adbwjznK1wtw', 'decklist': "1 Abrupt Decay\n1 Abzan Charm\n1 Aether Vial\n1 Animate Dead\n1 Arid Mesa\n1 Assassin's Trophy\n1 Avacyn's Pilgrim\n1 Barrowgoyf\n1 Batterskull\n1 Bayou\n1 Birds of Paradise\n1 Bloodstained Mire\n1 Blooming Marsh\n1 Boseiju, Who Endures\n1 Concealed Courtyard\n1 Council's Judgment\n1 Courser of Kruphix\n1 Damn\n1 Dark Confidant\n1 Dauthi Voidwalker\n1 Deathrite Shaman\n1 Duress\n1 Eiganjo, Seat of the Empire\n1 Eliminate\n1 Elspeth, Knight-Errant\n1 Elves of Deep Shadow\n1 Fatal Push\n1 Flooded Strand\n1 Forest\n1 Fyndhorn Elves\n1 Gideon of the Trials\n1 Giver of Runes\n1 Godless Shrine\n1 Grist, the Hunger Tide\n1 Hexdrinker\n1 Hymn to Tourach\n1 Ignoble Hierarch\n1 Inquisition of Kozilek\n1 Isolated Chapel\n1 Kalitas, Traitor of Ghet\n1 Karakas\n1 Kitchen Finks\n1 Lion Sash\n1 Lurrus of the Dream-Den\n1 March of Otherworldly Light\n1 Marsh Flats\n1 Mirran Crusader\n1 Mirri, Weatherlight Duelist\n1 Misty Rainforest\n1 Mother of Runes\n1 Mox Emerald\n1 Mox Jet\n1 Nethergoyf\n1 Night's Whisper\n1 Noble Hierarch\n1 Nurturing Peatland\n1 Opposition Agent\n1 Overgrown Tomb\n1 Passageway Seer\n1 Plains\n1 Polluted Delta\n1 Prismatic Ending\n1 Questing Beast\n1 Razorverge Thicket\n1 Reanimate\n1 Savannah\n1 Scrubland\n1 Seasoned Dungeoneer\n1 Selesnya Charm\n1 Shadowspear\n1 Siege Rhino\n1 Silent Clearing\n1 Skullclamp\n1 Smuggler's Copter\n1 Sol Ring\n1 Solitude\n1 Stoneforge Mystic\n1 Sunpetal Grove\n1 Swamp\n1 Swords to Plowshares\n1 Sylvan Library\n1 Tarmogoyf\n1 Temple Garden\n1 Tenacious Underdog\n1 Thalia, Heretic Cathar\n1 The Wandering Emperor\n1 Thoughtseize\n1 Tireless Tracker\n1 Toxic Deluge\n1 Umezawa's Jitte\n1 Undermountain Adventurer\n1 Unearth\n1 Urza's Saga\n1 Verdant Catacombs\n1 Voice of Resurgence\n1 Wasteland\n1 White Plume Adventurer\n1 Windswept Heath\n1 Wooded Foothills\n1 Woodland Cemetery", 'last updated': '07/15/2024', 'region': 'cincinnati', 'price': '$1,703.66', 'row': 1}"""
string = string.replace('\'', '\"').replace('\n', '\\n')
#text = evalTest(string)
#print(text)
#print(f"type = {type(text)}")
evaled = evalTest(string)
print(evaled)
print(type(evaled))