import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Wind,
  LineChart,
  GitCompare,
  HeartPulse,
  ArrowRight,
  MapPin,
  Activity,
} from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { BentoCard } from '../components/ui/BentoCard';
import { ForecastHeroCard } from '../components/forecast/ForecastHeroCard';
import { CitySelector } from '../components/forecast/CitySelector';
import { CategoryGauge } from '../components/bento/CategoryGauge';
import { PollutantBar } from '../components/bento/PollutantBar';
import { AQITrendChart } from '../components/charts/AQITrendChart';
import { getCityForecast } from '../services/api';
import { ELIGIBLE_CITIES, MONTHLY_SEASONALITY } from '../utils/datasetInfo';
import { getAqiCategory, formatAqi } from '../utils/aqiUtils';

export function DashboardPage() {
  const [selectedCity, setSelectedCity] = useState('Delhi');
  const [selectedDate, setSelectedDate] = useState('2020-07-01');
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadForecast = async (city, date) => {
    setLoading(true);
    setError(null);

    const result = await getCityForecast(city, date);

    if (result.success && result.data) {
      setForecastData(result.data);
    } else {
      const cityMeta = ELIGIBLE_CITIES.find((c) => c.name.toLowerCase() === city.toLowerCase());
      const fallbackAqi = cityMeta ? cityMeta.avgAqi : 150;

      setForecastData({
        city: city,
        feature_date: date || '2020-07-01',
        prediction_for_date: '2020-07-02',
        observed_aqi_on_feature_date: Math.round(fallbackAqi * 0.95),
        predicted_next_day_aqi: Math.round(fallbackAqi),
        model: 'Random Forest Regressor',
        data_mode: 'historical',
        features: {
          'PM2.5_today': Math.round(fallbackAqi * 0.55),
          PM10_today: Math.round(fallbackAqi * 0.9),
          NO2_today: 42.5,
          CO_today: 1.2,
          SO2_today: 14.8,
          O3_today: 34.0,
        },
      });

      if (result.error && !result.error.includes('400')) {
        setError('FastAPI service offline. Showing CPCB benchmark values.');
      } else if (result.error) {
        setError(result.error);
      }
    }

    setLoading(false);
  };

  useEffect(() => {
    loadForecast(selectedCity, selectedDate);
  }, [selectedCity, selectedDate]);

  const cityInfo = ELIGIBLE_CITIES.find((c) => c.name === selectedCity) || ELIGIBLE_CITIES[0];
  const predictedValue = forecastData?.predicted_next_day_aqi || cityInfo.avgAqi;
  const category = getAqiCategory(predictedValue);

  return (
    <PageContainer>
      {/* City & Quick Action Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold font-heading text-[#17231C]">
            {selectedCity} Air Quality Overview
          </h1>
          <p className="text-xs text-[#69766E]">
            {cityInfo.state} · Historical station average: {Math.round(cityInfo.avgAqi)} AQI
          </p>
        </div>

        <Link to="/forecast">
          <button className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#173D2D] text-white text-xs font-medium hover:bg-[#102C22] transition-colors">
            <Wind className="w-3.5 h-3.5" />
            <span>New Forecast</span>
          </button>
        </Link>
      </div>

      {/* Main Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
        {/* Forecast Hero Card (Col-span 8) */}
        <div className="md:col-span-8 min-w-0">
          <ForecastHeroCard
            city={selectedCity}
            prediction={forecastData}
            loading={loading}
            error={error}
          />
        </div>

        {/* City Selector (Col-span 4) */}
        <BentoCard
          title="Select City"
          icon={MapPin}
          className="md:col-span-4"
        >
          <CitySelector
            selectedCity={selectedCity}
            onSelectCity={(city) => setSelectedCity(city)}
          />
        </BentoCard>

        {/* CPCB Spectrum Gauge (Col-span 4) */}
        <BentoCard
          title="AQI Category Scale"
          icon={Activity}
          className="md:col-span-4"
        >
          <div className="space-y-3 pt-1">
            <CategoryGauge aqi={predictedValue} />
            <div className="p-2.5 rounded-lg bg-[#F7F8F4] border border-[#E3E8E1] text-xs text-[#69766E]">
              {category.advisory}
            </div>
          </div>
        </BentoCard>

        {/* Observed vs Error (Col-span 4) */}
        <BentoCard
          title="Observed & Validation"
          icon={Activity}
          className="md:col-span-4"
        >
          <div className="space-y-3 pt-1">
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-[#F7F8F4] border border-[#E3E8E1]">
              <span className="text-xs text-[#69766E]">Observed Base AQI:</span>
              <span className="text-sm font-bold font-mono text-[#17231C]">
                {formatAqi(forecastData?.observed_aqi_on_feature_date)}
              </span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-[#DDEBE0]/50 border border-[#A8BFA9]/30">
              <span className="text-xs text-[#173D2D]">City Validation Error:</span>
              <span className="text-sm font-bold font-mono text-[#173D2D]">
                ±{cityInfo.rfMae.toFixed(1)} MAE
              </span>
            </div>
          </div>
        </BentoCard>

        {/* Model Specs (Col-span 4) */}
        <BentoCard
          title="Model Info"
          icon={Wind}
          className="md:col-span-4"
        >
          <div className="space-y-2 pt-1 text-xs text-[#69766E]">
            <div className="flex justify-between py-1 border-b border-[#E3E8E1]">
              <span>Algorithm:</span>
              <span className="font-medium text-[#17231C]">Random Forest</span>
            </div>
            <div className="flex justify-between py-1 border-b border-[#E3E8E1]">
              <span>Features:</span>
              <span className="font-mono text-[#17231C]">17 inputs</span>
            </div>
            <div className="flex justify-between py-1">
              <span>Date Scope:</span>
              <span className="text-[#17231C]">2015 – July 2020</span>
            </div>
          </div>
        </BentoCard>

        {/* Monthly Trend (Col-span 7) */}
        <BentoCard
          title="Monthly Trend Profile"
          icon={LineChart}
          className="md:col-span-7"
          action={
            <Link to="/analytics" className="text-xs text-[#173D2D] hover:underline flex items-center gap-0.5 font-medium">
              Details <ArrowRight className="w-3 h-3" />
            </Link>
          }
        >
          <div className="pt-2">
            <AQITrendChart
              data={MONTHLY_SEASONALITY}
              dataKey={MONTHLY_SEASONALITY[0][selectedCity] !== undefined ? selectedCity : 'allAvg'}
              city={selectedCity}
              height={200}
            />
          </div>
        </BentoCard>

        {/* Pollutants (Col-span 5) */}
        <BentoCard
          title="Pollutant Concentrations"
          icon={Wind}
          className="md:col-span-5"
        >
          <div className="space-y-2 pt-1">
            <PollutantBar
              name="PM2.5"
              label="PM2.5"
              value={forecastData?.features?.['PM2.5_today'] || 85}
              unit="µg/m³"
              cpcbStandard={60}
              maxScale={250}
            />
            <PollutantBar
              name="PM10"
              label="PM10"
              value={forecastData?.features?.PM10_today || 140}
              unit="µg/m³"
              cpcbStandard={100}
              maxScale={350}
            />
            <PollutantBar
              name="NO2"
              label="NO₂"
              value={forecastData?.features?.NO2_today || 38.5}
              unit="µg/m³"
              cpcbStandard={80}
              maxScale={150}
            />
          </div>
        </BentoCard>

        {/* Quick Nav Links (Col-span 12) */}
        <div className="md:col-span-12 grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
          <Link
            to="/forecast"
            className="p-3.5 rounded-xl bg-white border border-[#E3E8E1] hover:border-[#173D2D] transition-colors flex items-center justify-between"
          >
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#DDEBE0] text-[#173D2D] flex items-center justify-center">
                <Wind className="w-4 h-4" />
              </div>
              <div>
                <div className="text-xs font-bold text-[#17231C]">Forecast by Date</div>
                <div className="text-[11px] text-[#69766E]">Predict next-day AQI</div>
              </div>
            </div>
            <ArrowRight className="w-3.5 h-3.5 text-[#69766E]" />
          </Link>

          <Link
            to="/comparison"
            className="p-3.5 rounded-xl bg-white border border-[#E3E8E1] hover:border-[#173D2D] transition-colors flex items-center justify-between"
          >
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#DDEBE0] text-[#173D2D] flex items-center justify-center">
                <GitCompare className="w-4 h-4" />
              </div>
              <div>
                <div className="text-xs font-bold text-[#17231C]">Compare Cities</div>
                <div className="text-[11px] text-[#69766E]">Side-by-side contrast</div>
              </div>
            </div>
            <ArrowRight className="w-3.5 h-3.5 text-[#69766E]" />
          </Link>

          <Link
            to="/health-advisor"
            className="p-3.5 rounded-xl bg-white border border-[#E3E8E1] hover:border-[#173D2D] transition-colors flex items-center justify-between"
          >
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#DDEBE0] text-[#173D2D] flex items-center justify-center">
                <HeartPulse className="w-4 h-4" />
              </div>
              <div>
                <div className="text-xs font-bold text-[#17231C]">Health Guidance</div>
                <div className="text-[11px] text-[#69766E]">Advisories & masks</div>
              </div>
            </div>
            <ArrowRight className="w-3.5 h-3.5 text-[#69766E]" />
          </Link>
        </div>
      </div>
    </PageContainer>
  );
}
