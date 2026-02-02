import numpy as np

class DiabetesPredictor:
    def __init__(self, model_path="diabetes_model.pkl"):
        self.model = None
    
    def predict_risk(self, user_data):
        bmi = user_data.get("BMI", 25)
        age = user_data.get("Age", 5)
        high_bp = user_data.get("HighBP", 0)
        high_chol = user_data.get("HighChol", 0)
        smoker = user_data.get("Smoker", 0)
        phys_activity = user_data.get("PhysActivity", 0)
        gen_hlth = user_data.get("GenHlth", 3)
        fruits = user_data.get("Fruits", 0)
        veggies = user_data.get("Veggies", 0)
        
        # Calculate base risk from multiple factors
        base_risk = 0.15  # Average population risk
        
        # BMI contribution (25% weight)
        if bmi > 30:
            base_risk += 0.3
        elif bmi > 25:
            base_risk += 0.15
        elif bmi < 18.5:
            base_risk += 0.05
        
        # Age contribution (15% weight)
        if age > 8:  # Age group > 55
            base_risk += 0.2
        elif age > 5:  # Age group 35-54
            base_risk += 0.1
        
        # Blood pressure contribution
        if high_bp == 1:
            base_risk += 0.15
        
        # Cholesterol contribution
        if high_chol == 1:
            base_risk += 0.12
        
        # Smoking contribution
        if smoker == 1:
            base_risk += 0.08
        
        # Physical activity (protective)
        if phys_activity == 1:
            base_risk -= 0.10
        
        # General health
        if gen_hlth >= 4:  # Fair or Poor health
            base_risk += 0.15
        elif gen_hlth <= 2:  # Excellent or Very good
            base_risk -= 0.05
        
        # Diet (protective)
        if fruits == 1:
            base_risk -= 0.04
        if veggies == 1:
            base_risk -= 0.04
        
        # Ensure risk is between 0 and 0.95
        base_risk = max(0.01, min(0.95, base_risk))
        
        # Determine risk level
        if base_risk < 0.3:
            risk_level = "Low"
        elif base_risk < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "risk_score": float(base_risk),
            "risk_level": risk_level,
            "risk_percentage": f"{base_risk * 100:.1f}%"
        }
    
    def get_recommendations(self, risk_score):
        if risk_score < 0.3:
            return {
                "level": "Low Risk",
                "message": "Excellent! Your diabetes risk is low. Keep up your healthy lifestyle!",
                "actions": [
                    "Continue regular physical activity (150+ mins/week)",
                    "Maintain balanced diet with 5+ servings of fruits/vegetables daily",
                    "Get annual health check-ups",
                    "Monitor weight and blood pressure regularly"
                ]
            }
        elif risk_score < 0.6:
            return {
                "level": "Medium Risk",
                "message": "You have moderate diabetes risk. Small changes can make a big difference!",
                "actions": [
                    "Aim to lose 5-10% of body weight if overweight",
                    "Increase physical activity to 150 minutes per week",
                    "Reduce processed foods and sugary drinks",
                    "Check blood sugar levels annually",
                    "Consider consulting a nutritionist"
                ]
            }
        else:
            return {
                "level": "High Risk",
                "message": "Your diabetes risk is high. Take action now to prevent diabetes!",
                "actions": [
                    "Consult with a healthcare provider immediately",
                    "Lose 7-10% of body weight",
                    "Start daily 30-minute walks",
                    "Eliminate sugary beverages completely",
                    "Get comprehensive blood tests (A1C, glucose)",
                    "Consider medication if recommended by doctor"
                ]
            }

def calculate_bmi(height_feet, height_inches, weight_lbs):
    """Calculate BMI from height and weight"""
    height_m = (height_feet * 12 + height_inches) * 0.0254
    weight_kg = weight_lbs * 0.453592
    
    if height_m > 0:
        bmi = weight_kg / (height_m ** 2)
    else:
        bmi = 22  # Default average
    
    # Categorize BMI
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return round(bmi, 1), category

# For testing
if __name__ == "__main__":
    predictor = DiabetesPredictor()
    test_data = {"BMI": 28, "Age": 6, "HighBP": 1, "HighChol": 0, "Smoker": 0}
    result = predictor.predict_risk(test_data)
    print(f"Test Result: {result}")
