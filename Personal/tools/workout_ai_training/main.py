import requests
from datetime import datetime
from env import *



# date and time:
date = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%X")

# User Spesifics:
GENDER = "male"
WEIGHT_KG = 72.5
HEIGHT_CM = 167.64
AGE = 28
exercise_text = input("Tell me which exercises you did: ")

# nutritionix - Smart API that will detect the exercise, duration and calories from a given string.
nutritionix_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}
nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json",
}
nutritionix_response = requests.post(url=nutritionix_url, json=nutritionix_params, headers=nutritionix_headers)
exercise_list = nutritionix_response.json()['exercises']



# Sheety API - Will make an API out of GOOGLE SHEET and will populate it with new lines:
sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {sheety_token_api_authorization_key}"
}
sheet_inputs = {
        "workout": {
            "date": "date",
            "time": "time",
            "exercise": "exercise",
            "duration": "duration",
            "calories": "calories"
        }
    }
for exercise_elem in exercise_list:
    exercise = exercise_elem['user_input']
    duration = exercise_elem['duration_min']
    calories = exercise_elem['nf_calories']
    sheet_inputs = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }
    sheety_response = requests.post(url=sheety_url, json=sheet_inputs, headers=sheety_headers)




