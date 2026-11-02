# AQI Forecaster

A historical, city-based Air Quality Index (AQI) forecasting backend
built with Python, FastAPI, and machine learning.

The project uses historical air-quality data from Indian cities to
estimate the AQI for the next calendar day. It currently focuses on
historical forecasting and model evaluation. **It does not fetch live
AQI readings or provide real-time forecasts.**

## Project Overview

Air pollution can change from day to day and from city to city. This
project explores how historical AQI values and pollutant measurements
can be used to estimate the following day's AQI.

The backend provides: - A machine-learning prediction endpoint that
accepts AQI-related input features. - A city-based endpoint that
retrieves a historical feature record and predicts the next day's AQI. -
Health and root endpoints for checking whether the API is running.

## Current Project Scope

**Implemented** - Historical dataset cleaning and exploratory data
analysis. - Daily feature engineering using AQI history, pollutant
measurements, and calendar features. - City-based train/test separation
to evaluate performance on cities not used for training. - A Random
Forest regression pipeline with median imputation. - FastAPI endpoints
for direct predictions and historical city-based forecasts. - Evaluation
against a persistence baseline.

**Planned for future development** - Integration of a live AQI data
source. - Real-time next-day forecasting using current observations. - A
React + Vite frontend. - A Personal Health Advisor. - Deployment.

These future features are not part of the current implementation.

## Dataset

The project uses the **City Day** air-quality dataset covering Indian
cities.

  Detail               Value
  -------------------- -------------------------------
  File                 `data/raw/city_day.csv`
  Records              29,531
  Original columns     16
  Cities               26
  Date range           1 January 2015 -- 1 July 2020
  Missing AQI values   4,681

The dataset contains city and date information, pollutant measurements,
AQI, and AQI category information.

The dataset is historical. It does not contain current 2026 readings.

The project history identifies the dataset as the Kaggle Air Quality
Data in India dataset by Rohan Rao. Check the dataset's Kaggle page and
licence before redistributing the original CSV. Add the exact source URL
here once it has been confirmed.

## Machine Learning Approach

The prediction task is a regression problem:

**Input:** Historical AQI, recent AQI trends, selected pollutant
measurements, and calendar features.

**Target:** The observed AQI on the next calendar day.

The final model is a scikit-learn `Pipeline` containing: 1. Median
imputation for missing feature values. 2. `RandomForestRegressor` for
AQI prediction.

The model uses 17 engineered features, including: - Current and previous
AQI values. - Rolling AQI mean and standard deviation. - One-day AQI
change. - Selected pollutant measurements. - Month and day-of-week
features.

The saved model is located at:

``` text
models/random_forest_aqi.joblib
```

The corresponding feature-name list is:

``` text
models/feature_names.txt
```

## Model Evaluation

The model was evaluated on five held-out cities that were not included
in the training-city group.

  Evaluation set   Model                      MAE    RMSE       R²
  ---------------- ---------------------- ------- ------- --------
  Test A           Random Forest            22.34   34.74   0.8606
  Test A           Persistence baseline     25.49   42.39   0.7925
  Test B           Random Forest            17.08   24.77   0.8482
  Test B           Persistence baseline     18.49   28.89   0.7935

-   **MAE** measures the average absolute prediction error. Lower is
    better.
-   **RMSE** penalizes larger errors more strongly. Lower is better.
-   **R²** indicates how much of the variation in the target is
    explained by the model. Higher is generally better.

The Random Forest model performed better than the persistence baseline
on both held-out test sets. These results describe evaluation on this
historical dataset; they do not guarantee the same performance on live
data or future conditions.

## Backend API

The API is built with FastAPI.

  -----------------------------------------------------------------------
  Method                  Endpoint                Purpose
  ----------------------- ----------------------- -----------------------
  `GET`                   `/`                     Root endpoint

  `GET`                   `/health`               Health check

  `POST`                  `/predict`              Predict AQI from 17
                                                  supplied numeric
                                                  features

  `GET`                   `/forecast/{city}`      Generate a historical
                                                  next-day forecast for a
                                                  city
  -----------------------------------------------------------------------

The city forecast endpoint also accepts an optional `date` query
parameter. Use the `YYYY-MM-DD` format.

### Example requests

Open the interactive API documentation after starting the server:

``` text
http://127.0.0.1:8000/docs
```

Example city forecast request:

``` text
GET http://127.0.0.1:8000/forecast/Delhi
```

Example with a date:

``` text
GET http://127.0.0.1:8000/forecast/Delhi?date=2020-07-01
```

The city endpoint uses the historical feature record for the requested
date and predicts the following calendar day's AQI. It is not a live
forecast.

## Project Structure

The following is the main backend layout:

``` text
backend/
├── data/
│   ├── raw/
│   │   └── city_day.csv
│   └── processed/
├── models/
│   ├── random_forest_aqi.joblib
│   └── feature_names.txt
├── report/
│   ├── eda/
│   └── evaluation outputs
└── src/
    ├── main.py
    ├── data_service.py
    ├── prediction_service.py
    └── data preparation, training, evaluation, and testing scripts
```

The `src` directory contains the Python scripts for data preparation,
exploratory analysis, feature engineering, data splitting, model
training, evaluation, API services, and tests.

## Setup and Run

### 1. Clone the repository

``` bash
git clone https://github.com/NPatel-ui/AQI-Forecaster.git
cd AQI-Forecaster
```

### 2. Open the backend directory

``` bash
cd backend
```

### 3. Create and activate a virtual environment

Windows Command Prompt:

``` bat
python -m venv .venv
.venv\Scripts\activate
```

Windows PowerShell:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install the backend packages

The project archive used to prepare this README did not include a
`requirements.txt` file. Install the packages required by the backend:

``` bash
python -m pip install --upgrade pip
pip install fastapi uvicorn pandas numpy scikit-learn joblib
```

If a script reports a missing package, install the package it names. A
pinned `requirements.txt` should be added after confirming the exact
working package versions.

### 5. Start the API

From the `backend` directory, run:

``` bash
uvicorn src.main:app --reload
```

Then open:

``` text
http://127.0.0.1:8000/docs
```

If your local package layout requires running from the `src` directory
instead, follow the import structure in `src/main.py`; the command above
assumes `src` is importable as a Python package.

## Notes and Limitations

-   This project uses historical data ending on **1 July 2020**.
-   The city-based forecast is a historical-data demonstration, not a
    current AQI service.
-   AQI values above 500 were retained in the source data during
    preprocessing rather than capped or removed.
-   Some pollutant and AQI values are missing. The model pipeline uses
    median imputation for missing model features.
-   Model performance can differ by city. An overall metric does not
    mean every city's predictions have the same error.
-   The model should be evaluated on new, reliable data before being
    used for operational or health-related decisions.
-   The predictions are estimates and should not be treated as official
    AQI measurements or medical advice.

## Technologies Used

-   Python
-   Pandas and NumPy
-   Matplotlib and Seaborn for exploratory data analysis
-   scikit-learn
-   Joblib
-   FastAPI
-   Uvicorn

## Future Work

1.  Connect a reliable live AQI data provider.
2.  Build a pipeline for current observations and real-time next-day
    forecasts.
3.  Develop a responsive React + Vite frontend.
4.  Add the Personal Health Advisor module.
5.  Test and deploy the complete application.

## Author

**Nitya Patel**\
B.Sc. Information Technology

------------------------------------------------------------------------

*This README describes the currently implemented historical forecasting
backend and separates it from planned future features.*
