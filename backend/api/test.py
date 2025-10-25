from fastapi import FastAPI
from pydantic import BaseModel
import random
from datetime import datetime

app = FastAPI(title="Weather API")

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    timestamp: str

weather_descriptions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy"]

@app.get("/weather/{city}")
def get_weather(city: str) -> WeatherResponse:
    # Имитация данных погоды
    temperature = round(random.uniform(-10, 35), 1)
    description = random.choice(weather_descriptions)
    humidity = random.randint(30, 90)
    
    return WeatherResponse(
        city=city.title(),
        temperature=temperature,
        description=description,
        humidity=humidity,
        timestamp=datetime.now().isoformat()
    )

@app.get("/cities")
def get_available_cities():
    return {
        "cities": [
            "Moscow", "London", "New York", "Tokyo", 
            "Paris", "Berlin", "Sydney", "Dubai"
        ]
    }