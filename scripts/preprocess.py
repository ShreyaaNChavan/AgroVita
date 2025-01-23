import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load Dataset
def load_dataset(file_path):
    """
    Load the dataset from a CSV or XLSX file.
    """
    try:
        # Check file extension to decide if it's CSV or XLSX
        if file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path, engine='openpyxl')  # Read Excel file
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path)  # Read CSV file
        else:
            raise ValueError("Unsupported file format. Please use .csv or .xlsx files.")

        print("Dataset loaded successfully!")
        print(f"Initial shape: {data.shape}")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Handle Missing Values
def handle_missing_values(data):
    """
    Handle missing values in the dataset.
    """
    print("Handling missing values...")

    # Check if there are NaN values before handling
    print(f"Missing values before handling:\n{data.isnull().sum()}")

    # Fill missing numerical values with mean
    numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_cols:
        data[col] = data[col].fillna(data[col].mean())  # Avoid inplace, directly assign

    # Fill missing categorical values with mode
    categorical_cols = data.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        data[col] = data[col].fillna(data[col].mode()[0])  # Avoid inplace, directly assign

    print(f"Missing values after handling:\n{data.isnull().sum()}")
    return data

# Encode Categorical Variables
def encode_categorical(data):
    """
    Encode categorical variables using LabelEncoder.
    """
    print("Encoding categorical variables...")

    label_encoder = LabelEncoder()
    categorical_cols = data.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        data[col] = label_encoder.fit_transform(data[col])
    print(f"Categorical columns encoded: {categorical_cols}")
    return data

# Scale Numerical Features
def scale_features(data):
    """
    Scale numerical features using StandardScaler.
    """
    print("Scaling numerical features...")

    scaler = StandardScaler()
    numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
    data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

    print(f"Numerical columns scaled: {numerical_cols}")
    return data

# Full Preprocessing Pipeline
def preprocess_data(file_path):
    """
    Full preprocessing pipeline: load, clean, encode, and scale the dataset.
    """
    # Step 1: Load Dataset
    data = load_dataset(file_path)
    if data is None:
        return None

    # Step 2: Handle Missing Values
    data = handle_missing_values(data)

    # Step 3: Encode Categorical Variables
    data = encode_categorical(data)

    # Step 4: Scale Numerical Features
    data = scale_features(data)

    print("Preprocessing complete!")
    return data

# Save Preprocessed Dataset
def save_preprocessed_data(data, output_path):
    """
    Save the preprocessed dataset to a new CSV file.
    """
    try:
        data.to_csv(output_path, index=False)
        print(f"Preprocessed dataset saved to {output_path}")
        print(data['health_status'].value_counts())

    except Exception as e:
        print(f"Error saving dataset: {e}")

# Main Execution
if __name__ == "__main__":
    # File paths
    input_file = "C:/Users/admin/ShreyaProjects/IBM/data/cattle_dataset.xlsx"  # Replace with your dataset file path (Excel file)
    output_file = "C:/Users/admin/ShreyaProjects/IBM/data/preprocessed_cattle_health_dataset.csv"  # Desired CSV output path

    # Preprocess dataset
    preprocessed_data = preprocess_data(input_file)

    # Save preprocessed dataset
    if preprocessed_data is not None:
        save_preprocessed_data(preprocessed_data, output_file)
