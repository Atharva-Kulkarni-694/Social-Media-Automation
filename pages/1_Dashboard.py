import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- CHECK LOGIN STATUS ---
if not st.session_state.get("logged_in", False):
    st.error("Please log in first from the main page.")
    st.stop()

# --- MOCK DATA GENERATION ---
@st.cache_data
def get_mock_data():
    """Generates a dictionary of mock dataframes and metrics."""
    data = {}
    
    # Summary Metrics
    data['total_followers'] = 24568
    data['followers_change'] = 12.1
    data['engagement_rate'] = 4.8
    data['engagement_change'] = 0.6
    data['optimal_time'] = "2:30 PM"
    data['scheduled_posts'] = 14
    
    # Engagement Chart Data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
    engagement_df = pd.DataFrame({
        'Month': months,
        'Instagram': np.random.uniform(3.2, 5.2, size=7).round(1),
        'Twitter': np.random.uniform(2.8, 3.8, size=7).round(1),
        'Facebook': np.random.uniform(3.5, 4.1, size=7).round(1),
        'LinkedIn': np.random.uniform(4.2, 6.5, size=7).round(1)
    })
    data['engagement_df'] = engagement_df

    # Platform Distribution Data
    platform_df = pd.DataFrame({
        'Platform': ['Instagram', 'Twitter', 'Facebook', 'LinkedIn'],
        'Followers': [10500, 5200, 6100, 2768]
    })
    data['platform_df'] = platform_df

    # Recent Activity Data
    activity_df = pd.DataFrame({
        'Platform': ['Instagram', 'Twitter', 'Facebook', 'LinkedIn'],
        'Content': ['New product launch', 'Industry news share', 'Customer testimonial', 'Company update'],
        'Engagement (%)': [5.2, 3.8, 4.1, 6.5],
        'Time': ['2 hours ago', '5 hours ago', '1 day ago', '2 days ago']
    })
    data['activity_df'] = activity_df

    # Optimal Times Data
    optimal_times = {
        'Instagram': {'time': '11 AM - 1 PM, 7 PM - 9 PM', 'score': 85},
        'Twitter': {'time': '9 AM - 11 AM, 1 PM - 3 PM', 'score': 72},
        'Facebook': {'time': '1 PM - 4 PM, 6 PM - 9 PM', 'score': 68},
        'LinkedIn': {'time': '8 AM - 10 AM, 5 PM - 7 PM', 'score': 78},
    }
    data['optimal_times'] = optimal_times

    return data

data = get_mock_data()


# --- DASHBOARD UI ---
st.title("📊 Dashboard Overview")
st.markdown("Welcome back! Here's a summary of your social media performance.")
st.write("---")


# --- METRIC CARDS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Total Followers",
        value=f"{data['total_followers']:,}",
        delta=f"{data['followers_change']}%"
    )
with col2:
    st.metric(
        label="Engagement Rate",
        value=f"{data['engagement_rate']}%",
        delta=f"{data['engagement_change']}%"
    )
with col3:
    st.metric(label="Optimal Post Time (Today)", value=data['optimal_time'])
with col4:
    st.metric(label="Scheduled Posts", value=data['scheduled_posts'])

st.write("---")

# --- CHARTS SECTION ---
chart_col1, chart_col2 = st.columns((2, 1))

with chart_col1:
    st.subheader("📈 Engagement Overview")
    engagement_df = data['engagement_df']
    fig_engagement = go.Figure()
    for col in engagement_df.columns[1:]:
        fig_engagement.add_trace(go.Scatter(
            x=engagement_df['Month'], 
            y=engagement_df[col],
            mode='lines+markers',
            name=col
        ))
    fig_engagement.update_layout(
        xaxis_title="Month",
        yaxis_title="Engagement Rate (%)",
        legend_title="Platform"
    )
    st.plotly_chart(fig_engagement, use_container_width=True)

with chart_col2:
    st.subheader("🌐 Platform Distribution")
    platform_df = data['platform_df']
    fig_platform = px.pie(
        platform_df,
        values='Followers',
        names='Platform',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_platform, use_container_width=True)

st.write("---")

# --- RECENT ACTIVITY & OPTIMAL TIMES ---
activity_col, optimal_col = st.columns((2, 1))

with activity_col:
    st.subheader("🔔 Recent Activity")
    st.dataframe(data['activity_df'], use_container_width=True)

with optimal_col:
    st.subheader("⏰ Optimal Posting Times")
    for platform, info in data['optimal_times'].items():
        st.markdown(f"**{platform}**")
        st.caption(f"Best times: {info['time']}")
        st.progress(info['score'])

# --- REFRESH BUTTON ---
if st.button("Refresh Data"):
    st.cache_data.clear()
    st.success("Data refreshed!")
    time.sleep(1)
    st.experimental_rerun()