import ast
import json

def evalTest(string):
    dict = ast.literal_eval(string)  # ast.literal_eval()
    #dict = json.loads(json.dumps(string))
    return dict

string = """{'deckName': 'Ch* Devin\\'s Paradox', 'colors': {'white': 'True', 'blue': 'True', 'black': 'False', 'red': 'True', 'green': 'True'}, 'tags': '()', 'user': 'grimdignitary', 'points': 'Ancient Tomb - 1\nMana Vault - 1\nSol Ring - 4\nTinker - 3\nTolarian Academy - 1\n', 'url': 'https://www.moxfield.com/decks/dkb4T3_-CEqqiqme9nxdMw', 'decklist': '1 Academy Ruins\n1 Aetherflux Reservoir\n1 Ancient Den\n1 Ancient Tomb\n1 Azorius Signet\n1 Balance\n1 Basalt Monolith\n1 Blightsteel Colossus\n1 Brainstorm\n1 Brainsurge\n1 Candelabra of Tawnos\n1 Capsize\n1 Channel\n1 City of Traitors\n1 Codex Shredder\n1 Crop Rotation\n1 Darksteel Citadel\n1 Defense Grid\n1 Deserted Temple\n1 Drift of Phantasms\n1 Enlightened Tutor\n1 Ensnaring Bridge\n1 Everflowing Chalice\n1 Expedition Map\n1 Fabricate\n1 Fabrication Foundry\n1 Fellwar Stone\n1 Firemind Vessel\n1 Flooded Strand\n1 Glimmervoid\n1 Grim Monolith\n1 Hedron Archive\n1 Hullbreacher\n1 Inventors Fair\n1 Mana Vault\n1 Manascape Refractor\n1 Manifold Key\n1 Memory Jar\n1 Minamo School at Waters Edge\n1 Mind Stone\n1 Mishras Workshop\n1 Misty Rainforest\n1 Monumental Henge\n1 Mox Diamond\n1 Mox Opal\n1 Mystic Forge\n1 Narset Parter of Veils\n1 Oko Thief of Crowns\n1 Otawara Soaring City\n1 Paradox Engine\n1 Phyrexian Metamorph\n1 Polluted Delta\n1 Portable Hole\n1 Rings of Brighthearth\n1 Savannah\n1 Scalding Tarn\n1 Search for Glory\n1 Seat of the Synod\n1 Senseis Divining Top\n1 Shifting Woodland\n1 Simic Signet\n1 Sisays Ring\n1 Snow-Covered Island\n1 Sol Ring\n1 Sowing Mycospawn\n1 Sparas Headquarters\n1 Sylvan Scrying\n1 Talisman of Creativity\n1 Talisman of Curiosity\n1 Talisman of Progress\n1 Talisman of Unity\n1 Teferi Time Raveler\n1 Tezzeret the Seeker\n1 The Mightstone and Weakstone\n1 The Mycosynth Gardens\n1 The One Ring\n1 Thought Monitor\n1 Thran Dynamo\n1 Time Spiral\n1 Timetwister\n1 Tinker\n1 Tolaria West\n1 Tolarian Academy\n1 Transmute Artifact\n1 Tree of Tales\n1 Trinket Mage\n1 Tropical Island\n1 Tundra\n1 Ugin the Spirit Dragon\n1 Urza Lord High Artificer\n1 Urzas Cave\n1 Urzas Saga\n1 Volcanic Island\n1 Voltaic Key\n1 Walking Ballista\n1 Wargate\n1 Wheel of Fortune\n1 Whir of Invention\n1 Windfall\n1 Windswept Heath', 'last updated': '7/18/2024', 'region': 'cincinnati', 'price': '$8,305.50', 'row': 4}"""
string = string.replace("'", '"').replace('\n', '\\\n')
#text = evalTest(string)
#print(text)
#print(f"type = {type(text)}")
evaled = evalTest(string)
print(evaled)
print(type(evaled))