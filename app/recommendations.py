import streamlit as st


# Function to generate recommendations based on cattle health data
def generate_recommendations(cattle_data):
    recommendations = []

    # Diet Adjustments
    if cattle_data['rumen_fill'] == 1:  # 'low' is mapped to 1
        recommendations.append("Increase fiber-rich feed.")
    if cattle_data['eating_duration'] < 4:
        recommendations.append("Monitor feed quality and accessibility.")

    # Medical Attention
    if cattle_data['faecal_consistency'] == 1:  # 'black' is mapped to 1
        recommendations.append("Consult a veterinarian immediately.")
    if cattle_data['respiratory_rate'] > 40 or cattle_data['heart_rate'] > 100:
        recommendations.append("Possible stress or disease. Recommend veterinary checkup.")

    # Environmental Changes
    if cattle_data['body_temperature'] > 39.5:
        recommendations.append("Provide cooling systems to reduce heat stress.")
    if cattle_data['sleeping_duration'] < 3:
        recommendations.append("Evaluate barn conditions to ensure adequate rest.")

    # Activity Monitoring
    if cattle_data['walking_capacity'] < 10:
        recommendations.append("Check for lameness or foot issues.")

    # Hydration
    recommendations.append(
        "Ensure access to clean and sufficient water, especially for high body temperature or respiratory rates.")

    return recommendations


# Main function for recommendations page
def main():
    st.title("Cattle Health Recommendations")

    # User inputs for recommendations (only relevant parameters)
    st.header("Input the following details:")

    body_temperature = st.number_input("Body Temperature (\u00b0C):", min_value=35.0, max_value=42.0, step=0.1)
    respiratory_rate = st.number_input("Respiratory Rate (breaths/min):", min_value=10, max_value=80)
    walking_capacity = st.number_input("Walking Capacity (hours/day):", min_value=0.0, max_value=24.0, step=0.1)
    sleeping_duration = st.number_input("Sleeping Duration (hours/day):", min_value=0.0, max_value=24.0, step=0.1)
    eating_duration = st.number_input("Eating Duration (hours/day):", min_value=0.0, max_value=24.0, step=0.1)
    rumen_fill = st.selectbox("Rumen Fill (1-5):", [1, 2, 3, 4, 5])

    # Add heart_rate input here
    heart_rate = st.number_input("Heart Rate (beats/min):", min_value=40, max_value=140)

    # Dropdown options
    faecal_consistency = st.selectbox("Faecal Consistency:", ["Normal", "Loose", "Black", "Fresh blood"])

    # Map categorical inputs to numerical values
    faecal_mapping = {"Normal": 0, "Loose": 1, "Black": 1, "Fresh blood": 1}

    # Prepare input data
    input_data = {
        "body_temperature": body_temperature,
        "respiratory_rate": respiratory_rate,
        "walking_capacity": walking_capacity,
        "sleeping_duration": sleeping_duration,
        "eating_duration": eating_duration,
        "rumen_fill": rumen_fill,
        "faecal_consistency": faecal_mapping[faecal_consistency],
        "heart_rate": heart_rate  # Include heart_rate here
    }

    # Generate and display recommendations
    recommendations = generate_recommendations(input_data)

    st.write("Cattle Health Recommendations:")
    for rec in recommendations:
        st.write(f"- {rec}")


# Run the app
if __name__ == "__main__":
    main()
