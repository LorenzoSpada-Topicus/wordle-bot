import base64
from openai import OpenAI
from pydantic import BaseModel


class GameStatus(BaseModel):
    found: bool
    finished: bool

model = "o4-mini-2025-04-16"

def llm_guess(image_path, req_word_len):

    client = OpenAI()
    

    with open(image_path, "rb") as image_file:
        base64_img = base64.b64encode(image_file.read()).decode("utf-8")

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Your job is to play wordle, I want you to think about all the possible combinations of words and suggest the next line based on the letters in the image. Please return a {req_word_len} string, and **output only that word**—no explanations. If you see that not a lot of letters are green or yellow you should focus on giving an anwer that uncovers a lot of letters. If there are no letters selected yet, start the first word. NEVER REPEAT THE SAME WORD AND GIVE ONLY {req_word_len} AMOUNT OF CHARACTERS BACK. thank you!"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}",
                        },
                    },
                ],
            }
        ],
        response_format={"type": "text"},
    )
    return completion.choices[0].message.content


def llm_eval(image_path):
    client = OpenAI()

    with open(image_path, "rb") as image_file:
        base64_img = base64.b64encode(image_file.read()).decode("utf-8")

        completion = client.chat.completions.parse(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "You’re playing Wordle. Your job is to evaluate if the **full** word has been found, not just one letter or a few, it has to be 5 letters in green in a single row. also if the bottom row below above the keyboard has been filled in, you give back finished, First, describe which tiles are green, yellow, gray. Then output the booleans.\nExample 1: image shows five green letters → found: true, finished: true\nExample 2: image shows no green letters but 6 rows used → found: false, finished: true\nExample 3: image shows some yellow/green but rows remain → found: false, finished: false\nPLEASE ONLY OUTPUT 5 letters DONT OUTPUT YOUR THOUGHT PROCESS"
                        "return **only** a JSON object matching this schema—and nothing else:"
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                }
            ]
        }],
        response_format=GameStatus,  
    )
        
    status: GameStatus = completion.choices[0].message.parsed # type: ignore
    print(f"Found?: {status.found}, Finished?: {status.finished}")
    return status.found, status.finished
    