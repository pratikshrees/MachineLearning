import streamlit as st
import pandas as pd
import pickle

# Load model
with open("diabetes_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Diabetes Predictor", page_icon="🩺")
st.title("🩺 Diabetes Prediction App")
st.markdown("Enter your health data to check your diabetes risk.")

def yes_no_to_binary(label):
    return 1 if st.selectbox(label, ["No", "Yes"]) == "Yes" else 0

# Collect inputs
gender = st.selectbox("Gender", ["Female", "Male", "Other"])
age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
hypertension = yes_no_to_binary("Hypertension?")
heart_disease = yes_no_to_binary("Heart Disease?")
smoking = st.selectbox("Smoking History", ['never', 'former', 'current', 'not current', 'ever', 'No Info'])
bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
hba1c = st.number_input("HbA1c Level", min_value=3.0, max_value=15.0, value=5.5, step=0.1)
glucose = st.number_input("Blood Glucose Level", min_value=50.0, max_value=400.0, value=100.0, step=1.0)


# Encode inputs
gender_map = {"Female": 0, "Male": 1, "Other": 2}
smoke_map = {'never': 0, 'No Info': 1, 'current': 2, 'ever': 3, 'former': 4, 'not current': 5}

input_df = pd.DataFrame([{
    "gender": gender_map[gender],
    "age": age,
    "hypertension": hypertension,
    "heart_disease": heart_disease,
    "smoking_history": smoke_map[smoking],
    "bmi": bmi,
    "HbA1c_level": hba1c,
    "blood_glucose_level": glucose
}])

# Show inputs
st.write("🔍 Input Data", input_df)

if st.button("Predict Diabetes"):
    try:
        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        if pred == 1:
            st.error(f"🔴 You may be at risk of Diabetes. (Probability: {prob:.2f})")
        else:
            st.success(f"🟢 You are not likely diabetic. (Probability: {prob:.2f})")
    except Exception as e:
        st.error(f"❌ Prediction Failed: {e}")
