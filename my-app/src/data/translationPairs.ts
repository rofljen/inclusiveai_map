export interface TranslationPair {
  id: number;
  chrf_score: number;
  bleu_score: number;
  source_language: string;
  target_language: string;
  role: 'Source' | 'Target';
}

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
  }
];
