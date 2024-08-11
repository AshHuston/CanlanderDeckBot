import asyncio
from playwright.async_api import async_playwright, Playwright
import time

#####       YOU HAVE TO SWAP TO THE ASYNC API FOR PLAYWRIGHT BC REASONS

async def run(playwright: Playwright, url):
    # Boilerplate
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()
    await page.goto(url)
    page.set_default_timeout(2000)
   
    # Deckname
    deckname_locator = page.locator(".deckheader-name")
    await deckname_locator.wait_for()
    deckName = await deckname_locator.text_content()

    # Colors
    whitePercent_locator = page.locator("#coloranalysis_pips_w")
    bluePercent_locator = page.locator("#coloranalysis_pips_u")
    blackPercent_locator = page.locator("#coloranalysis_pips_b")
    redPercent_locator = page.locator("#coloranalysis_pips_r")
    greenPercent_locator = page.locator("#coloranalysis_pips_g")
    await whitePercent_locator.wait_for()
    await bluePercent_locator.wait_for()
    await blackPercent_locator.wait_for()
    await redPercent_locator.wait_for()
    await greenPercent_locator.wait_for()
    whitePercent = await whitePercent_locator.text_content()
    whitePercent = whitePercent.split("%")[0]
    bluePercent = await bluePercent_locator.text_content()
    bluePercent = bluePercent.split("%")[0]
    blackPercent = await blackPercent_locator.text_content()
    blackPercent = blackPercent.split("%")[0]
    redPercent = await redPercent_locator.text_content()
    redPercent = redPercent.split("%")[0]
    greenPercent = await greenPercent_locator.text_content()
    greenPercent = greenPercent.split("%")[0]
    colors = {
        "white": f"{(float(whitePercent)>0)}",
        "blue": f"{(float(bluePercent)>0)}",
        "black": f"{(float(blackPercent)>0)}",
        "red": f"{(float(redPercent)>0)}",
        "green": f"{(float(greenPercent)>0)}"
    }
    
    # Price
    buy_btn_locator = page.get_by_text('BuyDeck')
    await buy_btn_locator.wait_for()
    await buy_btn_locator.click()
    tcg_radio_locator = page.locator("#affiliate-tcgplayer")
    await tcg_radio_locator.wait_for()
    await tcg_radio_locator.click()
    possiblePrices = page.locator(".ms-1")
    price = await possiblePrices.all()
    price = await price[-1].text_content()
    await page.keyboard.down('Escape')
    
    # Decklist
    more_btn_locator = page.locator('#subheader-more')
    await more_btn_locator.wait_for()
    await more_btn_locator.click()
    export_btn_locator = page.get_by_text('Export')
    await export_btn_locator.wait_for()
    await export_btn_locator.click()
    decklist = await page.locator("[name='mtgo']").text_content()
    await page.keyboard.down('Escape')

    #Last updated
    last_updated_btn_locator = page.locator('#lastupdated')
    await last_updated_btn_locator.wait_for()
    await last_updated_btn_locator.click()
    allUpdateDateLable_locator = page.locator(".cursor-help")
    time.sleep(2)
    allUpdateDateLable_locator = await allUpdateDateLable_locator.all()
    lastUpdateDateLable_locator = allUpdateDateLable_locator[0]
    await lastUpdateDateLable_locator.wait_for()
    while True:
        await lastUpdateDateLable_locator.click()
        try:
            lastUpdateDate = await page.locator("xpath=//div[@style = 'transform: translateY(1px);']").text_content()
            break
        except:
            continue

    await browser.close()

    decklistInfo = {
        "deckName": deckName,
        "colors": colors,
        "price": price,
        "lastUpdated": lastUpdateDate,
        "decklist": decklist
    }

    return decklistInfo

async def getDeckInfo(url, headless=True):
    async with async_playwright() as playwright:
        data = await run(playwright, url)
        print(data)
        return data

# For testing purposes
loop = asyncio.get_event_loop()
loop.run_until_complete(getDeckInfo('https://www.moxfield.com/decks/hlyRtm2pUUu5sDWMqvsZWQ'))
loop.close()
print('done')
#print(getDeckInfo('https://www.moxfield.com/decks/hlyRtm2pUUu5sDWMqvsZWQ'))