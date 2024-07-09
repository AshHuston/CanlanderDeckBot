import requests
from pyquery import PyQuery as pq

global pointsList

def getPointsList():
    url = 'https://canadianhighlander.ca/points-list/'
    request = requests.get(url)
    content = request.text
    if request.status_code == 200:
        doc = pq(content)
        table = doc("table")
        rows = table("tr")
        pointsList = []
        for row in rows:
            cardInfo = pq(row).text().split('\n')
            cardName = cardInfo[0]
            points = cardInfo[1]
            pointsList.append({
                'cardName': cardName,
                'points': points
                })
        return pointsList
    else:
        return f'HTML error: {request}'
    
def checkPointCost(checkCardName):
    global pointsList
    points = 0
    for pointedCard in pointsList:
        if pointedCard['cardName'] == checkCardName:
            points = int(pointedCard['points']) 
    return points

def listPointedCards(decklistArray):
    global pointsList
    pointsList = getPointsList()
    pointedCards = ""
    for cardName in decklistArray:
        points = checkPointCost(cardName)
        if points > 0:
            pointedCards += f'{cardName} - {points}\n'
    return pointedCards
