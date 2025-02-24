import streamlit as st
import pandas as pd
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load Google Sheets API credentials
try:
    creds_json = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_json, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=creds)
    st.success("Connected to Google Sheets API")
except Exception as e:
    st.error(f"Error loading credentials: {e}")
    st.stop()

# Google Sheet details
SPREADSHEET_ID = "your_google_sheet_id_here"  # Replace with your actual Sheet ID
RANGE_NAME = "Sheet1!A1:D100"  # Adjust range as needed

def read_sheet():
    """Fetch data from Google Sheet and return as DataFrame."""
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get("values", [])
        if not values:
            return pd.DataFrame()
        return pd.DataFrame(values[1:], columns=values[0])  # Convert to DataFrame
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

def append_to_sheet(data):
    """Append new data to Google Sheet."""
    try:
        sheet = service.spreadsheets()
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body={"values": data}
        ).execute()
        st.success("Data added successfully!")
    except Exception as e:
        st.error(f"Error writing data: {e}")

# Streamlit UI
st.title("Google Sheets Data Management with Streamlit")

data = read_sheet()
st.write("### Current Data in Google Sheet")
st.dataframe(data)

with st.form("entry_form"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        name = st.text_input("Name")
    with col2:
        email = st.text_input("Email")
    with col3:
        phone = st.text_input("Phone")
    with col4:
        city = st.text_input("City")
    submitted = st.form_submit_button("Add Entry")

if submitted and name and email:
    append_to_sheet([[name, email, phone, city]])
    st.experimental_rerun()  # Refresh the page to show new data
