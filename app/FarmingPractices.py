import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from streamlit.components.v1 import html

# Function to get real-time weather data
def get_weather_data(city):
    api_key = "bf00e932fd14f7003652465defc5fb37"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Function to display farming best practices
def display_farming_practices():
    st.header("🌱 Sustainable Farming Practices")

    practices = [
        {
            "title": "Crop Rotation",
            "image_path": r"C:\Users\admin\ShreyaProjects\IBM\Images\Crop-Rotation.webp",
            "description": "Crop rotation helps maintain soil fertility and reduce pests by alternating crops grown in a field each season.",
        },
        {
            "title": "Organic Fertilizers",
            "image_path": r"C:\Users\admin\ShreyaProjects\IBM\Images\organic_fertilizers.jpg",
            "description": "Using organic fertilizers improves soil structure and provides essential nutrients naturally.",
        },
        {
            "title": "Water Conservation",
            "image_path": r"C:\Users\admin\ShreyaProjects\IBM\Images\water_conservation.jpeg",
            "description": "Efficient water use techniques like drip irrigation conserve water and enhance productivity.",
        },
    ]

    for practice in practices:
        st.subheader(f"🌾 {practice['title']}")
        try:
            st.image(practice["image_path"], caption=practice["title"])
        except Exception:
            st.warning(f"Image not found or could not be displayed: {practice['image_path']}")
        st.write(practice["description"])
        st.markdown("---")

# Function to plot crop yield vs other variables
def plot_crop_yield(dataset):
    st.header("Crop Yield Analysis")
    st.write(
        "This section visualizes the relationship between various factors like rainfall, soil quality, farm size, and fertilizer usage on crop yield."
    )

    # 1. Scatter plot for Rainfall vs Crop Yield
    st.subheader("1. Rainfall vs Crop Yield")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=dataset, x="rainfall_mm", y="crop_yield", hue="soil_quality_index", palette="viridis")
    plt.title("Rainfall vs Crop Yield (Color coded by Soil Quality Index)")
    plt.xlabel("Rainfall (mm)")
    plt.ylabel("Crop Yield (kg)")
    st.pyplot(plt)

    # 2. Bar plot for Farm Size vs Crop Yield
    st.subheader("2. Farm Size vs Crop Yield")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dataset, x="farm_size_hectares", y="crop_yield", ci=None, palette="Blues")
    plt.title("Farm Size vs Crop Yield")
    plt.xlabel("Farm Size (Hectares)")
    plt.ylabel("Crop Yield (kg)")
    st.pyplot(plt)

    # 3. Line plot for Sunlight Hours vs Crop Yield
    st.subheader("3. Sunlight Hours vs Crop Yield")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=dataset, x="sunlight_hours", y="crop_yield", marker="o", color="green")
    plt.title("Sunlight Hours vs Crop Yield")
    plt.xlabel("Sunlight Hours")
    plt.ylabel("Crop Yield (kg)")
    st.pyplot(plt)

    # 4. Box plot for Fertilizer Used vs Crop Yield
    st.subheader("4. Fertilizer Used vs Crop Yield")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=dataset, x="fertilizer_kg", y="crop_yield", palette="coolwarm")
    plt.title("Fertilizer Used vs Crop Yield")
    plt.xlabel("Fertilizer Used (kg)")
    plt.ylabel("Crop Yield (kg)")
    st.pyplot(plt)

    # 5. Heatmap for Correlation Between Factors
    st.subheader("5. Correlation Heatmap")
    plt.figure(figsize=(10, 6))
    correlation_matrix = dataset.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Between Factors")
    st.pyplot(plt)

# Main function to create the Farming Practices page
def main():
    st.title("Farming Practices")

    # Load the pre-trained model
    try:
        model = joblib.load("crop_yield_model.pkl")
    except FileNotFoundError:
        st.error("Trained model file not found. Please ensure 'crop_yield_model.pkl' is present in the working directory.")
        return

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Weather Data", "Farming Practices", "Crop Yield Analysis"])

    # Tab 1: Weather Data
    with tab1:
            st.header("🌤️ Real-Time Weather Data")

            # Input for city with placeholder and styling
            city = st.text_input(
                "Enter your city",
                value="New York",
                placeholder="Type a city name...",
                help="Enter the name of your city to fetch real-time weather information."
            )

            if city:
                weather_data = get_weather_data(city)
                if weather_data.get("main"):
                    # Fetch weather details
                    temperature = weather_data["main"]["temp"]
                    humidity = weather_data["main"]["humidity"]
                    weather_description = weather_data["weather"][0]["description"].capitalize()

                    # Weather Icon and Description
                    weather_icon = weather_data["weather"][0]["icon"]
                    icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"

                    # Layout for weather info
                    st.markdown(
                        f"""
                        <div style="background-color: #AEEA94; padding: 20px; border-radius: 8px; text-align: center;">
                            <h2 style="color: #2c3e50;">Current Weather in {city}</h2>
                            <img src="{icon_url}" alt="Weather Icon" style="width: 100px;"/>
                            <h3 style="color: #34495e;">{weather_description}</h3>
                            <p style="font-size: 20px; color: #2c3e50;"><b>Temperature:</b> {temperature}°C</p>
                            <p style="font-size: 20px; color: #2c3e50;"><b>Humidity:</b> {humidity}%</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("⚠️ Sorry, we couldn't retrieve weather data. Please try again.")

    # Tab 2: Sustainable Farming Practices
    with tab2:
        display_farming_practices()

    # Tab 3: Crop Yield Analysis
    with tab3:
        st.header("Crop Yield Prediction and Analysis")

        # Inputs for visualization
        rainfall = st.number_input("Rainfall (mm)", min_value=0, step=10, value=1500)
        soil_quality = st.number_input("Soil Quality Index", min_value=1, max_value=10, step=1, value=5)
        farm_size = st.number_input("Farm Size (Hectares)", min_value=1, step=10, value=500)
        sunlight_hours = st.number_input("Sunlight Hours", min_value=1, max_value=24, step=1, value=10)
        fertilizer = st.number_input("Fertilizer Used (kg)", min_value=0, step=10, value=1000)

        # Predict button
        if st.button("Predict"):
            # Prepare input for prediction
            input_data = [[rainfall, soil_quality, farm_size, sunlight_hours, fertilizer]]

            # Predict crop yield
            try:
                predicted_yield = model.predict(input_data)[0]
                st.success(f"Predicted Crop Yield: {predicted_yield:.2f} kg")

                # Add predicted yield to the dataset for visualization
                user_data = {
                    "rainfall_mm": [rainfall],
                    "soil_quality_index": [soil_quality],
                    "farm_size_hectares": [farm_size],
                    "sunlight_hours": [sunlight_hours],
                    "fertilizer_kg": [fertilizer],
                    "crop_yield": [predicted_yield],
                }
                df = pd.DataFrame(user_data)

                st.write("Here is the dynamic dataset with your input:")
                st.dataframe(df)

                # Visualize dynamic data
                plot_crop_yield(df)

            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")


# Run the app
if __name__ == "__main__":
    main()
