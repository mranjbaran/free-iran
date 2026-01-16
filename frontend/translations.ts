import { Translation } from './types';

export const translations: Record<string, Translation> = {
  en: {
    hero: {
      badge: "Urgent: Day 20 - Internet Blackout",
      title: "STOP THE ",
      highlight: "BLOODSHED",
      description: "3,090 confirmed deaths; 3,882 under review. 22,123 arrests. Internet blackout has passed 190 hours.",
      ctaAction: "Act Now: Contact Bundestag",
      ctaRead: "Read Situation Report"
    },
    stats: {
      deaths: "3,090",
      deathsLabel: "Confirmed deaths",
      deathsSub: "Includes 19 children; 3,882 under review",
      arrests: "22,123",
      arrestsLabel: "Citizens Arrested",
      arrestsSub: "132 forced confessions broadcast",
      gatherings: "619",
      gatheringsLabel: "Recorded Protests",
      gatheringsSub: "Across 187 cities & 31 provinces"
    },
    report: {
      title: "What is Happening?",
      description: "Day 20: the internet blackout has exceeded 190 hours. HRANA reports 3,090 confirmed deaths, 22,123 arrests, and 2,055 severe injuries while 3,882 cases remain under review. Documentation is hampered, prompting calls for citizen evidence.",
      quote: "The deliberate shutdown of the internet has disrupted access to vital information... creating conditions for the continued excessive use of force.",
      quoteAuthor: "Human Rights Activists in Iran (HRANA)",
      timelineTitle: "Timeline of Repression",
      timeline: [
        { date: "Day 20", title: "Blackout >190 hours", description: "Fixed and mobile internet remain restricted; messaging and calls disrupted." },
        { date: "International", title: "Rising pressure", description: "MSC disinvites officials; governments warn citizens; G7 condemned the crackdown." },
        { date: "Accountability", title: "Evidence collection", description: "HRANA and Spreading Justice urge citizens to document abuses for legal action." }
      ],
      victimsTitle: "The Toll",
      victimsText: "3,090 confirmed deaths (2,885 protesters, 165 security, 21 civilians); at least 19 children. 2,055 severe injuries; 3,882 deaths under review; 22,123 arrests; 132 forced confessions broadcast.",
      impactAreas: "Impacted Provinces",
      impactAreasList: ["All 31 Provinces", "Tehran", "Kurdistan", "Sistan & Baluchestan"],
      blackoutTitle: "Information Blackout",
      blackoutText: "The shutdown, now beyond 190 hours, blocks calls, banking, and media. It hides evidence of abuses and complicates tracing detainees."
    },
    action: {
      title: "Germany: Take Action",
      subtitle: "If you live in Germany, your voice matters. Contact your Bundestag Member (Abgeordnete) and demand immediate sanctions and diplomatic pressure.",
      howItWorksTitle: "How it works",
      steps: [
        "Enter your German Postal Code (PLZ).",
        "Find your specific Bundestag Member.",
        "Copy the template and send the email."
      ],
      disclaimer: "We do not store your data. This tool connects you to official directories.",
      identifyTitle: "Identify your Representative",
      plzLabel: "German Postal Code (PLZ)",
      plzPlaceholder: "e.g., 10117",
      plzHint: "Enter the PLZ where you are registered to vote.",
      startBtn: "Start",
      sendTitle: "Send Your Message",
      changePlz: "Change PLZ",
      step1Title: "Step 1: Find your MP",
      step1Text: "Click below to open abgeordnetenwatch.de for your district.",
      findMpBtn: "Find Bundestag Member",
      step2Title: "Step 2: Copy Template",
      step2Text: "Don't forget to add your name and address.",
      openClientBtn: "Open Email Client",
      searchingMsg: "Searching... This may take up to 10 seconds.",
      emailTemplate: {
        subject: "DRINGEND: Staatsgewalt im Iran – Bitte handeln Sie",
        body: `Sehr geehrte Damen und Herren Abgeordnete,

      Ich wende mich als Bürger*in Ihres Wahlkreises an Sie mit großer Sorge über die eskalierende Gewalt des iranischen Regimes gegen die eigene Bevölkerung.

      Seit Ende Dezember 2025 kommt es im Iran landesweit zu massiver staatlicher Repression. Verlässliche Berichte internationaler Menschenrechtsorganisationen dokumentieren tausende Tote, zehntausende willkürliche Verhaftungen sowie gezielte Verstümmelungen von Demonstrierenden. Der vollständige Internet-Blackout dient offenbar dazu, schwere Menschenrechtsverbrechen ohne internationale Beobachtung zu begehen.

      Als meine Vertretung im Deutschen Bundestag bitte ich Sie eindringlich, sich für konkrete Maßnahmen einzusetzen, insbesondere:

      1. die zeitnahe Einstufung der IRGC als Terrororganisation auf EU-Ebene,
      2. ein Ende der politischen und wirtschaftlichen Normalisierung mit dem iranischen Regime,
      3. die Übernahme politischer Patenschaften für Inhaftierte, um Hinrichtungen durch öffentliche Aufmerksamkeit zu verhindern.

      Die Menschen im Iran kämpfen unter Lebensgefahr für Freiheit und Würde. Ich erwarte, dass Deutschland diesen Einsatz nicht nur rhetorisch, sondern politisch unterstützt.

      Ich bitte Sie um eine kurze persönliche Stellungnahme, welche dieser Schritte Sie konkret unterstützen werden.`
      }
    },
    footer: {
      source: "Data source: HRANA (Human Rights Activists News Agency) - Day 20 Report.",
      disclaimer: "Independent solidarity project. Not affiliated with any political party."
    }
  },
  de: {
    hero: {
      badge: "Dringend: Tag 20 - Internet-Blackout",
      title: "STOPPT DAS ",
      highlight: "BLUTVERGIEẞEN",
      description: "3.090 bestätigte Tote; 3.882 Fälle in Prüfung. 22.123 Festnahmen. Der Blackout dauert über 190 Stunden an.",
      ctaAction: "Jetzt handeln: Bundestag kontaktieren",
      ctaRead: "Lagebericht lesen"
    },
    stats: {
      deaths: "3.090",
      deathsLabel: "Bestätigte Todesfälle",
      deathsSub: "Darunter 19 Kinder; 3.882 Fälle in Prüfung",
      arrests: "22.123",
      arrestsLabel: "Verhaftungen",
      arrestsSub: "132 erzwungene Geständnisse ausgestrahlt",
      gatherings: "619",
      gatheringsLabel: "Erfasste Proteste",
      gatheringsSub: "In 187 Städten & 31 Provinzen"
    },
    report: {
      title: "Was passiert im Iran?",
      description: "Tag 20: Der Internet-Blackout überschreitet 190 Stunden. HRANA meldet 3.090 bestätigte Tote, 22.123 Festnahmen und 2.055 Schwerverletzte; 3.882 Fälle werden noch geprüft. Die Dokumentation ist erschwert, daher ruft HRANA zu Bürger*innen-Berichten auf.",
      quote: "Die absichtliche Abschaltung des Internets hat den Zugang zu lebenswichtigen Informationen unterbrochen... und schafft Bedingungen für weitere exzessive Gewaltanwendung.",
      quoteAuthor: "Human Rights Activists in Iran (HRANA)",
      timelineTitle: "Chronologie der Unterdrückung",
      timeline: [
        { date: "Tag 20", title: "Blackout >190 Std.", description: "Festnetz und Mobilfunk bleiben eingeschränkt; Messenger und Anrufe gestört." },
        { date: "International", title: "Wachsender Druck", description: "MSC lädt Funktionäre aus; Staaten warnen Bürger; G7 verurteilt das Vorgehen." },
        { date: "Rechenschaft", title: "Beweissicherung", description: "HRANA und Spreading Justice sammeln Beweise für rechtliche Schritte." }
      ],
      victimsTitle: "Die Opfer",
      victimsText: "3.090 bestätigte Tote (2.885 Demonstrierende, 165 Sicherheitskräfte, 21 Unbeteiligte); mind. 19 Kinder. 2.055 Schwerverletzte; 3.882 Todesfälle werden geprüft; 22.123 Festnahmen; 132 erzwungene Geständnisse.",
      impactAreas: "Betroffene Gebiete",
      impactAreasList: ["Alle 31 Provinzen", "Teheran", "Kurdistan", "Sistan & Belutschistan"],
      blackoutTitle: "Informationssperre",
      blackoutText: "Der nun über 190 Stunden andauernde Shutdown blockiert Anrufe, Banking und Medien. Er erschwert die Nachverfolgung von Festnahmen und verschleiert Beweise."
    },
    action: {
      title: "Deutschland: Handeln Sie",
      subtitle: "Wenn Sie in Deutschland leben, zählt Ihre Stimme. Kontaktieren Sie Ihre Bundestagsabgeordneten und fordern Sie sofortigen Druck auf das Regime.",
      howItWorksTitle: "So funktioniert es",
      steps: [
        "Geben Sie Ihre Postleitzahl (PLZ) ein.",
        "Finden Sie Ihre Abgeordneten.",
        "Kopieren Sie die Vorlage und senden Sie die E-Mail."
      ],
      disclaimer: "Wir speichern keine Daten. Dieses Tool leitet zu offiziellen Verzeichnissen weiter.",
      identifyTitle: "Ihren Wahlkreis finden",
      plzLabel: "Deutsche Postleitzahl (PLZ)",
      plzPlaceholder: "z.B. 10117",
      plzHint: "Geben Sie die PLZ Ihres Wohnorts ein.",
      startBtn: "Starten",
      sendTitle: "Nachricht senden",
      changePlz: "PLZ ändern",
      step1Title: "Schritt 1: Abgeordnete finden",
      step1Text: "Klicken Sie hier, um abgeordnetenwatch.de für Ihren Wahlkreis zu öffnen.",
      findMpBtn: "Abgeordnete finden",
      step2Title: "Schritt 2: Vorlage kopieren",
      step2Text: "Vergessen Sie nicht, Ihren Namen und Ihre Adresse hinzuzufügen.",
      openClientBtn: "E-Mail-Programm öffnen",
      searchingMsg: "Suche läuft... Dies kann bis zu 10 Sekunden dauern.",
      emailTemplate: {
        subject: "DRINGEND: Systematische Staatsgewalt im Iran – Bitte handeln",
        body: `Sehr geehrte Damen und Herren Abgeordnete,

      Ich wende mich als Bürger*in Ihres Wahlkreises an Sie mit großer Sorge über die eskalierende Gewalt des iranischen Regimes gegen die eigene Bevölkerung.

      Seit Ende Dezember 2025 kommt es im Iran landesweit zu massiver staatlicher Repression. Verlässliche Berichte internationaler Menschenrechtsorganisationen dokumentieren tausende Tote, zehntausende willkürliche Verhaftungen sowie gezielte Verstümmelungen von Demonstrierenden. Der vollständige Internet-Blackout dient offenbar dazu, schwere Menschenrechtsverbrechen ohne internationale Beobachtung zu begehen.

      Als meine Vertretung im Deutschen Bundestag bitte ich Sie eindringlich, sich für konkrete Maßnahmen einzusetzen, insbesondere:

      1. die zeitnahe Einstufung der IRGC als Terrororganisation auf EU-Ebene,
      2. ein Ende der politischen und wirtschaftlichen Normalisierung mit dem iranischen Regime,
      3. die Übernahme politischer Patenschaften für Inhaftierte, um Hinrichtungen durch öffentliche Aufmerksamkeit zu verhindern.

      Die Menschen im Iran kämpfen unter Lebensgefahr für Freiheit und Würde. Ich erwarte, dass Deutschland diesen Einsatz nicht nur rhetorisch, sondern politisch unterstützt.

      Ich bitte Sie um eine kurze persönliche Stellungnahme, welche dieser Schritte Sie konkret unterstützen werden.`
      }
    },
    footer: {
      source: "Datenquelle: HRANA (Human Rights Activists News Agency) - Bericht Tag 20.",
      disclaimer: "Unabhängiges Solidaritätsprojekt. Keine Parteizugehörigkeit."
    }
  },
  fa: {
    hero: {
      badge: "فوری: روز ۲۰ - قطع سراسری اینترنت",
      title: "",
      highlight: "توقف خونریزی",
      description: "۳٬۰۹۰ مرگ تأییدشده؛ ۳٬۸۸۲ مورد در حال بررسی. ۲۲٬۱۲۳ بازداشت. قطع اینترنت بیش از ۱۹۰ ساعت ادامه دارد.",
      ctaAction: "اقدام کنید: تماس با پارلمان آلمان",
      ctaRead: "گزارش وضعیت"
    },
    stats: {
      deaths: "۳٬۰۹۰",
      deathsLabel: "مرگ تأییدشده",
      deathsSub: "۱۹ کودک؛ ۳٬۸۸۲ مورد در حال بررسی",
      arrests: "۲۲٬۱۲۳",
      arrestsLabel: "بازداشت‌شدگان",
      arrestsSub: "پخش ۱۳۲ اعتراف اجباری",
      gatherings: "۶۱۹",
      gatheringsLabel: "تجمعات ثبت‌شده",
      gatheringsSub: "در ۱۸۷ شهر و ۳۱ استان"
    },
    report: {
      title: "چه اتفاقی در حال رخ دادن است؟",
      description: "روز ۲۰: قطع اینترنت بیش از ۱۹۰ ساعت طول کشیده است. هرانا ۳٬۰۹۰ مرگ تأییدشده، ۲۲٬۱۲۳ بازداشت و ۲٬۰۵۵ مجروح شدید گزارش می‌کند؛ ۳٬۸۸۲ مورد مرگ هنوز در حال بررسی است. مستندسازی سخت شده و هرانا از شاهدان می‌خواهد شواهد ارسال کنند.",
      quote: "قطع عمدی اینترنت دسترسی به اطلاعات حیاتی را مختل کرده... و شرایط را برای ادامه استفاده افراطی از زور فراهم کرده است.",
      quoteAuthor: "مجموعه فعالان حقوق بشر در ایران (هرانا)",
      timelineTitle: "گاه‌شمار سرکوب",
      timeline: [
        { date: "روز ۲۰", title: "بیش از ۱۹۰ ساعت", description: "اینترنت ثابت و همراه محدود است؛ پیام‌رسان و تماس‌ها مختل شده‌اند." },
        { date: "واکنش جهانی", title: "افزایش فشار", description: "کنفرانس امنیتی مونیخ دعوت را لغو کرد؛ دولت‌ها به شهروندان هشدار دادند؛ بیانیه G7 محکوم کرد." },
        { date: "پاسخگویی", title: "جمع‌آوری شواهد", description: "هرانا و Spreading Justice برای اقدام حقوقی به مستندسازی مردمی تکیه می‌کنند." }
      ],
      victimsTitle: "آمار قربانیان",
      victimsText: "۳٬۰۹۰ مرگ تأییدشده (۲٬۸۸۵ معترض، ۱۶۵ نیروی امنیتی، ۲۱ غیرمعترض)؛ حداقل ۱۹ کودک. ۲٬۰۵۵ مجروح شدید؛ ۳٬۸۸۲ مرگ در حال بررسی؛ ۲۲٬۱۲۳ بازداشت؛ ۱۳۲ اعتراف اجباری پخش‌شده.",
      impactAreas: "مناطق تحت تاثیر",
      impactAreasList: ["تمامی ۳۱ استان", "تهران", "کردستان", "سیستان و بلوچستان"],
      blackoutTitle: "بایکوت خبری",
      blackoutText: "قطع بیش از ۱۹۰ ساعته تماس‌ها، بانکداری و رسانه را مختل کرده و پیگیری بازداشتی‌ها و جمع‌آوری شواهد را دشوار می‌کند."
    },
    action: {
      title: "آلمان: اقدام کنید",
      subtitle: "اگر در آلمان زندگی می‌کنید، صدای شما اهمیت دارد. با نماینده بوندستاگ (مجلس) خود تماس بگیرید و خواستار فشار فوری بر رژیم شوید.",
      howItWorksTitle: "چگونه کار می‌کند",
      steps: [
        "کد پستی (PLZ) خود در آلمان را وارد کنید.",
        "نماینده خود را پیدا کنید.",
        "متن نامه را کپی کرده و ایمیل را ارسال کنید."
      ],
      disclaimer: "ما اطلاعات شما را ذخیره نمی‌کنیم. این ابزار شما را به دایرکتوری‌های رسمی متصل می‌کند.",
      identifyTitle: "شناسایی نماینده شما",
      plzLabel: "کد پستی آلمان (PLZ)",
      plzPlaceholder: "مثال: 10117",
      plzHint: "کد پستی محل سکونت خود در آلمان را وارد کنید.",
      startBtn: "شروع",
      sendTitle: "ارسال پیام",
      changePlz: "تغییر کد پستی",
      step1Title: "گام ۱: یافتن نماینده",
      step1Text: "برای باز کردن سایت abgeordnetenwatch.de برای منطقه خود کلیک کنید.",
      findMpBtn: "یافتن نماینده مجلس",
      step2Title: "گام ۲: کپی متن نامه",
      step2Text: "فراموش نکنید نام و آدرس خود را اضافه کنید.",
      openClientBtn: "باز کردن ایمیل",
      searchingMsg: "در حال جستجو... ممکن است تا ۱۰ ثانیه طول بکشد.",
      emailTemplate: {
        subject: "فوری: خشونت دولتی در ایران – لطفاً اقدام کنید",
        body: `نماینده محترم مجلس،

      به دلیل خشونت گسترده در ایران می‌نویسم: ۳٬۰۹۰ مرگ تأییدشده (حداقل ۱۹ کودک)، ۳٬۸۸۲ مورد در حال بررسی، ۲٬۰۵۵ مجروح شدید، ۲۲٬۱۲۳ بازداشت و قطع اینترنت سراسری بیش از ۱۹۰ ساعت که مستندسازی را مختل کرده است.

      خواهش می‌کنم از این اقدامات حمایت کنید:
      ۱) قرار دادن سپاه در فهرست تروریستی اتحادیه اروپا.
      ۲) تعلیق روابط دیپلماتیک و اقتصادی با نهادهای وابسته به حکومت.
      ۳) پذیرش سرپرستی سیاسی بازداشت‌شدگان برای جلوگیری از اعدام.

      لطفاً بگویید کدام‌یک از این اقدامات را در پارلمان پیگیری می‌کنید؟`
      }
    },
    footer: {
      source: "منبع داده: هرانا (خبرگزاری فعالان حقوق بشر) - گزارش روز ۲۰.",
      disclaimer: "پروژه همبستگی مستقل. وابسته به هیچ حزب سیاسی نیست."
    }
  }
};