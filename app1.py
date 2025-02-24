   import streamlit as st
   import gspread
   from google.oauth2.service_account import Credentials
   import pandas as pd

   # Load Google Sheets credentials securely
   def get_gsheet_client():
       scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
       creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
       return gspread.authorize(creds)

   # Google Sheet details
   SHEET_NAME = "Streamlit"
   SHEET_URL = "https://docs.google.com/spreadsheets/d/1BPVjObWp4nghthQ9VPXoreZjpAhV4lAFvRQ4CXjzak4/edit?gid=0#gid=0"

   # Initialize Google Sheets client
   gc = get_gsheet_client()
   sheet = gc.open(SHEET_NAME).sheet1  # Access first sheet

   # Streamlit UI
   st.title("Google Sheets API with Streamlit")
   st.write("Store data in Google Sheets using a Streamlit API")

   name = st.text_input("Enter your name")
   email = st.text_input("Enter your email")
   message = st.text_area("Enter your message")

   if st.button("Submit"):
       if name and email and message:
           sheet.append_row([name, email, message])
           st.success("Data stored successfully!")
       else:
           st.error("Please fill in all fields")

   # Show current data
   st.subheader("Stored Data")
   data = sheet.get_all_values()
   df = pd.DataFrame(data[1:], columns=data[0])  # Convert to DataFrame
   st.dataframe(df)
