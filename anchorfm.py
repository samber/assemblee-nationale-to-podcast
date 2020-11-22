import asyncio
import os

from pyppeteer import launch

ANCHOR_FM_EMAIL = os.environ['ANCHOR_FM_EMAIL']
ANCHOR_FM_PASSWORD = os.environ['ANCHOR_FM_PASSWORD']
DEBUG = os.environ['DEBUG'] == 'true'

UPLOAD_TIMEOUT = 600*1000  # 10 min

async def debug_screenshot(page, nbr):
    if DEBUG is True:
        if not os.path.exists('/tmp/screenshot'):
            os.makedirs('/tmp/screenshot')
        return await page.screenshot(path="/tmp/screenshot/{}.png".format(nbr))
    return

# inspired by => https://github.com/Schrodinger-Hat/youtube-to-anchorfm/blob/master/index.js
async def upload_podcast_to_anchor(podcast):
    print('open browser')
    browser = await launch(ignoreHTTPSErrors=True, args=['--no-sandbox'])
    # browser = await launch(headless=True, ignoreHTTPSErrors=True, executablePath='/usr/bin/chromium', args=['--no-sandbox'])
    page = await browser.newPage()

    # go to anchor login page
    await page.goto('https://anchor.fm/dashboard/episode/new')
    await page.setViewport({
        "width": 1600,
        "height": 789,
    })
    await debug_screenshot(page, '00')

    # login
    await page.type('#email', ANCHOR_FM_EMAIL)
    await page.type('#password', ANCHOR_FM_PASSWORD)
    await debug_screenshot(page, '01')
    
    await page.click('button[type=submit]')
    await page.waitForSelector('input[type=file]')
    await debug_screenshot(page, '02')

    # start upload
    inputFile = await page.querySelector('input[type=file]')
    await debug_screenshot(page, '03')
    await inputFile.uploadFile(podcast['timmmed_local_file'])
    await debug_screenshot(page, '04')
    print('Upload started:', podcast['timmmed_local_file'])
    await page.waitForFunction('document.querySelector("[class*=\'styles__saveButton\']").getAttribute("disabled") === null', {
        "timeout": UPLOAD_TIMEOUT,
    })
    print('Upload ended')
    await debug_screenshot(page, '05')
    await page.click('[class*=\'styles__saveButton\']')
    await page.waitForSelector('#title')
    await debug_screenshot(page, '06')

    # fill title + description
    await page.type('#title', podcast['name'])
    await debug_screenshot(page, '07')
    await page.click('[class*=\'styles__modeToggleText\']')
    await debug_screenshot(page, '08')
    await page.waitForSelector('textarea[name=description]')
    await debug_screenshot(page, '09')
    await page.type('textarea[name=description]', podcast['name'])
    await debug_screenshot(page, '10')

    # validate
    await page.click('[class*=\'styles__saveButtonWrapper\'] button')
    await page.waitFor(10 * 1000)
    await debug_screenshot(page, '11')

    print('close browser')
    await browser.close()
