"use client";

import React from 'react';

export function SimpleProgressBar() {
  return (
    <div className="fixed top-4 right-4 flex items-center gap-2">
      <div className="w-24 h-1.5 bg-gray-800 rounded-full overflow-hidden">
        <div
          className="h-full w-[72%] bg-gradient-to-r from-[#f87171] via-[#facc15] to-[#4ade80]"
        />
      </div>
      <span className="text-[10px] text-gray-400">
        72% to Goal
      </span>
    </div>
  );
}
