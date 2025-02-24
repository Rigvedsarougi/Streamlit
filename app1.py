import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Add your service account credentials
creds = {
  "type": "service_account",
  "project_id": "dev-utility-451912-h1",
  "private_key_id": "36f3736723d9bba1274504a8b4072c1162825c43",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDL0iNGUbfwsvQU\nv4sy4MKYNLzZALsV+mU6qHa4NvYdxkHv0ty4q9mTLrlsQ19t1iH6tgCTBvuVaszb\nu994el0s7gXsOKt0teNgLwkJIBoh2y/2BfLi/lwHOaCEDCIgRdOo+KbL8bWTxcJa\nkKaUYo+3ZhWKBaddGwQfjLUwiTLAN8ZdWAPj1UYHnUtGiWOcJi6+36B9S3Q9As8V\neNpq26eD+s+Lbf/EAL4E65AEvFGTMs2ba095A/O8VanQbWoZ7O8k5jgYxvIOfuCT\ncCD4bcmlrmxV1CQruFDJYjcNVdW/ZzWoDR26oT0F5zrX3EuFswvvi92U7bXgILs0\nw/SSWb1VAgMBAAECggEACdHihDFMuOqOSu+dj8J3bajgzl20Jc9uECDss1xmiDG0\nnI7etoEFFwvBwD8QunR+J5ucNHk6Js1B+HY5Qo82rQL8wxBJ5nIa9dfeShPDXo02\nZtaLiLczjN+QZbxF6qMimvn740iOdIOrJPziIbUL8oyXDhLOqPQzwyde1WtOyCbx\nuXEpg76LyB0suV0qoJixI1CjPg9cGn2Alh2BkCc/bcL9We4546WTxvCvWfkQiUxW\nf6u4ipEeG/4GA63RPlyxmQhKEZVl7EanLFD3CwJDjmgP1BKBTLStpUMUlO5yFUCa\n2ySpNB3gxRbTZZVwST4vJGZvX7vdg6yRHBbSycW2owKBgQDyaPB143lEbe2jj1AU\nqTNNOpy0zoK6BzHBu5+IC0ZQ/1Y++v/vzHVSgSqoblTxBryDByJHxjX2brD+Utf+\nxfOWuDkfQsBdEpShMAaJBc5ry2hBjAEmRCNbxeDnIJJtjvC9R0MFxpYrU8/pC7dB\n4gVMD2D4xgHQaUg2DSxVzBsWFwKBgQDXP16EpQV+xRs3djWJ/f1m4y4USUSEtjFy\nPdRSMsNiB8AphaPz1/fJCQv/p47xHqdb+DHTLYrDM+5eP501en2VvaP3ufnP1Oky\nnwiD9uUL/eXUL/6UuxzvV9jjR+6UR27Mt+ey8xqvg6q34WZvyAtH6mrhtrNdnesQ\nT3JqeNtXcwKBgApralKW6YKAeyN5qIaK01Kxf0TiT4oxfvkF2JCfc3FN2GYyocer\n8SsPtEazH2GQ2Y+EQfv10CH8lg0IgJJJ7fN/ja0DUINvpgXbq5w+LKZDgwK2QuJj\nMWXjdoxYwRKGf2CTbJUV+SR5oMkyoLjrPzEKxC9NS4yqydjQ7iPt9wgXAoGAWjLU\n4dLhPaFNaW1gvCWyNZZHrfqR+ub6S3w7aAKbu42x6fR1ou5CiH0BCS3nCYWl7jVQ\nc8Um2+v8HISd1VYyIDiq6FmHpJ785dic0ef5TZAk6kj+bscGNgni+kMfaAWTGbiL\nIIMdEKWlOY77xSXYDFfgWBueiEFvypLwSEvC5p8CgYEAxytmFuUMVBR/R/w//Lvy\nsGN6l5iKrF9Bgy4qQTsfLRClrNN18kvGmv0SVHEnINrd9AopfTHRUYWNVTdQkd7M\n1rYflGmo7CpP1Y02Byhw6qKkn0cqEF2MhXQVPw3oWy2Dtk1FC7D5Czro5r+8m/Df\nnCPKg0ZcA58Hl2pI0ebBkYg=\n-----END PRIVATE KEY-----\n",
  "client_email": "streamlit-app@dev-utility-451912-h1.iam.gserviceaccount.com",
  "client_id": "105183052715331510482",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-app%40dev-utility-451912-h1.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Create credentials using the service account info
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)

# Authorize the client
client = gspread.authorize(credentials)

# Open the Google Sheet (replace 'Your Google Sheet Name' with your actual sheet name)
sheet = client.open("Your Google Sheet Name").sheet1

# Streamlit app
st.title("Google Sheets with Streamlit")

# Fetch data from the sheet
data = sheet.get_all_records()

# Display data in Streamlit
st.write("Data from Google Sheet:")
st.write(data)

# Add a form to add new data to the sheet
with st.form("add_data_form"):
    st.write("Add new data to the sheet")
    new_data = st.text_input("Enter new data")
    submitted = st.form_submit_button("Submit")
    if submitted:
        sheet.append_row([new_data])
        st.success("Data added successfully!")
