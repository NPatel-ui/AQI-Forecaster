import { useState } from 'react';
import { GitCompare } from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { BentoCard } from '../components/ui/BentoCard';
import { AqiBadge } from '../components/ui/Badge';
import { ComparisonLineChart } from '../components/charts/ComparisonLineChart';
import { ELIGIBLE_CITIES, MONTHLY_SEASONALITY } from '../utils/datasetInfo';
import { getAqiCategory } from '../utils/aqiUtils';

export function ComparisonPage() {
  const [cityA, setCityA] = useState('Delhi');
  const [cityB, setCityB] = useState('Mumbai');

  const metaA = ELIGIBLE_CITIES.find((c) => c.name === cityA) || ELIGIBLE_CITIES[0];
  const metaB = ELIGIBLE_CITIES.find((c) => c.name === cityB) || ELIGIBLE_CITIES[1];

  const diffAqi = metaA.avgAqi - metaB.avgAqi;
  const diffMae = metaA.rfMae - metaB.rfMae;

  return (
    <PageContainer>
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold font-heading text-[#17231C]">
          City Air Quality Comparison
        </h1>
        <p className="text-xs text-[#69766E] mt-0.5">
          Compare multi-year historical averages, model precision, and monthly seasonality between two cities.
        </p>
      </div>

      {/* Selectors Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3.5 rounded-xl bg-white border border-[#E3E8E1]">
        <div className="space-y-1">
          <label className="block text-xs font-semibold text-[#173D2D]">
            City A (Focus)
          </label>
          <select
            value={cityA}
            onChange={(e) => setCityA(e.target.value)}
            className="w-full px-3 py-1.5 text-xs sm:text-sm rounded-lg border border-[#E3E8E1] bg-[#F7F8F4] text-[#17231C] font-medium focus:outline-none focus:ring-1 focus:ring-[#173D2D]"
          >
            {ELIGIBLE_CITIES.map((c) => (
              <option key={c.name} value={c.name} disabled={c.name === cityB}>
                {c.name} ({c.state})
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-1">
          <label className="block text-xs font-semibold text-emerald-800">
            City B (Benchmark)
          </label>
          <select
            value={cityB}
            onChange={(e) => setCityB(e.target.value)}
            className="w-full px-3 py-1.5 text-xs sm:text-sm rounded-lg border border-[#E3E8E1] bg-[#F7F8F4] text-[#17231C] font-medium focus:outline-none focus:ring-1 focus:ring-[#173D2D]"
          >
            {ELIGIBLE_CITIES.map((c) => (
              <option key={c.name} value={c.name} disabled={c.name === cityA}>
                {c.name} ({c.state})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* 2-Column City Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* City A */}
        <div className="p-5 rounded-2xl bg-white border border-[#173D2D] space-y-4">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h2 className="text-xl font-bold font-heading text-[#17231C]">
                {cityA}
              </h2>
              <div className="text-xs text-[#69766E]">{metaA.state}</div>
            </div>
            <AqiBadge aqi={metaA.avgAqi} />
          </div>

          <div className="grid grid-cols-2 gap-2.5">
            <div className="p-3 rounded-xl bg-[#F7F8F4] border border-[#E3E8E1]">
              <span className="text-[11px] text-[#69766E] block">Historical Average</span>
              <span className="text-xl font-bold font-heading text-[#17231C]">
                {Math.round(metaA.avgAqi)} AQI
              </span>
            </div>
            <div className="p-3 rounded-xl bg-[#DDEBE0]/40 border border-[#A8BFA9]/30">
              <span className="text-[11px] text-[#173D2D] block">Model Error</span>
              <span className="text-xl font-bold font-mono text-[#173D2D]">
                ±{metaA.rfMae.toFixed(1)} MAE
              </span>
            </div>
          </div>

          <div className="text-xs text-[#69766E] pt-1">
            <span>Validated reporting days: </span>
            <strong className="text-[#17231C] font-mono">{metaA.validDays}</strong>
          </div>
        </div>

        {/* City B */}
        <div className="p-5 rounded-2xl bg-white border border-[#10B981] space-y-4">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h2 className="text-xl font-bold font-heading text-[#17231C]">
                {cityB}
              </h2>
              <div className="text-xs text-[#69766E]">{metaB.state}</div>
            </div>
            <AqiBadge aqi={metaB.avgAqi} />
          </div>

          <div className="grid grid-cols-2 gap-2.5">
            <div className="p-3 rounded-xl bg-[#F7F8F4] border border-[#E3E8E1]">
              <span className="text-[11px] text-[#69766E] block">Historical Average</span>
              <span className="text-xl font-bold font-heading text-[#17231C]">
                {Math.round(metaB.avgAqi)} AQI
              </span>
            </div>
            <div className="p-3 rounded-xl bg-[#ECFDF5] border border-[#A7F3D0]">
              <span className="text-[11px] text-[#065F46] block">Model Error</span>
              <span className="text-xl font-bold font-mono text-[#065F46]">
                ±{metaB.rfMae.toFixed(1)} MAE
              </span>
            </div>
          </div>

          <div className="text-xs text-[#69766E] pt-1">
            <span>Validated reporting days: </span>
            <strong className="text-[#17231C] font-mono">{metaB.validDays}</strong>
          </div>
        </div>
      </div>

      {/* Concise Summary Banner */}
      <div className="p-4 rounded-xl bg-[#102C22] text-white flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <GitCompare className="w-4 h-4 text-[#B7E46A] shrink-0" />
          <span>
            {diffAqi > 0
              ? `${cityA} averages ${Math.round(diffAqi)} AQI points higher than ${cityB}.`
              : `${cityB} averages ${Math.round(Math.abs(diffAqi))} AQI points higher than ${cityA}.`}
          </span>
        </div>
        <div className="text-[#A8BFA9]">
          {diffMae < 0
            ? `Higher model precision on ${cityA} (MAE ${metaA.rfMae.toFixed(1)} vs ${metaB.rfMae.toFixed(1)}).`
            : `Higher model precision on ${cityB} (MAE ${metaB.rfMae.toFixed(1)} vs ${metaA.rfMae.toFixed(1)}).`}
        </div>
      </div>

      {/* Seasonality Comparison Chart */}
      <BentoCard
        title="Monthly Seasonality Comparison"
        icon={GitCompare}
      >
        <div className="pt-2">
          <ComparisonLineChart
            data={MONTHLY_SEASONALITY}
            cityA={MONTHLY_SEASONALITY[0][cityA] !== undefined ? cityA : 'Delhi'}
            cityB={MONTHLY_SEASONALITY[0][cityB] !== undefined ? cityB : 'Mumbai'}
            height={260}
          />
        </div>
      </BentoCard>
    </PageContainer>
  );
}
