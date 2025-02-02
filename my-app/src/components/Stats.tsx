"use client";

interface StatsProps {
  totalLanguages: number;
  totalModels: number;
  languagesWithModels: number;
}

export function Stats({ totalLanguages, totalModels, languagesWithModels }: StatsProps) {
  return (
    <div className="grid grid-cols-3 gap-4 mb-8">
      <div className="p-4 rounded-lg bg-white shadow-sm">
        <h3 className="text-sm font-medium text-gray-700">Total Languages</h3>
        <p className="mt-2 text-3xl font-semibold text-black">{totalLanguages}</p>
      </div>
      <div className="p-4 rounded-lg bg-white shadow-sm">
        <h3 className="text-sm font-medium text-gray-700">Total Model Implementations</h3>
        <p className="mt-2 text-3xl font-semibold text-black">{totalModels}</p>
      </div>
      <div className="p-4 rounded-lg bg-white shadow-sm">
        <h3 className="text-sm font-medium text-gray-700">Languages with Models</h3>
        <p className="mt-2 text-3xl font-semibold text-black">{languagesWithModels}</p>
      </div>
    </div>
  );
}
