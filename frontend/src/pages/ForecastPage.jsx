
import { useState, useEffect } from 'react';
import {
  Wind,
  Calendar,
  Sparkles,
  Activity,
  Layers,
  ChevronDown,
  ChevronUp,
  CheckCircle2,
} from 'lucide-react';

import { PageContainer } from '../components/layout/PageContainer';
import { BentoCard } from '../components/ui/BentoCard';
import { Button } from '../components/ui/Button';
import { ForecastHeroCard } from '../components/forecast/ForecastHeroCard';
import { CitySelector } from '../components/forecast/CitySelector';
import { DateSelector } from '../components/forecast/DateSelector';
import { PollutantBar } from '../components/bento/PollutantBar';
import { CategoryGauge } from '../components/bento/CategoryGauge';

import { getCityForecast } from '../services/api';
import { saveForecast } from '../services/forecastService';
import { ELIGIBLE_CITIES } from '../utils/datasetInfo';
import { getAqiCategory } from '../utils/aqiUtils';


export function ForecastPage() {

  // --------------------------------------------------
  // STATE MANAGEMENT
  // --------------------------------------------------

  const [city, setCity] = useState('Delhi');
  const [date, setDate] = useState('2020-07-01');

  const [forecast, setForecast] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [showModelDetails, setShowModelDetails] = useState(false);

  const [isSaved, setIsSaved] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const [saveNotice, setSaveNotice] = useState('');


  // --------------------------------------------------
  // FETCH CITY FORECAST
  // --------------------------------------------------

  const fetchForecast = async (
    targetCity = city,
    targetDate = date
  ) => {

    setLoading(true);
    setError(null);
    setForecast(null);

    setIsSaved(false);
    setSaveNotice('');

    try {

      const result = await getCityForecast(
        targetCity,
        targetDate
      );

      if (result.success && result.data) {

        setForecast(result.data);

      } else {

        setError(
          result.error ||
          'Unable to generate forecast. Please try again.'
        );

      }

    } catch (err) {

      setError(
        err.message ||
        'Unable to connect to the forecasting server.'
      );

    } finally {

      setLoading(false);

    }
  };


  // --------------------------------------------------
  // INITIAL FORECAST
  // --------------------------------------------------

  useEffect(() => {

    fetchForecast(city, date);

  }, []);


  // --------------------------------------------------
  // GENERATE FORECAST
  // --------------------------------------------------

  const handleGenerate = (e) => {

    e?.preventDefault();

    fetchForecast(city, date);

  };


  // --------------------------------------------------
  // SAVE FORECAST
  // --------------------------------------------------

  const handleSaveForecast = async () => {

    if (
      !forecast ||
      predictedValue === undefined ||
      predictedValue === null ||
      isSaved ||
      isSaving
    ) {
      return;
    }

    setIsSaving(true);
    setSaveNotice('');

    try {

      await saveForecast({
        city,
        forecastDate: forecast.prediction_for_date || date,
        predictedAqi: Math.round(predictedValue),
        aqiCategory: category.name,
      });

      setIsSaved(true);

      setSaveNotice(
        'Forecast saved to your profile.'
      );

      setTimeout(() => {
        setSaveNotice('');
      }, 3500);

    } catch (err) {

      setSaveNotice(
        err.message || 'Unable to save forecast.'
      );

    } finally {

      setIsSaving(false);

    }
  };


  // --------------------------------------------------
  // DERIVED DATA
  // --------------------------------------------------

  const currentCityInfo =
    ELIGIBLE_CITIES.find(
      (c) => c.name === city
    ) || ELIGIBLE_CITIES[0];

  const predictedValue =
    forecast?.predicted_next_day_aqi;

  const category =
    getAqiCategory(predictedValue);


  // Actual pollutant readings returned by backend
  const pollutants = forecast?.pollutants;


  // --------------------------------------------------
  // PAGE UI
  // --------------------------------------------------

  return (

    <PageContainer>

      {/* --------------------------------------------------
          PAGE TITLE
      -------------------------------------------------- */}

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">

        <div>

          <h1 className="text-xl font-bold font-heading text-[#17231C]">
            Next-Day Air Quality Forecast
          </h1>

          <p className="text-xs text-[#69766E]">
            Select a city and historical base date
            (2015 to 1 July 2020) to generate predictions.
          </p>

        </div>

        <Button
          onClick={handleGenerate}
          variant="primary"
          size="sm"
          isLoading={loading}
          icon={Sparkles}
        >
          Generate Forecast
        </Button>

      </div>


      {/* --------------------------------------------------
          SAVE NOTIFICATION
      -------------------------------------------------- */}

      {saveNotice && (

        <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">

          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />

          <span>{saveNotice}</span>

        </div>

      )}


      {/* --------------------------------------------------
          MAIN GRID
      -------------------------------------------------- */}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">


        {/* --------------------------------------------------
            LEFT COLUMN: INPUT CONTROLS
        -------------------------------------------------- */}

        <div className="lg:col-span-4 space-y-4">


          {/* CITY SELECTOR */}

          <BentoCard
            title="1. Select City"
            icon={Activity}
          >

            <CitySelector
              selectedCity={city}
              onSelectCity={(c) => setCity(c)}
            />

          </BentoCard>


          {/* DATE SELECTOR */}

          <BentoCard
            title="2. Select Base Date"
            icon={Calendar}
          >

            <DateSelector
              selectedDate={date}
              onSelectDate={(d) => setDate(d)}
            />

            <Button
              onClick={handleGenerate}
              variant="lime"
              size="md"
              className="w-full mt-3"
              isLoading={loading}
              icon={Sparkles}
            >
              Generate Forecast
            </Button>

          </BentoCard>

        </div>


        {/* --------------------------------------------------
            RIGHT COLUMN: FORECAST RESULTS
        -------------------------------------------------- */}

        <div className="lg:col-span-8 space-y-4">


          {/* MAIN FORECAST RESULT */}

          <ForecastHeroCard
            city={city}
            prediction={forecast}
            loading={loading}
            error={error}
            onSave={handleSaveForecast}
            isSaved={isSaved}
            isSaving={isSaving}
          />


          {/* --------------------------------------------------
              CPCB CLASSIFICATION AND HISTORICAL CONTEXT
          -------------------------------------------------- */}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">


            {/* CPCB CLASSIFICATION */}

            <BentoCard
              title="CPCB Classification"
              icon={Layers}
            >

              <div className="space-y-3 pt-1">

                <CategoryGauge
                  aqi={predictedValue}
                />

                <div className="text-xs text-[#69766E]">

                  <strong>Guidance:</strong>{' '}
                  {category.advisory}

                </div>

              </div>

            </BentoCard>


            {/* STATION HISTORICAL CONTEXT */}

            <BentoCard
              title="Station Historical Context"
              icon={Activity}
            >

              <div className="space-y-2 pt-1 text-xs text-[#69766E]">

                <div className="flex justify-between py-1 border-b border-[#E3E8E1]">

                  <span>
                    City-level validation MAE:
                  </span>

                  <span className="font-mono font-bold text-[#173D2D]">

                    {currentCityInfo.rfMae.toFixed(1)} AQI points

                  </span>

                </div>


                <div className="flex justify-between py-1 border-b border-[#E3E8E1]">

                  <span>
                    Historical Average:
                  </span>

                  <span className="font-mono text-[#17231C]">

                    {Math.round(currentCityInfo.avgAqi)} AQI

                  </span>

                </div>


                <div className="flex justify-between py-1">

                  <span>
                    Valid Records:
                  </span>

                  <span className="font-mono text-[#17231C]">

                    {currentCityInfo.validDays} days

                  </span>

                </div>

              </div>

            </BentoCard>

          </div>


          {/* --------------------------------------------------
              POLLUTANT BREAKDOWN
              ACTUAL BACKEND VALUES ONLY
          -------------------------------------------------- */}

          <BentoCard
            title="Pollutants on Base Date"
            icon={Wind}
          >

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">


              {/* PM2.5 */}

              <PollutantBar
                name="PM2.5"
                label="PM2.5"
                value={pollutants?.['PM2.5_today'] ?? null}
                unit="µg/m³"
                cpcbStandard={60}
                maxScale={250}
              />


              {/* PM10 */}

              <PollutantBar
                name="PM10"
                label="PM10"
                value={pollutants?.PM10_today ?? null}
                unit="µg/m³"
                cpcbStandard={100}
                maxScale={350}
              />


              {/* NO2 */}

              <PollutantBar
                name="NO2"
                label="NO₂"
                value={pollutants?.NO2_today ?? null}
                unit="µg/m³"
                cpcbStandard={80}
                maxScale={150}
              />


              {/* CO */}

              <PollutantBar
                name="CO"
                label="CO"
                value={pollutants?.CO_today ?? null}
                unit="mg/m³"
                cpcbStandard={2.0}
                maxScale={5.0}
              />


              {/* SO2 */}

              <PollutantBar
                name="SO2"
                label="SO₂"
                value={pollutants?.SO2_today ?? null}
                unit="µg/m³"
                cpcbStandard={80}
                maxScale={100}
              />


              {/* OZONE */}

              <PollutantBar
                name="O3"
                label="Ozone"
                value={pollutants?.O3_today ?? null}
                unit="µg/m³"
                cpcbStandard={100}
                maxScale={180}
              />

            </div>

          </BentoCard>


          {/* --------------------------------------------------
              MODEL ARCHITECTURE DETAILS
          -------------------------------------------------- */}

          <div className="border border-[#E3E8E1] rounded-xl bg-white overflow-hidden text-xs">

            <button
              onClick={() => setShowModelDetails(!showModelDetails)}
              className="w-full px-4 py-2.5 flex items-center justify-between text-left font-medium text-[#69766E] hover:text-[#17231C]"
            >

              <span>
                Model Architecture & Pipeline Details
              </span>

              {showModelDetails ? (

                <ChevronUp className="w-4 h-4" />

              ) : (

                <ChevronDown className="w-4 h-4" />

              )}

            </button>


            {showModelDetails && (

              <div className="p-4 pt-1 border-t border-[#E3E8E1] space-y-2 text-[#69766E]">

                <p>

                  Random Forest Regressor (200 estimators)
                  trained on 17 engineered features:

                  prior lags (t-1, t-2, t-7),
                  rolling averages (3-day and 7-day mean,
                  7-day standard deviation),
                  pollutant concentrations (PM2.5, PM10,
                  NO2, CO, SO2, O3), and cyclical calendar
                  features (month sine/cosine, day of week).

                </p>

                <p>

                  Trained on multi-city CPCB records
                  from 2015 to 2020.

                </p>

              </div>

            )}

          </div>

        </div>

      </div>

    </PageContainer>

  );

}
