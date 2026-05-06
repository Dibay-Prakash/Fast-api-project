from fastapi import FastAPI 
import converter

app = FastAPI()

@app.get("/")

def home():
    return {"message": "Welcome to the Unit Converter API!"}



@app.get("/convert/celsius-to-fahrenheit/{celsius}")
def convert_celsius_to_fahrenheit(celsius: float):
    fahrenheit = (celsius * 9/5) + 32
    return {
        "celsius": celsius,
        "fahrenheit": fahrenheit
    }