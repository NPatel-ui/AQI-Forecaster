import { Link } from 'react-router-dom';
import { Activity } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-[#102C22] text-[#DDEBE0] border-t border-[#173D2D] py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-8 border-b border-[#173D2D]">
          {/* Brand */}
          <div className="space-y-2">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-[#B7E46A] text-[#102C22] flex items-center justify-center font-bold">
                <Activity className="w-4 h-4 text-[#102C22]" />
              </div>
              <span className="font-heading font-bold text-base text-white">
                AQI Forecaster
              </span>
            </div>
            <p className="text-xs text-[#A8BFA9] leading-relaxed">
              Air quality forecasting and historical analytics for 18 major Indian cities.
            </p>
          </div>

          {/* Navigation */}
          <div className="space-y-2.5 text-xs">
            <div className="font-semibold text-white">Platform</div>
            <ul className="space-y-1.5 text-[#A8BFA9]">
              <li><Link to="/forecast" className="hover:text-white">Forecasting</Link></li>
              <li><Link to="/analytics" className="hover:text-white">Historical Trends</Link></li>
              <li><Link to="/comparison" className="hover:text-white">City Comparison</Link></li>
              <li><Link to="/health-advisor" className="hover:text-white">Health Guidance</Link></li>
            </ul>
          </div>

          {/* Dataset Info */}
          <div className="space-y-2.5 text-xs">
            <div className="font-semibold text-white">Data Scope</div>
            <ul className="space-y-1.5 text-[#A8BFA9]">
              <li>Source: CPCB National Records</li>
              <li>Period: 2015 – July 2020</li>
              <li>18 Verified Indian Metros</li>
              <li>Model: Random Forest (100 Trees)</li>
            </ul>
          </div>

          {/* Notice */}
          <div className="space-y-2 text-xs text-[#A8BFA9]">
            <div className="font-semibold text-white">Disclaimer</div>
            <p className="leading-relaxed text-[11px]">
              Predictions are generated from historical CPCB observations ending July 2020. This is
              a research and demonstration tool, not a live monitoring station.
            </p>
          </div>
        </div>

        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[#A8BFA9]">
          <p>© {new Date().getFullYear()} AQI Forecaster.</p>
          <div className="flex items-center gap-4">
            <Link to="/dashboard" className="hover:text-white">Dashboard</Link>
            <Link to="/signin" className="hover:text-white">Sign In</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
