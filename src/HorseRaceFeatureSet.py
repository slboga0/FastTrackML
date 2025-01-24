
from src import HorseRaceFeature


class HorseRaceFeatureSet:
    def __init__(self):
        self.features = {}

    def add_feature(self, feature_name):
        if feature_name not in self.features:
            self.features[feature_name] = HorseRaceFeature(feature_name)
        else:
            raise ValueError(f"Feature '{feature_name}' already exists.")

    def set_feature_metrics(self, feature_name, win_percentage, place_percentage, show_percentage, accuracy):
        if feature_name in self.features:
            self.features[feature_name].set_metrics(win_percentage, place_percentage, show_percentage, accuracy)
        else:
            raise ValueError(f"Feature '{feature_name}' does not exist.")

    def get_feature_metrics(self, feature_name):
        if feature_name in self.features:
            return self.features[feature_name].get_metrics()
        else:
            raise ValueError(f"Feature '{feature_name}' does not exist.")

    def get_all_features(self):
        return list(self.features.keys())

    def get_all_metrics(self):
        return {
            feature_name: feature.get_metrics()
            for feature_name, feature in self.features.items()
        }