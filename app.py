import streamlit as st
import plotly.graph_objects as go
from diabetes_model import DiabetesPredictor, calculate_bmi

# Page configuration
st.set_page_config(
    page_title="Diabetes.predict",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-size: 2.5rem;
    }
    .card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">Diabetes.predict</h1>', unsafe_allow_html=True)
st.write("AI-powered diabetes risk assessment")

# Initialize predictor
predictor = DiabetesPredictor()

# Sidebar for input
with st.sidebar:
    st.header("Your Health Profile")
    
    # Basic info
    age = st.slider("Age", 18, 100, 35)
    
    col1, col2 = st.columns(2)
    with col1:
        height_feet = st.selectbox("Height (feet)", [4, 5, 6, 7], index=1)
    with col2:
        height_inches = st.selectbox("Height (inches)", list(range(12)), index=8)
    
    weight_lbs = st.slider("Weight (lbs)", 80, 350, 160)
    
    # Calculate BMI
    bmi, bmi_category = calculate_bmi(height_feet, height_inches, weight_lbs)
    st.metric("Your BMI", f"{bmi} ({bmi_category})")
    
    # Health conditions
    st.subheader("Health Conditions")
    high_bp = st.checkbox("High Blood Pressure")
    high_chol = st.checkbox("High Cholesterol")
    smoker = st.checkbox("Smoker")
    
    # Lifestyle
    st.subheader("Lifestyle")
    exercise = st.select_slider(
        "Weekly Exercise",
        options=["None", "1-2 hours", "3-4 hours", "5+ hours"],
        value="1-2 hours"
    )
    
    diet_quality = st.slider("Diet Quality (1=Poor, 10=Excellent)", 1, 10, 6)
    
    general_health = st.select_slider(
        "General Health",
        options=["Excellent", "Very Good", "Good", "Fair", "Poor"],
        value="Good"
    )
    
    # Family History
    family_diabetes = st.checkbox("Family History of Diabetes")
    
    # Calculate button
    calculate_btn = st.button("Calculate My Risk", type="primary")

# Main content
if calculate_btn:
    # Prepare data
    user_data = {
        "BMI": bmi,
        "Age": min(13, (age - 18) // 5),  # Convert to age group
        "HighBP": 1 if high_bp else 0,
        "HighChol": 1 if high_chol else 0,
        "Smoker": 1 if smoker else 0,
        "PhysActivity": 1 if exercise != "None" else 0,
        "GenHlth": {"Excellent":1, "Very Good":2, "Good":3, "Fair":4, "Poor":5}[general_health],
        "Fruits": 1 if diet_quality >= 5 else 0,
        "Veggies": 1 if diet_quality >= 5 else 0
    }
    
    # Get prediction
    result = predictor.predict_risk(user_data)
    recommendations = predictor.get_recommendations(result["risk_score"])
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Risk Level", result["risk_level"])
    
    with col2:
        st.metric("Risk Score", result["risk_percentage"])
    
    with col3:
        st.metric("Recommendation", recommendations["level"])
    
    # Risk gauge
    st.subheader("Risk Assessment")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["risk_score"] * 100,
        title={"text": "Diabetes Risk Meter"},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 25], "color": "green"},
                {"range": [25, 50], "color": "yellow"},
                {"range": [50, 100], "color": "red"}
            ]
        }
    ))
    st.plotly_chart(fig)
    
    # Recommendations
    st.subheader("Your Action Plan")
    st.write(recommendations["message"])
    
    for i, action in enumerate(recommendations["actions"], 1):
        st.write(f"{i}. {action}")
    
    # Educational info
    with st.expander("Learn More About Diabetes Prevention"):
        st.write("""
        **Key Facts:**
        - 37 million Americans have diabetes
        - 96 million have prediabetes
        - BMI is the #1 predictor of diabetes risk
        - Exercise can reduce risk by up to 58%
        
        **Prevention Tips:**
        1. Maintain healthy weight
        2. Exercise regularly
        3. Eat more vegetables
        4. Get regular check-ups
        """)
else:
    st.info("Fill out your health profile and click 'Calculate My Risk'")

# Footer
st.markdown("---")
st.caption("This tool is for educational purposes. Always consult healthcare professionals for medical advice.")
