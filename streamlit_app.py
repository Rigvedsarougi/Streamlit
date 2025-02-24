# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Title of the app
st.title("Google Sheets Data Entry App")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Function to fetch existing data
def fetch_existing_data():
    df = conn.read()
    return df

# Function to add new data
def add_new_data(name, pet):
    df = fetch_existing_data()
    new_data = {"name": name, "pet": pet}
    df = df.append(new_data, ignore_index=True)
    conn.update(df)
    st.success("Data added successfully!")

# Fetch existing data
existing_data = fetch_existing_data()

# Display existing data
st.write("Existing Data:")
st.dataframe(existing_data)

# Form for new data entry
with st.form("data_entry_form"):
    name = st.text_input("Name")
    pet = st.text_input("Pet")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and pet:
            add_new_data(name, pet)
        else:
            st.error("Please fill in all fields.")
