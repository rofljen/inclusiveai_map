"use client";

import React from 'react';

interface BridgingProgressBarProps {
  progress?: number;
  onTabChange?: (tab: 'languages' | 'population') => void;
  activeTab?: 'languages' | 'population';
}

export function BridgingProgressBar({ 
  progress = 46,
  onTabChange,
  activeTab = 'languages'
}: BridgingProgressBarProps) {
  return (
    <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg p-6 w-[500px] mx-auto">
      <h2 className="text-white text-xl font-medium text-center mb-4">
        Bridging the Divide
      </h2>
      
      <div className="flex justify-center gap-2 mb-6">
        <button
          onClick={() => onTabChange?.('languages')}
          className={`px-4 py-1 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'languages'
              ? 'bg-blue-500 text-white'
              : 'text-gray-400 hover:text-white'
          }`}
        >
          By Languages
        </button>
        <button
          onClick={() => onTabChange?.('population')}
          className={`px-4 py-1 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'population'
              ? 'bg-blue-500 text-white'
              : 'text-gray-400 hover:text-white'
          }`}
        >
          By Population
        </button>
      </div>

      <div className="bg-gray-800 rounded-full h-2 overflow-hidden">
        <div
          style={{ width: `${progress}%` }}
          className="h-full bg-gradient-to-r from-[#f87171] via-[#facc15] to-[#4ade80] transition-all duration-300"
        />
      </div>
      
      <div className="text-gray-400 text-sm text-center mt-2">
        {progress}% to Goal
      </div>
    </div>
  );
}
