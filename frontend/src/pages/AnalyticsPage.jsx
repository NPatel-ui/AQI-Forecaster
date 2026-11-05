
import { useEffect, useState } from 'react';

import {
  Calendar,
  Database,
  BarChart2,
  PieChart as PieIcon,
  Layers,
} from 'lucide-react';

import { PageContainer } from '../components/layout/PageContainer';
import { BentoCard } from '../components/ui/BentoCard';
import { StatCard } from '../components/ui/StatCard';

import { AQITrendChart } from '../components/charts/AQITrendChart';
import { CategoryPieChart } from '../components/charts/CategoryPieChart';
import { CityBarChart } from '../components/charts/CityBarChart';

import {
  MONTHLY_SEASONALITY,
  YEARLY_TRENDS,
  CATEGORY_DISTRIBUTION,
  POLLUTANT_CORRELATIONS,
  ELIGIBLE_CITIES,
} from '../utils/datasetInfo';

import { getModelBenchmarks } from '../services/api';

export function AnalyticsPage() {
  const [selectedMetro, setSelectedMetro] = useState('Delhi');

  // Model benchmark state
  const [benchmarkData, setBenchmarkData] = useState(null);
  const [benchmarkLoading, setBenchmarkLoading] = useState(true);
  const [benchmarkError, setBenchmarkError] = useState(null);

  // Fetch model benchmarks from FastAPI
  useEffect(() => {
    let active = true;

    async function loadBenchmarks() {
      const result = await getModelBenchmarks();

      if (!active) return;

      if (result.success) {
        setBenchmarkData(result.data.benchmarks);
        setBenchmarkError(null);
      } else {
        setBenchmarkError(result.error);
      }

      setBenchmarkLoading(false);
    }

    loadBenchmarks();

    return () => {
      active = false;
    };
  }, []);

  const topPolluted = [...ELIGIBLE_CITIES].sort(
    (a, b) => b.avgAqi - a.avgAqi
  );

  return (
    <PageContainer>
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold font-heading text-[#17231C]">
          Historical Air Quality Analytics
        </h1>

        <p className="text-xs text-[#69766E] mt-0.5">
          Based on 29,531 daily records across 18 Indian cities (2015–2020).
        </p>
      </div>

      {/* 4 Key Statistics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <StatCard
          title="Monsoon Average"
          value="70.6"
          unit="AQI"
          description="Lowest month (August)"
        />

        <StatCard
          title="Winter Average"
          value="193.0"
          unit="AQI"
          description="Highest month (December)"
        />

        <StatCard
          title="PM2.5 Correlation"
          value="0.88"
          unit="r"
          description="Highest sub-index driver"
        />

        <StatCard
          title="Top Accuracy"
          value="9.91"
          unit="MAE"
          description="Thiruvananthapuram"
        />
      </div>

      {/* Row 1: Monthly Curve & Category Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">

        {/* Monthly Trend */}
        <BentoCard
          title="Monthly Seasonality"
          icon={Calendar}
          className="lg:col-span-8"
          action={
            <div className="flex items-center gap-1">
              {['Delhi', 'Mumbai', 'Bengaluru', 'Kolkata'].map((city) => (
                <button
                  key={city}
                  onClick={() => setSelectedMetro(city)}
                  className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                    selectedMetro === city
                      ? 'bg-[#173D2D] text-[#B7E46A]'
                      : 'bg-[#F7F8F4] text-[#69766E] hover:text-[#17231C]'
                  }`}
                >
                  {city}
                </button>
              ))}
            </div>
          }
        >
          <div className="pt-2">
            <AQITrendChart
              data={MONTHLY_SEASONALITY}
              dataKey={selectedMetro}
              city={selectedMetro}
              height={230}
            />
          </div>
        </BentoCard>

        {/* Category Breakdown */}
        <BentoCard
          title="Category Distribution"
          icon={PieIcon}
          className="lg:col-span-4"
        >
          <div className="flex flex-col items-center">
            <CategoryPieChart height={160} />

            <div className="grid grid-cols-2 gap-x-3 gap-y-1 w-full pt-2 text-[11px] text-[#69766E] border-t border-[#E3E8E1]">
              {CATEGORY_DISTRIBUTION.map((item) => (
                <div
                  key={item.name}
                  className="flex items-center justify-between"
                >
                  <span className="flex items-center gap-1 truncate">
                    <span
                      className="w-1.5 h-1.5 rounded-full shrink-0"
                      style={{ backgroundColor: item.color }}
                    />

                    <span className="truncate">
                      {item.name.split(' ')[0]}
                    </span>
                  </span>

                  <span className="font-semibold text-[#17231C] font-mono">
                    {item.value}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </BentoCard>
      </div>

      {/* Row 2: Top Polluted Cities & Yearly Evolution */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">

        {/* Top Cities Bar Chart */}
        <BentoCard
          title="Highest Average AQI Cities"
          icon={BarChart2}
          className="lg:col-span-7"
        >
          <div className="pt-1">
            <CityBarChart data={topPolluted} height={220} />
          </div>
        </BentoCard>

        {/* Yearly Evolution */}
        <BentoCard
          title="Yearly Averages (2015–2020)"
          icon={Database}
          className="lg:col-span-5"
        >
          <div className="space-y-1.5 pt-1 text-xs">
            {YEARLY_TRENDS.map((y) => (
              <div
                key={y.year}
                className="p-2 rounded-lg bg-[#F7F8F4] border border-[#E3E8E1] flex items-center justify-between"
              >
                <div>
                  <span className="font-semibold text-[#17231C]">
                    {y.year}
                  </span>

                  <span className="text-[10px] text-[#69766E] ml-2">
                    {y.coverage}
                  </span>
                </div>

                <div className="font-mono font-bold text-[#173D2D]">
                  {y.avgAqi} AQI
                </div>
              </div>
            ))}
          </div>
        </BentoCard>
      </div>

      {/* Row 3: Pollutant Correlations & Model Benchmarks */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">

        {/* Pollutant Correlation Card */}
        <BentoCard
          title="Pollutant Correlation with AQI"
          icon={Layers}
          className="lg:col-span-6"
        >
          <div className="space-y-2 pt-1 text-xs">
            {POLLUTANT_CORRELATIONS.map((p) => (
              <div
                key={p.pollutant}
                className="p-2.5 rounded-lg bg-[#F7F8F4] border border-[#E3E8E1] flex items-center justify-between gap-3"
              >
                <div>
                  <span className="font-bold text-[#17231C]">
                    {p.pollutant}
                  </span>

                  <span className="text-[11px] text-[#69766E] ml-2">
                    {p.peakSeason}
                  </span>
                </div>

                <div className="font-mono font-bold text-[#173D2D]">
                  r = +{p.rAqi}
                </div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Model Benchmarks */}
        <BentoCard
          title="Model Benchmarks"
          icon={Database}
          className="lg:col-span-6"
        >
          {benchmarkLoading ? (
            <p className="text-xs text-[#69766E] py-4">
              Loading model benchmarks...
            </p>
          ) : benchmarkError ? (
            <p className="text-xs text-red-600 py-4">
              Unable to load benchmarks: {benchmarkError}
            </p>
          ) : (
            <div className="space-y-4 pt-1 text-xs">
              {Object.entries(benchmarkData || {}).map(([key, result]) => (
                <div
                  key={key}
                  className="rounded-lg border border-[#E3E8E1] overflow-hidden"
                >
                  <div className="p-3 bg-[#F7F8F4]">
                    <div className="font-bold text-[#17231C]">
                      {result.split}
                    </div>

                    <div className="text-[11px] text-[#69766E] mt-1">
                      {result.evaluation_rows.toLocaleString()} records
                      {' · '}
                      {result.cities} cities
                    </div>
                  </div>

                  <div className="p-3 space-y-3">
                    {[
                      {
                        name: 'Random Forest',
                        metrics: result.random_forest,
                      },
                      {
                        name: 'Persistence Baseline',
                        metrics: result.persistence_baseline,
                      },
                    ].map((item, index) => (
                      <div key={item.name}>
                        <div className="flex justify-between items-center gap-2">
                          <span className="font-semibold text-[#17231C]">
                            {item.name}
                          </span>

                          <span className="font-mono font-bold text-[#173D2D]">
                            MAE: {item.metrics.mae.toFixed(2)}
                          </span>
                        </div>

                        <div className="text-[11px] text-[#69766E] mt-1">
                          RMSE: {item.metrics.rmse.toFixed(2)}
                          {' · '}
                          R²: {item.metrics.r2.toFixed(4)}
                        </div>

                        {index === 0 && (
                          <div className="border-b border-[#E3E8E1] mt-3" />
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </BentoCard>
      </div>
    </PageContainer>
  );
}
