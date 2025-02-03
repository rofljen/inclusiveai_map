"use client";

import { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { TranslationPair } from '@/types';

interface Props {
  languageId: string;
  languageName: string;
}

export default function TranslationPairs({ languageId, languageName }: Props) {
  const [pairs, setPairs] = useState<TranslationPair[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(`/api/languages/${languageId}/translation-pairs`);
        if (!response.ok) {
          throw new Error('Failed to fetch translation pairs');
        }
        const data = await response.json();
        // Convert string scores to numbers if needed
        const processedData = data.map((pair: any) => ({
          ...pair,
          chrf_score: Number(pair.chrf_score),
          bleu_score: Number(pair.bleu_score)
        }));
        setPairs(processedData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [languageId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  // Safely calculate averages
  const totalPairs = pairs.length;
  const avgChrfScore = totalPairs > 0 
    ? pairs.reduce((acc, pair) => acc + (pair.chrf_score || 0), 0) / totalPairs 
    : 0;
  const avgBleuScore = totalPairs > 0
    ? pairs.reduce((acc, pair) => acc + (pair.bleu_score || 0), 0) / totalPairs
    : 0;

  // Prepare data for the chart, ensuring numbers
  const chartData = pairs.map(pair => ({
    target_language: pair.target_language,
    chrf_score: Number(pair.chrf_score) || 0,
    bleu_score: Number(pair.bleu_score) || 0
  }));

  const formatScore = (score: number) => {
    return typeof score === 'number' ? score.toFixed(2) : '0.00';
  };

  return (
    <div className="space-y-8">
      {/* Statistics Cards */}
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800">Total Pairs</h3>
          <p className="text-3xl font-bold text-blue-600">{totalPairs}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800">Avg chrF++ Score</h3>
          <p className="text-3xl font-bold text-blue-600">{formatScore(avgChrfScore)}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800">Avg BLEU Score</h3>
          <p className="text-3xl font-bold text-blue-600">{formatScore(avgBleuScore)}</p>
        </div>
      </div>

      {/* Score Distribution Chart */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Translation Quality Scores by Target Language</h3>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="target_language"
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="chrf_score" name="chrF++ Score" fill="#8884d8" />
              <Bar dataKey="bleu_score" name="BLEU Score" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Translation Pairs Table */}
      <div className="bg-white p-6 rounded-lg shadow overflow-x-auto">
        <h3 className="text-lg font-semibold mb-4">Translation Pair Details</h3>
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                chrF++ Score
              </th>
              <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                BLEU Score
              </th>
              <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Source Language
              </th>
              <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Target Language
              </th>
              <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {pairs.map((pair, index) => (
              <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatScore(pair.chrf_score)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatScore(pair.bleu_score)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {pair.source_language}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {pair.target_language}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {pair.role}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
