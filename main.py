import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

from models.user import create_user, verify_user

# Page configuration
st.set_page_config(
    page_title="Heart Rate Monitor",
    page_icon="❤️",
    layout="wide"
)

# Initialize session states
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'heart_rate_data' not in st.session_state:
    st.session_state.heart_rate_data = {}

def login_page():
    st.title("❤️ Heart Rate Monitor - Login")

    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns(2)

        with col1:
            login_submitted = st.form_submit_button("Login")
        with col2:
            signup_submitted = st.form_submit_button("Sign Up")

        if login_submitted and username and password:
            if verify_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

        if signup_submitted and username and password:
            if create_user(username, password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists")

def main_app():
    st.title(f"❤️ Heart Rate Monitor - Welcome, {st.session_state.username}!")

    # Initialize user's heart rate data if not exists
    if st.session_state.username not in st.session_state.heart_rate_data:
        st.session_state.heart_rate_data[st.session_state.username] = pd.DataFrame(
            columns=['timestamp', 'heart_rate']
        )

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

    # Sidebar
    st.sidebar.header("Controls")

    # Manual heart rate input
    with st.sidebar.form("heart_rate_input"):
        input_heart_rate = st.number_input(
            "Enter Heart Rate (BPM)",
            min_value=40,
            max_value=200,
            value=75
        )
        submitted = st.form_submit_button("Submit")

        if submitted:
            new_data = pd.DataFrame({
                'timestamp': [datetime.now()],
                'heart_rate': [input_heart_rate]
            })
            st.session_state.heart_rate_data[st.session_state.username] = pd.concat(
                [st.session_state.heart_rate_data[st.session_state.username], new_data],
                ignore_index=True
            )

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Real-time Heart Rate Monitor")

        # Generate mock data if needed
        if st.button("Generate Sample Data"):
            st.session_state.heart_rate_data[st.session_state.username] = generate_heart_rate_data()

        # Plot real-time heart rate
        user_data = st.session_state.heart_rate_data[st.session_state.username]
        if not user_data.empty:
            fig_heart_rate = plot_heart_rate(user_data)
            st.plotly_chart(fig_heart_rate, use_container_width=True)

    with col2:
        st.subheader("Health Metrics")

        user_data = st.session_state.heart_rate_data[st.session_state.username]
        if not user_data.empty:
            metrics = calculate_health_metrics(user_data)

            # Display current heart rate
            current_hr = user_data['heart_rate'].iloc[-1]
            st.metric("Current Heart Rate", f"{current_hr} BPM")

            # Display other metrics
            col_metrics_1, col_metrics_2 = st.columns(2)
            with col_metrics_1:
                st.metric("Average HR", f"{metrics['average_hr']:.1f} BPM")
                st.metric("Min HR", f"{metrics['min_hr']} BPM")
            with col_metrics_2:
                st.metric("Max HR", f"{metrics['max_hr']} BPM")
                st.metric("HR Variability", f"{metrics['hr_variability']:.1f}")

            # Alert system
            alerts = check_alerts(current_hr)
            if alerts:
                st.warning(alerts)

    # Historical data
    st.subheader("Health Metrics History")
    if not user_data.empty:
        fig_metrics = plot_health_metrics(user_data)
        st.plotly_chart(fig_metrics, use_container_width=True)

# Main routing
if not st.session_state.authenticated:
    login_page()
else:
    main_app()

# Auto-refresh every 5 seconds
time.sleep(5)
st.rerun()
