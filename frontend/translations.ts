import { Translation } from './types';

export const translations: Record<string, Translation> = {
  en: {
    hero: {
      badge: "Urgent: Day 17 - Internet Blackout",
      title: "STOP THE ",
      highlight: "BLOODSHED",
      description: "2,400+ protesters killed. 18,000+ arrested. Internet acts as a weapon of silence. The world must act now.",
      ctaAction: "Act Now: Contact Bundestag",
      ctaRead: "Read Situation Report"
    },
    stats: {
      deaths: "2,403",
      deathsLabel: "Protesters Killed",
      deathsSub: "Includes 12 children & 9 bystanders",
      arrests: "18,434",
      arrestsLabel: "Citizens Arrested",
      arrestsSub: "97 forced confessions broadcast",
      gatherings: "614",
      gatheringsLabel: "Protest Gatherings",
      gatheringsSub: "Across 187 cities & 31 provinces"
    },
    report: {
      title: "What is Happening?",
      description: "As of Day 17, Iran is under a near-total communications blackout. HRANA reports a massive surge in violence. Security forces are using war-grade weaponry against unarmed civilians while the internet shutdown prevents real-time verification.",
      quote: "The deliberate shutdown of the internet has disrupted access to vital information... creating conditions for the continued excessive use of force.",
      quoteAuthor: "Human Rights Activists in Iran (HRANA)",
      timelineTitle: "Timeline of Repression",
      timeline: [
        { date: "Day 1-17", title: "Nationwide Uprising", description: "Protests spread to 187 cities despite severe repression." },
        { date: "Ongoing", title: "Digital Darkness", description: "Internet blackout limits access to medical services and verification." },
        { date: "Latest", title: "Diplomatic Escalation", description: "EU condemns violence; Canada advises citizens to leave; UN calls for restraint." }
      ],
      victimsTitle: "The Toll",
      victimsText: "Casualties have skyrocketed. 2,403 confirmed deaths. Hospitals are unsafe zones. 1,134 people have severe injuries but fear seeking help due to arrests at medical centers.",
      impactAreas: "Impacted Provinces",
      impactAreasList: ["All 31 Provinces", "Tehran", "Kurdistan", "Sistan & Baluchestan"],
      blackoutTitle: "Information Blackout",
      blackoutText: "The severing of communications is a strategic tactic to hide atrocities. Verifiable evidence is limited, but aggregated data confirms a massacre."
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
      searchingMsg: "Searching... This may take 3-5 seconds.",
      emailTemplate: {
        subject: "DRINGEND: Stoppen Sie das Massaker im Iran",
        body: `Sehr geehrte Damen und Herren Abgeordnete,

als Bürger/in Ihres Wahlkreises schreibe ich Ihnen, um mein Entsetzen über die Gräueltaten im Iran auszudrücken.

Glaubwürdige Berichte von HRANA bestätigen, dass bis zum 17. Protesttag über 2.403 Demonstranten getötet und 18.434 verhaftet wurden. Das iranische Regime nutzt einen totalen Internet-Blackout, um diese Verbrechen gegen die Menschlichkeit zu verbergen.

Deutschland darf nicht schweigen. Als meine Vertretung im Bundestag fordere ich Sie auf:
1. Fordern Sie ein sofortiges Ende des Blutvergießens und die Wiederherstellung des Internets.
2. Setzen Sie sich für scharfe EU-Sanktionen gegen die IRGC und Verantwortliche ein.
3. Unterstützen Sie die Ausweisung iranischer Botschafter, bis die Gewalt endet.

Bitte handeln Sie jetzt.

Mit freundlichen Grüßen,
[Ihr Name]
[Ihre Stadt/PLZ]`
      }
    },
    footer: {
      source: "Data source: HRANA (Human Rights Activists News Agency) - Day 17 Report.",
      disclaimer: "Independent solidarity project. Not affiliated with any political party."
    }
  },
  de: {
    hero: {
      badge: "Dringend: Tag 17 - Internet-Blackout",
      title: "STOPPT DAS ",
      highlight: "BLUTVERGIEẞEN",
      description: "2.400+ Demonstranten getötet. 18.000+ verhaftet. Das Regime nutzt das Internet als Waffe. Die Welt muss jetzt handeln.",
      ctaAction: "Jetzt handeln: Bundestag kontaktieren",
      ctaRead: "Lagebericht lesen"
    },
    stats: {
      deaths: "2.403",
      deathsLabel: "Getötete Demonstranten",
      deathsSub: "Darunter 12 Kinder & 9 Unbeteiligte",
      arrests: "18.434",
      arrestsLabel: "Verhaftungen",
      arrestsSub: "97 erzwungene Geständnisse",
      gatherings: "614",
      gatheringsLabel: "Protestversammlungen",
      gatheringsSub: "In 187 Städten & 31 Provinzen"
    },
    report: {
      title: "Was passiert im Iran?",
      description: "Am 17. Tag herrscht im Iran ein fast vollständiger Kommunikations-Blackout. HRANA berichtet von einem massiven Anstieg der Gewalt. Sicherheitskräfte setzen Kriegswaffen gegen unbewaffnete Zivilisten ein.",
      quote: "Die absichtliche Abschaltung des Internets hat den Zugang zu lebenswichtigen Informationen unterbrochen... und schafft Bedingungen für weitere exzessive Gewaltanwendung.",
      quoteAuthor: "Human Rights Activists in Iran (HRANA)",
      timelineTitle: "Chronologie der Unterdrückung",
      timeline: [
        { date: "Tag 1-17", title: "Landesweite Aufstände", description: "Proteste in 187 Städten trotz brutaler Repression." },
        { date: "Aktuell", title: "Digitale Dunkelheit", description: "Internet-Blackout verhindert Verifizierung und medizinische Hilfe." },
        { date: "Reaktionen", title: "Diplomatische Eskalation", description: "EU verurteilt Gewalt; Kanada rät zur Ausreise; UN fordert Zurückhaltung." }
      ],
      victimsTitle: "Die Opfer",
      victimsText: "Die Opferzahlen sind explodiert. 2.403 bestätigte Todesfälle. Krankenhäuser sind unsichere Zonen. 1.134 Menschen haben schwere Verletzungen, meiden aber aus Angst vor Verhaftung medizinische Hilfe.",
      impactAreas: "Betroffene Gebiete",
      impactAreasList: ["Alle 31 Provinzen", "Teheran", "Kurdistan", "Sistan & Belutschistan"],
      blackoutTitle: "Informationssperre",
      blackoutText: "Die Unterbrechung der Kommunikation ist eine strategische Taktik, um Gräueltaten zu verbergen. Beweise sind begrenzt, aber die Daten bestätigen ein Massaker."
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
      searchingMsg: "Suche läuft... Dies kann 3-5 Sekunden dauern.",
      emailTemplate: {
        subject: "DRINGEND: Stoppen Sie das Massaker im Iran",
        body: `Sehr geehrte Damen und Herren Abgeordnete,

als Bürger/in Ihres Wahlkreises schreibe ich Ihnen, um mein Entsetzen über die Gräueltaten im Iran auszudrücken.

Glaubwürdige Berichte von HRANA bestätigen, dass bis zum 17. Protesttag über 2.403 Demonstranten getötet und 18.434 verhaftet wurden. Das iranische Regime nutzt einen totalen Internet-Blackout, um diese Verbrechen gegen die Menschlichkeit zu verbergen.

Deutschland darf nicht schweigen. Als meine Vertretung im Bundestag fordere ich Sie auf:
1. Fordern Sie ein sofortiges Ende des Blutvergießens und die Wiederherstellung des Internets.
2. Setzen Sie sich für scharfe EU-Sanktionen gegen die IRGC und Verantwortliche ein.
3. Unterstützen Sie die Ausweisung iranischer Botschafter, bis die Gewalt endet.

Bitte handeln Sie jetzt.

Mit freundlichen Grüßen,
[Ihr Name]
[Ihre Stadt/PLZ]`
      }
    },
    footer: {
      source: "Datenquelle: HRANA (Human Rights Activists News Agency) - Bericht Tag 17.",
      disclaimer: "Unabhängiges Solidaritätsprojekt. Keine Parteizugehörigkeit."
    }
  },
  fa: {
    hero: {
      badge: "فوری: روز ۱۷ - قطع سراسری اینترنت",
      title: "",
      highlight: "توقف خونریزی",
      description: "بیش از ۲۴۰۰ کشته. ۱۸۰۰۰ بازداشتی. اینترنت به سلاحی برای سکوت تبدیل شده است. جهان باید همین حالا اقدام کند.",
      ctaAction: "اقدام کنید: تماس با پارلمان آلمان",
      ctaRead: "گزارش وضعیت"
    },
    stats: {
      deaths: "۲۴۰۳",
      deathsLabel: "کشته‌شدگان",
      deathsSub: "شامل ۱۲ کودک و ۹ عابر",
      arrests: "۱۸۴۳۴",
      arrestsLabel: "بازداشت‌شدگان",
      arrestsSub: "پخش ۹۷ اعتراف اجباری",
      gatherings: "۶۱۴",
      gatheringsLabel: "تجمع اعتراضی",
      gatheringsSub: "در ۱۸۷ شهر و ۳۱ استان"
    },
    report: {
      title: "چه اتفاقی در حال رخ دادن است؟",
      description: "در هفدهمین روز، ایران در خاموشی تقریباً کامل ارتباطی به سر می‌برد. هرانا گزارش می‌دهد که خشونت به شدت افزایش یافته است. نیروهای امنیتی از سلاح‌های جنگی علیه غیرنظامیان استفاده می‌کنند در حالی که قطع اینترنت مانع از اطلاع‌رسانی می‌شود.",
      quote: "قطع عمدی اینترنت دسترسی به اطلاعات حیاتی را مختل کرده... و شرایط را برای ادامه استفاده افراطی از زور فراهم کرده است.",
      quoteAuthor: "مجموعه فعالان حقوق بشر در ایران (هرانا)",
      timelineTitle: "گاه‌شمار سرکوب",
      timeline: [
        { date: "روز ۱-۱۷", title: "خیزش سراسری", description: "گسترش اعتراضات به ۱۸۷ شهر با وجود سرکوب شدید." },
        { date: "وضعیت فعلی", title: "تاریکی دیجیتال", description: "قطع اینترنت دسترسی به خدمات پزشکی و تایید اخبار را مختل کرده است." },
        { date: "واکنش‌ها", title: "فشار دیپلماتیک", description: "اتحادیه اروپا خشونت را محکوم کرد؛ کانادا به شهروندانش هشدار خروج داد." }
      ],
      victimsTitle: "آمار قربانیان",
      victimsText: "آمار تلفات به شدت افزایش یافته است. ۲۴۰۳ مرگ تایید شده. بیمارستان‌ها ناامن هستند. ۱۱۳۴ نفر به شدت مجروح شده‌اند اما از ترس بازداشت به مراکز درمانی مراجعه نمی‌کنند.",
      impactAreas: "مناطق تحت تاثیر",
      impactAreasList: ["تمامی ۳۱ استان", "تهران", "کردستان", "سیستان و بلوچستان"],
      blackoutTitle: "بایکوت خبری",
      blackoutText: "قطع ارتباطات تاکتیکی استراتژیک برای پنهان کردن جنایات است. شواهد محدود است، اما داده‌های تجمیعی یک کشتار را تایید می‌کند."
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
      searchingMsg: "در حال جستجو... ممکن است ۳ تا ۵ ثانیه طول بکشد.",
      emailTemplate: {
        subject: "DRINGEND: Stoppen Sie das Massaker im Iran",
        body: `Sehr geehrte Damen und Herren Abgeordnete,

als Bürger/in Ihres Wahlkreises schreibe ich Ihnen, um mein Entsetzen über die Gräueltaten im Iran auszudrücken.

Glaubwürdige Berichte von HRANA bestätigen, dass bis zum 17. Protesttag über 2.403 Demonstranten getötet und 18.434 verhaftet wurden. Das iranische Regime nutzt einen totalen Internet-Blackout, um diese Verbrechen gegen die Menschlichkeit zu verbergen.

Deutschland darf nicht schweigen. Als meine Vertretung im Bundestag fordere ich Sie auf:
1. Fordern Sie ein sofortiges Ende des Blutvergießens und die Wiederherstellung des Internets.
2. Setzen Sie sich für scharfe EU-Sanktionen gegen die IRGC und Verantwortliche ein.
3. Unterstützen Sie die Ausweisung iranischer Botschafter, bis die Gewalt endet.

Bitte handeln Sie jetzt.

Mit freundlichen Grüßen,
[Ihr Name]
[Ihre Stadt/PLZ]`
      }
    },
    footer: {
      source: "منبع داده: هرانا (خبرگزاری فعالان حقوق بشر) - گزارش روز ۱۷.",
      disclaimer: "پروژه همبستگی مستقل. وابسته به هیچ حزب سیاسی نیست."
    }
  }
};