import unittest
from app import app
from app import adjust_for_goal


class CalorieApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_calculate_calories_valid_data(self):
        response = self.app.post('/calculate-calories', json={
            "gender": "male",
            "weight": 70,
            "height": 175,
            "age": 25,
            "activity_level": "moderately active",
            "goal": "maintain weight"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("bmr", data)
        self.assertIn("caloriesNeeded", data)
        self.assertIn("goal", data)
        self.assertIn("activityLevel", data)

    def test_calculate_calories_missing_data(self):
        response = self.app.post('/calculate-calories', json={
            "gender": "male",
            "weight": 70,
            "height": 175,
            "age": 25,
            "activity_level": "moderately active"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing data in request")

    def test_calculate_calories_invalid_gender(self):
        response = self.app.post('/calculate-calories', json={
            "gender": "unknown",
            "weight": 70,
            "height": 175,
            "age": 25,
            "activity_level": "moderately active",
            "goal": "maintain weight"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid gender value")

    def test_calculate_calories_invalid_activity_level(self):
        response = self.app.post('/calculate-calories', json={
            "gender": "male",
            "weight": 70,
            "height": 175,
            "age": 25,
            "activity_level": "extremely active",
            "goal": "maintain weight"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid activity level")

    def test_calculate_calories_invalid_goal(self):
        response = self.app.post('/calculate-calories', json={
            "gender": "male",
            "weight": 70,
            "height": 175,
            "age": 25,
            "activity_level": "moderately active",
            "goal": "bulk up"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid goal value")



    def test_adjust_for_goal_lose_weight(self):
        self.assertEqual(adjust_for_goal(2500, "lose weight"), 2000)

    def test_adjust_for_goal_gain_weight(self):
        self.assertEqual(adjust_for_goal(2500, "gain weight"), 3000)

    def test_adjust_for_goal_maintain_weight(self):
        self.assertEqual(adjust_for_goal(2500, "maintain weight"), 2500)

    def test_adjust_for_goal_invalid_goal(self):
        self.assertEqual(adjust_for_goal(2500, "invalid goal"), 2500)



if __name__ == '__main__':
    unittest.main()