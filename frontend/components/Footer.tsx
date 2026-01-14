import React from 'react';
import { Translation } from '../types';

interface FooterProps {
  t: Translation['footer'];
}

const Footer: React.FC<FooterProps> = ({ t }) => {
  return (
    <footer className="bg-zinc-950 text-zinc-500 py-12 border-t border-zinc-900">
      <div className="container mx-auto px-4 text-center space-y-4">
        <p className="text-sm">
          {t.source}
        </p>
        <p className="text-xs max-w-2xl mx-auto opacity-60">
          {t.disclaimer}
        </p>
      </div>
    </footer>
  );
};

export default Footer;