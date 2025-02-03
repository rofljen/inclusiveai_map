"use client";

import { useState } from "react";
import Link from "next/link";
import TranslationPairs from "@/components/TranslationPairs";

// Default sample data
const sampleLanguages = [
  {
    id: 1,
    name: "English",
    iso_code: "eng",
    latitude: 51.5074,
    longitude: -0.1278,
    available_models: ["ASR", "NMT", "TTS"],
    nmt_pair_count: 4,
    family_name: "Indo-European",
    subfamily_name: "Germanic"
  }
];

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

export default function LanguageDetails({
  params,
}: {
  params: { id: string };
}) {
  const [activeTab, setActiveTab] = useState("overview");
  // Use sample data for now
  const language = sampleLanguages[0];

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "technology", label: "Language Technology" },
    { id: "pairs", label: "Translation Pairs" },
  ];

  return (
    <main className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">{language.name}</h1>
        <Link
          href="/"
          className="px-4 py-2 text-gray-600 hover:text-gray-800 flex items-center gap-2"
        >
          ← Back to Map
        </Link>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
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

      {/* Content */}
      {activeTab === "overview" && (
        <div className="grid grid-cols-2 gap-8">
          <div className="space-y-6">
            <section>
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="text-blue-500">🌍</span> Location and Geography
              </h2>
              <p className="text-gray-700">
                <strong>Coordinates:</strong> {language.latitude}, {language.longitude}
              </p>
            </section>
          </div>

          <div className="space-y-6">
            <section>
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="text-blue-500">🏷️</span> Classification and
                Identifiers
              </h2>
              <div className="space-y-2">
                <p className="text-gray-700">
                  <strong>ISO Code:</strong> {language.iso_code}
                </p>
                <p className="text-gray-700">
                  <strong>Family:</strong>{" "}
                  <span className="text-blue-600">
                    {language.family_name}
                  </span>
                </p>
                <p className="text-gray-700">
                  <strong>Subfamily:</strong>{" "}
                  <span className="text-blue-600">
                    {language.subfamily_name}
                  </span>
                </p>
              </div>
            </section>
          </div>
        </div>
      )}

      {activeTab === "technology" && (
        <div className="space-y-6">
          <section>
            <h2 className="text-xl font-semibold mb-4">Available Models</h2>
            <div className="flex gap-2">
              {language.available_models.map((model) => (
                <span
                  key={model}
                  className="px-3 py-1 rounded-full text-white text-sm"
                  style={{
                    backgroundColor:
                      model === "ASR"
                        ? "#FF4B4B"
                        : model === "NMT"
                        ? "#4CAF50"
                        : "#2196F3",
                  }}
                >
                  {model}
                </span>
              ))}
            </div>
          </section>
        </div>
      )}

      {activeTab === "pairs" && (
        <TranslationPairs />
      )}
    </main>
  );
}
