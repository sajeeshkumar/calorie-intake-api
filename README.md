# Calorie Intake Calculator API

A simple Flask-based API to calculate daily calorie intake based on user attributes.

## Features
- Calculates daily calorie needs using the Harris-Benedict equation.
- Supports activity levels and fitness goals (e.g., lose weight, gain weight).
- Provides activity level multipliers.

## Endpoints
- `POST /calculate-calories`: Calculate daily calorie needs.
- `GET /activity-levels`: Fetch activity level options.

## How to Run
1. Clone the repository: git clone <repo_url>
2. Install dependencies: pip install -r requirements.txt
3. Run the application: python app.py

## Sample test

curl -X POST https://calorie-intake-api.onrender.com/calculate-calories \
-H "Content-Type: application/json" \
-d '{"gender": "male", "weight": 97, "height": 180, "age": 44, "activity_level": "moderately active", "goal": "lose weight"}'
{"activityLevel":"Moderately active","bmr":2001.9,"caloriesNeeded":2602.95,"goal":"Lose weight"}

