"use client";

import React from 'react';

interface LanguageProgressBarProps {
  progress?: number; // Optional, will use default if not provided
  languageName: string;
}

export function LanguageProgressBar({ progress = 72, languageName }: LanguageProgressBarProps) {
  return (
    <div className="absolute top-0 right-0 p-4">
      <div className="flex items-center gap-2">
        <div className="w-24 h-1.5 bg-gray-800 rounded-full overflow-hidden">
          <div
            style={{ width: `${progress}%` }}
            className="h-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500"
          />
        </div>
        <span className="text-[10px] text-gray-400 font-medium whitespace-nowrap">
          {progress}% to Goal
        </span>
      </div>
    </div>
  );
}
