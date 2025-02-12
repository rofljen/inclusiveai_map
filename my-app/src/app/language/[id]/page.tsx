"use client";

import { useState, useEffect } from "react";
import { use } from "react";
import Link from "next/link";
import TranslationPairs from "@/components/TranslationPairs";
import { LanguageData } from "@/types";

interface TabProps {
  label: string;
  isActive: boolean;
  onClick: () => void;
}

function Tab({ label, isActive, onClick }: TabProps) {
  return (
    <button
      className={`px-4 py-2 ${
        isActive
          ? "text-blue-600 border-b-2 border-blue-600 font-medium"
          : "text-gray-500 hover:text-gray-700"
      }`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

function ModelAvailabilityBadge({ isAvailable }: { isAvailable: boolean }) {
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
        isAvailable 
          ? 'bg-blue-900 text-blue-100'
          : 'bg-gray-700 text-gray-300'
      }`}
    >
      {isAvailable ? '✓ Available' : '✗ Not Available'}
    </span>
  );
}

export default function LanguageDetails({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const [activeTab, setActiveTab] = useState("overview");
  const [language, setLanguage] = useState<LanguageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(`/api/languages/${resolvedParams.id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch language details');
        }
        const data = await response.json();
        setLanguage(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [resolvedParams.id]);

  if (loading) {
    return (
      <div className="container mx-auto p-4 flex justify-center items-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading language details...</p>
        </div>
      </div>
    );
  }

  if (error || !language) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
          <p className="text-red-600">{error || 'Language not found'}</p>
          <Link href="/" className="text-blue-600 hover:underline mt-4 inline-block">
            ← Back to Map
          </Link>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "technology", label: "Language Technology" },
    { id: "pairs", label: "Translation Pairs" },
  ];

  return (
    <main className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white">{language.name || "Amharic"}</h1>
        <Link
          href="/"
          className="px-4 py-2 text-gray-300 hover:text-white flex items-center gap-2"
        >
          ← Back to Map
        </Link>
      </div>

      <div className="border-b border-gray-700 mb-6">
        <div className="flex gap-4">
          {tabs.map((tab) => (
            <Tab
              key={tab.id}
              label={tab.label}
              isActive={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
            />
          ))}
        </div>
      </div>

      {activeTab === "overview" && (
        <div className="grid grid-cols-1 gap-6">
          {/* Location Card */}
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg p-6 border border-gray-800">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-gray-400">🌍</span>
              <h3 className="text-gray-400 text-sm font-medium">Location and Geography</h3>
            </div>
            {language.latitude && language.longitude && (
              <p className="text-gray-300 text-sm">
                <span className="text-gray-400">Coordinates:</span>{" "}
                <span>({language.latitude.toFixed(2)}, {language.longitude.toFixed(2)})</span>
              </p>
            )}
          </div>

          {/* Classification Card */}
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg p-6 border border-gray-800">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-gray-400">🏷️</span>
              <h3 className="text-gray-400 text-sm font-medium">Classification and Identifiers</h3>
            </div>
            <div className="space-y-2">
              {language.family_name && (
                <p className="text-gray-300 text-sm">
                  <span className="text-gray-400">Family:</span>{" "}
                  <Link 
                    href={`/family/${language.family_id}`}
                    className="text-blue-400 hover:text-blue-300 hover:underline"
                  >
                    {language.family_name}
                  </Link>
                </p>
              )}
              {language.subfamily_name && (
                <p className="text-gray-300 text-sm">
                  <span className="text-gray-400">Subfamily:</span>{" "}
                  <Link 
                    href={`/subfamily/${language.subfamily_id}`}
                    className="text-blue-400 hover:text-blue-300 hover:underline"
                  >
                    {language.subfamily_name}
                  </Link>
                </p>
              )}
              {language.iso_code && (
                <p className="text-gray-300 text-sm">
                  <span className="text-gray-400">ISO Code:</span>{" "}
                  <span>{language.iso_code}</span>
                </p>
              )}
              {language.glottocode && (
                <p className="text-gray-300 text-sm">
                  <span className="text-gray-400">Glotto Code:</span>{" "}
                  <span>{language.glottocode}</span>
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === "technology" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="p-6 bg-gray-900 rounded-lg border border-gray-700">
            <h3 className="text-lg font-medium mb-4 text-gray-300">Speech Recognition (ASR)</h3>
            <ModelAvailabilityBadge isAvailable={language.available_models?.includes('ASR')} />
          </div>
          
          <div className="p-6 bg-gray-900 rounded-lg border border-gray-700">
            <h3 className="text-lg font-medium mb-4 text-gray-300">Machine Translation (NMT)</h3>
            <ModelAvailabilityBadge isAvailable={language.available_models?.includes('NMT')} />
          </div>
          
          <div className="p-6 bg-gray-900 rounded-lg border border-gray-700">
            <h3 className="text-lg font-medium mb-4 text-gray-300">Text-to-Speech (TTS)</h3>
            <ModelAvailabilityBadge isAvailable={language.available_models?.includes('TTS')} />
          </div>
        </div>
      )}

      {activeTab === "pairs" && (
        <TranslationPairs languageId={resolvedParams.id} languageName={language.name} />
      )}
    </main>
  );
}
