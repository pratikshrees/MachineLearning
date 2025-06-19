import streamlit as st
import pandas as pd
import pickle

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🏠 House Price Prediction")

# Reusable Yes/No selector converted to binary
def yes_no_to_binary(label):
    return 1 if st.selectbox(label, ['Yes', 'No']) == 'Yes' else 0

# User Inputs
area = st.number_input("Area (sq ft)", value=5000)
bedrooms = st.number_input("Number of Bedrooms", value=3)
bathrooms = st.number_input("Number of Bathrooms", value=2)
stories = st.number_input("Number of Stories", value=1)
mainroad = yes_no_to_binary("Is there access to Main Road?")
guestroom = yes_no_to_binary("Is there a Guest Room?")
basement = yes_no_to_binary("Does it have a Basement?")
hotwaterheating = yes_no_to_binary("Hot Water Heating?")
airconditioning = yes_no_to_binary("Air Conditioning?")
parking = st.number_input("Number of Parking Spaces", value=1)
prefarea = yes_no_to_binary("Is it in a Preferred Area?")

# Furnishing status using Ordinal Encoding
furnishing = st.selectbox("Furnishing Status", ["unfurnished", "semi-furnished", "furnished"])
furnishing_map = {
    "unfurnished": 0,
    "semi-furnished": 1,
    "furnished": 2
}
furnishingstatus = furnishing_map[furnishing]

# Final input DataFrame for prediction
input_data = pd.DataFrame([{
    "area": area,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "stories": stories,
    "mainroad": mainroad,
    "guestroom": guestroom,
    "basement": basement,
    "hotwaterheating": hotwaterheating,
    "airconditioning": airconditioning,
    "parking": parking,
    "prefarea": prefarea,
    "furnishingstatus": furnishingstatus
}])

# Prediction
if st.button("Predict Price"):
    price = model.predict(input_data)[0]
    st.success(f"🏷️ Predicted House Price: RS {int(price):,}")
