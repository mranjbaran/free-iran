import React, { useState } from 'react';
import { Mail, Copy, Check, ExternalLink, ArrowRight, AlertCircle } from 'lucide-react';
import { Translation, MP } from '../types';
import MPList from './MPList';

interface ActionCenterProps {
  t: Translation['action'];
}

interface WahlkreisOption {
  title: string;
  url: string;
}

const ActionCenter: React.FC<ActionCenterProps> = ({ t }) => {
  const [plz, setPlz] = useState('');
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [members, setMembers] = useState<MP[]>([]);
  const [wahlkreisOptions, setWahlkreisOptions] = useState<WahlkreisOption[]>([]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (plz.length !== 5) {
      setError('Bitte geben Sie eine 5-stellige PLZ ein');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:5000/api/search?plz=${plz}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Fehler beim Abrufen der Daten');
      }

      if (data.type === 'multiple_wahlkreis') {
        setWahlkreisOptions(data.options);
        setStep(2);
      } else if (data.type === 'members') {
        setMembers(data.members);
        setStep(3);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unbekannter Fehler');
    } finally {
      setLoading(false);
    }
  };

  const handleWahlkreisSelect = async (url: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:5000/api/scrape-url?url=${encodeURIComponent(url)}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Fehler beim Abrufen der Daten');
      }

      setMembers(data.members);
      setStep(3);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unbekannter Fehler');
    } finally {
      setLoading(false);
    }
  };

  const resetSearch = () => {
    setStep(1);
    setPlz('');
    setMembers([]);
    setWahlkreisOptions([]);
    setError(null);
  };

  const copyToClipboard = () => {
    const fullText = `Subject: ${t.emailTemplate.subject}\n\n${t.emailTemplate.body}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // If we have members, show the MPList component
  if (step === 3 && members.length > 0) {
    return (
      <MPList 
        members={members}
        plz={plz}
        onBack={resetSearch}
        emailTemplate={t.emailTemplate}
      />
    );
  }

  return (
    <section id="action-center" className="py-20 bg-white text-zinc-900">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="text-center mb-12">
          {/* Germany Flag Indicator */}
          <div className="flex justify-center mb-4">
             <div className="flex rounded overflow-hidden shadow-sm border border-zinc-200 h-6 w-9">
               <div className="bg-black flex-1"></div>
               <div className="bg-red-600 flex-1"></div>
               <div className="bg-yellow-400 flex-1"></div>
             </div>
          </div>
          <h2 className="text-4xl font-black mb-4">{t.title}</h2>
          <p className="text-xl text-zinc-600 max-w-2xl mx-auto">
            {t.subtitle}
          </p>
        </div>

        <div className="bg-zinc-50 rounded-2xl shadow-xl overflow-hidden border border-zinc-200">
          <div className="grid md:grid-cols-12 min-h-[400px]">
            {/* Sidebar / Progress */}
            <div className="md:col-span-4 bg-zinc-900 text-white p-8 flex flex-col justify-between">
              <div>
                <h3 className="text-2xl font-bold mb-6">{t.howItWorksTitle}</h3>
                <ol className="space-y-6">
                  {t.steps.map((stepText, idx) => (
                    <li key={idx} className={`flex items-start gap-3 ${step >= idx + 1 ? 'opacity-100' : 'opacity-50'}`}>
                      <span className="flex-shrink-0 w-8 h-8 rounded-full bg-red-600 flex items-center justify-center font-bold">{idx + 1}</span>
                      <p className="text-sm mt-1">{stepText}</p>
                    </li>
                  ))}
                </ol>
              </div>
              <div className="mt-8 pt-8 border-t border-zinc-800">
                <p className="text-xs text-zinc-500">
                  {t.disclaimer}
                </p>
              </div>
            </div>

            {/* Content Area */}
            <div className="md:col-span-8 p-8 md:p-12">
              {error && (
                <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg flex items-center gap-2 text-red-700">
                  <AlertCircle size={20} />
                  <span>{error}</span>
                </div>
              )}

              {step === 1 && (
                <div className="flex flex-col justify-center h-full space-y-6">
                   <h3 className="text-2xl font-bold">{t.identifyTitle}</h3>
                   <form onSubmit={handleSearch} className="space-y-4">
                     <div>
                       <label htmlFor="plz" className="block text-sm font-medium text-zinc-700 mb-2">{t.plzLabel}</label>
                       <div className="flex gap-2">
                         <input 
                            type="text" 
                            id="plz"
                            value={plz}
                            onChange={(e) => setPlz(e.target.value)}
                            placeholder={t.plzPlaceholder}
                            className="flex-1 p-4 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-red-600 focus:border-transparent outline-none text-lg text-left"
                            required
                            maxLength={5}
                            disabled={loading}
                         />
                         <button 
                            type="submit"
                            disabled={loading || plz.length !== 5}
                            className="bg-zinc-900 text-white px-8 py-4 rounded-lg font-bold hover:bg-zinc-800 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                         >
                           {loading ? t.searchingMsg : t.startBtn} {!loading && <ArrowRight size={20} className="rtl:rotate-180" />}
                         </button>
                       </div>
                       {loading && (
                         <p className="text-sm text-zinc-600 mt-2 italic">{t.searchingMsg}</p>
                       )}
                       {!loading && (
                         <p className="text-sm text-zinc-500 mt-2">{t.plzHint}</p>
                       )}
                     </div>
                   </form>
                </div>
              )}

              {step === 2 && wahlkreisOptions.length > 0 && (
                <div className="space-y-6">
                  <div className="flex justify-between items-start">
                    <h3 className="text-2xl font-bold">Wahlkreis auswählen</h3>
                    <button onClick={resetSearch} className="text-sm text-zinc-500 underline">Zurück</button>
                  </div>
                  <p className="text-zinc-600">Mehrere Wahlkreise gefunden für PLZ {plz}. Bitte wählen Sie Ihren Wahlkreis:</p>
                  {loading && (
                    <p className="text-sm text-zinc-600 italic">{t.searchingMsg}</p>
                  )}
                  <div className="space-y-2">
                    {wahlkreisOptions.map((option, index) => (
                      <button
                        key={index}
                        onClick={() => handleWahlkreisSelect(option.url)}
                        disabled={loading}
                        className="w-full text-left px-4 py-3 bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 rounded-lg transition-colors disabled:opacity-50"
                      >
                        {option.title}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ActionCenter;