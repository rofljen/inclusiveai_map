"use client";

import dynamic from "next/dynamic";

const Map = dynamic(() => import("@/components/Map"), {
  ssr: false,
});

export default function Home() {
  return (
    <main className="p-4">
      <div className="container mx-auto space-y-6">
        <div className="max-w-3xl">
          <h1 className="text-4xl font-bold mb-3">Inclusive AI Map</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
            Welcome to Phase 1 of our project. This interactive map will showcase AI companies 
            and organizations, highlighting their commitment to diversity, equity, and inclusion. 
            Currently in the initial setup phase, we're building the foundation for visualizing 
            the global AI landscape through an inclusion lens.
          </p>
        </div>
        <div className="rounded-lg border border-gray-200 shadow-sm h-[600px]">
          <Map />
        </div>
      </div>
    </main>
  );
}