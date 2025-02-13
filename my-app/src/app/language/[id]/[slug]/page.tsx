"use client";

import React from 'react';
import Link from 'next/link';
import { SimpleProgressBar } from '@/components/SimpleProgressBar';

interface LanguagePageProps {
  params: {
    slug: string;
  };
}

export default function LanguagePage({ params }: LanguagePageProps) {
  const languageName = decodeURIComponent(params.slug);

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white relative">
      {/* Back button */}
      <div className="absolute top-0 left-0 p-4">
        <Link 
          href="/map" 
          className="text-gray-400 hover:text-white transition-colors flex items-center gap-1 text-xs font-medium"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3.5 h-3.5">
            <path fillRule="evenodd" d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z" clipRule="evenodd" />
          </svg>
          Back to Map
        </Link>
      </div>

      <SimpleProgressBar />

      {/* Language name */}
      <div className="px-4 py-2">
        <h1 className="text-2xl font-bold">{languageName}</h1>
      </div>

      {/* Navigation tabs */}
      <div className="border-b border-gray-800">
        <nav className="px-4 flex gap-6">
          {['Overview', 'Language Technology', 'Translation Pairs'].map((tab) => (
            <button
              key={tab}
              className={`py-2 text-sm font-medium border-b-2 ${
                tab === 'Overview'
                  ? 'text-blue-500 border-blue-500'
                  : 'text-gray-400 border-transparent hover:text-gray-300'
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {/* Content area */}
      <div className="p-4">
        <div className="space-y-4">
          {/* Location and Geography */}
          <div className="bg-[#111827] rounded-lg p-4 border border-gray-800">
            <h2 className="text-sm font-medium text-gray-200 mb-2 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-blue-500">
                <path fillRule="evenodd" d="M9.69 18.933l.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 00.281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 103 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 002.273 1.765 11.842 11.842 0 00.976.544l.062.029.018.008.006.003zM10 11.25a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5z" clipRule="evenodd" />
              </svg>
              Location and Geography
            </h2>
            <div className="text-sm text-gray-400">
              <p>Coordinates: (39.54, 11.71)</p>
            </div>
          </div>

          {/* Classification and Identifiers */}
          <div className="bg-[#111827] rounded-lg p-4 border border-gray-800">
            <h2 className="text-sm font-medium text-gray-200 mb-2 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-blue-500">
                <path fillRule="evenodd" d="M7.84 1.804A1 1 0 018.82 1h2.36a1 1 0 01.98.804l.331 1.652a6.993 6.993 0 011.929 1.115l1.598-.54a1 1 0 011.186.447l1.18 2.044a1 1 0 01-.205 1.251l-1.267 1.113a7.047 7.047 0 010 2.228l1.267 1.113a1 1 0 01.206 1.25l-1.18 2.045a1 1 0 01-1.187.447l-1.598-.54a6.993 6.993 0 01-1.929 1.115l-.33 1.652a1 1 0 01-.98.804H8.82a1 1 0 01-.98-.804l-.331-1.652a6.993 6.993 0 01-1.929-1.115l-1.598.54a1 1 0 01-1.186-.447l-1.18-2.044a1 1 0 01.205-1.251l1.267-1.113a7.047 7.047 0 010-2.228L1.821 7.773a1 1 0 01-.206-1.25l1.18-2.045a1 1 0 011.187-.447l1.598.54A6.993 6.993 0 017.51 3.456l.33-1.652zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
              </svg>
              Classification and Identifiers
            </h2>
            <div className="space-y-1 text-sm text-gray-400">
              <p>Family: Afro-Asiatic</p>
              <p>Subfamily: Semitic</p>
              <p>ISO Code: amh</p>
              <p>Glotto Code: amha1245</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
