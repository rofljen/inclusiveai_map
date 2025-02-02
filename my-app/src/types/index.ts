export type ModelType = 'ASR' | 'NMT' | 'TTS';

export interface LanguageData {
  id: number;
  name: string;
  iso_code: string;
  latitude: number;
  longitude: number;
  available_models: ModelType[];
  nmt_pair_count?: number;
  connected_languages?: string;
}
