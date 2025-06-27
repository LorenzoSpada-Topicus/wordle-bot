# https://www.nytimes.com/games/wordle/index.html
from playwright.sync_api import sync_playwright
from page_actions import init_wordle, enter_word
from utils import check_len

def main():
    first_guess = "break"
    if not check_len:
        return 
    
    p, browser, page = init_wordle(first_guess)
    enter_word(page, first_guess)

    page.screenshot(path=f"example.png")

    browser.close()
    p.stop()



if __name__ == "__main__":
    main()



