from flask import Flask, request, jsonify

app = Flask(__name__)

# Activity Level Multipliers
activity_multipliers = {
    "sedentary": 1.2,
    "lightly active": 1.375,
    "moderately active": 1.55,
    "very active": 1.725,
}

activity_multipliers = {k.lower(): v for k, v in activity_multipliers.items()}

"""
Endpoint to calculate daily calorie needs based on user data.
This endpoint expects a POST request with a JSON payload containing the following fields:
- gender (str): The gender of the user ("male" or "female").
- weight (float): The weight of the user in kilograms.
- height (float): The height of the user in centimeters.
- age (int): The age of the user in years.
- activity_level (str): The activity level of the user (e.g., "sedentary", "lightly active", "moderately active", "very active", "extra active").
- goal (str): The user's goal ("lose weight", "gain weight", "maintain weight").
Returns:
- JSON response with the following fields:
    - bmr (float): The Basal Metabolic Rate (BMR) of the user.
    - caloriesNeeded (float): The daily calorie needs of the user adjusted for activity level and goal.
    - goal (str): The user's goal, capitalized.
    - activityLevel (str): The user's activity level, capitalized.
Possible error responses:
- 400: If any required data is missing or invalid.
"""
@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()
    gender = data.get("gender")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    activity_level = data.get("activity_level")
    if activity_level.lower() not in activity_multipliers:
        return jsonify({"error": "Invalid activity level"}), 400
    goal = data.get("goal")

    if any(data.get(key) is None for key in ["gender", "weight", "height", "age", "activity_level", "goal"]):
        return jsonify({"error": "Missing data in request"}), 400

    if gender.lower() not in ["male", "female"]:
        return jsonify({"error": "Invalid gender value"}), 400

    
    if gender.lower() == "male":
        bmr = calculate_bmr_male(weight, height, age)
    else:
        bmr = calculate_bmr_female(weight, height, age)

    # Adjust for activity level
    # Validate goal
    if goal.lower() not in ["lose weight", "gain weight", "maintain weight"]:
        return jsonify({"error": "Invalid goal value"}), 400

    # Adjust for activity level
    calories = bmr * activity_multipliers[activity_level.lower()]

    # Adjust for goal
    calories = adjust_for_goal(calories, goal)

    
    return jsonify({
        "bmr": round(bmr, 2),
        "caloriesNeeded": round(calories, 2),
        "goal": goal.capitalize(),
        "activityLevel": activity_level.capitalize(),
    })

"""
Adjusts the calorie intake based on the user's goal.

Parameters:
calories (int): The current calorie intake.
goal (str): The user's goal, which can be "lose weight" or "gain weight".

Returns:
int: The adjusted calorie intake. If the goal is "lose weight", 500 calories are subtracted.
        If the goal is "gain weight", 500 calories are added. If the goal is neither, the original
        calorie intake is returned.
"""
def adjust_for_goal(calories, goal):
    
    if goal.lower() == "lose weight":
        return calories - 500
    elif goal.lower() == "gain weight":
        return calories + 500
    return calories

# BMR Calculation
def calculate_bmr_male(weight, height, age):
    return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)

def calculate_bmr_female(weight, height, age):
    return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)