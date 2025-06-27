from playwright.sync_api import sync_playwright

STD_DELAY = 1000

def init_wordle(startphrase):
    
    p = sync_playwright().start()
    browser = p.webkit.launch()
    page = browser.new_page()
    page.goto("https://www.nytimes.com/games/wordle/index.html")
    page.wait_for_timeout(STD_DELAY)

    for _ in range(4):
        page.keyboard.press("Tab")

    page.keyboard.press("Enter", delay=STD_DELAY)

    for i in range(2):
        page.keyboard.press("Tab")

    page.keyboard.press("Enter", delay=STD_DELAY)
    page.keyboard.press("Enter", delay=STD_DELAY)

    page.wait_for_timeout(STD_DELAY)
    page.mouse.wheel(0, 1000)
    page.wait_for_timeout(STD_DELAY)

    

    return p, browser, page

def enter_word(page, word):
    for letter in word:
        page.keyboard.press(letter, delay=STD_DELAY)
    page.keyboard.press("Enter", delay=STD_DELAY)
    page.wait_for_timeout(STD_DELAY)

    