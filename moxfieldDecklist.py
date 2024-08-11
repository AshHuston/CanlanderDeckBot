from playwright.sync_api import sync_playwright, Playwright
import time

#####       YOU HAVE TO SWAP TO THE ASYNC API FOR PLAYWRIGHT BC REASONS

def run(playwright: Playwright, url):
    # Boilerplate
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.goto(url)
   
    # Deckname
    deckname_locator = page.locator(".deckheader-name")
    deckname_locator.wait_for()
    deckName = deckname_locator.text_content()
    
    # Colors
    whitePercent_locator = page.locator("#coloranalysis_pips_w")
    bluePercent_locator = page.locator("#coloranalysis_pips_u")
    blackPercent_locator = page.locator("#coloranalysis_pips_b")
    redPercent_locator = page.locator("#coloranalysis_pips_r")
    greenPercent_locator = page.locator("#coloranalysis_pips_g")
    whitePercent_locator.wait_for()
    bluePercent_locator.wait_for()
    blackPercent_locator.wait_for()
    redPercent_locator.wait_for()
    greenPercent_locator.wait_for()
    whitePercent = whitePercent_locator.text_content().split("%")[0]
    bluePercent = bluePercent_locator.text_content().split("%")[0]
    blackPercent = blackPercent_locator.text_content().split("%")[0]
    redPercent = redPercent_locator.text_content().split("%")[0]
    greenPercent = greenPercent_locator.text_content().split("%")[0]
    colors = {
        "white": f"{(float(whitePercent)>0)}",
        "blue": f"{(float(bluePercent)>0)}",
        "black": f"{(float(blackPercent)>0)}",
        "red": f"{(float(redPercent)>0)}",
        "green": f"{(float(greenPercent)>0)}"
    }
    
    # Price
    buy_btn_locator = page.get_by_text('BuyDeck')
    buy_btn_locator.wait_for()
    buy_btn_locator.click()
    tcg_radio_locator = page.locator("#affiliate-tcgplayer")
    tcg_radio_locator.wait_for()
    tcg_radio_locator.click()
    possiblePrices = page.locator(".ms-1")
    price = possiblePrices.all()[-1].text_content()
    page.keyboard.down('Escape')
    
    # Decklist
    more_btn_locator = page.locator('#subheader-more')
    more_btn_locator.wait_for()
    more_btn_locator.click()
    export_btn_locator = page.get_by_text('Export')
    export_btn_locator.wait_for()
    export_btn_locator.click()
    decklist = page.locator("[name='mtgo']").text_content()
    page.keyboard.down('Escape')

    #Last updated
    last_updated_btn_locator = page.locator('#lastupdated')
    last_updated_btn_locator.wait_for()
    last_updated_btn_locator.click()
    allUpdateDateLable_locator = page.locator(".cursor-help")
    time.sleep(2)
    lastUpdateDateLable_locator = allUpdateDateLable_locator.all()[0]
    lastUpdateDateLable_locator.wait_for()
    while True:
        lastUpdateDateLable_locator.click()
        try:
            lastUpdateDate = page.locator("xpath=//div[@style = 'transform: translateY(1px);']").text_content()
            break
        except:
            continue

    browser.close()

    decklistInfo = {
        "deckName": deckName,
        "colors": colors,
        "price": price,
        "lastUpdated": lastUpdateDate,
        "decklist": decklist
    }

    return decklistInfo

def getDeckInfo(url, headless=True):
    with sync_playwright() as playwright:
        return(run(playwright, url))

# For testing purposes
#print(getDeckInfo('https://www.moxfield.com/decks/hlyRtm2pUUu5sDWMqvsZWQ/history'))