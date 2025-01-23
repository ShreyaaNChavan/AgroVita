import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def load_dataset(file_path):
    """
    Load the preprocessed dataset from a CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        print("Dataset loaded successfully!")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def train_and_save_model(data, model_save_path, feature_save_path):
    """
    Train a Random Forest model on the preprocessed data and save it.
    """
    # Reconvert continuous 'health_status' to categorical values
    data['health_status'] = data['health_status'].apply(lambda x: 1 if x > 0 else 0)

    # Encode categorical columns
    categorical_columns = data.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        print(f"Encoding categorical columns: {categorical_columns.tolist()}")
        data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)

    # Split the data into features and target
    X = data.drop(columns=['health_status'])  # Drop the target column
    y = data['health_status']  # Target variable (health_status)

    # Save feature names
    feature_names = list(X.columns)
    with open(feature_save_path, "w") as f:
        f.write("\n".join(feature_names))
    print(f"Feature names saved to {feature_save_path}")

    # Split the dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(random_state=42)

    try:
        # Train the model
        model.fit(X_train, y_train)
        print("Model trained successfully!")

        # Predict on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy * 100:.2f}%")

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        # Save evaluation metrics to a file
        with open("C:/Users/admin/ShreyaProjects/IBM/data/evaluation_report.txt", "w") as f:
            f.write(f"Accuracy: {accuracy * 100:.2f}%\n")
            f.write("\nClassification Report:\n")
            f.write(classification_report(y_test, y_pred))
            f.write("\nConfusion Matrix:\n")
            f.write(str(confusion_matrix(y_test, y_pred)))

        # Save the trained model to a file
        joblib.dump(model, model_save_path)
        print(f"Model saved successfully to {model_save_path}")
    except Exception as e:
        print(f"Error during training or saving: {e}")

if __name__ == "__main__":
    input_file = "C:/Users/admin/ShreyaProjects/IBM/data/preprocessed_cattle_health_dataset.csv"
    model_save_path = "C:/Users/admin/ShreyaProjects/IBM/data/cattle_health_model.pkl"
    feature_save_path = "C:/Users/admin/ShreyaProjects/IBM/data/cattle_health_features.txt"

    data = load_dataset(input_file)

    if data is not None:
        train_and_save_model(data, model_save_path, feature_save_path)
