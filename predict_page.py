import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_remote = data["le_remote"]
mm = data["scaler"]

def show_predict_page():
    st.title("Salary Prediction")
    
    st.write("Select the country to predict the salary")
    
    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "India",
        "France",
        "Netherlands",
        "Australia",
        "Brazil",
        "Spain",
        "Sweden",
        "Italy",
        "Poland",
        "Switzerland",
        "Denmark",
        "Norway",
        "Israel",
    )
    
    education_levels = (
        "Bachelor’s degree", 
        "Less than a Bachelors", 
        "Master’s degree",
        "Post grad",
    )

    remote_options = (
        "Remote", 
        "In-person", 
        "Hybrid"
    )
    
    country = st.selectbox("Country:", countries)
    education = st.selectbox("Education Level:", education_levels)
    remote = st.selectbox("Remote Work:", remote_options)
    age = st.slider("Age:", 18, 65, 25)

    # Calculate the maximum possible experience based on age
    max_experience = max(0, age - 18)
    experience = st.slider("Years of Experience:", 0, max_experience, 3 if max_experience >= 3 else max_experience)
    
    calculate = st.button("Calculate")
    if calculate:
        if experience > max_experience:
            st.error("Experience cannot be greater than the age minus 18.")
        else:
            X = np.array([[country, age, remote, education, experience]])
            X[:, 0] = le_country.transform([X[0, 0]])
            X[:, 2] = le_remote.transform([X[0, 2]])
            X[:, 3] = le_education.transform([X[0, 3]])
            X = X.astype(float)
            X = mm.transform(X)

            salary = regressor.predict(X)
            st.subheader(f"The estimated salary for the year 2023 is ${salary[0]:,.2f}")

