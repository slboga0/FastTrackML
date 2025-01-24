class HorseRacePredictionUI:
    @staticmethod
    def upload_today_race(file_path):
        # Placeholder for uploading today's race data
        data = pd.read_csv(file_path)
        return data

    @staticmethod
    def display_predictions(predictions):
        print("Race Predictions:")
        for position, probability in predictions.items():
            print(f"{position}: {probability:.2%}")
