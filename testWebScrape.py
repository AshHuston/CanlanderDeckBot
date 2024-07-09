from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options

def getDeckInfo(url):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options) 
    driver.get(url)
    waitSeconds = 20
    driver.implicitly_wait(waitSeconds)
    deckName = driver.find_element(By.CLASS_NAME, 'deckheader-name').text
    elem = driver.find_element(By.ID, "subheader-more")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    exportBtn = driver.find_element(By.LINK_TEXT, 'Export')
    exportBtn.send_keys(Keys.RETURN)
    decklistTextBox = driver.find_element(By.NAME, "mtgo")
    decklist = decklistTextBox.get_attribute('value')

    decklistTextBox.send_keys(Keys.ESCAPE)

    # Get colors
    whitePercent = driver.find_element(By.ID, "coloranalysis_pips_w").text.split("%")[0]
    bluePercent = driver.find_element(By.ID, "coloranalysis_pips_u").text.split("%")[0]
    blackPercent = driver.find_element(By.ID, "coloranalysis_pips_b").text.split("%")[0]
    redPercent = driver.find_element(By.ID, "coloranalysis_pips_r").text.split("%")[0]
    greenPercent = driver.find_element(By.ID, "coloranalysis_pips_g").text.split("%")[0]
    colors = {
        'white': (float(whitePercent)>0),
        'blue': (float(bluePercent)>0),
        'black': (float(blackPercent)>0),
        'red': (float(redPercent)>0),
        'green': (float(greenPercent)>0)
    }

    buyBtn = driver.find_element(By.PARTIAL_LINK_TEXT, 'Buy')
    buyBtn.click()
    buyBtn.send_keys(Keys.RETURN)
    tcgRadio = driver.find_element(By.ID, 'affiliate-tcgplayer')
    tcgRadio.click()
    tcgRadio.send_keys(Keys.RETURN)
    price = driver.find_element(By.ID, 'shoppingcart').text

    decklistInfo = {
        'decklist': decklist,
        'deckName': deckName,
        'colors': colors,
        'price': price
    }
    
    driver.close()
    return decklistInfo