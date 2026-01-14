import React from 'react';
import { AlertTriangle, ChevronDown, Globe } from 'lucide-react';
import { Language, Translation } from '../types';

interface HeroProps {
  lang: Language;
  setLang: (l: Language) => void;
  t: Translation['hero'];
}

const Hero: React.FC<HeroProps> = ({ lang, setLang, t }) => {
  const scrollToReport = () => {
    const element = document.getElementById('report');
    if (element) element.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="relative bg-zinc-950 text-white min-h-[90vh] flex flex-col items-center justify-center px-4 py-20 overflow-hidden">
      {/* Language Switcher */}
      <div className="absolute top-6 right-6 z-50 flex items-center gap-2 bg-zinc-900/80 p-1 rounded-lg border border-zinc-800 backdrop-blur-sm">
        <Globe size={16} className="ml-2 text-zinc-400" />
        <button 
          onClick={() => setLang('en')} 
          className={`px-3 py-1 rounded text-sm font-bold transition-all ${lang === 'en' ? 'bg-red-600 text-white' : 'text-zinc-400 hover:text-white'}`}
        >
          EN
        </button>
        <button 
          onClick={() => setLang('de')} 
          className={`px-3 py-1 rounded text-sm font-bold transition-all ${lang === 'de' ? 'bg-red-600 text-white' : 'text-zinc-400 hover:text-white'}`}
        >
          DE
        </button>
        <button 
          onClick={() => setLang('fa')} 
          className={`px-3 py-1 rounded text-sm font-bold transition-all ${lang === 'fa' ? 'bg-red-600 text-white' : 'text-zinc-400 hover:text-white'}`}
        >
          فا
        </button>
      </div>

      {/* Background Graphic Elements */}
      <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
        <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] bg-red-600 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-20%] left-[-10%] w-[500px] h-[500px] bg-red-800 rounded-full blur-[100px]" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto text-center space-y-8">
        <div className="inline-flex items-center space-x-2 bg-red-600/20 border border-red-600/50 rounded-full px-4 py-1.5 text-red-400 font-medium animate-pulse">
          <AlertTriangle size={16} />
          <span className="text-sm uppercase tracking-wider">{t.badge}</span>
        </div>

        <h1 className="text-5xl md:text-7xl font-black tracking-tighter leading-tight text-white">
          {t.title} <span className="text-red-600">{t.highlight}</span>
          {lang === 'fa' && <span className="block mt-2">در ایران</span>}
          {lang !== 'fa' && " IN IRAN"}
        </h1>

        <p className="text-xl md:text-2xl text-zinc-300 max-w-2xl mx-auto leading-relaxed">
          {t.description}
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <button 
            onClick={() => document.getElementById('action-center')?.scrollIntoView({ behavior: 'smooth' })}
            className="w-full sm:w-auto px-8 py-4 bg-red-600 hover:bg-red-700 text-white font-bold text-lg rounded-lg transition-all shadow-[0_0_20px_rgba(220,38,38,0.5)] transform hover:scale-105"
          >
            {t.ctaAction}
          </button>
          <button 
            onClick={scrollToReport}
            className="w-full sm:w-auto px-8 py-4 bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-lg rounded-lg transition-all border border-zinc-700"
          >
            {t.ctaRead}
          </button>
        </div>
      </div>

      <button 
        onClick={scrollToReport}
        className="absolute bottom-10 left-1/2 -translate-x-1/2 text-zinc-500 hover:text-white transition-colors animate-bounce"
      >
        <ChevronDown size={32} />
      </button>
    </div>
  );
};

export default Hero;