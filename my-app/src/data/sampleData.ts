import { LanguageData } from "@/types";

export const sampleLanguages: LanguageData[] = [
  {
    id: 1,
    name: "Dari (Pashto)",
    iso_code: "prs",
    latitude: 34.5553,
    longitude: 69.2075,
    available_models: ["ASR", "NMT"],
    nmt_pair_count: 5,
    connected_languages: "English, Urdu, Persian"
  },
  {
    id: 2,
    name: "Swahili",
    iso_code: "swh",
    latitude: -6.3690,
    longitude: 34.8888,
    available_models: ["NMT", "TTS"],
    nmt_pair_count: 3,
    connected_languages: "English, Arabic"
  },
  {
    id: 3,
    name: "Yoruba",
    iso_code: "yor",
    latitude: 7.3775,
    longitude: 3.9470,
    available_models: ["ASR"],
    nmt_pair_count: 0,
    connected_languages: ""
  }
];
