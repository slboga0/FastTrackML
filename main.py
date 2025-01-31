import pandas as pd
from src import Config
from src.HorseRaceDataProcessor import HorseRaceDataProcessor
from src.HorseRaceModel import HorseRaceModel
from src.HorseRacePredictionUI import HorseRacePredictionUI

def main():
     # Load configuration
    config = Config("config.json")

    # Step 1: Fetch and prepare data
    api_url = config.get("api_url", "https://example.com/past_performance_data.csv")
    save_path = config.get("save_path", "past_performance_data.csv")

    data_processor = HorseRaceDataProcessor()
    file_path = data_processor.fetch_past_performance_data(api_url, save_path)
    historical_data = data_processor.prepare_dataframe(file_path)

    # Step 2: Split data into train,clear validation, and test
    train_data, validation_data, test_data = data_processor.split_data(historical_data)

    # Step 3: Train model
    model = HorseRaceModel()
    model.train(train_data)
    model.validate(validation_data)

    # Step 4: Operationalize prediction
    ui = HorseRacePredictionUI()
    today_race_data = ui.upload_today_race(config.get("today_race_file", "today_race_data.csv"))
    today_race_data = pd.read_today_race("today_race_data.csv")
    predictions = model.predict(today_race_data)
    ui.display_predictions(predictions)

if __name__ == "__main__":
    main()
