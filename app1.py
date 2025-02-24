import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set page title
st.set_page_config(page_title="Google Sheets Data Entry", layout="centered")

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Read existing data
sheet_url = "https://docs.google.com/spreadsheets/d/1BPVjObWp4nghthQ9VPXoreZjpAhV4lAFvRQ4CXjzak4/edit?gid=0#gid=0"  # Replace with your sheet URL
df = conn.read(worksheet="Sheet1")

# Ensure the DataFrame has the correct structure
if df is None or df.empty:
    df = pd.DataFrame(columns=["name", "pet"])

# UI for data entry
st.title("Google Sheets Data Entry App")

name = st.text_input("Enter Name:")
pet = st.selectbox("Select Pet:", ["dog", "cat", "bird", "other"])

if st.button("Submit"):
    if name:
        # Append new data
        new_data = pd.DataFrame({"name": [name], "pet": [pet]})
        updated_df = pd.concat([df, new_data], ignore_index=True)
        
        # Write back to Google Sheet
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success("Data added successfully!")
        st.experimental_rerun()
    else:
        st.error("Please enter a name.")

# Display current data
st.subheader("Current Data")
st.dataframe(df)
