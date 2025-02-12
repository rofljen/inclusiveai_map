"use client";

import { useState, useEffect } from 'react';
import { use } from 'react';
import Link from 'next/link';

interface Language {
  id: number;
  name: string;
  iso_code: string;
  glottocode: string;
  family_name: string;
  family_id: number;
}

export default function FamilyPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const [languages, setLanguages] = useState<Language[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [familyName, setFamilyName] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(`/api/family/${resolvedParams.id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch family languages');
        }
        const data = await response.json();
        setLanguages(data);
        if (data.length > 0) {
          setFamilyName(data[0].family_name);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [resolvedParams.id]);

  if (loading) {
    return (
      <div className="container mx-auto p-4 flex justify-center items-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading languages...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
          <p className="text-red-600">{error}</p>
          <Link href="/" className="text-blue-600 hover:underline mt-4 inline-block">
            ← Back to Map
          </Link>
        </div>
      </div>
    );
  }

  return (
    <main className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white">Languages in Family: {familyName}</h1>
        <Link
          href="/"
          className="px-4 py-2 text-gray-300 hover:text-white flex items-center gap-2"
        >
          ← Back to Map
        </Link>
      </div>

      <div className="space-y-2">
        {languages.map((language) => (
          <Link
            key={language.id}
            href={`/language/${language.id}`}
            className="block text-blue-400 hover:text-blue-300 hover:underline"
          >
            • {language.name}
          </Link>
        ))}
      </div>
    </main>
  );
}
