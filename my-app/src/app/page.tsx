"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { Stats } from "@/components/Stats";
import { ModelFilters } from "@/components/ModelFilters";
import { BridgingProgressBar } from "@/components/BridgingProgressBar";
import { LanguageData } from "@/types";

const Map = dynamic(() => import("@/components/Map"), {
  ssr: false,
});

export default function Home() {
  const [selectedModels, setSelectedModels] = useState<string[]>([]);
  const [activeProgressTab, setActiveProgressTab] = useState<'languages' | 'population'>('languages');
  const [languages, setLanguages] = useState<LanguageData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const response = await fetch('/api/languages');
        if (!response.ok) {
          throw new Error('Failed to fetch languages');
        }
        const data = await response.json();
        setLanguages(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch languages');
      } finally {
        setLoading(false);
      }
    };

    fetchLanguages();
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="flex items-center justify-center min-h-screen text-red-500">{error}</div>;
  }

  const stats = {
    totalLanguages: languages.length,
    totalModels: languages.reduce((sum, lang) => 
      sum + (lang.available_models?.filter(Boolean).length || 0), 0),
    languagesWithModels: languages.filter(lang => 
      lang.available_models?.some(Boolean)).length,
  };

  return (
    <main className="p-4">
      <div className="container mx-auto space-y-8">
        <Stats {...stats} />
        <BridgingProgressBar
          progress={46}
          activeTab={activeProgressTab}
          onTabChange={setActiveProgressTab}
        />
        <div className="grid grid-cols-4 gap-4">
          <div className="space-y-4">
            <ModelFilters onFilterChange={setSelectedModels} />
          </div>
          <div className="col-span-3 rounded-lg border border-gray-200 shadow-sm h-[600px] bg-white">
            <Map languages={languages} selectedModels={selectedModels} />
          </div>
        </div>
      </div>
    </main>
  );
}