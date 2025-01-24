class HorseRaceFeature:
    def __init__(self, feature_name):
        self.feature_name = feature_name
        self.value = 0.0

    def set_metrics(self, feature_value):
        self.feature_value = feature_value

    def get_metrics(self):
        return {
            "feature_value" : self.feature_value
        }