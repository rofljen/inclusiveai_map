"use client";

import { LanguageData, ModelType } from "@/types";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

interface LanguageMarkerProps {
  language: LanguageData;
  selectedModels: ModelType[];
}

const MODEL_COLORS = {
  ASR: "#FF4B4B",
  NMT: "#4CAF50",
  TTS: "#2196F3",
};

function createModelIndicatorHtml(models: ModelType[]): string {
  if (models.length === 0) return "";

  if (models.length === 1) {
    return `
      <div style="
        width: 24px;
        height: 24px;
        background-color: ${MODEL_COLORS[models[0]]};
        border-radius: 50%;
        border: 2px solid white;
      "></div>
    `;
  }

  const segments = models.map((model, index) => {
    const rotation = (360 / models.length) * index;
    return `
      <div style="
        position: absolute;
        width: 12px;
        height: 24px;
        overflow: hidden;
        transform-origin: 100% 50%;
        transform: rotate(${rotation}deg);
      ">
        <div style="
          width: 24px;
          height: 24px;
          background-color: ${MODEL_COLORS[model]};
          border-radius: 50%;
          transform: rotate(-${rotation}deg);
          border: 2px solid white;
        "></div>
      </div>
    `;
  }).join("");

  return `
    <div style="
      position: relative;
      width: 24px;
      height: 24px;
    ">${segments}</div>
  `;
}

export function LanguageMarker({ language, selectedModels }: LanguageMarkerProps) {
  const availableModels = selectedModels.length === 0 
    ? language.available_models 
    : language.available_models.filter(model => selectedModels.includes(model));

  if (selectedModels.length > 0 && availableModels.length === 0) {
    return null;
  }

  const icon = L.divIcon({
    html: createModelIndicatorHtml(availableModels),
    className: "custom-marker",
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });

  return (
    <Marker
      position={[language.latitude, language.longitude]}
      icon={icon}
    >
      <Popup>
        <div className="w-[250px]">
          <h4 className="text-lg font-semibold mb-2">{language.name}</h4>
          <p className="mb-2">
            <strong>ISO Code:</strong> {language.iso_code || "N/A"}
          </p>
          <p className="mb-2">
            <strong>Available Models:</strong>
          </p>
          <div className="flex gap-1 mb-2">
            {language.available_models.map((model) => (
              <span
                key={model}
                className="px-2 py-1 text-xs text-white rounded"
                style={{ backgroundColor: MODEL_COLORS[model] }}
              >
                {model}
              </span>
            ))}
          </div>
          {language.nmt_pair_count > 0 && (
            <p className="mb-2">
              <strong>NMT Pairs:</strong> {language.nmt_pair_count} language pairs
            </p>
          )}
          {language.connected_languages && (
            <div className="mb-2">
              <strong>Connected Languages:</strong>
              <div className="mt-1 max-h-[100px] overflow-y-auto">
                {language.connected_languages.split(", ").map((lang) => (
                  <div key={lang}>• {lang}</div>
                ))}
              </div>
            </div>
          )}
          <button
            className="mt-2 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={() => {
              window.location.href = `/language/${language.id}`;
            }}
          >
            View Details
          </button>
        </div>
      </Popup>
    </Marker>
  );
}
