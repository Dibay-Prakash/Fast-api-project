import os
import random
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)

@app.get("/")
def index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/random/{min_val}/{max_val}")
def get_random_number(min_val: int, max_val: int):
    # This generates a random integer between the user's min and max
    res = random.randint(min_val, max_val)
    
    return {
        "min_input": min_val,
        "max_input": max_val,
        "random_number": res
    }