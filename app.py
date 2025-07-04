import streamlit as st
import requests
import json
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
from io import BytesIO

st.title("User Metadata Fetcher")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file with a 'UID' column", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if 'UID' not in df.columns:
        st.error("CSV must contain a 'UID' column.")
    else:
        user_ids = df['UID'].unique().tolist()

        # Base URL
        base_url = "https://sso-dev.tpml.in/auth/get-user-metadata?userId="

        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "User Metadata"
        headers = ["User ID", "Display Name", "First Name", "Last Name", "Email", "Gender", "DOB", "College"]
        ws.append(headers)

        with st.spinner("Fetching metadata for users..."):
            for user_id in user_ids:
                url = base_url + user_id
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    metadata = data.get("metadata", {})
                    display_name = metadata.get("displayName", "N/A")
                    first_name = metadata.get("first_name", "N/A")
                    last_name = metadata.get("last_name", "N/A")
                    email = metadata.get("dh", {}).get("newsLetter", {}).get("email", "N/A")
                    gender = metadata.get("gender", "N/A")
                    dob = f'{metadata.get("dob", {}).get("day", "N/A")}-{metadata.get("dob", {}).get("month", "N/A")}-{metadata.get("dob", {}).get("year", "N/A")}'
                    college = metadata.get("college", "N/A")
                    row = [user_id, display_name, first_name, last_name, email, gender, dob, college]
                else:
                    row = [user_id, "Failed to retrieve data", "", "", "", "", "", ""]

                ws.append(row)

        # Save Excel to memory
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        filename = f"user_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        st.success("Metadata fetched and Excel file is ready!")

        st.download_button(
            label="📥 Download Excel File",
            data=output,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
