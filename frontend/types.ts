export type Language = 'en' | 'de' | 'fa';

export interface MP {
  name: string;
  party: string;
  constituency: string;
  image_url?: string;
  contact_url?: string;
  gender?: string;
  profile_url?: string;
}

export interface TimelineEvent {
  date: string;
  title: string;
  description: string;
}

export interface Stat {
  value: string;
  label: string;
}

export interface EmailTemplate {
  subject: string;
  body: string;
}

export interface Translation {
  hero: {
    badge: string;
    title: string;
    highlight: string;
    description: string;
    ctaAction: string;
    ctaRead: string;
  };
  stats: {
    deaths: string;
    deathsLabel: string;
    deathsSub: string;
    arrests: string;
    arrestsLabel: string;
    arrestsSub: string;
    gatherings: string;
    gatheringsLabel: string;
    gatheringsSub: string;
  };
  report: {
    title: string;
    description: string;
    quote: string;
    quoteAuthor: string;
    timelineTitle: string;
    timeline: TimelineEvent[];
    victimsTitle: string;
    victimsText: string;
    impactAreas: string;
    impactAreasList: string[];
    blackoutTitle: string;
    blackoutText: string;
  };
  action: {
    title: string;
    subtitle: string;
    howItWorksTitle: string;
    steps: string[];
    disclaimer: string;
    identifyTitle: string;
    plzLabel: string;
    plzPlaceholder: string;
    plzHint: string;
    startBtn: string;
    sendTitle: string;
    changePlz: string;
    step1Title: string;
    step1Text: string;
    findMpBtn: string;
    step2Title: string;
    step2Text: string;
    openClientBtn: string;
    searchingMsg: string;
    emailTemplate: EmailTemplate;
  };
  footer: {
    source: string;
    disclaimer: string;
  };
}