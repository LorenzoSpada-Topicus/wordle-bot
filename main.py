from dotenv import load_dotenv
from page_actions import init_wordle, enter_word
from llm import llm_guess, llm_eval

def main():
    
    req_word_len = 5
    screen_path = "image/wordlecapture.png"

    # init environment
    p, browser, page = init_wordle()
    load_dotenv() # use a .env file with OPENAI_API_KEY

    found = False
    finished = False

    while not found and not finished:
        page.screenshot(path=screen_path)
        found, finished = llm_eval(screen_path)

        guess = llm_guess(screen_path, req_word_len)
        if not enter_word(page, guess):
            break
        print(f"LLM guessed: {guess}")

    browser.close()
    p.stop()

    if found:
        print("Word found succesfully!")
        return
    
    print("Didn't find word :(")

if __name__ == "__main__":
    main()
