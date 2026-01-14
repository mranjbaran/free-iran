import React, { useState } from 'react';
import Hero from './components/Hero';
import SituationReport from './components/SituationReport';
import ActionCenter from './components/ActionCenter';
import Footer from './components/Footer';
import { Language } from './types';
import { translations } from './translations';

function App() {
  const [lang, setLang] = useState<Language>('en');
  const t = translations[lang];
  const dir = lang === 'fa' ? 'rtl' : 'ltr';
  const fontClass = lang === 'fa' ? 'font-sans' : 'font-sans'; // System fonts handle Farsi well usually

  return (
    <main 
      className={`min-h-screen bg-zinc-950 text-white selection:bg-red-500 selection:text-white ${fontClass}`}
      dir={dir}
    >
      <Hero lang={lang} setLang={setLang} t={t.hero} />
      <SituationReport t={t.report} stats={t.stats} />
      <ActionCenter t={t.action} />
      <Footer t={t.footer} />
    </main>
  );
}

export default App;