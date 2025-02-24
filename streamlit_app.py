# streamlit_app.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Load credentials from secrets.toml
def load_credentials():
    creds = {
        "type": st.secrets["connections.gsheets"]["type"],
        "project_id": st.secrets["connections.gsheets"]["project_id"],
        "private_key_id": st.secrets["connections.gsheets"]["private_key_id"],
        "private_key": st.secrets["connections.gsheets"]["private_key"],
        "client_email": st.secrets["connections.gsheets"]["client_email"],
        "client_id": st.secrets["connections.gsheets"]["client_id"],
        "auth_uri": st.secrets["connections.gsheets"]["auth_uri"],
        "token_uri": st.secrets["connections.gsheets"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["connections.gsheets"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["connections.gsheets"]["client_x509_cert_url"],
    }
    return Credentials.from_service_account_info(creds, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# Connect to Google Sheets
def connect_to_gsheets():
    creds = load_credentials()
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(st.secrets["connections.gsheets"]["spreadsheet"])
    return spreadsheet.sheet1  # Use the first sheet by default

# Fetch existing data
def fetch_existing_data():
    sheet = connect_to_gsheets()
    return sheet.get_all_records()

# Add new data
def add_new_data(name, pet):
    sheet = connect_to_gsheets()
    sheet.append_row([name, pet])
    st.success("Data added successfully!")

# Title of the app
st.title("Google Sheets Data Entry App")

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
