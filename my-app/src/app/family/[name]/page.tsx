"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { LanguageData } from '@/types';

interface Props {
  params: {
    name: string;
  };
}

export default function FamilyPage({ params }: Props) {
  const [languages, setLanguages] = useState<LanguageData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const familyName = decodeURIComponent(params.name);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(`/api/languages/family/${encodeURIComponent(familyName)}`);
        if (!response.ok) {
          throw new Error('Failed to fetch languages');
        }
        const data = await response.json();
        setLanguages(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchLanguages();
  }, [familyName]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
          <p className="text-red-600">{error}</p>
          <Link href="/" className="text-blue-500 hover:text-blue-600 mt-4 inline-block">
            ← Back to Map
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Languages in {familyName} Family</h1>
        <Link href="/" className="text-blue-500 hover:text-blue-600">← Back to Map</Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {languages.map((lang) => (
          <Link 
            key={lang.id} 
            href={`/language/${lang.id}`}
            className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
          >
            <div className="text-lg font-medium text-blue-500 hover:text-blue-600 mb-2">{lang.name}</div>
            <div className="text-sm text-gray-500">
              <p>ISO Code: {lang.iso_code}</p>
              {lang.subfamily_name && <p>Subfamily: {lang.subfamily_name}</p>}
              <p>NMT Pairs: {lang.nmt_pair_count}</p>
            </div>
            <div className="mt-2 flex gap-2 flex-wrap">
              {lang.available_models.map((model) => (
                <span
                  key={model}
                  className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                >
                  {model}
                </span>
              ))}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
