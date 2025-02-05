export type ModelType = 'ASR' | 'NMT' | 'TTS';

export interface LanguageData {
  id: number;
  name: string;
  iso_code: string;
  latitude: number;
  longitude: number;
  available_models: string[];
  nmt_pair_count: number;
  connected_languages?: string[] | string;
  connected_coords?: number[][] | string;
  family_name?: string;
  subfamily_name?: string;
  glotto_code?: string;
}

export interface TranslationPair {
  source_language: string;
  target_language: string;
  chrf_score: number;
  bleu_score: number;
  role: 'Source' | 'Target';
}
