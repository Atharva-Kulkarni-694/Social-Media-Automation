import streamlit as st
import pandas as pd

# --- CHECK LOGIN STATUS ---
if not st.session_state.get("logged_in", False):
    st.error("Please log in first from the main page.")
    st.stop()

st.title("🚀 Campaign Management")

# --- MOCK DATA: CAMPAIGNS ---
@st.cache_data
def get_campaign_data():
    campaigns = pd.DataFrame({
        'Campaign Name': ['Q3 Product Launch', 'Summer Sale 2025', 'Brand Awareness Push'],
        'Status': ['Active', 'Completed', 'Planning'],
        'Platforms': ['Instagram, Facebook', 'Twitter, Instagram', 'LinkedIn'],
        'Start Date': ['2025-07-01', '2025-06-15', '2025-10-01'],
        'End Date': ['2025-09-30', '2025-07-15', '2025-10-31'],
        'Budget ($)': [5000, 2500, 7500]
    })
    return campaigns

campaign_df = get_campaign_data()

# --- DISPLAY CAMPAIGNS ---
st.subheader("Your Campaigns")
st.dataframe(campaign_df, use_container_width=True)

st.write("---")

# --- CREATE NEW CAMPAIGN (Placeholder) ---
with st.expander("➕ Create a New Campaign"):
    st.text_input("Campaign Name")
    st.selectbox("Status", ['Planning', 'Active', 'Paused'])
    st.multiselect("Platforms", ['Instagram', 'Twitter', 'Facebook', 'LinkedIn'])
    st.date_input("Start Date")
    st.date_input("End Date")
    st.number_input("Budget ($)", min_value=0)
    st.button("Save Campaign")
    st.info("Note: This is a UI placeholder. Logic for saving is not implemented.")