export function DateSelector({ selectedDate, onSelectDate, className = '' }) {
  const presets = [
    { label: 'Latest (2020-07-01)', value: '2020-07-01' },
    { label: 'Winter Peak (2019-11-15)', value: '2019-11-15' },
    { label: 'Lockdown (2020-04-10)', value: '2020-04-10' },
    { label: 'Monsoon (2019-08-15)', value: '2019-08-15' },
  ];

  return (
    <div className={`space-y-3 ${className}`}>
      <div className="space-y-1">
        <label className="text-xs font-semibold text-[#69766E] block">
          Base Date (2015-01-01 to 2020-07-01)
        </label>
        <input
          type="date"
          min="2015-01-01"
          max="2020-07-01"
          value={selectedDate || '2020-07-01'}
          onChange={(e) => onSelectDate(e.target.value)}
          className="w-full px-3 py-2 text-xs sm:text-sm rounded-xl border border-[#E3E8E1] bg-white text-[#17231C] focus:outline-none focus:ring-2 focus:ring-[#173D2D]/20 focus:border-[#173D2D]"
        />
      </div>

      <div className="space-y-1.5">
        <span className="text-[11px] text-[#69766E] block">
          Quick Dates:
        </span>
        <div className="grid grid-cols-2 gap-1.5">
          {presets.map((preset) => (
            <button
              key={preset.value}
              type="button"
              onClick={() => onSelectDate(preset.value)}
              className={`p-2 rounded-lg text-left text-xs transition-colors border ${
                selectedDate === preset.value
                  ? 'bg-[#173D2D] text-[#B7E46A] border-[#102C22] font-semibold'
                  : 'bg-white text-[#17231C] border-[#E3E8E1] hover:bg-[#F7F8F4]'
              }`}
            >
              <div className="truncate">{preset.label}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
