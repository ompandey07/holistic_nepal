/**
 * Holistic Hospital & Clinical Services - Bilingual Translation Engine
 * Shared across the entire site (Navbar, Hero, Products, Hospital, Services,
 * Gallery, News, Cart, Checkout, Auth, User Dashboard, Order Tracking, Footer).
 * Persists user preference via localStorage ('holistic_lang').
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'holistic_lang';

  const i18nDict = {
    // ==========================================
    // 1. Navigation & Breadcrumbs (Site-Wide)
    // ==========================================
    "nav_home": { en: "Home page", np: "गृहपृष्ठ" },
    "nav_products": { en: "Our Products", np: "हाम्रा उत्पादनहरू" },
    "nav_news": { en: "News", np: "समाचार" },
    "nav_hospital": { en: "Holistic Hospital", np: "होलिस्टिक हस्पिटल" },
    "nav_gallery": { en: "Gallery", np: "ग्यालरी" },
    "nav_cart": { en: "Cart", np: "कार्ट" },
    "nav_account": { en: "Account", np: "खाता" },
    "nav_login": { en: "Sign In", np: "साइन इन" },
    "nav_register": { en: "Register", np: "दर्ता" },
    "nav_logout": { en: "Sign Out", np: "बाहिरिनुहोस्" },
    "nav_track_order": { en: "Track My Order", np: "अर्डर ट्र्याक गर्नुहोस्" },
    "breadcrumb_home": { en: "Home", np: "गृहपृष्ठ" },
    "breadcrumb_products": { en: "Our Products", np: "हाम्रा उत्पादनहरू" },
    "breadcrumb_hospital": { en: "Holistic Hospital", np: "होलिस्टिक हस्पिटल" },
    "breadcrumb_services": { en: "Services", np: "सेवाहरू" },
    "breadcrumb_gallery": { en: "Photo Gallery", np: "फोटो ग्यालरी" },
    "breadcrumb_news": { en: "News & Advisories", np: "समाचार तथा सल्लाह" },
    "breadcrumb_cart": { en: "Botanical Basket", np: "हर्बल बास्केट" },
    "breadcrumb_checkout": { en: "Secure Checkout", np: "सुरक्षित चेकआउट" },
    "breadcrumb_track": { en: "Order Tracking", np: "अर्डर ट्र्याकिङ" },
    "lang_label": { en: "Language / भाषा:", np: "भाषा / Language:" },

    // ==========================================
    // 2. Home Page: Hero, Philosophy, Categories & Showcase
    // ==========================================
    "hero_himalayan": { en: "Himalayan", np: "हिमाली" },
    "hero_herbs_w": { en: "H", np: "ज" },
    "hero_herbs_rest": { en: "erbs,", np: "डीबुटी," },
    "hero_pure_wellness": { en: "Pure Holistic Wellness.", np: "शुद्ध समग्र स्वास्थ्य।" },
    "hero_desc": {
      en: "Harvested from the pristine heights of Nepal, our herbs carry generations of natural healing. From pure wildcrafted Himalayan botanicals to your daily wellness ritual, we bring nature’s potent remedies closer to you with authenticity and care.",
      np: "नेपालका स्वच्छ हिमाली भेगबाट संकलित हाम्रा जडीबुटीहरूमा पुस्तौँदेखिको प्राकृतिक उपचार शक्ति छ। शुद्ध प्राकृतिक जडीबुटीदेखि तपाईंको दैनिक आरोग्य जीवनशैलीसम्म, हामी प्रकृतिका शक्तिशाली उपचारहरू प्रामाणिकताका साथ उपलब्ध गराउँछौं।"
    },
    "btn_shop": { en: "Shop", np: "किनमेल" },
    "btn_shop_all": { en: "Shop All Products", np: "सबै उत्पादनहरू हेर्नुहोस्" },
    "btn_our_approach": { en: "Our approach", np: "हाम्रो पद्धति" },
    "trust_quality": { en: "Quality-led herbal formulations", np: "उच्च गुणस्तरीय जडीबुटी उत्पादन" },
    "trust_haccp": { en: "HACCP-minded sourcing", np: "HACCP मापदण्ड अनुसार संकलन" },
    "trust_scroll": { en: "Scroll to explore", np: "थप हेर्न तल स्क्रोल गर्नुहोस्" },
    "terroir_origin": { en: "Wildcrafted Himalayan Origin", np: "प्राकृतिक हिमाली उत्पत्ति" },

    // Wellness / Approach Section
    "wellness_title_1": { en: "Wellness begins", np: "आरोग्यको सुरुवात" },
    "wellness_title_2": { en: "with attention.", np: "सचेत हेरचाहबाट हुन्छ।" },
    "wellness_desc": {
      en: "We bring Nepal’s herbal wisdom into modern life through carefully considered products, honest education, and rituals that feel good to return to.",
      np: "हामी नेपालको परम्परागत जडीबुटीय ज्ञानलाई आधुनिक जीवनशैलीमा रूपान्तरण गरी प्रभावकारी उत्पादन, उचित परामर्श र स्वस्थ जीवनशैली प्रदान गर्दछौं।"
    },
    "wellness_btn": { en: "Meet our approach", np: "हाम्रो पद्धति बुझ्नुहोस्" },

    // Categories Section
    "categories_eyebrow": { en: "Curated Collections", np: "विशेष संकलन" },
    "categories_title": { en: "Explore by Category", np: "विधा अनुसार उत्पादनहरू हेर्नुहोस्" },
    "categories_subtitle": {
      en: "Every botanical formula is rooted in indigenous knowledge, harvested sustainably in Nepal, and prepared to the highest purity standards.",
      np: "प्रत्येक जडीबुटी उत्पादन रैथाने ज्ञानमा आधारित छ, नेपालमा दिगो रूपमा संकलन गरी उच्च शुद्धताका साथ तयार गरिन्छ।"
    },
    "categories_view_all": { en: "View Full Catalog", np: "सबै उत्पादनहरू हेर्नुहोस्" },
    "cat_nutraceutical": { en: "Nutraceuticals", np: "न्युट्रास्युटिकल्स" },
    "cat_beverages": { en: "Beverages & Herbal Teas", np: "हर्बल चिया तथा पेय" },
    "cat_personal_care": { en: "Personal Care", np: "सौन्दर्य तथा हेरचाह" },

    // Botanical Specimen / Showcase Section
    "showcase_eyebrow": { en: "Botanical Specimen Catalog", np: "हर्बल उत्पादन सूची" },
    "showcase_title": { en: "Client-Favorite Botanical Remedies", np: "ग्राहकहरूले अत्यधिक रुचाएका उत्पादनहरू" },
    "showcase_subtitle": {
      en: "Handcrafted with pure Himalayan ingredients. Real experiences from our verified clients across Nepal.",
      np: "शुद्ध हिमाली जडीबुटीबाट हस्तनिर्मित। नेपालभरका प्रमाणित ग्राहकहरूको वास्तविक अनुभव।"
    },
    "filter_all": { en: "All Remedies", np: "सबै उत्पादनहरू" },
    "add_to_basket": { en: "Add to Basket", np: "कार्टमा थप्नुहोस्" },
    "inspect_specs": { en: "Inspect Botanical Specs", np: "विस्तृत विवरण हेर्नुहोस्" },
    "verified_client": { en: "✓ Verified Client", np: "✓ प्रमाणित ग्राहक" },
    "what_clients_say": { en: "💬 WHAT CLIENTS SAY", np: "💬 ग्राहकहरूको अनुभव" },
    "herbal_action_label": { en: "HERBAL ACTION · विवरण:", np: "औषधीय प्रभाव · विवरण:" },
    "apothecary_eyebrow": { en: "Apothecary Collection · Pure Botanicals", np: "औषधि संकलन · शुद्ध जडीबुटी" },
    "view_all_remedies": { en: "View All Remedies", np: "सबै औषधिहरू हेर्नुहोस्" },
    "news_subhead": { en: "Stay updated with company announcements, certifications, and botanical releases.", np: "कम्पनीका सूचनाहरू, प्रमाणीकरण र नयाँ जडीबुटीय उत्पादनहरूको जानकारी लिनुहोस्।" },
    "news_view_details": { en: "View details", np: "विस्तृत हेर्नुहोस्" },
    "ratings_title": { 
      en: 'What Clients Say <span class="title-italic-accent">About Each Herbal Item</span>', 
      np: 'प्रत्येक जडीबुटीय उत्पादनबारे <span class="title-italic-accent">ग्राहकहरूको धारणा</span>' 
    },
    "ratings_subtitle": { en: "100% verified transparency. Explore genuine ratings, clinical results, and honest experiences shared by clients across Nepal for each botanical remedy.", np: "१००% प्रमाणित पारदर्शिता। नेपालभरका ग्राहकहरूले साझा गरेका वास्तविक प्रतिक्रिया, अनुभव र मूल्याङ्कन हेर्नुहोस्।" },
    "slider_title": { en: "Himalayan Remedies Showcase", np: "हिमाली औषधिहरूको प्रस्तुति" },

    // ==========================================
    // 3. Hospital & Clinical Services (Preserved & Extended)
    // ==========================================
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

    // ==========================================
    // 4. Products Catalog & Details
    // ==========================================
    "catalog_title": { en: "Our Herbal Products", np: "हाम्रा जडीबुटी उत्पादनहरू" },
    "catalog_subtitle": { en: "Formulated with pure Himalayan herbs for holistic wellness and vitality.", np: "समग्र स्वास्थ्य र स्फूर्तिका लागि शुद्ध हिमाली जडीबुटीबाट निर्मित।" },
    "search_placeholder": { en: "Search botanicals, teas, or remedies...", np: "जडीबुटी, चिया वा औषधि खोज्नुहोस्..." },
    "filter_categories": { en: "Categories", np: "उत्पादन विधा" },
    "sort_label": { en: "Sort by", np: "क्रमबद्ध" },
    "sort_default": { en: "Default", np: "पूर्वनिर्धारित" },
    "sort_price_low": { en: "Price: Low to High", np: "मूल्य: सस्तोबाट महँगो" },
    "sort_price_high": { en: "Price: High to Low", np: "मूल्य: महँगोबाट सस्तो" },
    "btn_add_to_cart": { en: "Add to Cart", np: "कार्टमा थप्नुहोस्" },
    "btn_buy_now": { en: "Buy Now", np: "अहिले किन्नुहोस्" },
    "out_of_stock": { en: "Out of Stock", np: "स्टक सकिएको" },
    "in_stock": { en: "In Stock", np: "स्टक उपलब्ध" },
    "prod_desc_title": { en: "Product Description :", np: "नेपाली भाषामा विस्तृत विवरण :" },
    "prod_ingredients_title": { en: "Active Botanical Ingredients", np: "सक्रिय जडीबुटीय घटकहरू" },
    "prod_usage_title": { en: "Directions for Use", np: "प्रयोग गर्ने तरिका" },

    // ==========================================
    // 5. Cart & Checkout
    // ==========================================
    "cart_title": { en: "Your Botanical Basket", np: "तपाईंको कार्ट (बास्केट)" },
    "cart_table_remedy": { en: "Remedy", np: "औषधि / उत्पादन" },
    "cart_table_price": { en: "Price", np: "मूल्य" },
    "cart_table_qty": { en: "Quantity", np: "परिमाण" },
    "cart_table_subtotal": { en: "Subtotal", np: "जम्मा" },
    "cart_summary_title": { en: "Basket Summary", np: "खर्च विवरण" },
    "cart_free_dispatch": { en: "Free Himalayan Dispatch", np: "निःशुल्क डेलिभरी" },
    "cart_items_subtotal": { en: "Items Subtotal", np: "सामानको जम्मा रकम" },
    "cart_standard_shipping": { en: "Standard Nepal Dispatch", np: "डेलिभरी शुल्क" },
    "cart_grand_total": { en: "Grand Total", np: "कुल जम्मा" },
    "cart_btn_checkout": { en: "Proceed to Checkout →", np: "चेकआउटमा जानुहोस् →" },
    "cart_btn_signin": { en: "Sign In to Proceed →", np: "अघि बढ्न साइन इन गर्नुहोस् →" },
    "cart_btn_continue": { en: "← Continue Exploring Remedies", np: "← अन्य उत्पादनहरू हेर्नुहोस्" },
    "checkout_h1": { en: "Complete Your Remedy Order", np: "तपाईंको अर्डर पूरा गर्नुहोस्" },
    "checkout_step_client": { en: "1. Client Information", np: "१. ग्राहक विवरण" },
    "checkout_step_delivery": { en: "2. Himalayan Delivery Address", np: "२. डेलिभरी ठेगाना" },
    "checkout_step_payment": { en: "3. Payment Method", np: "३. भुक्तानी माध्यम" },
    "checkout_order_summary": { en: "Order Summary", np: "अर्डर सारांश" },
    "checkout_btn_place_order": { en: "Place Order Now", np: "अर्डर पुष्टि गर्नुहोस्" },

    // ==========================================
    // 6. News & Gallery
    // ==========================================
    "news_title": { en: "News & Botanical Advisories", np: "समाचार तथा जडीबुटी जानकारी" },
    "news_read_more": { en: "Read Full Advisory →", np: "विस्तृत विवरण पढ्नुहोस् →" },
    "gallery_title": { en: "Photo Gallery & Clinical Archives", np: "फोटो ग्यालरी तथा क्लिनिकल अभिलेख" },

    // ==========================================
    // 7. Order Tracking
    // ==========================================
    "track_hero_title": { en: "Track Your Botanical Order", np: "तपाईंको अर्डर ट्र्याक गर्नुहोस्" },
    "track_hero_subtitle": {
      en: "Enter your order identifier (#ORD-000005) below to view live preparation, packaging, and courier dispatch milestones.",
      np: "तपाईंको अर्डर नम्बर (#ORD-000005) प्रविष्ट गरी अर्डरको तयारी, प्याकेजिङ तथा डेलिभरी विवरण हेर्नुहोस्।"
    },
    "track_order_number_label": { en: "Order Number", np: "अर्डर नम्बर" },
    "track_order_hint": { en: "Accepts #ORD-000005, ORD-000005, or order ID", np: "#ORD-000005, ORD-000005 वा अर्डर आईडी मान्य छ" },
    "track_btn_submit": { en: "Track Order Status →", np: "अर्डर स्थिति हेर्नुहोस् →" },
    "track_not_found_title": { en: "Order Not Found", np: "अर्डर फेला परेन" },

    // ==========================================
    // 8. Auth (Login, Register, Password Reset)
    // ==========================================
    "auth_login_title": { en: "Sign In to Your Account", np: "आफ्नो खातामा लगइन गर्नुहोस्" },
    "auth_register_title": { en: "Create an Account", np: "नयाँ खाता खोल्नुहोस्" },
    "auth_fill_details": { en: "Fill in your details below to get started.", np: "सुरु गर्न तल आफ्नो विवरण भर्नुहोस्।" },
    "auth_fullname": { en: "Full Name", np: "पूरा नाम" },
    "auth_email": { en: "Email Address", np: "इमेल ठेगाना" },
    "auth_mobile": { en: "Mobile Number", np: "मोबाइल नम्बर" },
    "auth_address": { en: "Address", np: "ठेगाना" },
    "auth_password": { en: "Password", np: "पासवर्ड" },
    "auth_confirm_password": { en: "Confirm Password", np: "पासवर्ड पुनः प्रविष्ट गर्नुहोस्" },
    "auth_forgot": { en: "Forgot password?", np: "पासवर्ड बिर्सनुभयो?" },
    "auth_btn_login": { en: "Sign In", np: "लगइन गर्नुहोस्" },
    "auth_btn_register": { en: "Create Account", np: "खाता बनाउनुहोस्" },
    "auth_already_have_account": { en: "Already have an account?", np: "पहिले नै खाता छ?" },
    "auth_sign_in_link": { en: "Sign in", np: "साइन इन" },

    // ==========================================
    // 9. Footer (Site-Wide)
    // ==========================================
    "footer_tagline": { en: "Wildcrafted Himalayan botanicals, bottled by hand in Nepal.", np: "नेपालमा हातैले संकलित र तयार गरिएका शुद्ध हिमाली जडीबुटीहरू।" },
    "footer_wildcrafted": { en: "100% Wildcrafted", np: "१००% प्राकृतिक" },
    "footer_terroir": { en: "Himalayan Terroir", np: "हिमाली पहिचान" },
    "footer_hand_bottled": { en: "Hand-Bottled", np: "हस्तनिर्मित" },
    "footer_nepal_time": { en: "Nepal Time", np: "नेपाल समय" },
    "footer_col_shop": { en: "Shop", np: "किनमेल" },
    "footer_col_company": { en: "Company", np: "कम्पनी" },
    "footer_col_contact": { en: "Contact", np: "सम्पर्क" },
    "footer_nutraceuticals": { en: "Nutraceuticals", np: "न्युट्रास्युटिकल्स" },
    "footer_beverages": { en: "Beverages", np: "पेय पदार्थ" },
    "footer_personal_care": { en: "Personal care", np: "सौन्दर्य हेरचाह" },
    "footer_track_order": { en: "Track My Order", np: "अर्डर ट्र्याक गर्नुहोस्" },
    "footer_news": { en: "News & Advisories", np: "समाचार तथा जानकारी" },
    "footer_gallery": { en: "Gallery", np: "ग्यालरी" },
    "footer_hospital": { en: "Holistic Hospital", np: "होलिस्टिक हस्पिटल" },
    "footer_location": { en: "Kathmandu, Nepal", np: "काठमाडौं, नेपाल" },
    "footer_inquiries": { en: "Inquiries & Consultations Welcome", np: "सोधपुछ तथा परामर्श स्वागत छ" },
    "footer_copyright": { en: "© 2026 Holistic Herbs Pvt. Ltd.", np: "© २०२६ होलिस्टिक हर्ब्स प्रा.लि." },
    "footer_rights": { en: "© 2026 Holistic Herbs Pvt. Ltd. All rights reserved.", np: "© २०२६ होलिस्टिक हर्ब्स प्रा.लि. सर्वाधिकार सुरक्षित।" },
    "footer_return_home": { en: "Return to Home", np: "गृहपृष्ठ फर्कनुहोस्" }
  };

  /**
   * Set the active language across the entire page
   * @param {string} lang - 'eng' or 'nep'
   */
  function setHospitalLanguage(lang) {
    if (lang !== 'nep' && lang !== 'eng') {
      lang = 'eng';
    }

    // 1. Persistence across multiple storage keys for backwards-compatibility
    try {
      localStorage.setItem('holistic_lang', lang);
      localStorage.setItem('site_lang', lang);
      localStorage.setItem('holistic_hospital_lang', lang);
    } catch (e) {
      // Ignore private browsing storage errors
    }

    document.documentElement.setAttribute('data-lang', lang);
    if (document.body) {
      document.body.setAttribute('data-lang', lang);
    }
    document.documentElement.lang = (lang === 'nep' ? 'ne' : 'en');

    const isNep = (lang === 'nep');

    // 2. Full DOM swap: Update all dictionary nodes [data-i18n]
    const i18nElements = document.querySelectorAll('[data-i18n]');
    i18nElements.forEach(function (el) {
      const key = el.getAttribute('data-i18n');
      if (i18nDict[key]) {
        const text = isNep ? i18nDict[key].np : i18nDict[key].en;
        if (text !== undefined && text !== null) {
          if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = text;
          } else if (text.indexOf('<') !== -1) {
            el.innerHTML = text;
          } else {
            el.textContent = text;
          }
        }
      }
    });

    // 3. Update placeholder nodes [data-i18n-placeholder]
    const i18nPlaceholders = document.querySelectorAll('[data-i18n-placeholder]');
    i18nPlaceholders.forEach(function (el) {
      const key = el.getAttribute('data-i18n-placeholder');
      if (i18nDict[key]) {
        const text = isNep ? i18nDict[key].np : i18nDict[key].en;
        if (text !== undefined && text !== null) {
          el.placeholder = text;
        }
      }
    });

    // 4. Full DOM swap: Toggle all bilingual span wrappers (.lang-eng / .lang-nep)
    document.querySelectorAll('.lang-eng').forEach(function (el) {
      el.style.display = isNep ? 'none' : '';
    });
    document.querySelectorAll('.lang-nep').forEach(function (el) {
      el.style.display = isNep ? '' : 'none';
    });
    document.querySelectorAll('[data-lang="en"]').forEach(function (el) {
      el.style.display = isNep ? 'none' : '';
    });
    document.querySelectorAll('[data-lang="np"]').forEach(function (el) {
      el.style.display = isNep ? '' : 'none';
    });

    // 5. Toggle quote blocks (.say-quote-eng / .say-quote-nep)
    document.querySelectorAll('.say-quote-eng').forEach(function (el) {
      el.style.display = isNep ? 'none' : 'inline';
    });
    document.querySelectorAll('.say-quote-nep').forEach(function (el) {
      el.style.display = isNep ? 'inline' : 'none';
    });

    // 6. Support Product Detail Page descriptions if present
    const descEng = document.getElementById('pdp-desc-eng');
    const descNep = document.getElementById('pdp-desc-nep');
    const boxTitle = document.getElementById('pdp-box-title');
    if (descEng && descNep) {
      descEng.style.display = isNep ? 'none' : 'block';
      descNep.style.display = isNep ? 'block' : 'none';
      if (boxTitle) {
        boxTitle.textContent = isNep ? 'नेपाली भाषामा विस्तृत विवरण :' : 'Product Description :';
      }
    }

    // 7. Update active state across ALL language toggle buttons site-wide
    const toggleButtons = document.querySelectorAll(
      '.nav-lang-btn, [id$="-lang-eng"], [id$="-lang-nep"], [data-lang="eng"], [data-lang="nep"]'
    );
    toggleButtons.forEach(function (btn) {
      const btnLang = btn.getAttribute('data-lang') || (btn.id && btn.id.indexOf('-nep') !== -1 ? 'nep' : 'eng');
      const isActive = (btnLang === lang);
      btn.classList.toggle('is-active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });

    // 8. Inform modality inspector if present on hospital page
    if (typeof window.updateInspectorOnLangSwitch === 'function') {
      try {
        window.updateInspectorOnLangSwitch(lang);
      } catch (e) {
        console.warn('updateInspectorOnLangSwitch error:', e);
      }
    }

    // 9. Dispatch custom events for any listener components
    window.dispatchEvent(new CustomEvent('holistic:languageChange', { detail: { lang: lang } }));
    window.dispatchEvent(new CustomEvent('siteLanguageChange', { detail: { lang: lang } }));
  }

  /**
   * Helper to retrieve currently saved language with fallback
   */
  function getSavedLanguage() {
    try {
      return localStorage.getItem('holistic_lang') ||
             localStorage.getItem('site_lang') ||
             localStorage.getItem('holistic_hospital_lang') ||
             'eng';
    } catch (e) {
      return 'eng';
    }
  }

  /**
   * Toggle between English and Nepali
   */
  function toggleSiteLanguage() {
    const currentLang = document.documentElement.getAttribute('data-lang') || getSavedLanguage();
    const nextLang = (currentLang === 'nep') ? 'eng' : 'nep';
    setHospitalLanguage(nextLang);
    return nextLang;
  }

  /**
   * Attach global click listeners and initialize language
   */
  function initI18n() {
    function handleToggleClick(e) {
      // 1. If clicked a specific language button
      const btn = e.target.closest('.nav-lang-btn, [id$="-lang-eng"], [id$="-lang-nep"], [data-lang="eng"], [data-lang="nep"]');
      if (btn) {
        e.preventDefault();
        e.stopPropagation();
        const currentLang = document.documentElement.getAttribute('data-lang') || getSavedLanguage();
        const btnLang = btn.getAttribute('data-lang') || (btn.id && btn.id.indexOf('-nep') !== -1 ? 'nep' : 'eng');
        // If clicking the already active button, toggle to the other language
        if (btn.classList.contains('is-active') && btnLang === currentLang) {
          toggleSiteLanguage();
        } else {
          setHospitalLanguage(btnLang);
        }
        return;
      }

      // 2. If clicked the capsule switch wrapper itself
      const wrapper = e.target.closest('.nav-lang-switch, [role="group"][aria-label*="Language"]');
      if (wrapper) {
        e.preventDefault();
        e.stopPropagation();
        toggleSiteLanguage();
      }
    }

    // Delegated click listener so dynamically injected or drawer buttons work
    document.addEventListener('click', handleToggleClick, true);

    // Direct listener on all current switches for high responsiveness
    document.querySelectorAll('.nav-lang-switch, .nav-lang-btn').forEach(function (el) {
      el.addEventListener('click', handleToggleClick);
    });

    // Initial language synchronization
    const initialLang = getSavedLanguage();
    setHospitalLanguage(initialLang);
  }

  // Expose immediately so inline scripts and early calls never fail
  window.setHospitalLanguage = setHospitalLanguage;
  window.setSiteLanguage = setHospitalLanguage;
  window.toggleSiteLanguage = toggleSiteLanguage;
  window.getHospitalLanguage = function () {
    return document.documentElement.getAttribute('data-lang') || getSavedLanguage();
  };
  window.i18nDict = i18nDict;

  // Run on DOM ready or immediately if DOM is already parsed
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initI18n);
  } else {
    initI18n();
  }
})();

