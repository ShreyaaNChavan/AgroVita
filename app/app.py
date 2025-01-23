import streamlit as st
import requests
import plotly.graph_objects as go


# Function to get IAM token
def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    payload = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # Ensure the request was successful
    return response.json()["access_token"]


# Function to call IBM Cloud AI model API
def call_ibm_cloud_model(mltoken, endpoint, input_data):
    # IBM Cloud API headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mltoken}"
    }

    # Prepare the payload
    payload = {
        "input_data": [
            {
                "fields": list(input_data.keys()),
                "values": [list(input_data.values())]
            }
        ]
    }

    # Make the API request
    response = requests.post(endpoint, headers=headers, json=payload)

    # Handle response
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()  # Raise an HTTPError if the request fails


# Function to process the IBM Cloud model response
def process_response(response):
    if "predictions" in response:
        predictions = response["predictions"][0]
        prediction = predictions["values"][0][0]  # Extract "prediction" field
        probabilities = predictions["values"][0][1]  # Extract "probability" field

        # Set Unhealthy as the positive class (check the correct index for unhealthy)
        healthy_prob = probabilities[0]  # Healthy probability
        unhealthy_prob = probabilities[1]  # Unhealthy probability

        # Based on probabilities, decide the health status
        health_status = "Unhealthy" if unhealthy_prob > healthy_prob else "Healthy"
        return health_status, healthy_prob, unhealthy_prob
    else:
        raise ValueError("Invalid response format from the model")


# Function to plot a pie chart using plotly
def plot_pie_chart(healthy_prob, unhealthy_prob):
    labels = ['Healthy', 'Unhealthy']
    values = [healthy_prob, unhealthy_prob]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3,
                                 marker_colors=['#66b3ff', '#ff6666'],
                                 textinfo='percent', pull=[0.1, 0])])

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)


# Main function
def main():
    st.set_page_config(page_title="Cattle Health Prediction", page_icon="🐄", layout="wide")

    # Title with styling
    st.title("🐄 Cattle Health Prediction System")
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            font-size: 2.5em;
            color: #4CAF50;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar for inputs
    st.sidebar.header("Enter Cattle Data")
    body_temperature = st.sidebar.number_input("Body Temperature (°C):", min_value=35.0, max_value=42.0, step=0.1)
    milk_production = st.sidebar.number_input("Milk Production (liters):", min_value=0.0, max_value=50.0, step=0.1)
    respiratory_rate = st.sidebar.number_input("Respiratory Rate (breaths/min):", min_value=10, max_value=80)
    walking_capacity = st.sidebar.number_input("Walking Capacity (hours/day):", min_value=0.0, max_value=24.0, step=0.1)
    sleeping_duration = st.sidebar.number_input("Sleeping Duration (hours/day):", min_value=0.0, max_value=24.0,
                                                step=0.1)
    body_condition_score = st.sidebar.number_input("Body Condition Score (1-5):", min_value=1.0, max_value=5.0,
                                                   step=0.1)
    heart_rate = st.sidebar.number_input("Heart Rate (beats/min):", min_value=40, max_value=140)
    eating_duration = st.sidebar.number_input("Eating Duration (hours/day):", min_value=0.0, max_value=24.0, step=0.1)
    lying_down_duration = st.sidebar.number_input("Lying Down Duration (hours/day):", min_value=0.0, max_value=24.0,
                                                  step=0.1)
    ruminating = st.sidebar.number_input("Ruminating Time (hours/day):", min_value=0.0, max_value=24.0, step=0.1)
    rumen_fill = st.sidebar.number_input("Rumen Fill (scale 1-5):", min_value=1, max_value=5)

    # Dropdown options
    faecal_consistency = st.sidebar.selectbox("Faecal Consistency:", ["Normal", "Loose", "Hard"])
    breed_type = st.sidebar.selectbox("Breed Type:", ["Dairy", "Beef", "Dual-purpose"])

    # Map categorical inputs to numerical values
    faecal_mapping = {"Normal": 0, "Loose": 1, "Hard": 2}
    breed_mapping = {"Dairy": 0, "Beef": 1, "Dual-purpose": 2}

    # Prepare input data
    input_data = {
        "body_temperature": body_temperature,
        "milk_production": milk_production,
        "respiratory_rate": respiratory_rate,
        "walking_capacity": walking_capacity,
        "sleeping_duration": sleeping_duration,
        "body_condition_score": body_condition_score,
        "heart_rate": heart_rate,
        "eating_duration": eating_duration,
        "lying_down_duration": lying_down_duration,
        "ruminating": ruminating,
        "rumen_fill": rumen_fill,
        "faecal_consistency": faecal_mapping[faecal_consistency],
        "breed_type": breed_mapping[breed_type]
    }

    # Display input data
    st.sidebar.write("### Input Data Preview")
    st.sidebar.json(input_data)

    # Button to trigger prediction
    if st.sidebar.button("Predict Cattle Health"):
        try:
            # IBM Cloud details
            api_key = "ZII18t5wncEbcRhyHM_G_qEsK3pPyowTwrSS7mRfVpgr"  # Replace with your actual API key
            endpoint = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/25994928-be04-48ce-b69e-b73c5c4db565/predictions?version=2021-05-01"  # Replace with your endpoint

            # Get IAM token
            mltoken = get_iam_token(api_key)

            # Call model
            response = call_ibm_cloud_model(mltoken, endpoint, input_data)

            # Process and display response
            health_status, healthy_prob, unhealthy_prob = process_response(response)
            st.write(f"Healthy Probability: {healthy_prob:.4f}")
            st.write(f"Unhealthy Probability: {unhealthy_prob:.4f}")

            # Plot the pie chart
            plot_pie_chart(healthy_prob, unhealthy_prob)
            st.write(f"Full Response: {response}")

        except Exception as e:
            st.error(f"An error occurred: {e}")


# Run the app
if __name__ == "__main__":
    main()
