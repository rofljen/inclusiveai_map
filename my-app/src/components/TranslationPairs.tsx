"use client";

import { TranslationPair } from "@/types";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

// Default sample data
const defaultPairs: TranslationPair[] = [
  {
    source_language: "English",
    target_language: "French",
    chrf_score: 0.65,
    bleu_score: 0.72,
    role: "Source"
  },
  {
    source_language: "English",
    target_language: "Spanish",
    chrf_score: 0.68,
    bleu_score: 0.75,
    role: "Source"
  },
  {
    source_language: "German",
    target_language: "English",
    chrf_score: 0.62,
    bleu_score: 0.70,
    role: "Target"
  },
  {
    source_language: "French",
    target_language: "English",
    chrf_score: 0.64,
    bleu_score: 0.71,
    role: "Target"
  }
];

interface TranslationPairsProps {
  pairs?: TranslationPair[];
  sourceLang?: string;
}

export default function TranslationPairs({ pairs = defaultPairs, sourceLang = "English" }: TranslationPairsProps) {
  // Calculate averages
  const avgChrfScore =
    pairs.reduce((sum, pair) => sum + (pair.chrf_score || 0), 0) / pairs.length;
  const avgBleuScore =
    pairs.reduce((sum, pair) => sum + (pair.bleu_score || 0), 0) / pairs.length;

  // Prepare data for the chart
  const chartData = pairs.map((pair) => ({
    name: pair.role === 'Source' ? pair.target_language : pair.source_language,
    chrf_score: pair.chrf_score,
    bleu_score: pair.bleu_score,
  }));

  return (
    <div className="space-y-8">
      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-sm font-medium text-gray-700">Total Pairs</h3>
          <p className="mt-2 text-3xl font-semibold text-black">{pairs.length}</p>
        </div>
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-sm font-medium text-gray-700">Avg chrF++ Score</h3>
          <p className="mt-2 text-3xl font-semibold text-black">
            {avgChrfScore.toFixed(2)}
          </p>
        </div>
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-sm font-medium text-gray-700">Avg BLEU Score</h3>
          <p className="mt-2 text-3xl font-semibold text-black">
            {avgBleuScore.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Score Distribution Chart */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">
          Translation Quality Scores by Language
        </h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="name"
                angle={-45}
                textAnchor="end"
                height={80}
                interval={0}
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="bleu_score" fill="#8884d8" name="BLEU Score" />
              <Bar dataKey="chrf_score" fill="#82ca9d" name="chrF++ Score" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Translation Pairs Tables */}
      <div className="space-y-8">
        {/* Source Language Pairs */}
        <section>
          <h2 className="text-xl font-semibold mb-4">
            Translations from {sourceLang}
          </h2>
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Target Language
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    chrF++ Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    BLEU Score
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {pairs.filter(p => p.role === 'Source').map((pair, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {pair.target_language}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {pair.chrf_score?.toFixed(2) || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {pair.bleu_score?.toFixed(2) || 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Target Language Pairs */}
        <section>
          <h2 className="text-xl font-semibold mb-4">
            Translations to {sourceLang}
          </h2>
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source Language
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    chrF++ Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    BLEU Score
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {pairs.filter(p => p.role === 'Target').map((pair, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {pair.source_language}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {pair.chrf_score?.toFixed(2) || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {pair.bleu_score?.toFixed(2) || 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
