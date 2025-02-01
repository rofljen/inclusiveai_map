"use client";

interface ModelFiltersProps {
  onFilterChange: (selectedModels: string[]) => void;
}

export function ModelFilters({ onFilterChange }: ModelFiltersProps) {
  const modelTypes = [
    { id: "ASR", label: "ASR", color: "rose" },
    { id: "NMT", label: "NMT", color: "blue" },
    { id: "TTS", label: "TTS", color: "green" },
  ];

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const checkbox = e.target;
    const selectedModels = modelTypes
      .filter((model) => {
        const element = document.getElementById(model.id) as HTMLInputElement;
        return element?.checked;
      })
      .map((model) => model.id);
    onFilterChange(selectedModels);
  };

  return (
    <div className="p-4 rounded-lg bg-white shadow-sm">
      <h3 className="text-sm font-medium text-gray-500 mb-4">Model Types</h3>
      <div className="space-y-2">
        {modelTypes.map((model) => (
          <label key={model.id} className="flex items-center space-x-2">
            <input
              type="checkbox"
              id={model.id}
              className={`h-4 w-4 rounded border-gray-300 text-${model.color}-600 focus:ring-${model.color}-600`}
              onChange={handleCheckboxChange}
            />
            <span className="text-sm text-gray-700">{model.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
