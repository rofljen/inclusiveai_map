import { LanguageData } from "@/types";
import { TranslationPair } from "./translationPairs";

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

export const sampleTranslationPairs: TranslationPair[] = [
  {
    id: 1,
    chrf_score: 46.80,
    bleu_score: 28.60,
    source_language: 'Amharic',
    target_language: 'Tamil',
    role: 'Source'
  },
  {
    id: 2,
    chrf_score: 45.80,
    bleu_score: 27.80,
    source_language: 'Amharic',
    target_language: 'Hindi',
    role: 'Source'
  },
  {
    id: 3,
    chrf_score: 45.60,
    bleu_score: 30.30,
    source_language: 'Amharic',
    target_language: 'Telugu',
    role: 'Source'
  },
  {
    id: 4,
    chrf_score: 45.20,
    bleu_score: 29.70,
    source_language: 'Amharic',
    target_language: 'Kannada',
    role: 'Source'
  },
  {
    id: 5,
    chrf_score: 44.50,
    bleu_score: 21.90,
    source_language: 'Amharic',
    target_language: 'Zulu',
    role: 'Source'
  },
  {
    id: 6,
    chrf_score: 44.20,
    bleu_score: 20.70,
    source_language: 'Amharic',
    target_language: 'Hausa',
    role: 'Source'
  },
  {
    id: 7,
    chrf_score: 43.60,
    bleu_score: 29.10,
    source_language: 'Amharic',
    target_language: 'Malayalam',
    role: 'Source'
  }
];
