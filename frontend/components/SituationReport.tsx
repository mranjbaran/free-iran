import React from 'react';
import { MapPin, Users, Calendar, AlertCircle, WifiOff } from 'lucide-react';
import { Translation } from '../types';

interface SituationReportProps {
  t: Translation['report'];
  stats: Translation['stats'];
}

const SituationReport: React.FC<SituationReportProps> = ({ t, stats }) => {
  return (
    <section id="report" className="py-20 bg-zinc-900 text-zinc-100">
      <div className="container mx-auto px-4 max-w-5xl">
        {/* Stats Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-zinc-800/50 p-6 rounded-xl border border-zinc-700/50">
            <h3 className="text-4xl font-bold text-red-500 mb-2">{stats.deaths}</h3>
            <p className="text-zinc-400 font-medium text-lg">{stats.deathsLabel}</p>
            <p className="text-sm text-zinc-500 mt-2">{stats.deathsSub}</p>
          </div>
          <div className="bg-zinc-800/50 p-6 rounded-xl border border-zinc-700/50">
            <h3 className="text-4xl font-bold text-red-500 mb-2">{stats.arrests}</h3>
            <p className="text-zinc-400 font-medium text-lg">{stats.arrestsLabel}</p>
            <p className="text-sm text-zinc-500 mt-2">{stats.arrestsSub}</p>
          </div>
          <div className="bg-zinc-800/50 p-6 rounded-xl border border-zinc-700/50">
            <h3 className="text-4xl font-bold text-red-500 mb-2">{stats.gatherings}</h3>
            <p className="text-zinc-400 font-medium text-lg">{stats.gatheringsLabel}</p>
            <p className="text-sm text-zinc-500 mt-2">{stats.gatheringsSub}</p>
          </div>
        </div>

        <div className="space-y-12">
          {/* Main Context */}
          <div className="prose prose-invert max-w-none">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <AlertCircle className="text-red-500" />
              {t.title}
            </h2>
            <p className="text-lg leading-relaxed text-zinc-300 mb-6">
              {t.description}
            </p>

            <div className="bg-zinc-800 p-6 rounded-lg border-l-4 border-red-600 my-8">
              <p className="italic text-zinc-300 text-lg">
                "{t.quote}"
              </p>
              <p className="text-right text-zinc-500 mt-2 font-semibold">— {t.quoteAuthor}</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Timeline */}
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Calendar className="text-red-500" size={20} />
                {t.timelineTitle}
              </h3>
              <ul className="space-y-6 border-l border-zinc-700 pl-6 ml-2">
                {t.timeline.map((event, idx) => (
                  <li key={idx} className="relative">
                    <span className="absolute -left-[29px] top-1 w-3 h-3 bg-red-600 rounded-full"></span>
                    <strong className="block text-white text-lg">{event.date}</strong>
                    <h4 className="font-bold text-zinc-300">{event.title}</h4>
                    <span className="text-zinc-400 text-sm">{event.description}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Victims & Areas */}
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Users className="text-red-500" size={20} />
                {t.victimsTitle}
              </h3>
              <p className="text-zinc-300 leading-relaxed">
                {t.victimsText}
              </p>
              <div className="bg-zinc-800/30 p-4 rounded-lg border border-zinc-700">
                <h4 className="font-semibold text-white mb-2 flex items-center gap-2">
                  <MapPin size={16} /> {t.impactAreas}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {t.impactAreasList.map((area, idx) => (
                    <span key={idx} className="bg-zinc-700 text-zinc-200 text-xs px-2 py-1 rounded">
                      {area}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          {/* Blackout Notice */}
          <div className="bg-red-900/10 border border-red-900/30 p-6 rounded-lg flex flex-col md:flex-row gap-4 items-start">
             <div className="bg-red-900/20 p-3 rounded-full shrink-0">
               <WifiOff className="text-red-500" size={24} />
             </div>
             <div>
               <h3 className="text-red-400 font-bold mb-2 text-lg">{t.blackoutTitle}</h3>
               <p className="text-zinc-300 leading-relaxed">
                 {t.blackoutText}
               </p>
             </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SituationReport;