"use client";

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { LanguageData } from '@/types';
import { useRouter } from 'next/navigation';

const MODEL_COLORS = {
  ASR: '#FF4B4B',
  NMT: '#4CAF50',
  TTS: '#2196F3'
} as const;

interface MapProps {
  languages: LanguageData[];
  selectedModels: string[];
}

export default function Map({ languages, selectedModels }: MapProps) {
  const mapRef = useRef<L.Map | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!mapRef.current) {
      // Initialize map
      mapRef.current = L.map('map', {
        center: [20, 0],
        zoom: 2,
        layers: [
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: ' OpenStreetMap contributors'
          })
        ]
      });
    }

    // Clear existing markers
    mapRef.current.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        layer.remove();
      }
    });

    // Add markers for each language
    languages.forEach((language) => {
      const modelsPresent = language.available_models?.filter(Boolean) || [];
      const modelsToShow = selectedModels.length > 0 
        ? modelsPresent.filter(m => selectedModels.includes(m))
        : modelsPresent;

      if (modelsToShow.length === 0 && selectedModels.length > 0) {
        return;
      }

      // Create marker HTML
      const markerHtml = createMarkerHtml(modelsToShow);
      
      // Create custom icon
      const icon = L.divIcon({
        html: markerHtml,
        className: 'custom-marker',
        iconSize: [24, 24]
      });

      // Create popup content with View Details button
      const popupContent = `
        <div class="min-w-[200px] p-4">
          <h3 class="text-lg font-semibold mb-2">${language.name}</h3>
          <p class="mb-2"><strong>ISO Code:</strong> ${language.iso_code}</p>
          ${modelsPresent.length > 0 ? `
            <p class="mb-2"><strong>Available Models:</strong></p>
            <div class="flex gap-2 mb-2">
              ${modelsPresent.map(model => `
                <span class="px-2 py-1 rounded-full text-white text-xs" style="background-color: ${MODEL_COLORS[model]}">${model}</span>
              `).join('')}
            </div>
          ` : ''}
          <p class="mb-4"><strong>NMT Pairs:</strong> ${language.nmt_pair_count || 0}</p>
          <button
            class="view-details-btn bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md text-sm w-full transition-colors"
            data-language-id="${language.id}"
          >
            View Details
          </button>
        </div>
      `;

      // Add marker to map
      const marker = L.marker([language.latitude, language.longitude], { icon })
        .bindPopup(popupContent)
        .addTo(mapRef.current!);

      // Add click handler for View Details button
      marker.on('popupopen', () => {
        const btn = document.querySelector(`button[data-language-id="${language.id}"]`);
        if (btn) {
          btn.addEventListener('click', () => {
            router.push(`/language/${language.id}`);
          });
        }
      });

      // If language has NMT pairs and connected languages, draw connections
      if (language.connected_languages && language.connected_coords) {
        const connectedLanguages = Array.isArray(language.connected_languages) 
          ? language.connected_languages 
          : language.connected_languages.split(',');

        const connectedCoords = Array.isArray(language.connected_coords) 
          ? language.connected_coords 
          : JSON.parse(language.connected_coords);

        connectedCoords.forEach((coords: number[], index: number) => {
          if (coords && coords.length === 2) {
            const line = L.polyline(
              [[language.latitude, language.longitude], coords],
              {
                color: MODEL_COLORS.NMT,
                weight: 1,
                opacity: 0.5
              }
            ).addTo(mapRef.current!);

            // Add popup to line
            const pairPopup = `
              <div class="min-w-[200px] p-4">
                <h4 class="text-lg font-semibold mb-2">Translation Pair</h4>
                <p class="mb-2">
                  <strong>Source:</strong> ${language.name}<br>
                  <strong>Target:</strong> ${connectedLanguages[index]}
                </p>
              </div>
            `;
            line.bindPopup(pairPopup);
          }
        });
      }
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [languages, selectedModels, router]);

  return <div id="map" className="w-full h-full" />;
}

function createMarkerHtml(models: string[]): string {
  if (models.length === 0) {
    return `
      <div class="w-6 h-6 rounded-full bg-gray-400 opacity-40 border-2 border-white"></div>
    `;
  }

  if (models.length === 1) {
    return `
      <div class="w-6 h-6 rounded-full opacity-80 border-2 border-white" style="background-color: ${MODEL_COLORS[models[0]]}"></div>
    `;
  }

  const segmentSize = 360 / models.length;
  const conicGradient = models.map((model, index) => {
    const startAngle = index * segmentSize;
    const endAngle = startAngle + segmentSize;
    return `${MODEL_COLORS[model]} ${startAngle}deg ${endAngle}deg`;
  }).join(', ');

  return `
    <div class="w-6 h-6 rounded-full opacity-80 border-2 border-white" style="background: conic-gradient(${conicGradient})"></div>
  `;
}
