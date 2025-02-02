"use client";

import { TranslationPair } from "@/data/translationPairs";
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

interface TranslationPairsProps {
  pairs: TranslationPair[];
}

export default function TranslationPairs({ pairs }: TranslationPairsProps) {
  // Calculate averages
  const avgChrfScore =
    pairs.reduce((sum, pair) => sum + pair.chrf_score, 0) / pairs.length;
  const avgBleuScore =
    pairs.reduce((sum, pair) => sum + pair.bleu_score, 0) / pairs.length;

  // Prepare data for the chart
  const chartData = pairs.map((pair) => ({
    name: pair.target_language,
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
          Translation Quality Scores by Target Language
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

      {/* Translation Pairs Table */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Translation Pair Details</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  chrF++ Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  BLEU Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Source Language
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Target Language
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Role
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {pairs.map((pair) => (
                <tr key={pair.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-black">
                    {pair.chrf_score.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-black">
                    {pair.bleu_score.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-black">
                    {pair.source_language}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-black">
                    {pair.target_language}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-black">{pair.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
