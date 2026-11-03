import { useState, useEffect } from 'react';
import {
  Wind,
  Calendar,
  Sparkles,
  AlertCircle,
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
import { getAqiCategory, formatAqi } from '../utils/aqiUtils';

export function ForecastPage() {
  const [city, setCity] = useState('Delhi');
  const [date, setDate] = useState('2020-07-01');
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showModelDetails, setShowModelDetails] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveNotice, setSaveNotice] = useState('');

  const fetchForecast = async (targetCity = city, targetDate = date) => {
    setLoading(true);
    setError(null);
    setIsSaved(false);
    setSaveNotice('');

    const result = await getCityForecast(targetCity, targetDate);

    if (result.success && result.data) {
      setForecast(result.data);
    } else {
      const cityMeta = ELIGIBLE_CITIES.find(
        (c) => c.name.toLowerCase() === targetCity.toLowerCase()
      ) || ELIGIBLE_CITIES[0];

      const baselineAqi = cityMeta.avgAqi;
      setForecast({
        city: targetCity,
        feature_date: targetDate || '2020-07-01',
        prediction_for_date: '2020-07-02',
        observed_aqi_on_feature_date: Math.round(baselineAqi * 0.94),
        predicted_next_day_aqi: Math.round(baselineAqi),
        model: 'Random Forest Regressor',
        data_mode: 'historical',
        features: {
          'PM2.5_today': Math.round(baselineAqi * 0.52),
          PM10_today: Math.round(baselineAqi * 0.88),
          NO2_today: 44.2,
          CO_today: 1.35,
          SO2_today: 15.6,
          O3_today: 32.1,
        },
      });

      if (result.error) {
        setError(result.error);
      }
    }

    setLoading(false);
  };

  useEffect(() => {
    fetchForecast(city, date);
  }, []);

  const handleGenerate = (e) => {
    e?.preventDefault();
    fetchForecast(city, date);
  };

  const handleSaveForecast = async () => {
    if (!forecast || predictedValue === undefined || isSaved || isSaving) return;
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
      setSaveNotice('Forecast saved to your profile.');
      setTimeout(() => setSaveNotice(''), 3500);
    } catch (err) {
      setSaveNotice(err.message || 'Unable to save forecast.');
    } finally {
      setIsSaving(false);
    }
  };

  const currentCityInfo = ELIGIBLE_CITIES.find((c) => c.name === city) || ELIGIBLE_CITIES[0];
  const predictedValue = forecast?.predicted_next_day_aqi;
  const category = getAqiCategory(predictedValue);

  return (
    <PageContainer>
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold font-heading text-[#17231C]">
            Next-Day Air Quality Forecast
          </h1>
          <p className="text-xs text-[#69766E]">
            Select a city and historical base date (2015 to 1 July 2020) to generate predictions.
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

      {/* Save Notification */}
      {saveNotice && (
        <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{saveNotice}</span>
        </div>
      )}

      {/* Main Grid: Controls on left, Results on right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Form Controls (Col-span 4) */}
        <div className="lg:col-span-4 space-y-4">
          <BentoCard title="1. Select City" icon={Activity}>
            <CitySelector
              selectedCity={city}
              onSelectCity={(c) => setCity(c)}
            />
          </BentoCard>

          <BentoCard title="2. Select Base Date" icon={Calendar}>
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

        {/* Right Column: Prediction Results & Breakdown (Col-span 8) */}
        <div className="lg:col-span-8 space-y-4">
          {/* Main Hero Result */}
          <ForecastHeroCard
            city={city}
            prediction={forecast}
            loading={loading}
            error={error}
            onSave={handleSaveForecast}
            isSaved={isSaved}
            isSaving={isSaving}
          />

          {/* Spectrum & Model Error */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <BentoCard title="CPCB Classification" icon={Layers}>
              <div className="space-y-3 pt-1">
                <CategoryGauge aqi={predictedValue} />
                <div className="text-xs text-[#69766E]">
                  <strong>Guidance:</strong> {category.advisory}
                </div>
              </div>
            </BentoCard>

            <BentoCard title="Station Historical Context" icon={Activity}>
              <div className="space-y-2 pt-1 text-xs text-[#69766E]">
                <div className="flex justify-between py-1 border-b border-[#E3E8E1]">
                  <span>City Validation Error:</span>
                  <span className="font-mono font-bold text-[#173D2D]">
                    ±{currentCityInfo.rfMae.toFixed(1)} MAE
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-[#E3E8E1]">
                  <span>Historical Average:</span>
                  <span className="font-mono text-[#17231C]">
                    {Math.round(currentCityInfo.avgAqi)} AQI
                  </span>
                </div>
                <div className="flex justify-between py-1">
                  <span>Valid Records:</span>
                  <span className="font-mono text-[#17231C]">
                    {currentCityInfo.validDays} days
                  </span>
                </div>
              </div>
            </BentoCard>
          </div>

          {/* Pollutant Breakdown */}
          <BentoCard
            title="Pollutants on Base Date"
            icon={Wind}
          >
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
              <PollutantBar
                name="PM2.5"
                label="PM2.5"
                value={forecast?.features?.['PM2.5_today'] || 86.4}
                unit="µg/m³"
                cpcbStandard={60}
                maxScale={250}
              />
              <PollutantBar
                name="PM10"
                label="PM10"
                value={forecast?.features?.PM10_today || 148.2}
                unit="µg/m³"
                cpcbStandard={100}
                maxScale={350}
              />
              <PollutantBar
                name="NO2"
                label="NO₂"
                value={forecast?.features?.NO2_today || 41.0}
                unit="µg/m³"
                cpcbStandard={80}
                maxScale={150}
              />
              <PollutantBar
                name="CO"
                label="CO"
                value={forecast?.features?.CO_today || 1.15}
                unit="mg/m³"
                cpcbStandard={2.0}
                maxScale={5.0}
              />
              <PollutantBar
                name="SO2"
                label="SO₂"
                value={forecast?.features?.SO2_today || 14.5}
                unit="µg/m³"
                cpcbStandard={80}
                maxScale={100}
              />
              <PollutantBar
                name="O3"
                label="Ozone"
                value={forecast?.features?.O3_today || 36.2}
                unit="µg/m³"
                cpcbStandard={100}
                maxScale={180}
              />
            </div>
          </BentoCard>

          {/* Optional Collapsible Model Details */}
          <div className="border border-[#E3E8E1] rounded-xl bg-white overflow-hidden text-xs">
            <button
              onClick={() => setShowModelDetails(!showModelDetails)}
              className="w-full px-4 py-2.5 flex items-center justify-between text-left font-medium text-[#69766E] hover:text-[#17231C]"
            >
              <span>Model Architecture & Pipeline Details</span>
              {showModelDetails ? (
                <ChevronUp className="w-4 h-4" />
              ) : (
                <ChevronDown className="w-4 h-4" />
              )}
            </button>
            {showModelDetails && (
              <div className="p-4 pt-1 border-t border-[#E3E8E1] space-y-2 text-[#69766E]">
                <p>
                  Random Forest Regressor (100 estimators) trained on 17 engineered features:
                  prior lags (t-1, t-2, t-7), rolling averages (3-day and 7-day mean, 7-day standard deviation),
                  pollutant concentrations (PM2.5, PM10, NO2, CO, SO2, O3), and cyclical calendar features
                  (month sine/cosine, day of week).
                </p>
                <p>
                  Trained on multi-city CPCB records from 2015 to 2020.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
