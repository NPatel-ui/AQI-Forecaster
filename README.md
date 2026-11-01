## Inspiration

Air pollution affects millions of people, especially in Indian cities where air quality can change significantly from one day to another. We wanted to build a system that uses historical air-quality data and machine learning to estimate the next day's Air Quality Index (AQI). Our goal is to make air-quality information easier to understand and eventually help people make better decisions about their outdoor activities.

## What it does

AQI Forecaster is a machine-learning project that predicts next-day AQI using historical air-quality patterns, pollutant measurements, and date-related features.

The backend uses a Random Forest Regression model trained on Indian city-level air-quality data from 2015 to 2020. It uses 17 engineered features to generate predictions and exposes them through a FastAPI endpoint.

The project also plans a Personal Health Advisor that will provide general health precautions based on AQI categories and user profiles. This will be a separate rule-based component.

## How we built it

We used Python and pandas to inspect, clean, and prepare the historical dataset. We performed Exploratory Data Analysis (EDA) to understand AQI patterns across cities, months, and pollutant measurements.

We then engineered 17 features using current and previous AQI values, rolling statistics, pollutant readings, and calendar information. We created separate training and held-out test datasets, keeping 13 cities for training and five different cities for evaluation.

We compared multiple regression approaches against a persistence baseline, which predicts tomorrow's AQI as today's AQI. We then tuned a Random Forest Regressor using RandomizedSearchCV and GroupKFold cross-validation.

Finally, we trained and saved the model using Joblib and integrated it with FastAPI to provide predictions through a REST API.

## Challenges we ran into

One major challenge was handling missing pollutant measurements and unusually high AQI values. Instead of automatically removing extreme AQI readings, we investigated them and retained the original values.

Another challenge was ensuring that the next-day target was correctly aligned with historical features while avoiding data leakage. We also discovered that the simple persistence baseline initially performed better than our machine-learning models during cross-validation.

We investigated city-level errors, tuned the Random Forest hyperparameters, and evaluated the final model on held-out datasets. This taught us that a more complex algorithm does not automatically produce better predictions.

## Accomplishments that we're proud of

We successfully developed an end-to-end machine-learning backend, from raw-data inspection and feature engineering to model training, evaluation, and API-based prediction.

The final Random Forest achieved an MAE of 22.34 on Test A, containing unseen cities, and 17.08 on Test B, containing later dates from those held-out cities. It outperformed the persistence baseline on both final test sets.

We also successfully integrated the saved model with FastAPI and validated the prediction endpoint using a real historical Gurugram record.

## What we learned

We learned how to work with real-world environmental data, handle missing values, investigate outliers, engineer time-based features, and build a supervised regression pipeline.

We gained practical experience with Random Forest Regression, hyperparameter tuning, GroupKFold cross-validation, and evaluation metrics such as MAE, RMSE, and R².

Most importantly, we learned the importance of using proper baselines, preventing data leakage, evaluating models on held-out data, and reporting limitations honestly.

## What's next for AQI Forecaster

Our next steps are to build a React-based dashboard, allow users to select a city, and automate the process of preparing the model's input features.

We also plan to integrate a suitable current AQI data source, add historical trend visualizations, and implement the rule-based Personal Health Advisor.

The long-term goal is to turn AQI Forecaster into a user-friendly application that combines next-day AQI estimates with clear, responsible health guidance.
