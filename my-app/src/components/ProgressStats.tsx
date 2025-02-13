import React from 'react';

interface LanguageMetrics {
  bleu: number;
  chrf: number;
  wer: number;
  hasTTS: boolean;
}

function calculateLanguageScore(metrics: LanguageMetrics): number {
  let score = 0;

  // BLEU scoring
  if (metrics.bleu >= 20) score += 15;
  else if (metrics.bleu >= 15) score += 10;
  else if (metrics.bleu >= 10) score += 7;
  else if (metrics.bleu >= 5) score += 3;

  // ChRF scoring
  if (metrics.chrf >= 50) score += 15;
  else if (metrics.chrf >= 40) score += 10;
  else if (metrics.chrf >= 30) score += 7;
  else if (metrics.chrf >= 20) score += 3;

  // WER scoring (lower is better)
  if (metrics.wer < 30) score += 25;
  else if (metrics.wer < 40) score += 15;
  else if (metrics.wer < 60) score += 10;
  else if (metrics.wer < 80) score += 5;

  // TTS scoring
  if (metrics.hasTTS) score += 20;

  return score;
}

interface StatsCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, icon }) => (
  <div className="bg-[#1f2937] rounded-lg p-4 border border-gray-800 shadow-lg hover:border-gray-700 transition-colors">
    <div className="flex items-center justify-between">
      <div>
        <h2 className="text-2xl font-bold text-white leading-none mb-1">{value}</h2>
        <p className="text-xs text-gray-400 font-medium">{title}</p>
      </div>
      <span className="bg-blue-500/10 text-blue-500 p-1.5 rounded-lg">
        {icon}
      </span>
    </div>
  </div>
);

interface ProgressBarProps {
  progress: number;
  activeTab: 'languages' | 'population';
  onTabChange: (tab: 'languages' | 'population') => void;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ progress, activeTab, onTabChange }) => (
  <div className="bg-[#1f2937] rounded-lg p-4 border border-gray-800 shadow-lg">
    <div className="flex justify-between items-center mb-3">
      <div className="flex items-center space-x-2">
        <span className="bg-blue-500/10 text-blue-500 p-1 rounded-md">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
            <path d="M15.98 1.804a1 1 0 00-1.96 0l-.24 1.192a1 1 0 01-.784.785l-1.192.238a1 1 0 000 1.962l1.192.238a1 1 0 01.785.785l.238 1.192a1 1 0 001.962 0l.238-1.192a1 1 0 01.785-.785l1.192-.238a1 1 0 000-1.962l-1.192-.238a1 1 0 01-.785-.785l-.238-1.192zM6.949 5.684a1 1 0 00-1.898 0l-.683 2.051a1 1 0 01-.633.633l-2.051.683a1 1 0 000 1.898l2.051.684a1 1 0 01.633.632l.683 2.051a1 1 0 001.898 0l.683-2.051a1 1 0 01.633-.633l2.051-.683a1 1 0 000-1.898l-2.051-.683a1 1 0 01-.633-.633L6.95 5.684z" />
          </svg>
        </span>
        <h2 className="text-base font-semibold text-white">Bridging the Divide</h2>
      </div>
      <div className="flex gap-1.5">
        <button
          onClick={() => onTabChange('languages')}
          className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
            activeTab === 'languages'
              ? 'bg-blue-500 hover:bg-blue-600 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          By Languages
        </button>
        <button
          onClick={() => onTabChange('population')}
          className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
            activeTab === 'population'
              ? 'bg-blue-500 hover:bg-blue-600 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          By Population
        </button>
      </div>
    </div>
    <div className="relative">
      <div className="flex mb-2 items-center justify-between">
        <div>
          <span className="text-[10px] font-semibold inline-block py-0.5 px-2 uppercase rounded-md text-blue-500 bg-blue-500/20">
            PROGRESS
          </span>
        </div>
        <div className="text-right">
          <span className="text-xs font-medium text-gray-400">
            {progress}% to Goal
          </span>
        </div>
      </div>
      <div className="overflow-hidden h-1.5 text-xs flex rounded-full bg-gray-800/50">
        <div
          style={{ width: `${progress}%` }}
          className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 transition-all duration-500"
        ></div>
      </div>
    </div>
  </div>
);

export default function ProgressStats() {
  const [activeTab, setActiveTab] = React.useState<'languages' | 'population'>('languages');

  // Example language data with metrics
  const languageData: Record<string, LanguageMetrics> = {
    'Swahili': { bleu: 22, chrf: 55, wer: 25, hasTTS: true },
    'Yoruba': { bleu: 18, chrf: 45, wer: 35, hasTTS: true },
    'Hausa': { bleu: 15, chrf: 35, wer: 45, hasTTS: false },
    'Igbo': { bleu: 12, chrf: 32, wer: 55, hasTTS: false },
    'Amharic': { bleu: 8, chrf: 28, wer: 65, hasTTS: false }
  };

  // Calculate total progress
  const maxScorePerLanguage = 75; // 15 (BLEU) + 15 (ChRF) + 25 (WER) + 20 (TTS) = 75
  const totalScore = Object.values(languageData).reduce(
    (sum, metrics) => sum + calculateLanguageScore(metrics), 
    0
  );
  const maxPossibleScore = Object.keys(languageData).length * maxScorePerLanguage;
  const progress = Math.round((totalScore / maxPossibleScore) * 100);

  const stats = {
    totalLanguages: Object.keys(languageData).length,
    totalImplementations: Object.values(languageData).filter(m => m.hasTTS).length * 2 + 
                         Object.values(languageData).length, // Each language has NMT, some have TTS
    languagesWithModels: Object.keys(languageData).length,
    progress
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatsCard 
          title="Total Languages" 
          value={stats.totalLanguages}
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
              <path d="M7.75 2.75a.75.75 0 00-1.5 0v1.258a32.987 32.987 0 00-3.599.278.75.75 0 10.198 1.487A31.545 31.545 0 018.7 5.545 19.381 19.381 0 017 9.56a19.418 19.418 0 01-1.002-2.05.75.75 0 00-1.384.577 20.935 20.935 0 001.492 2.91 19.613 19.613 0 01-3.828 4.154.75.75 0 10.945 1.168A21.116 21.116 0 007 12.331c.095.132.192.262.29.391a.75.75 0 001.194-.91c-.204-.266-.4-.538-.59-.815a20.888 20.888 0 002.333-5.332c.31.031.618.068.924.108a.75.75 0 00.198-1.487 32.832 32.832 0 00-3.599-.278V2.75z" />
            </svg>
          } 
        />
        <StatsCard 
          title="Total Model Implementations" 
          value={stats.totalImplementations}
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
              <path d="M4.649 3.084A1 1 0 015.163 4.4 13.95 13.95 0 004 10c0 1.993.416 3.886 1.164 5.6a1 1 0 01-1.832.8A15.95 15.95 0 012 10c0-2.274.475-4.44 1.332-6.4a1 1 0 011.317-.516zM12.96 7a3 3 0 00-2.342 1.126l-.328.41-.111-.279A2 2 0 008.323 7H8a1 1 0 000 2h.323l.532 1.33-1.035 1.295a1 1 0 01-.781.375H7a1 1 0 100 2h.039a3 3 0 002.342-1.126l.328-.41.111.279A2 2 0 0011.677 14H12a1 1 0 100-2h-.323l-.532-1.33 1.035-1.295A1 1 0 0112.961 9H13a1 1 0 100-2h-.039zm1.874-2.6a1 1 0 011.833-.8A15.95 15.95 0 0118 10c0 2.274-.475 4.44-1.332 6.4a1 1 0 11-1.832-.8A13.949 13.949 0 0016 10c0-1.993-.416-3.886-1.165-5.6z" />
            </svg>
          } 
        />
        <StatsCard 
          title="Languages with Models" 
          value={stats.languagesWithModels}
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
              <path fillRule="evenodd" d="M1 2.75A.75.75 0 011.75 2h16.5a.75.75 0 010 1.5H18v8.75A2.75 2.75 0 0115.25 15h-1.072l.798 3.06a.75.75 0 01-1.452.38L13.41 18H6.59l-.114.44a.75.75 0 01-1.452-.38L5.823 15H4.75A2.75 2.75 0 012 12.25V3.5h-.25A.75.75 0 011 2.75zM7 5a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1zm1 3a1 1 0 100 2h4a1 1 0 100-2H8z" clipRule="evenodd" />
            </svg>
          } 
        />
      </div>
      <ProgressBar
        progress={stats.progress}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
    </div>
  );
}
;
