# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Set up the title of the app
st.title("Google Sheets Data Entry App")

# Create a connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Function to read data from Google Sheets
def read_data():
    df = conn.read(worksheet="Sheet1", ttl="10m")
    return df

# Function to write data to Google Sheets
def write_data(data):
    conn.update(worksheet="Sheet1", data=data)

# Main form for data entry
with st.form("data_entry_form"):
    st.write("Enter your details below:")
    
    name = st.text_input("Name")
    pet = st.text_input("Pet")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if name and pet:
            # Read existing data
            df = read_data()
            
            # Append new data
            new_data = {"name": [name], "pet": [pet]}
            new_df = df.append(new_data, ignore_index=True)
            
            # Write updated data back to Google Sheets
            write_data(new_df)
            
            st.success("Data submitted successfully!")
        else:
            st.error("Please fill in all fields.")

# Display the current data in the Google Sheet
st.write("Current Data in Google Sheet:")
df = read_data()
st.dataframe(df)
