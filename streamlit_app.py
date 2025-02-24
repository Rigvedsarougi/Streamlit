import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Function to authenticate and connect to Google Sheets
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# Function to append data to the Google Sheet
def append_to_sheet(data, sheet_url):
    client = connect_to_google_sheets()
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.append_row(data)

# Streamlit app
def main():
    st.title("Data Entry App")

    # Form for data entry
    with st.form("data_entry_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        age = st.number_input("Age", min_value=0, max_value=120)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Prepare data for submission
        data = [name, email, age]
        
        # Append data to Google Sheet
        sheet_url = "https://docs.google.com/spreadsheets/d/1BPVjObWp4nghthQ9VPXoreZjpAhV4lAFvRQ4CXjzak4/edit?gid=0#gid=0"
        append_to_sheet(data, sheet_url)
        
        st.success("Data submitted successfully!")

if __name__ == "__main__":
    main()
