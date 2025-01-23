import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="AgroVita", page_icon="🌿", layout="wide")

# Sidebar Navigation
st.sidebar.title("AgroVita Navigation")
nav_options = ["Home", "About Us", "Explore Us", "Contact"]
selected_page = st.sidebar.radio("Navigate", nav_options)

# Define Home Page
def home_page():
    st.title("Welcome to AgroVita!")
    st.subheader("Empowering Farmers with Technology 🌱")
    st.write("Your go-to platform for improving cattle welfare, farming practices, and productivity through smart technology and data-driven insights.")

# Define About Us Page
def about_us_page():
    st.title("About Us")
    st.write("At AgroVita, we are committed to improving the welfare and productivity of cattle through technology and data-driven insights.")

# Define Explore Page with Links to Your Local Files
def explore_page():
    st.title("Explore AgroVita's Tools")
    st.subheader("Select a tool to get started:")

    explore_option = st.radio("Choose a tool:", ["Cattle Health Prediction", "Common Recommendations", "Farming Practices"])

    if explore_option == "Cattle Health Prediction":
        # Link to the original file for cattle health prediction
        st.markdown("[Go to Cattle Health Prediction](http://localhost:8501/app/cattle_health_prediction.py)", unsafe_allow_html=True)
    elif explore_option == "Common Recommendations":
        # Link to the original file for common recommendations
        st.markdown("[Go to Common Recommendations](http://localhost:8501/app/recommendations.py)", unsafe_allow_html=True)
    elif explore_option == "Farming Practices":
        # Link to the original file for farming practices
        st.markdown("[Go to Farming Practices](http://localhost:8501/app/FarmingPractices.py)", unsafe_allow_html=True)

# Define Contact Page
def contact_page():
    st.title("Contact Us")
    st.write("Your cattle's care is our priority! Reach out to us using the form below.")

# Routing Logic
if selected_page == "Home":
    home_page()
elif selected_page == "About Us":
    about_us_page()
elif selected_page == "Explore Us":
    explore_page()
elif selected_page == "Contact":
    contact_page()
