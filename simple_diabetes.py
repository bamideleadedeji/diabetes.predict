from diabetes_model import DiabetesPredictor, calculate_bmi

def main():
    print("="*50)
    print("Diabetes.predict - Command Line Version")
    print("="*50)
    
    print("\nEnter your health information:")
    
    try:
        # Get user input
        age = int(input("Age: ") or "35")
        
        print("\nHeight:")
        height_feet = int(input("  Feet: ") or "5")
        height_inches = int(input("  Inches: ") or "8")
        
        weight_lbs = int(input("\nWeight (lbs): ") or "160")
        
        print("\nHealth Conditions (y/n):")
        high_bp = input("  High Blood Pressure? ").lower() == 'y'
        high_chol = input("  High Cholesterol? ").lower() == 'y'
        smoker = input("  Smoker? ").lower() == 'y'
        
        print("\nLifestyle:")
        exercise = input("  Weekly Exercise (none/low/medium/high): ").lower() or "medium"
        diet = int(input("  Diet Quality (1-10): ") or "6")
        
        # Calculate BMI
        bmi, category = calculate_bmi(height_feet, height_inches, weight_lbs)
        print(f"\nYour BMI: {bmi} ({category})")
        
        # Prepare data for prediction
        user_data = {
            "BMI": bmi,
            "Age": min(13, (age - 18) // 5),
            "HighBP": 1 if high_bp else 0,
            "HighChol": 1 if high_chol else 0,
            "Smoker": 1 if smoker else 0,
            "PhysActivity": 1 if exercise != "none" else 0,
            "Fruits": 1 if diet >= 5 else 0,
            "Veggies": 1 if diet >= 5 else 0
        }
        
        # Make prediction
        predictor = DiabetesPredictor()
        result = predictor.predict_risk(user_data)
        recommendations = predictor.get_recommendations(result["risk_score"])
        
        # Display results
        print("\n" + "="*50)
        print("YOUR RESULTS:")
        print("="*50)
        print(f"Diabetes Risk: {result['risk_percentage']}")
        print(f"Risk Level: {result['risk_level']}")
        
        print("\nRECOMMENDATIONS:")
        print(f"{recommendations['message']}")
        print("\nAction Steps:")
        for i, action in enumerate(recommendations["actions"], 1):
            print(f"  {i}. {action}")
        
        print("\n" + "="*50)
        print("Tips for Prevention:")
        print("Maintain healthy weight")
        print("Exercise 150+ minutes/week")
        print("Eat more fruits/vegetables")
        print("Get regular health check-ups")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
