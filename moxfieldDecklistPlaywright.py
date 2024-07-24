from playwright.sync_api import sync_playwright, Playwright
import time 

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("https://www.moxfield.com/")
    print(page.url)

    #page.locator("div", has=page.locator('a', has=page.locator('span', has_text="More"))).click()
    page.locator("div").filter(has=page.get_by_role("link").filter(has=page.locator("span").filter(has_text="More"))).click()
    print(page.url)
    #time.sleep(10)
    # other actions...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

"""
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
    #.replace("'", "`")


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
    price = driver.find_element(By.ID, 'shoppingcart').text

    decklistInfo = {
        "decklist": decklist,
        "deckName": deckName,
        "colors": colors,
        "price": price
    }
    
    driver.close()
    return decklistInfo
"""
from zenrows import ZenRowsClient
def getZenrowsInfo(url):
    client = ZenRowsClient("a4f31946464b27a08396ea5e149bf675d014cd29")
   # params = {"autoparse":"true"}  
    response = client.get(url)#, params=params)
    return response


url = "https://www.moxfield.com/"
#print(getZenrowsInfo(url))
#print(getDeckInfo(url).text)