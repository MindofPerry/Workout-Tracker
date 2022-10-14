import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = 89.35
HEIGHT_CM = 180.34
AGE = 25

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")
SHEET_ID = os.environ.get("SHEET_ID")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = f"https://api.sheety.co/{SHEET_ID}/myWorkoutsPythonProject/workouts"

exercise_input = input("Tell me which exercises you did: ")

exercise_params = {
    "query": exercise_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

exercise_header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_response = requests.post(url=exercise_endpoint, json=exercise_params, headers=exercise_header)
result = exercise_response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%H:%M:%S")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheet_header = {
        "Authorization": f"Bearer {SECRET_TOKEN}"
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs, headers=sheet_header)

    print(sheet_response.text)
