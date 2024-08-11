from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.options import Options

# I'd rather a way to do this all without simulating a browser. But some of the data I need is behind dynamic elements in the webpage so IDK how.

def getDeckInfo(url, headless=True):
    options = Options()
    service = webdriver.FirefoxService(executable_path='geckodriver.exe')
    if headless:
        options.add_argument("--headless=new")
    driver = webdriver.Firefox(options=options, service=service)
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
        "white": f"{(float(whitePercent)>0)}",
        "blue": f"{(float(bluePercent)>0)}",
        "black": f"{(float(blackPercent)>0)}",
        "red": f"{(float(redPercent)>0)}",
        "green": f"{(float(greenPercent)>0)}"
    }

    buyBtn = driver.find_element(By.PARTIAL_LINK_TEXT, 'Buy')
    buyBtn.click()
    buyBtn.send_keys(Keys.RETURN)
    tcgRadio = driver.find_element(By.ID, 'affiliate-tcgplayer')
    tcgRadio.click()
    tcgRadio.send_keys(Keys.RETURN)
    possiblePrices = driver.find_elements(By.CLASS_NAME, 'ms-1')
    textCandidates =[]
    for each in possiblePrices:
        textCandidates.append(each.text)
    price = textCandidates[-1]

    tcgRadio.send_keys(Keys.ESCAPE)
    
    lastUpdatedLable = driver.find_element(By.ID, "lastupdated")
    lastUpdatedLable.click()
    lastUpdateDateLable = driver.find_elements(By.CLASS_NAME, "cursor-help")[0]#.text
    while True:
        lastUpdateDateLable.click()
        try:
            lastUpdateDate = driver.find_element(By.XPATH, "//div[@style = 'transform: translateY(1px);']").text
            break
        except:
            continue
        
    decklistInfo = {
        "deckName": deckName,
        "colors": colors,
        "price": price,
        "lastUpdated": lastUpdateDate,
        "decklist": decklist
    }
    
    driver.close()
    return decklistInfo

# This test is only here so on startup it will check if selenium works. Still trying to get it to work on the cloud. 
print(getDeckInfo('https://www.moxfield.com/decks/kIe_Vt25jk6-e4ZCkFIeTg'))