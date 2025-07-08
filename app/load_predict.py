# This is for loading the model, preprocessing the data, and making predictions

from xgboost import XGBRegressor
import pandas as pd

def load_model():
    # Load the pre-trained XGBoost model
    low_duration_model = XGBRegressor()
    high_duration_model = XGBRegressor()

    model_path1 = 'app/artifacts/low_duration_model.json'
    model_path2 = 'app/artifacts/high_duration_model.json'

    low_duration_model.load_model(model_path1)
    high_duration_model.load_model(model_path2)

    return low_duration_model, high_duration_model


def preprocess(input_features):
    expected_columns = ['age', 'height', 'weight', 'duration', 'heart_rate', 'gender_male', 'cardio_load', 'mass_ratio']

    # Create a DataFrame with the expected columns and initialize with zeros
    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    
    # Fill the DataFrame with input features
    # Handle gender encoding
    if input_features['gender'].lower() == 'male':
        df['gender_male'] = 1
    else:
        df['gender_male'] = 0

    # Assign other inputs
    df['age'] = input_features['age']
    df['weight'] = input_features['weight']
    df['height'] = input_features['height']
    df['duration'] = input_features['duration']
    df['heart_rate'] = input_features['heart_rate']

    # Derived features
    df['cardio_load'] = df['duration'] * df['heart_rate']
    df['mass_ratio'] = df['weight'] / df['height']

    return df


def predict_calories(input_features):
    # This function is for loading the model, preprocessing the data, and making predictions

    input_df = preprocess(input_features)

    # Load the pre-trained models
    low_duration_model, high_duration_model = load_model()

    # Choose model based on duration
    duration = input_features.get('duration', 0)

    # Predict using the appropriate model based on duration
    if duration <= 10:
        prediction = low_duration_model.predict(input_df)
    else:
        prediction = high_duration_model.predict(input_df)

    return float(prediction[0])  # Return the first prediction value

