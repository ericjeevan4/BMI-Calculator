import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Constants
DATA_FILE = 'bmi_data.csv'

def load_data():
    try:
        data = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Name", "Height", "Weight", "BMI", "Date"])
    return data

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

def show_trend(data, name):
    user_data = data[data['Name'] == name]
    if not user_data.empty:
        user_data['Date'] = pd.to_datetime(user_data['Date'])
        plt.figure(figsize=(10, 5))
        plt.plot(user_data['Date'], user_data['BMI'], marker='o', linestyle='-', color='b')
        plt.title(f'BMI Trend for {name}')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.grid(True)
        st.pyplot(plt.gcf())
    else:
        st.info("No data available for this user.")

def main():
    st.set_page_config(page_title="BMI Calculator", page_icon=":bar_chart:", layout="centered")
    st.title("BMI Calculator")
    
    menu = ["Home", "View History", "Trend Analysis"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    data = load_data()
    
    if choice == "Home":
        st.subheader("Calculate Your BMI")
        
        name = st.text_input("Name")
        height = st.number_input("Height (cm)", min_value=0.0, format="%.2f")
        weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")
        
        if st.button("Calculate BMI"):
            if name and height > 0 and weight > 0:
                bmi = calculate_bmi(weight, height)
                st.success(f"{name}, your BMI is: {bmi:.2f}")
                
                new_data = pd.DataFrame({
                    "Name": [name],
                    "Height": [height],
                    "Weight": [weight],
                    "BMI": [bmi],
                    "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })
                
                data = pd.concat([data, new_data], ignore_index=True)
                save_data(data)
            else:
                st.warning("Please enter valid data.")
    
    elif choice == "View History":
        st.subheader("User BMI History")
        name = st.text_input("Enter Name to View History")
        
        if st.button("View History"):
            user_data = data[data['Name'] == name]
            if not user_data.empty:
                st.dataframe(user_data)
            else:
                st.info("No data available for this user.")
    
    elif choice == "Trend Analysis":
        st.subheader("BMI Trend Analysis")
        name = st.text_input("Enter Name to View Trend")
        
        if st.button("Show Trend"):
            show_trend(data, name)

if __name__ == "__main__":
    main()
