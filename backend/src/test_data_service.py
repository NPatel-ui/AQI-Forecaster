
from data_service import get_city_features, FEATURES


def test_city(city):

    print("\n================================")
    print("TESTING CITY:", city)
    print("================================")

    try:

        result = get_city_features(city)

        print("City:", result["city"])
        print("Feature date:", result["feature_date"])
        print("Prediction date:", result["prediction_for_date"])

        print(
            "Observed AQI:",
            result["observed_aqi_on_feature_date"]
        )

        print("\nMODEL FEATURES:")

        for feature, value in result["features"].items():
            print(f"{feature}: {value}")

        print("\nTotal features:", len(result["features"]))

        missing_count = sum(
            value is None
            for value in result["features"].values()
        )

        print("Missing features:", missing_count)

        assert list(result["features"].keys()) == FEATURES
        assert result["features"]["aqi_today"] is not None

        print("\nRESULT: SUCCESS")

    except Exception as error:

        print("\nRESULT: FAILED")
        print("Error:", error)


if __name__ == "__main__":

    test_city("Delhi")
    test_city("Mumbai")
    test_city("Bengaluru")
    test_city("Coimbatore")
    test_city("UnknownCity")
