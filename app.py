import streamlit as st
from streamlit_option_menu import option_menu
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SocialSync",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MOCK AUTHENTICATION ---
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Enter Password to Launch App (use 'socialsync')", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Enter Password to Launch App (use 'socialsync')", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

# You should use st.secrets for a real app. For this example, we'll hardcode it.
if 'secrets' not in st.session_state:
    st.session_state['secrets'] = {'password': 'socialsync'}

# --- LANDING PAGE CONTENT ---
def show_landing_page():
    # --- HERO SECTION ---
    with st.container():
        st.markdown(
            """
            <style>
                .hero-gradient {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 5rem 2rem;
                    border-radius: 1rem;
                    color: white;
                }
                .stButton > button {
                    width: 100%;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        with st.container():
            col1, col2 = st.columns((2, 1))
            with col1:
                st.markdown(
                    "<div class='hero-gradient'>"
                    "<h1>Automate Your <span style='color: #c3dafe;'>Social Media Growth</span></h1>"
                    "<p>Connect, schedule, analyze and optimize your social media presence across multiple platforms with one powerful tool.</p>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col2:
                st.image("http://static.photos/technology/1024x576/42", use_column_width=True)

    st.write("---")

    # --- FEATURES SECTION ---
    with st.container():
        st.markdown("<h2 style='text-align: center;'>Everything you need to grow on social media</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: grey;'>Our automation platform helps you save time while maximizing your social media impact.</p>", unsafe_allow_html=True)
        st.write("")

        features = {
            "🔗 Multi-Platform Integration": "Connect Instagram, Twitter, Facebook, LinkedIn, and more. Manage all your accounts from one dashboard.",
            "📅 Smart Scheduling": "Schedule posts in advance with our optimal timing recommendations for each platform.",
            "📊 Advanced Analytics": "Track engagement, growth, and performance across all your connected accounts.",
            "🚀 Campaign Management": "Create and run targeted campaigns across multiple platforms with automated workflows.",
            "⏰ Optimal Timing": "Get data-driven recommendations for the best times to post on each platform.",
            "💡 AI Content Suggestions": "Get intelligent content ideas tailored to your audience and performance history.",
        }

        cols = st.columns(3)
        for i, (title, description) in enumerate(features.items()):
            with cols[i % 3]:
                st.info(title)
                st.write(description)

    st.write("---")

    # --- CTA SECTION ---
    with st.container():
        st.success("Ready to automate your social media? Enter the password above to launch the app!")
        st.info("For this demo, use the password: `socialsync`")

# --- MAIN APP LOGIC ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("Login to Launch")
    username = st.sidebar.text_input("Username", value="demouser")
    password = st.sidebar.text_input("Password", type="password", value="socialsync")
    login_button = st.sidebar.button("Login")
    
    if login_button:
        if password == "socialsync": # Simple check
            st.session_state.logged_in = True
            #st.experimental_rerun()
        else:
            st.sidebar.error("Incorrect password.")
    
    show_landing_page()

else:
    # --- SIDEBAR NAVIGATION (for logged-in user) ---
    with st.sidebar:
        st.title("⚡ SocialSync")
        st.write("Welcome, John Doe!")
        st.write("---")
    
    st.success("Login Successful! Please select a page from the sidebar to continue.")
    st.balloons()
    time.sleep(2)
    # This is a bit of a hack to auto-navigate, Streamlit doesn't have a native redirect
    st.switch_page("pages/1_Dashboard.py")