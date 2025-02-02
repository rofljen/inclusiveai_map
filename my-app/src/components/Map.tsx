"use client";

import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { ModelType } from "@/types";
import { sampleLanguages } from "@/data/sampleData";
import { LanguageMarker } from "./LanguageMarker";

interface MapProps {
  selectedModels?: ModelType[];
}

export default function Map({ selectedModels = [] }: MapProps) {
  const position: [number, number] = [20, 0]; // World view coordinates

  return (
    <MapContainer
      center={position}
      zoom={2}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%", minHeight: "400px" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {sampleLanguages.map((language) => (
        <LanguageMarker
          key={language.id}
          language={language}
          selectedModels={selectedModels}
        />
      ))}
    </MapContainer>
  );
}
