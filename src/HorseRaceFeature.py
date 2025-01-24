import pandas as pd
import requests
from datetime import datetime, timedelta

class HorseRaceFeature:
    def __init__(self, feature_name):
        self.feature_name = feature_name
        self.win_percentage = 0.0
        self.place_percentage = 0.0
        self.show_percentage = 0.0
        self.accuracy = 0.0

    def set_metrics(self, win_percentage, place_percentage, show_percentage, accuracy):
        self.win_percentage = win_percentage
        self.place_percentage = place_percentage
        self.show_percentage = show_percentage
        self.accuracy = accuracy

    def get_metrics(self):
        return {
            "win_percentage": self.win_percentage,
            "place_percentage": self.place_percentage,
            "show_percentage": self.show_percentage,
            "accuracy": self.accuracy
        }