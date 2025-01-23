import streamlit as st
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import uuid

# Setting up the page configuration
st.set_page_config(page_title="AgroVita", page_icon="🌿", layout="wide")

# Sidebar (Navbar)
st.sidebar.title("AgroVita Navigation")
nav_options = ["Home", "About Us", "Explore Us", "Contact"]
selected_page = st.sidebar.radio("Navigate", nav_options)


# Define Home Page
def home_page():
    st.title("Welcome to AgroVita!")
    st.subheader("Empowering Farmers with Technology 🌱")
    st.write(
        "Your go-to platform for improving cattle welfare, farming practices, and productivity through smart technology and data-driven insights."
    )
    st.image(r"C:\Users\admin\ShreyaProjects\IBM\Images\home.jpg",
             caption="Empowering Farmers Globally")  # Use raw string


# Define About Us Page
def about_us_page():
    # Add custom CSS for enhanced styling
    st.markdown(
        """
        <style>
        .about-us-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background-color: #574964;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .service-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 15px;
            background-color: #574964;
            height: auto;
            width: 100%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # About Us Section
    st.title("About Us")
    st.markdown(
        """
        <div class="about-us-container">
            <p>
                At AgroVita, we are committed to improving the welfare and productivity of cattle 
                through technology and data-driven insights. Our platform helps farmers optimize 
                cattle care, feeding patterns, and environmental factors, ensuring healthy livestock 
                and better farming practices.
            </p>
            <p>
                Our mission is to empower farmers with the tools and knowledge they need to succeed, 
                creating a sustainable future for agriculture.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Services Section
    st.subheader("Our Services")

    # Define card data
    services = [
        {
            "img_path": "Images/farmp.webp",
            "title": "Farming Practices",
            "description": "We offer guidance on best farming practices to improve yield, sustainability, and livestock well-being.",
        },
        {
            "img_path": "Images/home.png",
            "title": "Cattle Health Prediction",
            "description": "Analyze cattle data to predict health conditions, enabling early interventions to ensure optimal cattle health.",
        },
        {
            "img_path": "Images/cattlehealth.webp",
            "title": "Common Diseases & Prediction",
            "description": "Early detection and prediction of common cattle diseases, helping farmers take preventive measures and reduce losses.",
        },
        {
            "img_path": "Images/sustainable.webp",
            "title": "Sustainable Farming Practices",
            "description": "Promoting sustainable farming practices that protect the environment while improving farm productivity and cattle welfare.",
        },
    ]

    # Create a grid layout for services
    cols = st.columns(2)  # Create two columns for the grid
    for i, service in enumerate(services):
        col = cols[i % 2]
        with col:
            # Display card layout with image, title, and description
            with st.container():
                st.markdown(
                    f"""
                       <div class="service-card">
                           <h3>{service['title']}</h3>
                       </div>
                       """,
                    unsafe_allow_html=True,
                )
                st.image(service["img_path"], use_container_width=True, caption=service["title"])
                st.markdown(f"<p>{service['description']}</p>", unsafe_allow_html=True)


# Define Contact Page
def contact_page():
    st.title("Contact Us")
    st.write("Your cattle's care is our priority! Reach out to us using the form below.")
    with st.form("contact_form"):
        name = st.text_input("Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        message = st.text_area("Message", placeholder="Share your thoughts or concerns")
        submitted = st.form_submit_button("Send Message")
        if submitted:
            st.success(f"Thank you, {name}! Your message has been sent successfully.")

    st.subheader("Other Contact Details")
    st.write("📍 AgroTech Park, 789 Farm Lane, AgriCity, Country")
    st.write("📞 +1 (800) 555-1234")
    st.write("📧 cattlecare_support@gmail.com")


# Define Cattle Health Prediction Page
def cattle_health_prediction():
    st.title("Cattle Health Prediction")
    st.write("Here you can predict cattle health based on data and provide early interventions.")
    # Add your code for cattle health prediction here (e.g., input fields, prediction model, etc.)


# Define Common Recommendations Page
def common_recommendations():
    st.title("Common Recommendations")
    st.write("Here we offer common recommendations to help farmers optimize cattle care and farm practices.")
    # Add your code for common recommendations here (e.g., tips, guidelines, etc.)


# Define Farming Practices Page
def farming_practices():
    st.title("Farming Practices")
    st.write("Discover sustainable and efficient farming practices to improve yield and cattle welfare.")
    # Add your code for farming practices here (e.g., articles, tips, videos, etc.)


# Watson Assistant Chatbot Integration
import uuid


# Watson Assistant Chatbot Integration
def chatbot():
    # Watson Assistant setup with credentials
    assistant_id = "fa066656-028a-4dd8-8ca6-d6786705cb7d"
    api_key = "DrJaFYXTDpPgnbKZQzXFOUUCSqU-Mb_WnB3PM74Qjy1j"
    url = "https://api.au-syd.assistant.watson.cloud.ibm.com/instances/5cb3c724-68ce-42dc-bd4b-aee02c0ee1d8"

    authenticator = IAMAuthenticator(api_key)
    assistant = AssistantV2(
        version="2021-06-14", authenticator=authenticator
    )
    assistant.set_service_url(url)

    # Define the environment ID (choose draft or live)
    environment_id = "ece2135f-7006-4185-9f16-28773aa15790"  # Draft Environment ID

    # Create a new session (no environment_id here)
    session_response = assistant.create_session(
        assistant_id=assistant_id
    ).get_result()

    # Store the session ID
    session_id = session_response['session_id']

    # Chatbot interaction
    st.markdown(
        """
        <style>
        .chatbox-container {
            position: fixed;
            bottom: 10px;
            right: 10px;
            width: 300px;
            height: 400px;
            background-color: white;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            padding: 10px;
            z-index: 9999;
        }
        .chatbox-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .chatbox-body {
            overflow-y: auto;
            height: 80%;
            margin-bottom: 10px;
        }
        .user-input {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chatbox-container">', unsafe_allow_html=True)
    st.markdown('<div class="chatbox-header">Chat with Our Assistant</div>', unsafe_allow_html=True)

    user_input = st.text_input("Ask a question", key="user_input", placeholder="Enter your question here...")
    if user_input:
        response = assistant.message(
            assistant_id=assistant_id,
            environment_id=environment_id,  # Add the environment_id here for the message request
            session_id=session_id,
            input={'text': user_input}
        ).get_result()
        st.markdown(f"<div class='chatbox-body'>{response['output']['generic'][0]['text']}</div>",
                    unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# Routing
if selected_page == "Home":
    home_page()
elif selected_page == "About Us":
    about_us_page()
elif selected_page == "Explore Us":
    explore_option = st.radio("Choose an option:",
                              ["Cattle Health Prediction", "Common Recommendations", "Farming Practices"])

    if explore_option == "Cattle Health Prediction":
        cattle_health_prediction()
    elif explore_option == "Common Recommendations":
        common_recommendations()
    elif explore_option == "Farming Practices":
        farming_practices()
elif selected_page == "Contact":
    contact_page()

# Add chatbot
chatbot()
