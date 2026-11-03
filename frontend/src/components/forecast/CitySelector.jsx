import { useState } from 'react';
import { Search, Check } from 'lucide-react';
import { ELIGIBLE_CITIES } from '../../utils/datasetInfo';

export function CitySelector({ selectedCity, onSelectCity, className = '' }) {
  const [search, setSearch] = useState('');

  const quickCities = ['Delhi', 'Mumbai', 'Bengaluru', 'Kolkata', 'Chennai', 'Hyderabad'];

  const filtered = ELIGIBLE_CITIES.filter(
    (c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.state.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className={`space-y-3 ${className}`}>
      {/* Quick Pills */}
      <div className="flex items-center gap-1.5 flex-wrap">
        {quickCities.map((city) => (
          <button
            key={city}
            type="button"
            onClick={() => onSelectCity(city)}
            className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
              selectedCity === city
                ? 'bg-[#173D2D] text-[#B7E46A]'
                : 'bg-white text-[#17231C] border border-[#E3E8E1] hover:bg-[#F7F8F4]'
            }`}
          >
            {city}
          </button>
        ))}
      </div>

      {/* Search Filter */}
      <div className="relative">
        <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#69766E]" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filter cities..."
          className="w-full pl-8 pr-3 py-1.5 text-xs rounded-xl border border-[#E3E8E1] bg-white text-[#17231C] focus:outline-none focus:ring-1 focus:ring-[#173D2D]"
        />
      </div>

      {/* City List Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-1.5 max-h-44 overflow-y-auto pr-1">
        {filtered.map((item) => {
          const isSelected = selectedCity === item.name;
          return (
            <button
              key={item.name}
              type="button"
              onClick={() => onSelectCity(item.name)}
              className={`flex items-center justify-between p-2 rounded-lg border text-left transition-colors ${
                isSelected
                  ? 'bg-[#DDEBE0] border-[#173D2D] text-[#173D2D] font-semibold'
                  : 'bg-white border-[#E3E8E1] text-[#17231C] hover:bg-[#F7F8F4]'
              }`}
            >
              <div className="min-w-0 pr-1">
                <div className="text-xs font-medium truncate">{item.name}</div>
                <div className="text-[10px] text-[#69766E] truncate">{item.state}</div>
              </div>
              {isSelected && <Check className="w-3 h-3 text-[#173D2D] shrink-0" />}
            </button>
          );
        })}
      </div>
    </div>
  );
}
