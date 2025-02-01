"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import { Stats } from "@/components/Stats";
import { ModelFilters } from "@/components/ModelFilters";

const Map = dynamic(() => import("@/components/Map"), {
  ssr: false,
});

export default function Home() {
  const [selectedModels, setSelectedModels] = useState<string[]>([]);

  // TODO: Replace with actual API data
  const stats = {
    totalLanguages: 21,
    totalModels: 25,
    languagesWithModels: 16,
  };

  return (
    <main className="p-4">
      <div className="container mx-auto">
        <Stats {...stats} />
        <div className="grid grid-cols-4 gap-4">
          <div className="space-y-4">
            <ModelFilters onFilterChange={setSelectedModels} />
          </div>
          <div className="col-span-3 rounded-lg border border-gray-200 shadow-sm h-[600px] bg-white">
            <Map selectedModels={selectedModels} />
          </div>
        </div>
      </div>
    </main>
  );
}