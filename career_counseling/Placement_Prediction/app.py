# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Load the trained model
model = pickle.load(open('placement_model.pkl', 'rb'))

# Encode categorical data
le_gender = LabelEncoder()
le_stream = LabelEncoder()
genders = ['Male', 'Female']
streams = ['Electronics And Communication', 'Computer Science', 'Information Technology', 'Mechanical', 'Civil']

le_gender.fit(genders)
le_stream.fit(streams)

# Streamlit UI Setup
st.set_page_config(page_title="Placement Predictor", page_icon="🎯", layout="centered")

# Title
st.title("🎯 Placement Predictor")
st.markdown("### Predict your placement chances based on academic details!")

# Input Form
st.sidebar.header("📥 Input Features")

age = st.sidebar.number_input("Age", min_value=18, max_value=30, value=21)
gender = st.sidebar.selectbox("Gender", genders)
stream = st.sidebar.selectbox("Stream", streams)
internships = st.sidebar.slider("Internships", 0, 5, 1)
cgpa = st.sidebar.slider("CGPA", 0.0, 10.0, 7.0)
hostel = st.sidebar.radio("Staying in Hostel?", [0, 1])
backlogs = st.sidebar.radio("History of Backlogs?", [0, 1])

# Prediction
if st.sidebar.button("🚀 Predict"):
    # ✅ Fixed Warning Issue — Match Input to Training Format
    input_data = pd.DataFrame(
        [[age, le_gender.transform([gender])[0], le_stream.transform([stream])[0],
          internships, cgpa, hostel, backlogs]],
        columns=['Age', 'Gender', 'Stream', 'Internships', 'CGPA', 'Hostel', 'HistoryOfBacklogs']
    )
    
    prediction = model.predict(input_data)[0]
    
    if prediction == 1:
        st.success("🎉 **Congratulations! You are likely to be placed!** 😎")
    else:
        st.error("😟 **Oops! You might not get placed. Keep working hard!**")

# Display Stats & Performance
st.markdown("---")
st.markdown("### 📊 Model Performance")

# Load test data stats for display
accuracy = 90.99
confusion_matrix = np.array([[495, 25], [82, 585]])

col1, col2 = st.columns(2)

# Accuracy
with col1:
    st.metric(label="🔥 **Accuracy**", value=f"{accuracy:.2f}%")

# Confusion Matrix
with col2:
    st.markdown("**Confusion Matrix**")
    fig, ax = plt.subplots()
    sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['Not Placed', 'Placed'], yticklabels=['Not Placed', 'Placed'])
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("💡 **Powered by AI | Developed by Animesh Gupta**")

