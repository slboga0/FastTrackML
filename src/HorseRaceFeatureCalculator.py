import pandas as pd
from HorseRaceFeatureSet import HorseRaceFeatureSet


class HorseRaceFeatureCalculator:
    @staticmethod
    def calculate_trainer_win_percentage_2_years(data : pd.DataFrame):
        # Logic for calculating trainer win percentage over 2 years
        return 25.0

    @staticmethod
    def calculate_best_lifetime_speed(data):
        # Logic for calculating best lifetime speed
        """Calculate speed in the last race, returning 0 for empty or NA values."""
        speed = data.get('best_bris_speed_life', '')
        if not speed or pd.isna(speed):
            return 0.0
        return speed

    @staticmethod
    def calculate_speed_last_race(data):
        """Calculate speed in the last race, returning 0 for empty or NA values."""
        speed = data.get('speed_rating_856', '')
        if not speed or pd.isna(speed):
            return 0.0
        return speed

    @staticmethod
    def calculate_best_speed_fast_track(data):
        # Logic for calculating best speed on a fast track
        """Calculate speed in the last race, returning 0 for empty or NA values."""
        speed = data.get('best_bris_speed_fast_track', '')
        if not speed or pd.isna(speed):
            return 0.0
        return speed

    @staticmethod
    def calculate_best_speed_this_distance(data):
        # Logic for calculating best speed at this distance
        """Calculate speed in the last race, returning 0 for empty or NA values."""
        speed = data.get('best_bris_speed_distance', '')
        if not speed or pd.isna(speed):
            return 0.0
        return speed
    
    @staticmethod
    def calculate_average_turf_earnings(data):
        # Logic for calculating average turf earnings
        """Calculate speed in the last race, returning 0 for empty or NA values."""
        speed = data.get('horses_lifetime_turf_record_earnings', '')
        if not speed or pd.isna(speed):
            return 0.0
        return speed

    @staticmethod
    def calculate_best_speed_last_3(data):
        # Logic for calculating best speed in the last 3 races
        return 33.0

    @staticmethod
    def calculate_in_the_money_percentage(data):
        # Logic for calculating in the money percentage
        return 50.0

    @staticmethod
    def calculate_best_speed_turf(data):
        # Logic for calculating best speed on turf
        return 38.0

    # Additional methods for each feature calculation go here
    # Implementing placeholder logic for all features for demonstration purposes

    @staticmethod
    def calculate_win_percentage(data):
        return 26.0

    @staticmethod
    def calculate_last_purse(data):
        return 45.0

    @staticmethod
    def calculate_last_finish_position(data):
        return 22.0

    @staticmethod
    def calculate_trainer_jockey_roi_meet(data):
        return 20.0

    # Add more feature calculation logic as needed


def add_all_features_to_set(feature_set: HorseRaceFeatureSet, data: pd.DataFrame) -> None:
    # Define all features
        features = [
           # "trainer_win_percentage_2_years_this_race_type",
            "best_lifetime_speed",
            "speed_last_race",
            "best_speed_fast_track",
            "best_speed_this_distance",
            "average_turf_earnings",
            "best_speed_last_3",
            "in_the_money_percentage",
            "best_speed_turf",
            "win_percentage",
            "last_purse",
            "last_finish_position",
            "average_all_weather_earnings",
            "best_speed_todays_track",
            "best_speed_all_weather",
            "average_speed_last_3",
            "average_earnings_todays_distance",
            "average_best_2_of_last_3",
            "distance_pedigree_rating",
            "last_race_class",
            "average_of_last_3_late_pace",
            "trainer_current_meet",
            "average_lifetime_earnings",
            "average_earnings_todays_track",
            "trainer_current_year",
            "last_e1_pace",
            "dirt_pedigree_rating",
            "horses_beaten_percentage",
            "trainer_win_percentage_1_year",
            "last_e2_pace",
            "turf_pedigree_rating",
            "trainer_win_percentage_6_months",
            "average_of_last_3_e2_pace",
            "last_turn_time",
            "jockey_win_percentage_2_years_this_race_type",
            "jockey_current_meet",
            "jockey_win_percentage_6_months",
            "mud_pedigree_rating",
            "trainer_jockey_win_percentage_2_years",
            "trainer_jockey_combo_win_percentage_meet",
            "jockey_current_year",
            "average_of_last_3_e1_pace",
            "best_speed_off_track",
            "average_off_track_earnings",
            "jockey_win_percentage_1_year",
            "average_of_last_3_turn_time",
            "distance_worked_since_last_race",
            "last_late_pace",
            "average_last_3_races_classes",
            "average_last_3_purse",
            "days_since_last_race",
            "trainer_jockey_roi_meet"
        ]

        # Add and calculate each feature
        for feature in features:
            feature_set.add_feature(feature)
            if feature == "trainer_win_percentage_2_years":
                feature_value = HorseRaceFeatureCalculator.calculate_trainer_win_percentage_2_years(data)
            elif feature == "best_lifetime_speed":
                feature_value = HorseRaceFeatureCalculator.calculate_best_lifetime_speed(data)
            elif feature == "speed_last_race":
                feature_value = HorseRaceFeatureCalculator.calculate_speed_last_race(data)
            elif feature == "best_speed_fast_track":
                feature_value = HorseRaceFeatureCalculator.calculate_best_speed_fast_track(data)
            elif feature == "best_speed_this_distance":
                feature_value = HorseRaceFeatureCalculator.calculate_best_speed_this_distance(data)
            elif feature == "average_turf_earnings":
                feature_value = HorseRaceFeatureCalculator.calculate_average_turf_earnings(data)
            elif feature == "best_speed_last_3":
                feature_value = HorseRaceFeatureCalculator.calculate_best_speed_last_3(data)
            elif feature == "in_the_money_percentage":
                feature_value = HorseRaceFeatureCalculator.calculate_in_the_money_percentage(data)
            elif feature == "best_speed_turf":
                feature_value = HorseRaceFeatureCalculator.calculate_best_speed_turf(data)
            elif feature == "win_percentage":
                feature_value = HorseRaceFeatureCalculator.calculate_win_percentage(data)
            elif feature == "last_purse":
                feature_value = HorseRaceFeatureCalculator.calculate_last_purse(data)
            elif feature == "last_finish_position":
                feature_value = HorseRaceFeatureCalculator.calculate_last_finish_position(data)
            elif feature == "trainer_jockey_roi_meet":
                feature_value = HorseRaceFeatureCalculator.calculate_trainer_jockey_roi_meet(data)
            else:
                # Default placeholder logic for unimplemented features
                feature_value = 0.0
            feature_set.set_feature_metrics(feature, feature_value)

# Example Usage
if __name__ == "__main__":
    feature_set = HorseRaceFeatureSet()
    data = pd.DataFrame()  # Placeholder for input DataFrame
    add_all_features_to_set(feature_set, data)
    print(feature_set.get_all_metrics())
