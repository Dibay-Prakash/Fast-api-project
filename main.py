from fastapi import FastAPI
import random



quotes = [
    "Stay hungry, stay foolish.",
    "The best way to get started is to quit talking and begin doing.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Success is not in what you have, but who you are.",
    "Push yourself, because no one else is going to do it for you.",
    "Dream big and dare to fail."
]





app = FastAPI()

@app.get("/quote")
def get_random_quote():
    return {"quote": random.choice(quotes)} 




