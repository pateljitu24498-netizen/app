import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
SHEET_NAME = "TimberData"  # Change to your Google Sheet name

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open(SHEET_NAME).sheet1  # first sheet

# Define available lengths
lengths = [2.0, 2.3, 2.6, 2.9] + list(range(3, 9))

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 1
if "width" not in st.session_state:
    st.session_state.width = None
if "height" not in st.session_state:
    st.session_state.height = None
if "counts" not in st.session_state:
    st.session_state.counts = {l: 0 for l in lengths}

# -------- Screen 1 --------
if st.session_state.page == 1:
    st.title("Step 1: Enter Dimensions")

    width = st.number_input("Enter Width", min_value=0.0, step=0.1)
    height = st.number_input("Enter Height", min_value=0.0, step=0.1)

    if st.button("Next ➡️"):
        st.session_state.width = width
        st.session_state.height = height
        st.session_state.page = 2
        st.rerun()

# -------- Screen 2 --------
elif st.session_state.page == 2:
    st.title("Step 2: Select Lengths")

    for l in lengths:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(f"+ {l} m"):
                st.session_state.counts[l] += 1
                st.rerun()
        with col2:
            st.write(f"Count: {st.session_state.counts[l]}")

    if st.button("💾 Save to Google Sheet"):
        # Prepare row as list
        row = [st.session_state.width, st.session_state.height] + [st.session_state.counts[l] for l in lengths]

        # Append to Google Sheet
        sheet.append_row(row)

        st.success("✅ Data saved to Google Sheet!")

        # Reset for next entry
        st.session_state.page = 1
        st.session_state.counts = {l: 0 for l in lengths}
        st.rerun()
