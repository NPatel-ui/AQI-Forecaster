
from prediction_service import predict_city_aqi


def test_prediction(city):

    print("\n================================")
    print("PREDICTION TEST:", city)
    print("================================")

    try:

        result = predict_city_aqi(city)

        for key, value in result.items():
            print(f"{key}: {value}")

        print("\nRESULT: SUCCESS")

    except Exception as error:

        print("\nRESULT: FAILED")
        print("Error:", error)


if __name__ == "__main__":

    test_prediction("Delhi")
    test_prediction("Mumbai")
    test_prediction("Bengaluru")
    test_prediction("Coimbatore")
