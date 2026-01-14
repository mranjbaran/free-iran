import React, { useState } from 'react';
import { Mail, Copy, Check, X } from 'lucide-react';
import { MP } from '../types';

interface MPListProps {
  members: MP[];
  plz: string;
  onBack: () => void;
  emailTemplate: { subject: string; body: string };
}

const MPList: React.FC<MPListProps> = ({ members, plz, onBack, emailTemplate }) => {
  const [selectedMP, setSelectedMP] = useState<MP | null>(null);
  const [copied, setCopied] = useState(false);

  const getPartyColor = (party: string) => {
    const p = party.toLowerCase();
    if (p.includes('spd')) return 'bg-red-600';
    if (p.includes('cdu') || p.includes('csu')) return 'bg-black';
    if (p.includes('grün')) return 'bg-green-600';
    if (p.includes('fdp')) return 'bg-yellow-400 text-black';
    if (p.includes('afd')) return 'bg-blue-500';
    if (p.includes('linke')) return 'bg-pink-600';
    return 'bg-zinc-500';
  };

  const getPersonalizedEmail = (mp: MP) => {
    const lastName = mp.name.split(' ').pop() || mp.name;
    let salutation;
    
    if (mp.gender === 'male') {
      salutation = `Sehr geehrter Herr ${lastName}`;
    } else if (mp.gender === 'female') {
      salutation = `Sehr geehrte Frau ${lastName}`;
    } else {
      salutation = 'Sehr geehrtes Mitglied des Deutschen Bundestages';
    }

    return `Betreff:\n${emailTemplate.subject}\n////\nNachricht:\n\n${salutation},\n\n${emailTemplate.body.split('\n').slice(2).join('\n')}`;
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-2xl font-bold">{members.length} Abgeordnete gefunden</h3>
          <p className="text-sm text-zinc-600">PLZ: {plz}</p>
        </div>
        <button onClick={onBack} className="text-sm text-zinc-500 underline hover:text-zinc-700">
          PLZ ändern
        </button>
      </div>

      {/* MP Cards */}
      <div className="space-y-4">
        {members.map((mp, idx) => (
          <div key={idx} className="bg-white border border-zinc-200 rounded-lg p-6 hover:shadow-lg transition-all">
            <div className="flex items-start gap-4">
              <img 
                src={mp.image_url || 'https://via.placeholder.com/80?text=No+Image'} 
                alt={mp.name}
                className="w-20 h-20 rounded-full object-cover border-2 border-zinc-200"
                onError={(e) => e.currentTarget.src = 'https://via.placeholder.com/80?text=No+Image'}
              />
              <div className="flex-1">
                <h4 className="text-xl font-bold text-zinc-900">{mp.name}</h4>
                <span className={`inline-block px-3 py-1 rounded-full text-sm font-bold mt-1 ${getPartyColor(mp.party)} text-white`}>
                  {mp.party}
                </span>
                <p className="text-sm text-zinc-600 mt-2">{mp.constituency}</p>
                {mp.contact_url ? (
                  <button 
                    onClick={() => setSelectedMP(mp)}
                    className="mt-3 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-all inline-flex items-center gap-2"
                  >
                    <Mail size={16} /> Kontakt aufnehmen
                  </button>
                ) : (
                  <p className="mt-3 text-sm text-zinc-400">⚠️ Kontakt-URL nicht verfügbar</p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Email Modal */}
      {selectedMP && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" onClick={() => setSelectedMP(null)}>
          <div className="bg-zinc-900 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-auto" onClick={(e) => e.stopPropagation()}>
            <div className="p-8">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold text-white">✉️ E-Mail an {selectedMP.name}</h3>
                  <p className="text-zinc-400 text-sm mt-1">{selectedMP.party} • {selectedMP.constituency}</p>
                </div>
                <button onClick={() => setSelectedMP(null)} className="text-zinc-400 hover:text-white">
                  <X size={24} />
                </button>
              </div>

              <div className="bg-red-600/10 border border-red-600/30 rounded-lg p-4 mb-6">
                <h4 className="font-bold text-red-400 mb-2">📋 Anleitung:</h4>
                <ol className="text-sm text-zinc-300 space-y-2">
                  <li><strong>1.</strong> Bearbeiten Sie die Nachricht nach Bedarf</li>
                  <li><strong>2.</strong> Klicken Sie auf "Nachricht kopieren"</li>
                  <li><strong>3.</strong> Klicken Sie auf "Zum Kontaktformular"</li>
                  <li><strong>4.</strong> Fügen Sie die Nachricht im Bundestag-Formular ein (Strg+V)</li>
                </ol>
              </div>

              <div className="bg-zinc-800 rounded-lg border border-zinc-700 p-4 mb-6">
                <textarea 
                  id="emailText"
                  defaultValue={getPersonalizedEmail(selectedMP)}
                  className="w-full min-h-[350px] bg-transparent text-zinc-100 font-mono text-sm resize-y border-none outline-none"
                />
              </div>

              <div className="flex gap-3">
                <button 
                  onClick={() => {
                    const textarea = document.getElementById('emailText') as HTMLTextAreaElement;
                    copyToClipboard(textarea.value);
                  }}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-all flex items-center justify-center gap-2"
                >
                  {copied ? <Check size={20} /> : <Copy size={20} />}
                  {copied ? 'Kopiert!' : '1. Nachricht kopieren'}
                </button>
                <button 
                  onClick={() => {
                    if (selectedMP.contact_url) {
                      window.open(selectedMP.contact_url, '_blank');
                    }
                  }}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition-all flex items-center justify-center gap-2"
                >
                  <Mail size={20} /> 2. Zum Kontaktformular
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MPList;
