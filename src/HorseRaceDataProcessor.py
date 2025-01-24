import logging
import pandas as pd
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from HorseRaceDataPrep import run_data_prep
from Utility_functions import load_field_mapping

class HorseRaceDataProcessor:
    @staticmethod
    def fetch_past_performance_data(api_url, save_path):
        response = requests.get(api_url)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            return save_path
        else:
            raise Exception(f"Failed to fetch data from {api_url}")

    @staticmethod
    def prepare_dataframe(file_path):
        # Example: Read data into a pandas DataFrame
        data = pd.read_csv(file_path)
        return data

    @staticmethod
    def split_data(data):
        train = data.sample(frac=0.7, random_state=42)
        temp = data.drop(train.index)
        validation = temp.sample(frac=0.5, random_state=42)
        test = temp.drop(validation.index)
        return train, validation, test

def prepare_data_for_modeling(df, field_map, target_column):
    """Prepare data for training, validation, and testing."""
    # Select predictive features
    predictive_features = [
        col['field_name'] for col in field_map if col['predictive_feature'] == 1
    ]

    # Keep only relevant features and target
    features_df = df[predictive_features]
    target_df = df[target_column]

    print (f'Number of rows in features_df: {len(features_df)}')
    print (f'Number of rows in target_df: {len(target_df)}')

    print (features_df.head())

    features_df.to_csv('features.csv', index=False)
    # Drop rows with NaN in the target column or features
    valid_rows = features_df.notna().all(axis=1) & target_df.notna()

    print (valid_rows.head())
    print (f'Number of valid rows: {valid_rows.sum()}')

    features_df = features_df[valid_rows]
    target_df = target_df[valid_rows]

    # Ensure there is data to split
    if features_df.empty or target_df.empty:
        raise ValueError("No valid data available for training after filtering for missing values.")

    # One-hot encode categorical variables
    features_df = pd.get_dummies(features_df, drop_first=True)

    # Split into train, validation, and test sets
    if len(features_df) < 3:
        raise ValueError("Insufficient data to split into train, validation, and test sets.")

    X_train, X_temp, y_train, y_temp = train_test_split(features_df, target_df, test_size=0.4, random_state=42)
    X_validate, X_test, y_validate, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    return X_train, X_validate, X_test, y_train, y_validate, y_test


def binary_regression_classifier(X_train, X_validate, X_test, y_train, y_validate, y_test):
    """Perform binary regression classification and analyze feature importance."""
    logging.info("Training the binary regression classifier.")

    # Train the model
    model = LogisticRegression(random_state=42, max_iter=500)
    model.fit(X_train, y_train)

    # Validate the model
    y_validate_pred = model.predict(X_validate)
    validation_accuracy = accuracy_score(y_validate, y_validate_pred)
    logging.info(f"Validation Accuracy: {validation_accuracy:.2f}")

    # Test the model
    y_test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    logging.info(f"Test Accuracy: {test_accuracy:.2f}")

    # Print classification report
    logging.info("Classification Report:")
    logging.info(classification_report(y_test, y_test_pred))

    # Feature importance (coefficients)
    feature_importance = pd.DataFrame({
        'Feature': X_train.columns,
        'Coefficient': model.coef_[0]
    }).sort_values(by='Coefficient', ascending=False)

    logging.info("Feature Importance:")
    logging.info(feature_importance)

    return model, feature_importance


def main():
    # 1. Read past performance for host race in csv format to put together entire data
    #    into a single dataframe to begin ML - Train, Val, Test

    df, field_map = run_data_prep()

    df.to_csv('pp_data.csv', index=False)
    print (f'Number of valid rows: {df.sum()}')

     # Prepare data for modeling
    X_train, X_validate, X_test, y_train, y_validate, y_test = prepare_data_for_modeling(df, field_map, target_column='res_finish')

    print("Training describe", X_train.to_string())
    print("Validation describe", X_validate.to_string())
    print("Test describe", X_test.to_string())

    X_train.to_csv('Train_data.csv', index=False)


    # Print shapes of resulting datasets
    print("Training set shape:", X_train.shape, y_train.shape)
    print("Validation set shape:", X_validate.shape, y_validate.shape)
    print("Test set shape:", X_test.shape, y_test.shape)
    
     # Train and evaluate binary regression classifier
    #model = binary_regression_classifier(X_train, X_validate, X_test, y_train, y_validate, y_test)

    # Print model coefficients
    logging.info("Model Coefficients:")
    #logging.info(model.coef_)

    #feature_set = HorseRaceFeatureSet()
    #add_all_features_to_set(feature_set, data_frame)

    print ('Modeling Completed.')

if __name__ == "__main__":
    main()