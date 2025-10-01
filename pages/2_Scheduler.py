import streamlit as st
import pandas as pd
from datetime import datetime

# --- CHECK LOGIN STATUS ---
if not st.session_state.get("logged_in", False):
    st.error("Please log in first from the main page.")
    st.stop()

st.title("📅 Post Scheduler")

# --- MOCK DATA: UPCOMING POSTS ---
if 'scheduled_posts_df' not in st.session_state:
    st.session_state.scheduled_posts_df = pd.DataFrame({
        'Platform': ['Twitter', 'Instagram'],
        'Content': ['Hello World!', 'Check out our new feature!'],
        'Scheduled Time': [datetime(2025, 9, 25, 10, 0), datetime(2025, 9, 26, 14, 30)]
    })

# --- SCHEDULER FORM ---
with st.form("scheduler_form", clear_on_submit=True):
    st.subheader("Create a New Post")
    
    platforms = st.multiselect(
        "Select Platforms",
        ['Instagram', 'Twitter', 'Facebook', 'LinkedIn']
    )
    
    post_content = st.text_area("Post Content", height=150)
    
    uploaded_file = st.file_uploader("Upload Image/Video (Optional)", type=['png', 'jpg', 'jpeg', 'mp4'])
    
    schedule_date = st.date_input("Schedule Date")
    schedule_time = st.time_input("Schedule Time")
    
    submit_button = st.form_submit_button(label="Schedule Post")

    if submit_button:
        if not platforms or not post_content:
            st.warning("Please select at least one platform and write some content.")
        else:
            schedule_datetime = datetime.combine(schedule_date, schedule_time)
            for platform in platforms:
                 new_post = pd.DataFrame([{
                     'Platform': platform,
                     'Content': post_content,
                     'Scheduled Time': schedule_datetime
                 }])
                 st.session_state.scheduled_posts_df = pd.concat(
                     [st.session_state.scheduled_posts_df, new_post],
                     ignore_index=True
                 )
            st.success(f"Post scheduled for {', '.join(platforms)} on {schedule_datetime.strftime('%Y-%m-%d %H:%M')}!")

st.write("---")

# --- DISPLAY SCHEDULED POSTS ---
st.subheader("🗓️ Upcoming Scheduled Posts")
if not st.session_state.scheduled_posts_df.empty:
    st.dataframe(
        st.session_state.scheduled_posts_df.sort_values(by="Scheduled Time").reset_index(drop=True),
        use_container_width=True
    )
else:
    st.info("No posts scheduled yet.")