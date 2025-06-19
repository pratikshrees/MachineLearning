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
age = st.slider("Age", 1, 120, 30)
hypertension = yes_no_to_binary("Hypertension?")
heart_disease = yes_no_to_binary("Heart Disease?")
smoking = st.selectbox("Smoking History", ['never', 'former', 'current', 'not current', 'ever', 'No Info'])
bmi = st.slider("BMI", 10.0, 60.0, 25.0)
hba1c = st.slider("HbA1c Level", 3.0, 15.0, 5.5)
glucose = st.slider("Blood Glucose Level", 50.0, 400.0, 100.0)

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
