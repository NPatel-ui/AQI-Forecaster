/**
 * CPCB Air Quality Dataset Reference Information
 * Based on Central Pollution Control Board (CPCB) India historical records (2015-01-01 to 2020-07-01)
 */

export const ELIGIBLE_CITIES = [
  { name: 'Ahmedabad', state: 'Gujarat', region: 'West', validDays: 1334, minDate: '2015-01-01', maxDate: '2020-07-01', avgAqi: 243.6, rfMae: 243.56 },
  { name: 'Amaravati', state: 'Andhra Pradesh', region: 'South', validDays: 841, minDate: '2017-11-24', maxDate: '2020-07-01', avgAqi: 95.2, rfMae: 15.80 },
  { name: 'Amritsar', state: 'Punjab', region: 'North', validDays: 1126, minDate: '2017-02-27', maxDate: '2020-07-01', avgAqi: 153.8, rfMae: 22.69 },
  { name: 'Bengaluru', state: 'Karnataka', region: 'South', validDays: 1910, minDate: '2015-01-01', maxDate: '2020-07-01', avgAqi: 104.5, rfMae: 25.51 },
  { name: 'Brajrajnagar', state: 'Odisha', region: 'East', validDays: 713, minDate: '2017-12-07', maxDate: '2020-07-01', avgAqi: 150.2, rfMae: 19.11 },
  { name: 'Chennai', state: 'Tamil Nadu', region: 'South', validDays: 1884, minDate: '2015-01-01', maxDate: '2020-07-01', avgAqi: 114.5, rfMae: 21.40 },
  { name: 'Delhi', state: 'Delhi NCR', region: 'North', validDays: 1999, minDate: '2015-01-01', maxDate: '2020-07-01', avgAqi: 259.5, rfMae: 39.09 },
  { name: 'Gurugram', state: 'Haryana', region: 'North', validDays: 1453, minDate: '2015-11-27', maxDate: '2020-07-01', avgAqi: 225.1, rfMae: 37.94 },
  { name: 'Hyderabad', state: 'Telangana', region: 'South', validDays: 1880, minDate: '2015-01-04', maxDate: '2020-07-01', avgAqi: 109.2, rfMae: 24.30 },
  { name: 'Jaipur', state: 'Rajasthan', region: 'North', validDays: 1094, minDate: '2017-06-14', maxDate: '2020-07-01', avgAqi: 133.7, rfMae: 20.01 },
  { name: 'Jorapokhar', state: 'Jharkhand', region: 'East', validDays: 771, minDate: '2017-04-20', maxDate: '2020-07-01', avgAqi: 159.2, rfMae: 25.25 },
  { name: 'Kolkata', state: 'West Bengal', region: 'East', validDays: 754, minDate: '2018-04-10', maxDate: '2020-07-01', avgAqi: 140.6, rfMae: 28.15 },
  { name: 'Lucknow', state: 'Uttar Pradesh', region: 'North', validDays: 1893, minDate: '2015-01-01', maxDate: '2020-07-01', avgAqi: 217.9, rfMae: 34.60 },
  { name: 'Mumbai', state: 'Maharashtra', region: 'West', validDays: 775, minDate: '2015-01-01', maxDate: '2020-07-01', avgAqi: 105.4, rfMae: 13.44 },
  { name: 'Patna', state: 'Bihar', region: 'East', validDays: 1459, minDate: '2015-06-01', maxDate: '2020-07-01', avgAqi: 240.8, rfMae: 27.84 },
  { name: 'Talcher', state: 'Odisha', region: 'East', validDays: 698, minDate: '2017-12-20', maxDate: '2020-07-01', avgAqi: 172.9, rfMae: 24.69 },
  { name: 'Thiruvananthapuram', state: 'Kerala', region: 'South', validDays: 1052, minDate: '2017-06-16', maxDate: '2020-07-01', avgAqi: 75.8, rfMae: 9.91 },
  { name: 'Visakhapatnam', state: 'Andhra Pradesh', region: 'South', validDays: 1171, minDate: '2016-07-01', maxDate: '2020-07-01', avgAqi: 117.3, rfMae: 23.50 },
];

export const MODEL_BENCHMARKS = [
  {
    model: 'Random Forest Regressor (Final)',
    meanCvMae: 44.68,
    stdCvMae: 35.71,
    bestCity: 'Thiruvananthapuram (MAE 9.91)',
    status: 'Production Deployment',
    trees: 100,
    features: 17,
  },
  {
    model: 'HistGradientBoosting Regressor',
    meanCvMae: 42.96,
    stdCvMae: 31.82,
    bestCity: 'Thiruvananthapuram (MAE 11.23)',
    status: 'Evaluated Benchmark',
    trees: 100,
    features: 17,
  },
  {
    model: 'Ridge Regression (L2)',
    meanCvMae: 40.55,
    stdCvMae: 18.64,
    bestCity: 'Thiruvananthapuram (MAE 12.02)',
    status: 'Linear Baseline',
    trees: null,
    features: 17,
  },
  {
    model: 'Persistence Baseline (AQI(t-1))',
    meanCvMae: 39.07,
    stdCvMae: 19.44,
    bestCity: 'Thiruvananthapuram (MAE 11.29)',
    status: 'Naïve Benchmark',
    trees: null,
    features: 1,
  },
];

export const MONTHLY_SEASONALITY = [
  { month: 'Jan', Delhi: 345, Mumbai: 145, Bengaluru: 118, Kolkata: 220, Chennai: 125, allAvg: 190.6 },
  { month: 'Feb', Delhi: 290, Mumbai: 138, Bengaluru: 112, Kolkata: 185, Chennai: 112, allAvg: 167.4 },
  { month: 'Mar', Delhi: 220, Mumbai: 115, Bengaluru: 108, Kolkata: 135, Chennai: 98, allAvg: 135.2 },
  { month: 'Apr', Delhi: 245, Mumbai: 95, Bengaluru: 95, Kolkata: 110, Chennai: 90, allAvg: 127.0 },
  { month: 'May', Delhi: 260, Mumbai: 88, Bengaluru: 88, Kolkata: 92, Chennai: 102, allAvg: 126.0 },
  { month: 'Jun', Delhi: 185, Mumbai: 65, Bengaluru: 72, Kolkata: 75, Chennai: 92, allAvg: 97.8 },
  { month: 'Jul', Delhi: 115, Mumbai: 52, Bengaluru: 62, Kolkata: 60, Chennai: 85, allAvg: 74.8 },
  { month: 'Aug', Delhi: 105, Mumbai: 48, Bengaluru: 60, Kolkata: 58, Chennai: 82, allAvg: 70.6 },
  { month: 'Sep', Delhi: 112, Mumbai: 55, Bengaluru: 68, Kolkata: 68, Chennai: 88, allAvg: 78.2 },
  { month: 'Oct', Delhi: 265, Mumbai: 92, Bengaluru: 82, Kolkata: 118, Chennai: 94, allAvg: 130.2 },
  { month: 'Nov', Delhi: 375, Mumbai: 132, Bengaluru: 95, Kolkata: 195, Chennai: 110, allAvg: 181.4 },
  { month: 'Dec', Delhi: 360, Mumbai: 142, Bengaluru: 105, Kolkata: 230, Chennai: 128, allAvg: 193.0 },
];

export const YEARLY_TRENDS = [
  { year: '2015', avgAqi: 182, records: 3410, coverage: '7 Cities' },
  { year: '2016', avgAqi: 178, records: 4520, coverage: '10 Cities' },
  { year: '2017', avgAqi: 169, records: 5810, coverage: '15 Cities' },
  { year: '2018', avgAqi: 164, records: 6420, coverage: '18 Cities' },
  { year: '2019', avgAqi: 158, records: 6570, coverage: '18 Cities' },
  { year: '2020', avgAqi: 122, records: 2801, coverage: '18 Cities (Lockdown window to July)' },
];

export const CATEGORY_DISTRIBUTION = [
  { name: 'Good (0-50)', value: 16.2, count: 4210, color: '#10B981' },
  { name: 'Satisfactory (51-100)', value: 31.8, count: 8270, color: '#22C55E' },
  { name: 'Moderate (101-200)', value: 29.4, count: 7640, color: '#F59E0B' },
  { name: 'Poor (201-300)', value: 12.1, count: 3150, color: '#F97316' },
  { name: 'Very Poor (301-400)', value: 7.3, count: 1898, color: '#EF4444' },
  { name: 'Severe (>400)', value: 3.2, count: 832, color: '#881337' },
];

export const POLLUTANT_CORRELATIONS = [
  { pollutant: 'PM2.5', rAqi: 0.88, impact: 'Dominant driver of National AQI formula', peakSeason: 'Winter (Nov-Jan)' },
  { pollutant: 'PM10', rAqi: 0.82, impact: 'Strong secondary particulate indicator', peakSeason: 'Pre-monsoon / Winter' },
  { pollutant: 'NO2', rAqi: 0.54, impact: 'Correlated with vehicular & urban traffic', peakSeason: 'Winter evenings' },
  { pollutant: 'CO', rAqi: 0.49, impact: 'Combustion signature & incomplete burning', peakSeason: 'Winter mornings' },
  { pollutant: 'SO2', rAqi: 0.31, impact: 'Industrial & power generation marker', peakSeason: 'Year-round industrial' },
  { pollutant: 'O3', rAqi: 0.22, impact: 'Photochemical smog & daytime summer spikes', peakSeason: 'Summer afternoons' },
];

