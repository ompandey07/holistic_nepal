/**
 * Holistic Hospital & Clinical Services - Bilingual Translation Engine
 * Shared across /hospital/ and /services/<slug>/
 * Persists user preference via localStorage ('holistic_hospital_lang')
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'holistic_hospital_lang';

  const i18nDict = {
    // Nav & General
    "nav_home": { en: "Home page", np: "गृहपृष्ठ" },
    "nav_products": { en: "Our Products", np: "हाम्रा उत्पादनहरू" },
    "nav_news": { en: "News", np: "समाचार" },
    "nav_hospital": { en: "Holistic Hospital", np: "होलिस्टिक हस्पिटल" },
    "nav_gallery": { en: "Gallery", np: "ग्यालरी" },
    "breadcrumb_home": { en: "Home", np: "गृहपृष्ठ" },
    "breadcrumb_hospital": { en: "Holistic Hospital", np: "होलिस्टिक हस्पिटल" },
    "breadcrumb_services": { en: "Services", np: "सेवाहरू" },
    "breadcrumb_gallery": { en: "Photo Gallery", np: "फोटो ग्यालरी" },

    // Hospital Hero
    "hero_live_status": {
      en: "OPD & Inpatient Admissions Open · 8:00 AM – 7:00 PM",
      np: "ओपीडी तथा आवासीय भर्ना खुला · बिहान ८:०० – साँझ ७:००"
    },
    "hero_eyebrow": {
      en: "HOLISTIC HOSPITAL & RESEARCH CENTER · ESTD. KATHMANDU",
      np: "होलिस्टिक हस्पिटल एण्ड रिसर्च सेन्टर · काठमाडौं"
    },
    "hero_title": {
      en: "Natural Healing Through Authentic Ayurveda, Acupuncture & Herbal Therapies",
      np: "शुद्ध आयुर्वेद, जडीबुटी, अकुपञ्चर तथा कपिङ थेरापीबाट प्राकृतिक उपचार"
    },
    "hero_lead": {
      en: "Kathmandu's dedicated natural healing center treating chronic health issues through pure Himalayan herbs, Ayurvedic medicine, acupuncture, cupping therapy, and physiotherapy — restoring wellness naturally without surgery.",
      np: "शुद्ध हिमाली जडीबुटी, शास्त्रीय आयुर्वेद, अकुपञ्चर, कपिङ थेरापी, र फिजियोथेरापीमार्फत दीर्घरोगहरूको जरादेखि नै प्राकृतिक र सुरक्षित उपचार गरिने काठमाडौंको विशिष्ट हस्पिटल तथा थेरापी केन्द्र ।"
    },
    "hero_cta_book": { en: "Book Clinical Consultation", np: "परामर्श समय लिनुहोस्" },
    "hero_cta_phone": { en: "Direct Hotline: 01-4115830", np: "हटलाइन: ०१-४११५८३०" },
    "badge_suites": { en: "30+ Residential Suites", np: "३०+ आवासीय शय्या" },
    "badge_noninvasive": { en: "100% Non-Invasive Care", np: "पूर्ण गैर-हानिकारक पद्धति" },
    "badge_doctors": { en: "Registered MDs & Vaidyas", np: "विशेषज्ञ डाक्टरहरूको रेखदेख" },

    // Credentials Band
    "cred_modalities_num": { en: "08", np: "०८" },
    "cred_modalities_title": { en: "Integrated Modalities", np: "८ क्लिनिकल पद्धतिहरू" },
    "cred_modalities_sub": { en: "Physiotherapy, Panchakarma, Acupuncture & more", np: "फिजियोथेरापी, पञ्चकर्म, अकुपंचर आदि" },
    "cred_conditions_num": { en: "24+", np: "२४+" },
    "cred_conditions_title": { en: "Chronic Conditions", np: "२४+ दीर्घरोग व्यवस्थापन" },
    "cred_conditions_sub": { en: "Neuromuscular, spine & metabolic care", np: "स्नायु, मेरूदण्ड तथा पाचन विकार" },
    "cred_noninvasive_num": { en: "100%", np: "१००%" },
    "cred_noninvasive_title": { en: "Non-Invasive Protocol", np: "१००% गैर-हानिकारक" },
    "cred_noninvasive_sub": { en: "Zero harsh chemical interventions", np: "प्राकृतिक तथा सुरक्षित चिकित्सा" },
    "cred_nursing_num": { en: "24/7", np: "२४/७" },
    "cred_nursing_title": { en: "Residential Nursing", np: "२४/७ आवासीय रेखदेख" },
    "cred_nursing_sub": { en: "Full inpatient recovery care support", np: "पूर्ण आवासीय बिरामी स्याहार सेवा" },

    // Services Section

    "services_eyebrow": { en: "Comprehensive Natural Healthcare", np: "समग्र प्राकृतिक उपचार सेवाहरू" },
    "services_title": { en: "Our Specialized Clinical Services", np: "हाम्रा विशेषज्ञ क्लिनिकल सेवाहरू" },
    "services_subtitle": {
      en: "Explore our 11 evidence-guided holistic therapies. Each modality is customized by our clinical physicians to resolve chronic root causes.",
      np: "हाम्रा ११ वटा प्रमाणित प्राकृतिक उपचार सेवाहरू। प्रत्येक थेरापी विशेषज्ञ चिकित्सकहरूको निगरानीमा बिरामीको आवश्यकता अनुसार सञ्चालन गरिन्छ।"
    },
    "service_learn_more": { en: "Learn More →", np: "विस्तृत विवरण →" },

    // Modalities Section
    "modalities_eyebrow": { en: "Verified Clinical Procedures", np: "प्रमाणित क्लिनिकल उपचारहरू" },
    "modalities_title": { en: "Eight Signature Natural Healing Modalities", np: "आठ प्रमुख प्राकृतिक उपचार पद्धतिहरू" },
    "modalities_subtitle": {
      en: "Photographed directly inside our clinical rooms in Kathmandu. Select any therapeutic modality to review its physiological action and clinical indications.",
      np: "हाम्रो आफ्नै क्लिनिकमा सञ्चालन हुने उपचारका प्रत्यक्ष तस्बिरहरू । विस्तृत विवरण तथा असर हेर्न कुनै पनि थेरापीमा क्लिक गर्नुहोस् ।"
    },
    "tab_all": { en: "All Modalities (8)", np: "सबै थेरापीहरू (८)" },
    "tab_spine": { en: "Spinal & Orthopedic", np: "मेरूदण्ड तथा हाडजोर्नी" },
    "tab_neuro": { en: "Neuro & Mind", np: "स्नायु तथा तनाव" },
    "tab_thermal": { en: "Thermal & Detox", np: "थर्मल तथा डिटक्स" },
    "spec_duration": { en: "Session Duration", np: "उपचार समय" },
    "spec_action": { en: "Physiological Action", np: "शारीरिक प्रभाव" },
    "spec_indication": { en: "Primary Indication", np: "मुख्य प्रयोग" },
    "spec_book_btn": { en: "Direct Consultation Call: 01-4115830", np: "सिधा फोन सम्पर्क: ०१-४११५८३०" },

    // Neuro-Rehabilitation Section
    "neuro_badge": { en: "FLAGSHIP CLINICAL DEPARTMENT", np: "विशेष क्लिनिकल शाखा" },
    "neuro_title": { en: "Comprehensive Stroke & Paralysis Rehabilitation", np: "प्यारालाइसिस तथा पक्षघातको सफल प्राकृतिक उपचार" },
    "neuro_lead": {
      en: "At Holistic Hospital & Research Center, complex neurological challenges including post-stroke hemiplegia, Bell's palsy, and acute motor nerve deficits are treated through a structured multidisciplinary rehabilitation protocol combining Naturopathy, Clinical Physiotherapy, Electro-Acupuncture, and specialized botanical therapies.",
      np: "पक्षघात, मुख बाङ्गो हुने, हातखुट्टा नचल्ने तथा नसा सम्बन्धी जटिल समस्याहरूका लागि प्राकृतिक चिकित्सा, फिजियोथेरापी, अकुपंचर र हर्बल थेरापीको एकीकृत संयोजनद्वारा प्रभावकारी सुधार ल्याइन्छ ।"
    },
    "neuro_f1_title": { en: "Early Neuro-Mobilization", np: "नसा तथा मांशपेशी सक्रियता" },
    "neuro_f1_desc": { en: "Prevent contractures and re-educate neural motor pathways.", np: "नसा जाम हुन नदिई मांशपेशीको चाल पुनः फर्काउने ।" },
    "neuro_f2_title": { en: "Meridian Electro-Acupuncture", np: "अकुपंचर नर्भ स्टिमुलेसन" },
    "neuro_f2_desc": { en: "Targeted bio-electric frequency to restore motor tone.", np: "सूक्ष्म तरंगमार्फत स्नायु प्रणालीलाई उत्तेजित बनाउने ।" },
    "neuro_f3_title": { en: "Supervised Gait Retraining", np: "हिँड्ने तथा सन्तुलन अभ्यास" },
    "neuro_f3_desc": { en: "Parallel bar and balance board functional mobility exercises.", np: "विशेषज्ञको सहयोगमा हिँडडुल र सन्तुलन फर्काउने अभ्यास ।" },
    "neuro_f4_title": { en: "Botanical Neuro-Nourishment", np: "हर्बल नर्भ टोनिक" },
    "neuro_f4_desc": { en: "Medicated warm oil basti and classical nerve revitalizers.", np: "शास्त्रीय औषधि तथा औषधीय तेलको बाहिरी र भित्री प्रयोग ।" },
    "neuro_urgent_btn": { en: "Direct Helpline: 01-4115830", np: "सिधा हेल्पलाइन: ०१-४११५८३०" },

    // 4-Stage Pathway
    "pathway_eyebrow": { en: "The Patient Roadmap", np: "उपचार प्रक्रिया" },
    "pathway_title": { en: "Your Four-Stage Journey to Sustained Health", np: "स्वास्थ्य लाभका चार महत्वपूर्ण चरणहरू" },
    "pathway_subtitle": {
      en: "Transparent, physician-led clinical progression from initial diagnostic assessment to full functional lifestyle restoration.",
      np: "पहिलो दिनको स्वास्थ्य परीक्षणदेखि पूर्ण निको भएर सामान्य जीवनमा नफर्किँदासम्मको व्यवस्थित क्लिनिकल मार्गचित्र ।"
    },
    "step_01_title": { en: "Diagnostic Evaluation", np: "पूर्ण स्वास्थ्य परीक्षण" },
    "step_01_desc": {
      en: "Comprehensive Ayurvedic pulse diagnosis (Nadi Pariksha), constitution assessment, and clinical neuromuscular examination by licensed doctors.",
      np: "नाडी परीक्षण, शारीरिक प्रकृति विश्लेषण र विशेषज्ञ डाक्टरहरूद्वारा स्नायु तथा जोर्नीको क्लिनिकल जाँच ।"
    },
    "step_02_title": { en: "Custom Protocol Design", np: "व्यक्तिगत उपचार योजना" },
    "step_02_desc": {
      en: "Formulation of your integrated multidisciplinary regimen blending physiotherapy, classical Panchakarma, acupuncture, and botanical decoctions.",
      np: "फिजियोथेरापिस्ट, प्राकृतिक चिकित्सक र आयुर्वेदिक डाक्टरहरू मिलेर बिरामी अनुसारको विशेष उपचार तालिका तयार गर्दछन् ।"
    },
    "step_03_title": { en: "Supervised Treatment", np: "प्रत्यक्ष क्लिनिकल उपचार" },
    "step_03_desc": {
      en: "Daily therapeutic administration in our clean treatment suites or residential inpatient rooms under continuous medical supervision.",
      np: "हाम्रो आधुनिक थेरापी कोठा वा आवासीय शय्यामा दक्ष प्राविधिकहरूद्वारा दैनिक उपचार सञ्चालन ।"
    },
    "step_04_title": { en: "Post-Care Maintenance", np: "दीर्घकालीन हेरचाह" },
    "step_04_desc": {
      en: "Personalized home dietary recommendations, restorative exercise plans, and routine follow-up reviews to ensure lasting results.",
      np: "घरमा गर्नुपर्ने खानपान र व्यायाम सम्बन्धी परामर्श तथा पुनः समस्या दोहोरिन नदिने दीर्घकालीन फलोअप ।"
    },

    // Booking CTA Bar
    "cta_banner_title": { en: "Begin Your Clinical Healing Journey Today", np: "आजै आफ्नो स्वास्थ्य लाभको यात्रा सुरु गर्नुहोस्" },
    "cta_banner_lead": {
      en: "Consult with our licensed medical doctors and Ayurvedic specialists. We welcome outpatient consultations and residential recovery admissions at our Kathmandu center.",
      np: "काठमाडौंको ठूलो खरीबोट मार्गमा अवस्थित हाम्रो अस्पतालमा ओपीडी परामर्श वा आवासीय भर्नाका लागि सम्पर्क गर्नुहोस् ।"
    },
    "cta_schedule_btn": { en: "Schedule Consultation", np: "परामर्श समय बुक गर्नुहोस्" },
    "cta_reception_btn": { en: "Direct Reception: 01-4115830", np: "फोन: ०१-४११५८३०" },

    // Service Detail Specific
    "service_book_this": { en: "Book This Service", np: "यो सेवाको लागि समय लिनुहोस्" },
    "service_what_it_treats": { en: "What It Treats", np: "उपचार गरिने समस्याहरू" },
    "service_what_it_treats_sub": {
      en: "Conditions and clinical pathologies successfully managed through this specialized therapy protocol.",
      np: "यस उपचार पद्धतिद्वारा सफलतापूर्वक निको पारिने मुख्य रोग तथा शारीरिक समस्याहरू।"
    },
    "service_how_it_works": { en: "How It Works", np: "उपचार प्रक्रियाका चरणहरू" },
    "service_how_it_works_sub": {
      en: "Our physician-directed multi-step clinical procedure designed for maximum safety, comfort, and efficacy.",
      np: "बिरामीको आराम, सुरक्षा र प्रभावकारी स्वास्थ्य लाभका लागि विशेषज्ञ डाक्टरहरूद्वारा सञ्चालित वैज्ञानिक प्रक्रिया।"
    },
    "service_session_details": { en: "Session Details", np: "उपचार विवरण" },
    "service_related_title": { en: "Related Clinical Services", np: "सम्बन्धित अन्य सेवाहरू" },
    "service_related_sub": {
      en: "Complementary therapies frequently combined to accelerate recovery and enhance therapeutic synergy.",
      np: "यस थेरापीसँगै थप प्रभावकारी नतिजाका लागि सिफारिस गरिने अन्य समन्वयात्मक सेवाहरू।"
    },
    "service_back_to_services": { en: "← All Services", np: "← सबै सेवाहरू" },

    // Booking Modal
    "modal_title": { en: "Clinical Appointment Booking", np: "क्लिनिकल परामर्श समय दर्ता" },
    "modal_subtitle": { en: "Connect instantly with our reception desk via WhatsApp or direct phone.", np: "हाम्रो रिसेप्सनमा ह्वाट्सएप वा फोनमार्फत तुरुन्त समय लिनुहोस् ।" },
    "modal_patient_name": { en: "Patient Full Name *", np: "बिरामीको पूरा नाम *" },
    "modal_patient_phone": { en: "Phone Number *", np: "सम्पर्क फोन / मोबाइल *" },
    "modal_shift": { en: "Preferred Shift", np: "उपयुक्त समय" },
    "modal_dept": { en: "Clinical Specialty Wing", np: "उपचार गराउन खोज्नुभएको विभाग" },
    "modal_notes": { en: "Brief Symptoms / Medical Notes (Optional)", np: "समस्याको संक्षिप्त विवरण (ऐच्छिक)" },
    "modal_submit_whatsapp": { en: "Confirm & Send via WhatsApp Concierge", np: "ह्वाट्सएपमार्फत तुरुन्त पठाउनुहोस्" },
    "modal_call_direct": { en: "Or Call Front Desk Now: 01-4115830", np: "वा सिधै फोन गर्नुहोस्: ०१-४११५८३०" },

    // Footer
    "footer_return_home": { en: "Return to Home", np: "गृहपृष्ठमा फर्कनुहोस्" },
    "footer_copy": {
      en: "© 2026 Holistic Hospital & Research Center Pvt. Ltd. All rights reserved.",
      np: "© २०२६ होलिस्टिक हस्पिटल एण्ड रिसर्च सेन्टर प्रा.लि. सर्वाधिकार सुरक्षित।"
    }
  };

  /**
   * Set the active language across the entire page
   * @param {string} lang - 'eng' or 'nep'
   */
  function setHospitalLanguage(lang) {
    if (lang !== 'nep' && lang !== 'eng') {
      lang = 'eng';
    }

    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      // Ignore private browsing storage errors
    }

    document.documentElement.setAttribute('data-lang', lang);
    document.body.setAttribute('data-lang', lang);

    // 1. Update all dictionary nodes [data-i18n]
    const i18nElements = document.querySelectorAll('[data-i18n]');
    i18nElements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (i18nDict[key]) {
        const text = (lang === 'nep') ? i18nDict[key].np : i18nDict[key].en;
        if (text) {
          el.textContent = text;
        }
      }
    });

    // 2. Update navbar pill toggle button states
    const engBtn = document.getElementById('hospital-lang-eng');
    const nepBtn = document.getElementById('hospital-lang-nep');

    if (engBtn && nepBtn) {
      if (lang === 'nep') {
        nepBtn.classList.add('is-active');
        nepBtn.setAttribute('aria-pressed', 'true');
        engBtn.classList.remove('is-active');
        engBtn.setAttribute('aria-pressed', 'false');
      } else {
        engBtn.classList.add('is-active');
        engBtn.setAttribute('aria-pressed', 'true');
        nepBtn.classList.remove('is-active');
        nepBtn.setAttribute('aria-pressed', 'false');
      }
    }

    // 3. Inform modality inspector if present
    if (typeof window.updateInspectorOnLangSwitch === 'function') {
      window.updateInspectorOnLangSwitch(lang);
    }

    // 4. Dispatch custom event for custom components
    window.dispatchEvent(new CustomEvent('holistic:languageChange', { detail: { lang } }));
  }

  // Initialize language on DOM ready
  document.addEventListener('DOMContentLoaded', function () {
    let savedLang = 'eng';
    try {
      savedLang = localStorage.getItem(STORAGE_KEY) || 'eng';
    } catch (e) {
      savedLang = 'eng';
    }

    // Attach click listeners to language switch buttons
    const engBtn = document.getElementById('hospital-lang-eng');
    const nepBtn = document.getElementById('hospital-lang-nep');

    if (engBtn) {
      engBtn.addEventListener('click', function () {
        setHospitalLanguage('eng');
      });
    }

    if (nepBtn) {
      nepBtn.addEventListener('click', function () {
        setHospitalLanguage('nep');
      });
    }

    // Apply initial language
    setHospitalLanguage(savedLang);
  });

  // Expose globally
  window.setHospitalLanguage = setHospitalLanguage;
  window.getHospitalLanguage = function () {
    return document.documentElement.getAttribute('data-lang') || 'eng';
  };
  window.i18nDict = i18nDict;
})();
