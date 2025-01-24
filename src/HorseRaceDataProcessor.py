import pandas as pd
import requests


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

def main():
    print("Hello from my_package!")
    # Your main application logic here

if __name__ == "__main__":
    main()