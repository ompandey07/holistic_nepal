from django.core.management.base import BaseCommand
from admin_panel.models import Service


class Command(BaseCommand):
    help = "Seed the 11 clinical services for Holistic Hospital & Research Center"

    def handle(self, *args, **options):
        services_data = [
            {
                "slug": "hydrotherapy",
                "name_en": "Hydrotherapy",
                "name_np": "हाइड्रोथेरापी",
                "summary_en": "Therapeutic water baths and herbal compresses to stimulate vitality and accelerate cellular circulation.",
                "summary_np": "औषधीय तातो-चिसो पानी तथा बाफद्वारा रक्तसञ्चार सुधार र शरीरका विकार निष्कासन गर्ने प्राकृतिक चिकित्सा।",
                "hero_description_en": "Hydrotherapy harnesses the physiological thermal and mechanical properties of pure Himalayan mineral water and botanical infusions. By systematically modulating peripheral blood flow, lymphatic drainage, and neuro-muscular tension through specialized contrast baths, spinal sprays, and medicinal immersion, our clinical protocols accelerate metabolic healing and restore systemic equilibrium.",
                "hero_description_np": "हाइड्रोथेरापीले शुद्ध हिमाली खनिज पानी र जडीबुटीको औषधीय गुणलाई एकीकृत गरी शरीरको रक्तसञ्चार, स्नायु प्रणाली र मांशपेशीलाई पुनर्ताजगी प्रदान गर्दछ। विभिन्न तापक्रमका बाथ, स्पाइनल स्प्रे तथा औषधीय जल-सम्पर्कमार्फत विषाक्त तत्वहरू निष्कासन गरी प्राकृतिक तवरले रोग प्रतिरोधात्मक क्षमता बढाइन्छ।",
                "conditions_treated_en": [
                    "Chronic Joint Inflammation & Arthritis",
                    "Poor Peripheral Blood Circulation",
                    "Fibromyalgia & Muscular Fatigue",
                    "Tension Headaches & Nervous Stress",
                    "Varicose Veins & Lymphatic Stagnation"
                ],
                "conditions_treated_np": [
                    "जोर्नी दुखाइ तथा बाथ रोग",
                    "कमजोर रक्तसञ्चार र हातगोडा झम्झमाउने",
                    "मांशपेशीको कडापन तथा थकान",
                    "टाउको दुखाइ तथा मानसिक तनाव",
                    "सुन्निएको र नसा सम्बन्धी समस्या"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Constitutional Assessment",
                        "title_np": "व्यक्तिगत परीक्षण",
                        "desc_en": "Physician evaluation of vital indicators, vascular response, and thermal sensitivity.",
                        "desc_np": "बिरामीको शारीरिक प्रकृति, नाडी र तापक्रम सहनशीलताको चिकित्सकीय परीक्षण।"
                    },
                    {
                        "step": 2,
                        "title_en": "Medicinal Herbal Decoction",
                        "title_np": "जडीबुटी मिश्रण",
                        "desc_en": "Infusion of customized organic Himalayan botanicals into temperature-controlled water.",
                        "desc_np": "रोग अनुसार शुद्ध हिमाली जडीबुटीको काढा उपयुक्त तापक्रमको पानीमा मिश्रण।"
                    },
                    {
                        "step": 3,
                        "title_en": "Controlled Immersion & Jet Therapy",
                        "title_np": "वैज्ञानिक जल उपचार",
                        "desc_en": "Targeted hydromassage and contrast immersion to stimulate deeper cellular pathways.",
                        "desc_np": "निर्देशित जलप्रवाह र बाथ विधिद्वारा मांशपेशी तथा स्नायु विन्दुहरूको सक्रियता।"
                    },
                    {
                        "step": 4,
                        "title_en": "Restorative Thermal Wrap",
                        "title_np": "आराम तथा पुनस्र्थापना",
                        "desc_en": "Dry herbal linen wrapping to normalize core body temperature and stabilize circulation.",
                        "desc_np": "उपचारपछि शरीरको तापक्रम सन्तुलनमा राखी दीर्घकालीन स्वास्थ्य लाभ सुनिश्चित।"
                    }
                ],
                "duration": "45 Mins",
                "physiological_action_en": "Thermal Modulation & Microcirculation",
                "physiological_action_np": "रक्तसञ्चार सुधार तथा मांसपेशी शिथिलीकरण",
                "primary_indication_en": "Joint Stiffness, Muscle Soreness, Stress",
                "primary_indication_np": "जोर्नी कडापन, मांशपेशी दुखाइ, तनाव",
                "icon": "droplet",
                "order": 1,
                "related_slugs": ["relaxation", "physiotherapy", "manipulation"]
            },
            {
                "slug": "diet-therapy",
                "name_en": "Diet Therapy",
                "name_np": "डाइट थेरापी",
                "summary_en": "Constitutionally tailored clinical nutrition and sattvic meal regimens to kindle metabolic digestive fire.",
                "summary_np": "पाचन प्रणाली सुधार गर्न र विषाक्त तत्व हटाउन व्यक्तिगत शारीरिक प्रकृति अनुसारको वैज्ञानिक खानपान।",
                "hero_description_en": "In holistic clinical science, food is the foundational medicine. Our Diet Therapy program assesses your unique biological constitution (Prakriti), metabolic strength (Agni), and cellular toxicity (Ama). Under physician supervision, we design restorative nutritional regimens incorporating organic whole foods, healing herbal teas, and fasting protocols to heal gastrointestinal disorders and optimize metabolic vitality.",
                "hero_description_np": "होलिस्टिक चिकित्सामा भोजन नै पहिलो औषधि मानिन्छ। हाम्रो डाइट थेरापीले व्यक्तिको पाचन शक्ति (अग्नि) र शारीरिक प्रकृति अनुसार खानपानको वैज्ञानिक तालिका निर्धारण गर्दछ। प्राकृतिक खाना, जडीबुटी काढा र डिटक्स आहारमार्फत ग्यास्ट्राइटिस, अल्सर, कब्जियत जस्ता जटिल पाचन समस्याको दिगो समाधान गरिन्छ।",
                "conditions_treated_en": [
                    "Chronic Gastritis, Ulcers & Acid Reflux",
                    "Irritable Bowel Syndrome (IBS) & Colitis",
                    "Metabolic Syndrome, Diabetes & High Cholesterol",
                    "Chronic Constipation & Dyspepsia",
                    "Food Intolerances & Gut Inflammation"
                ],
                "conditions_treated_np": [
                    "ग्यास्ट्राइटिस, अल्सर तथा एसिडिटी",
                    "आन्द्राको समस्या (IBS) तथा कोलाइटिस",
                    "मोटोपन, मधुमेह तथा कोलेस्ट्रोल",
                    "कब्जियत, अपच तथा पेट फुल्ने",
                    "खाना नपच्ने र पाचन विकार"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Digestive Fire (Agni) Diagnostics",
                        "title_np": "अग्नि तथा पाचन परीक्षण",
                        "desc_en": "Comprehensive clinical analysis of metabolic rate, gut microbiome, and dietary habits.",
                        "desc_np": "पाचन क्षमता, मेटाबोलिक दर र वर्तमान खानपान बानीको विस्तृत मूल्याङ्कन।"
                    },
                    {
                        "step": 2,
                        "title_en": "Purifying Elimination Phase",
                        "title_np": "निर्विसिकरण (डिटक्स)",
                        "desc_en": "Targeted short-term cleansing broths and mild fasting to clear metabolic endotoxins.",
                        "desc_np": "पाचन नलीमा जमेको फोहोर र विषाक्त तत्व सफा गर्न हल्का डिटक्स आहार।"
                    },
                    {
                        "step": 3,
                        "title_en": "Reconstructive Nutrition Blueprint",
                        "title_np": "पुनर्निर्माण आहार तालिका",
                        "desc_en": "Introduction of individualized therapeutic meals rich in natural digestive enzymes.",
                        "desc_np": "व्यक्तिगत आवश्यकता अनुसार पौष्टिक, सुपाच्य र औषधीय गुणयुक्त भोजन।"
                    },
                    {
                        "step": 4,
                        "title_en": "Sustainable Lifestyle Integration",
                        "title_np": "दीर्घकालीन जीवनशैली",
                        "desc_en": "Guidance on meal timing, food pairing principles, and mindful seasonal eating.",
                        "desc_np": "ऋतु र समय अनुसार सही भोजन छनोट र स्वस्थ बानीहरूको दिगो व्यवस्थापन।"
                    }
                ],
                "duration": "40 Mins Consultation",
                "physiological_action_en": "Metabolic Balancing & Gastrointestinal Repair",
                "physiological_action_np": "मेटाबोलिक सन्तुलन तथा पाचन प्रणाली सुधार",
                "primary_indication_en": "Acid Peptic Disorder, IBS, Metabolic Syndrome",
                "primary_indication_np": "ग्यास्ट्रिक, अल्सर, कब्जियत तथा मोटोपन",
                "icon": "nutrition",
                "order": 2,
                "related_slugs": ["herbal-therapy", "lifestyle-management", "integrated-treatment"]
            },
            {
                "slug": "relaxation",
                "name_en": "Relaxation",
                "name_np": "विश्राम",
                "summary_en": "Guided somatic unwinding and nervous system downregulation to reverse systemic burnout and insomnia.",
                "summary_np": "गहिरो मानसिक शान्ति, निद्रा सुधार र स्नायु तनाव घटाउन निर्देशित विश्राम तथा योगिक अभ्यास।",
                "hero_description_en": "Chronic sympathetic nervous overactivity is the hidden root of hypertension, insomnia, and neuro-hormonal breakdown. Our clinical Relaxation therapy integrates therapeutic Shavasana, biofeedback-assisted somatic release, and pranic nervous balancing. Sessions gently transition the brain into restorative theta-wave activity, dissolving accumulated deep-tissue tension and restoring deep restorative sleep.",
                "hero_description_np": "दैनिक तनाव र अतिव्यस्तताले स्नायु प्रणाली कमजोर भई उच्च रक्तचाप, अनिद्रा र माइग्रेन निम्त्याउँछ। हाम्रो क्लिनिकल विश्राम थेरापीले गहिरो श्वासप्रश्वास, योगनिद्रा र स्नायु शान्त पार्ने वैज्ञानिक विधिमार्फत शरीरको कोर्टिसोल हार्मोन घटाई प्राकृतिक निद्रा र मानसिक सन्तुलन पुनर्स्थापित गर्दछ।",
                "conditions_treated_en": [
                    "Chronic Insomnia & Sleep Fragmentation",
                    "General Anxiety Disorder & Chronic Worry",
                    "High Blood Pressure & Autonomic Dysregulation",
                    "Tension Headaches & Cervical Tightness",
                    "Executive Burnout & Cognitive Fatigue"
                ],
                "conditions_treated_np": [
                    "अनिद्रा तथा राती निद्रा नलाग्ने",
                    "मानसिक चिन्ता, छटपटी र तनाव",
                    "उच्च रक्तचाप तथा मुटुको धड्कन",
                    "माइग्रेन तथा टाउको र गर्धन दुखाइ",
                    "अत्यधिक मानसिक थकान र तनाव"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Autonomic Nervous Screening",
                        "title_np": "स्नायु तनाव जाँच",
                        "desc_en": "Heart rate variability (HRV) and respiratory baseline evaluation by clinicians.",
                        "desc_np": "मुटुको चाल, श्वासको गति र स्नायु तनावको अवस्था जाँच।"
                    },
                    {
                        "step": 2,
                        "title_en": "Somatic Muscular De-armoring",
                        "title_np": "मांशपेशी विश्राम",
                        "desc_en": "Sequential progressive relaxation to release chronic micro-contractions in muscles.",
                        "desc_np": "टाउकोदेखि पैतालासम्मका संकुचित मांशपेशीहरूलाई क्रमशः खुकुलो बनाउने।"
                    },
                    {
                        "step": 3,
                        "title_en": "Guided Pranic Downregulation",
                        "title_np": "प्राणायाम तथा श्वास नियन्त्रण",
                        "desc_en": "Slow-frequency diaphragmatic breathing to stimulate vagal nerve parasympathetic tone.",
                        "desc_np": "नाडी शोधन र भ्रामरी प्राणायामद्वारा मस्तिष्कका तरंगहरूलाई शान्त पार्ने।"
                    },
                    {
                        "step": 4,
                        "title_en": "Neuro-Cognitive Grounding",
                        "title_np": "मानसिक स्थिरता",
                        "desc_en": "Gentle awakening and integrative self-regulation techniques for everyday resilience.",
                        "desc_np": "दैनिक जीवनमा तनाव व्यवस्थापन गर्न सकिने सजिला विश्राम अभ्यासहरूको तालिम।"
                    }
                ],
                "duration": "50 Mins",
                "physiological_action_en": "Parasympathetic Activation & Cortisol Reduction",
                "physiological_action_np": "स्नायु प्रणाली नियन्त्रण तथा तनाव निवारण",
                "primary_indication_en": "Severe Stress, Insomnia, Autonomic Dysregulation",
                "primary_indication_np": "अत्यधिक तनाव, अनिद्रा, उच्च रक्तचाप",
                "icon": "lotus",
                "order": 3,
                "related_slugs": ["mental-health-and-counselling", "hydrotherapy", "reflexology"]
            },
            {
                "slug": "herbal-therapy",
                "name_en": "Herbal Therapy",
                "name_np": "हर्बल थेरापी",
                "summary_en": "Fresh Himalayan botanical decoctions, medicated ghritas, and personalized clinical poultices.",
                "summary_np": "शुद्ध हिमाली जडीबुटीबाट ताजा तयार गरिएका काढा, तेल र औषधीय लेपद्वारा प्राकृतिक उपचार।",
                "hero_description_en": "Rooted in authentic Himalayan Ayurvedic pharmacopoeia, our on-site botanical laboratory prepares individualized herbal formulas using pure, chemical-free medicinal plants harvested at peak potency. Each decoction (Kashayam), herbal oil (Taila), and botanical poultice is freshly prepared and prescribed by licensed doctors to treat underlying chronic pathology at the cellular level.",
                "hero_description_np": "हाम्रो अस्पतालको आफ्नै जडीबुटी प्रयोगशालामा शुद्ध र ताजा हिमाली जडीबुटी प्रशोधन गरी बिरामीको रोग अनुसार विशेष काढा, तेल र लेप तयार गरिन्छ। अनुभवी चिकित्सकहरूको प्रत्यक्ष सिफारिसमा कुनै रासायनिक मिसावट बिना तयार गरिएका यी औषधिहरूले रोगको जरोमै पुगेर स्थायी उपचार गर्दछन्।",
                "conditions_treated_en": [
                    "Chronic Respiratory Allergies & Asthma",
                    "Hepatic Sluggishness & Fatty Liver",
                    "Skin Disorders (Eczema, Psoriasis)",
                    "Chronic Immune Deficiencies",
                    "Persistent Inflammatory Joint Conditions"
                ],
                "conditions_treated_np": [
                    "दम, खोकी, पिनास तथा एलर्जी",
                    "कलेजो सम्बन्धी समस्या तथा जन्डिस",
                    "छालाको रोग (दाद, एक्जिमा, सोरायसिस)",
                    "कमजोर रोग प्रतिरोधात्मक क्षमता",
                    "पुरानो जोर्नी दुखाइ तथा सुन्निएको"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Phytochemical Matching",
                        "title_np": "जडीबुटी चयन",
                        "desc_en": "Physician determines synergistic botanical combinations for your physiological state.",
                        "desc_np": "बिरामीको शारीरिक प्रकृति र रोगको गम्भीरता अनुसार जडीबुटीको छनोट।"
                    },
                    {
                        "step": 2,
                        "title_en": "Laboratory Fresh Decoction",
                        "title_np": "ताजा काढा निर्माण",
                        "desc_en": "Slow-heat aqueous extraction in traditional vessels preserving active botanical bioactives.",
                        "desc_np": "परम्परागत विधिअनुसार वैज्ञानिक तवरले ताजा काढा तथा तेल निष्कासन।"
                    },
                    {
                        "step": 3,
                        "title_en": "Bimodal Administration",
                        "title_np": "आन्तरिक तथा बाह्य प्रयोग",
                        "desc_en": "Synchronized internal medicinal intake combined with external herbal warm poultices.",
                        "desc_np": "औषधि सेवनसँगै प्रभावित अंगमा तातो हर्बल लेप र मालिस।"
                    },
                    {
                        "step": 4,
                        "title_en": "Cellular Clearance Monitoring",
                        "title_np": "स्वास्थ्य सुधार अनुगमन",
                        "desc_en": "Periodic laboratory reviews to track toxin clearance and adjust botanical strengths.",
                        "desc_np": "उपचारको प्रभावकारिता परीक्षण गरी आवश्यक अनुसार मात्रा समायोजन।"
                    }
                ],
                "duration": "Daily Regimen",
                "physiological_action_en": "Cellular Detoxification & Tissue Rejuvenation",
                "physiological_action_np": "कोषीय निर्विसिकरण तथा तन्तु पुनर्ताजगी",
                "primary_indication_en": "Chronic Inflammation, Low Immunity, Skin Disorders",
                "primary_indication_np": "दीर्घरोग, कमजोर प्रतिरोधी क्षमता, एलर्जी",
                "icon": "herb",
                "order": 4,
                "related_slugs": ["diet-therapy", "integrated-treatment", "manipulation"]
            },
            {
                "slug": "integrated-treatment",
                "name_en": "Integrated Treatment",
                "name_np": "एकिकृत उपचार",
                "summary_en": "Multi-modality protocols blending Naturopathy, Panchakarma, Physiotherapy, and botanical medicine.",
                "summary_np": "प्राकृतिक चिकित्सा, पञ्चकर्म, फिजियोथेरापी र जडीबुटीको समन्वयात्मक समग्र उपचार।",
                "hero_description_en": "Complex chronic diseases rarely respond to isolated singular therapies. Our flagship Integrated Treatment brings together naturopathic doctors, Ayurvedic vaidyas, physiotherapists, and clinical dietitians under one collaborative treatment plan. By harmonizing internal cleansing, mechanical spinal alignment, meridian stimulation, and restorative nutrition, we resolve complicated multi-system illnesses.",
                "hero_description_np": "जटिल र पुराना रोगहरू केवल एउटा औषधिको भरमा निको हुन कठिन हुन्छ। हाम्रो एकीकृत उपचार पद्धतिले प्राकृतिक चिकित्सक, पञ्चकर्म विशेषज्ञ, फिजियोथेरापिस्ट र डाइटिसियनलाई एउटै छानामुनि ल्याई समन्वयात्मक उपचार गर्दछ। यसले शरीर, मन र आत्मा तीनै पक्षलाई स्वस्थ बनाई स्थायी स्वास्थ्य लाभ दिन्छ।",
                "conditions_treated_en": [
                    "Multi-System Chronic Degenerative Illnesses",
                    "Post-Stroke Recovery & Severe Hemiplegia",
                    "Complicated Cervico-Lumbar Disc Herniations",
                    "Chronic Fatigue & Autoimmune Discomfort",
                    "Post-Traumatic & Post-Surgical Rehabilitation"
                ],
                "conditions_treated_np": [
                    "जटिल तथा पुराना दीर्घरोगहरू",
                    "पक्षघात (प्यारालाइसिस) तथा स्नायु समस्या",
                    "नसा च्यापिएको र ढाडको डिस्क समस्या",
                    "पुरानो बाथ तथा मांशपेशी दुख्ने",
                    "शल्यक्रिया तथा चोटपटकपछिको पुनर्स्थापना"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Multi-Disciplinary Board Review",
                        "title_np": "संयुक्त विशेषज्ञ समीक्षा",
                        "desc_en": "Comprehensive clinical case review by Ayurvedic and Naturopathic specialists.",
                        "desc_np": "विभिन्न विभागका विशेषज्ञ डाक्टरहरूद्वारा बिरामीको समग्र रिपोर्टको समीक्षा।"
                    },
                    {
                        "step": 2,
                        "title_en": "Synchronized Daily Modalities",
                        "title_np": "दैनिक एकीकृत थेरापी",
                        "desc_en": "Carefully timed succession of physical therapy, herbal wraps, and bio-cleansing.",
                        "desc_np": "फिजियोथेरापी, अकुपंचर, पञ्चकर्म र डाइटको दैनिक समयतालिका अनुसार उपचार।"
                    },
                    {
                        "step": 3,
                        "title_en": "Continuous Clinical Titration",
                        "title_np": "निरन्तर स्वास्थ्य अनुगमन",
                        "desc_en": "Daily progress measurement and dynamic protocol adjustments based on patient response.",
                        "desc_np": "बिरामीको दैनिक स्वास्थ्य सुधार हेरी उपचार विधिमा आवश्यक परिमार्जन।"
                    },
                    {
                        "step": 4,
                        "title_en": "Comprehensive Health Independence",
                        "title_np": "आत्मनिर्भर जीवनशैली",
                        "desc_en": "Structured transition plan empowering the patient with self-care tools at home.",
                        "desc_np": "अस्पतालबाट डिस्चार्जपछि घरमा स्वस्थ रहन आवश्यक खानपान र व्यायाम योजना।"
                    }
                ],
                "duration": "60 – 90 Mins Daily",
                "physiological_action_en": "Synergistic Multi-System Physiological Restoration",
                "physiological_action_np": "समग्र शारीरिक प्रणालीको समन्वयात्मक पुनस्र्थापना",
                "primary_indication_en": "Complicated Chronic Diseases, Stroke Rehabilitation",
                "primary_indication_np": "पक्षघात, नसा च्यापिएको, जटिल दीर्घरोग",
                "icon": "synergy",
                "order": 5,
                "related_slugs": ["physiotherapy", "acupuncture-acupressure", "herbal-therapy"]
            },
            {
                "slug": "lifestyle-management",
                "name_en": "Lifestyle Management",
                "name_np": "जीवनशैली व्यवस्थापन",
                "summary_en": "Circadian rhythm alignment (Dinacharya & Ritucharya) with personalized ergonomic and behavioral habits.",
                "summary_np": "स्वस्थ र निरोगी रहन दैनिक दिनचर्या, निद्रा, व्यायाम र आनीबानीको वैज्ञानिक सुधार।",
                "hero_description_en": "Modern non-communicable diseases are overwhelmingly lifestyle-induced. Our clinical Lifestyle Management protocol provides individual coaching on circadian rhythm optimization (Dinacharya), seasonal adaptations (Ritucharya), ergonomic posture alignment, and stress resilience. We equip you with actionable daily routines that make radiant wellness your automatic default.",
                "hero_description_np": "आजका अधिकांश रोगहरू गलत जीवनशैली र अव्यवस्थित दिनचर्याको उपज हुन्। हाम्रो जीवनशैली व्यवस्थापन कार्यक्रमले उठ्ने-सुत्ने समय, भोजनको नियम, कार्यस्थलको शारीरिक आसन (Ergonomics) र तनाव व्यवस्थापनका वैज्ञानिक उपायहरू सिकाउँछ, जसले रोग लाग्नै नदिने जीवनशक्ति विकास गर्छ।",
                "conditions_treated_en": [
                    "Sedentary Musculoskeletal Deconditioning",
                    "Circadian Rhythm Sleep Disturbances",
                    "Pre-Diabetes & Metabolic Inflexibility",
                    "Occupational Postural Pain & Repetitive Strain",
                    "Chronic Lethargy & Low Vitality"
                ],
                "conditions_treated_np": [
                    "अस्वस्थ जीवनशैलीबाट उत्पन्न समस्याहरू",
                    "दिनरातको सुत्ने-उठ्ने समय बिग्रेको",
                    "मोटोपन तथा सुरुवाती मधुमेह",
                    "कम्प्युटरमा बस्दा हुने ढाड-गर्धन दुखाइ",
                    "अल्छीपन र दैनिक ऊर्जाको कमी"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "24-Hour Circadian Audit",
                        "title_np": "दैनिक दिनचर्या अडिट",
                        "desc_en": "Mapping of sleep cycles, eating windows, screen habits, and physical exertion.",
                        "desc_np": "सुत्ने, खाने, काम गर्ने र हिँडडुल गर्ने दैनिक तालिकाको विस्तृत अध्ययन।"
                    },
                    {
                        "step": 2,
                        "title_en": "Bio-Rhythmic Blueprint Formulation",
                        "title_np": "व्यक्तिगत दिनचर्या योजना",
                        "desc_en": "Creation of personalized morning and evening routines aligned with biological clocks.",
                        "desc_np": "आयुर्वेदिक दिनचर्या र आधुनिक विज्ञान अनुसारको नयाँ कार्यतालिका।"
                    },
                    {
                        "step": 3,
                        "title_en": "Ergonomic & Movement Coaching",
                        "title_np": "आसन तथा व्यायाम तालिम",
                        "desc_en": "Correction of sitting, walking, and postural patterns to prevent spinal degradation.",
                        "desc_np": "ढाड र जोर्नीलाई सुरक्षित राख्ने सहि आसन र दैनिक सूक्ष्म व्यायामको अभ्यास।"
                    },
                    {
                        "step": 4,
                        "title_en": "Habit Sustenance & Relapse Prevention",
                        "title_np": "दिगो बानी विकास",
                        "desc_en": "Practical strategies to preserve healthy lifestyle choices amid professional pressure.",
                        "desc_np": "व्यस्त समयमा पनि स्वस्थ बानी कायम राख्ने व्यावहारिक उपायहरू।"
                    }
                ],
                "duration": "45 Mins Session",
                "physiological_action_en": "Circadian Alignment & Endocrine Homeostasis",
                "physiological_action_np": "दिनचर्या सन्तुलन तथा हर्मोन स्थिरता",
                "primary_indication_en": "Sedentary Syndrome, Insomnia, Metabolic Imbalance",
                "primary_indication_np": "अव्यवस्थित जीवनशैली, तनाव, थकान",
                "icon": "clock",
                "order": 6,
                "related_slugs": ["diet-therapy", "relaxation", "mental-health-and-counselling"]
            },
            {
                "slug": "mental-health-and-counselling",
                "name_en": "Mental Health & Counselling",
                "name_np": "मानसिक परामर्श",
                "summary_en": "Empathetic, confidential clinical psychotherapy combined with Ayurvedic Sattvavajaya Chikitsa.",
                "summary_np": "मानसिक तनाव, चिन्ता र डिप्रेसन व्यवस्थापनका लागि विशेषज्ञ मनोपरामर्श तथा मनोचिकित्सा।",
                "hero_description_en": "True health requires harmony of mind and spirit. Our Mental Health & Counselling department provides compassionate, confidential psychotherapeutic support paired with classical Ayurvedic Sattvavajaya Chikitsa (mind-restraining therapy). By addressing emotional trauma, negative cognitive cycles, and autonomic stress responses, we empower patients to overcome depression, anxiety, and psychosomatic distress.",
                "hero_description_np": "शारीरिक स्वास्थ्यका साथै मानसिक शान्ति जीवनको प्रमुख आधार हो। हाम्रो मानसिक परामर्श विभागले डिप्रेसन, एन्जाइटी, अनिद्रा, पारिवारिक तनाव तथा भावनात्मक समस्याहरूका लागि पूर्ण गोप्य र प्रभावकारी मनोपरामर्श प्रदान गर्दछ। मनोचिकित्सा र ध्यान पद्धतिमार्फत मनलाई सकारात्मक र सबल बनाइन्छ।",
                "conditions_treated_en": [
                    "Depression & Persistent Depressive Episodes",
                    "General & Social Anxiety Disorders",
                    "Psychosomatic Gut & Heart Distress",
                    "Grief, Relationship & Marital Discord",
                    "Post-Traumatic Stress & Emotional Exhaustion"
                ],
                "conditions_treated_np": [
                    "निराशापन (Depression) तथा उत्साहहीनता",
                    "अत्यधिक चिन्ता, डर र छटपटी (Anxiety)",
                    "मानसिक तनावका कारण पेट र मुटुमा समस्या",
                    "पारिवारिक तथा सम्बन्ध सम्बन्धी समस्या",
                    "भावनात्मक चोट तथा मानसिक आघात"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Compassionate Confidential Intake",
                        "title_np": "गोप्य तथा सुरक्षित परामर्श",
                        "desc_en": "A supportive, non-judgmental environment to understand your emotional journey.",
                        "desc_np": "बिना कुनै पूर्वाग्रह बिरामीका कुरा सुन्ने र समस्याको मूल कारण बुझ्ने।"
                    },
                    {
                        "step": 2,
                        "title_en": "Cognitive-Emotional Exploration",
                        "title_np": "सोच तथा भावना विश्लेषण",
                        "desc_en": "Unpacking restrictive belief systems, behavioral loops, and unresolved trauma.",
                        "desc_np": "नकारात्मक सोच र तनाव उत्पन्न गराउने कारणहरूको पहिचान।"
                    },
                    {
                        "step": 3,
                        "title_en": "Somatic Mindfulness Integration",
                        "title_np": "सकारात्मक सोच तथा ध्यान",
                        "desc_en": "Training in emotional regulation, breath-anchoring, and cognitive reframing.",
                        "desc_np": "भावना नियन्त्रण, माइन्डफुलनेस र सकारात्मक चिन्तनका व्यावहारिक विधिहरू।"
                    },
                    {
                        "step": 4,
                        "title_en": "Empowered Self-Sufficiency",
                        "title_np": "आत्मविश्वास र आत्मबल",
                        "desc_en": "Building lifelong emotional resilience and healthy boundary mechanisms.",
                        "desc_np": "कठिन परिस्थितिमा पनि मानसिक सन्तुलन कायम राख्ने आत्मबल विकास।"
                    }
                ],
                "duration": "50 Mins",
                "physiological_action_en": "Cognitive Reframing & Neuro-Emotional De-escalation",
                "physiological_action_np": "सोच रूपान्तरण तथा स्नायु-भावनात्मक शान्ति",
                "primary_indication_en": "Depression, Anxiety, Emotional Trauma, Grief",
                "primary_indication_np": "डिप्रेसन, तनाव, चिन्ता, भावनात्मक समस्या",
                "icon": "heart-mind",
                "order": 7,
                "related_slugs": ["relaxation", "lifestyle-management", "integrated-treatment"]
            },
            {
                "slug": "physiotherapy",
                "name_en": "Physiotherapy",
                "name_np": "फिजियोथेरापी",
                "summary_en": "Evidence-guided clinical kinesiology, spinal traction, and gait re-education for paralysis and pain.",
                "summary_np": "प्यारालाइसिस, ढाड, गर्धन र जोर्नीको चाल पुनर्स्थापित गर्न वैज्ञानिक व्यायाम र म्यानुअल थेरापी।",
                "hero_description_en": "Our modern Physiotherapy and Neuro-Rehabilitation gymnasium is equipped for comprehensive motor recovery. Supervised by licensed physical therapists, our protocols combine manual joint articulation, computerized spinal decompression traction, parallel-bar gait retraining, and neuromuscular electrotherapy to resolve disc herniation, post-stroke deficits, and musculoskeletal trauma.",
                "hero_description_np": "हाम्रो आधुनिक फिजियोथेरापी तथा पुनर्स्थापना केन्द्रमा विशेषज्ञ फिजियोथेरापिस्टहरूको प्रत्यक्ष रेखदेखमा उपचार गरिन्छ। पक्षघातका बिरामीलाई हिँडाउन सिकाउने, नसा च्यापिएको खोल्ने ट्रयाक्सन, म्यानुअल थेरापी र आधुनिक मेसिनहरूको प्रयोगबाट ढाड, गर्धन र जोर्नीको दुखाइ पूर्ण रूपमा निको पारिन्छ।",
                "conditions_treated_en": [
                    "Post-Stroke Hemiplegia & Motor Impairments",
                    "Cervical & Lumbar Spondylosis (Disc Herniation)",
                    "Sciatica & Peripheral Nerve Compression",
                    "Osteoarthritis, Knee Pain & Frozen Shoulder",
                    "Sports Ligament Tears, Sprains & Tennis Elbow"
                ],
                "conditions_treated_np": [
                    "पक्षघात (प्यारालाइसिस) तथा मुख बाङ्गेको",
                    "गर्धन तथा ढाडको नसा च्यापिएको (Disc Problem)",
                    "कम्मरदेखि खुट्टासम्म दुख्ने (Sciatica)",
                    "घुँडा, कुम तथा जोर्नी दुख्ने वा जाम भएको",
                    "लिगामेन्ट च्यातिएको र खेलकुदका चोटपटक"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Biomechanical & Motor Diagnostics",
                        "title_np": "शारीरिक चाल तथा जोर्नी जाँच",
                        "desc_en": "Comprehensive assessment of range of motion, muscle strength, and gait balance.",
                        "desc_np": "मांशपेशीको बल, जोर्नीको लचकता र हिँडाइको सन्तुलन परीक्षण।"
                    },
                    {
                        "step": 2,
                        "title_en": "Manual Joint & Soft-Tissue Mobilization",
                        "title_np": "म्यानुअल थेरापी तथा ट्रयाक्सन",
                        "desc_en": "Hands-on joint de-rotation, spinal traction, and myofascial release.",
                        "desc_np": "च्यापिएको नसा खुकुलो पार्न विशेष ट्रयाक्सन र म्यानुअल प्रविधि।"
                    },
                    {
                        "step": 3,
                        "title_en": "Functional Neuro-Motor Retraining",
                        "title_np": "सक्रिय व्यायाम तथा हिँड्ने अभ्यास",
                        "desc_en": "Targeted parallel-bar gait work, balance board drills, and resistance training.",
                        "desc_np": "विशेषज्ञको सहयोगमा हिँडडुल र शारीरिक सन्तुलन फर्काउने सक्रिय व्यायाम।"
                    },
                    {
                        "step": 4,
                        "title_en": "Ergonomic Home Exercise Program",
                        "title_np": "घरेलु व्यायाम तालिका",
                        "desc_en": "Personalized strengthening drills to prevent injury recurrence and safeguard joints.",
                        "desc_np": "समस्या पुनः दोहोरिन नदिन घरमै गर्न सकिने दैनिक व्यायाम योजना।"
                    }
                ],
                "duration": "45 – 60 Mins",
                "physiological_action_en": "Biomechanical Realignment & Neuroplastic Motor Recovery",
                "physiological_action_np": "जोर्नी तथा मांशपेशी सन्तुलन र स्नायु पुनर्स्थापना",
                "primary_indication_en": "Stroke Paralysis, Disc Herniation, Arthritis, Sciatica",
                "primary_indication_np": "पक्षघात, ढाड-गर्धन दुखाइ, नसा च्यापिएको",
                "icon": "joint",
                "order": 8,
                "related_slugs": ["acupuncture-acupressure", "manipulation", "integrated-treatment"]
            },
            {
                "slug": "acupuncture-acupressure",
                "name_en": "Acupuncture / Acupressure",
                "name_np": "अकुपंचर / अकुप्रेसर",
                "summary_en": "Meridian filiform needle cannulation and micro-current stimulation to alleviate severe chronic pain.",
                "summary_np": "शरीरका मुख्य ऊर्जा विन्दुहरूमा मसिनो सियो र हल्का करेन्टद्वारा दुखाइ निवारण र स्नायु सक्रियता।",
                "hero_description_en": "By accessing key energetic meridians and neuro-vascular trigger zones with sterile ultra-fine filiform needles, Clinical Electro-Acupuncture interrupts pain signaling, triggers systemic endorphin cascades, and stimulates microvascular perfusion. Highly effective for facial Bell's palsy, severe paralysis, intractable migraines, and acute spinal nerve compressions.",
                "hero_description_np": "अकुपंचर परम्परागत पूर्वीय चिकित्साको अत्यन्त प्रभावकारी पद्धति हो। शरीरका विशेष मेरिडियन विन्दुहरूमा अति मसिनो सियो र हल्का विद्युत तरंगमार्फत स्नायु प्रणालीलाई उत्तेजित बनाइन्छ। यसले पक्षाघात भएका बिरामीको हातखुट्टा चलाउन, मुख बाङ्गो भएको सिधा पार्न र पुरानो माइग्रेन हटाउन तत्काल प्रभाव देखाउँछ।",
                "conditions_treated_en": [
                    "Bell's Palsy & Facial Nerve Asymmetry",
                    "Post-Stroke Flaccid & Spastic Paralysis",
                    "Chronic Migraines & Trigeminal Neuralgia",
                    "Severe Sciatica & Radiculopathy",
                    "Chronic Musculoskeletal Pain & Spasms"
                ],
                "conditions_treated_np": [
                    "अनुहारको प्यारालाईसिस (Bell's Palsy) / मुख बाङ्गेको",
                    "पक्षघातपछि हातखुट्टा नचल्ने समस्या",
                    "पुरानो माइग्रेन तथा टाउको दुखाइ",
                    "नसा च्यापिएको तीव्र दुखाइ (Sciatica)",
                    "कडा भएको मांशपेशी तथा स्नायु विकार"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Meridian Energy Palpation",
                        "title_np": "नाडी तथा विन्दु पहिचान",
                        "desc_en": "Identification of meridian blockages, Ah-Shi tender points, and neurological zones.",
                        "desc_np": "रोग अनुसारका मुख्य अकुपंचर विन्दुहरू र अवरुद्ध ऊर्जा मार्गको पहिचान।"
                    },
                    {
                        "step": 2,
                        "title_en": "Sterile Needle Cannulation",
                        "title_np": "सियो प्रवेश (Acupuncture)",
                        "desc_en": "Gentle, painless insertion of disposable, hair-thin sterile filiform needles.",
                        "desc_np": "दुखाइरहित तरिकाले डिस्पोजेबल मसिनो सियोहरूको सही स्थानमा प्रयोग।"
                    },
                    {
                        "step": 3,
                        "title_en": "Controlled Micro-Current Stimulation",
                        "title_np": "विद्युत तरंग सक्रियता",
                        "desc_en": "Application of calibrated electrical frequency to reactivate motor nerve conduction.",
                        "desc_np": "हल्का विद्युत तरंग दिएर निष्क्रिय नसाहरूलाई पुनः सक्रिय बनाउने।"
                    },
                    {
                        "step": 4,
                        "title_en": "Acupressure Grounding",
                        "title_np": "अकुप्रेसर विश्राम",
                        "desc_en": "Manual acupressure to seal meridian points and harmonize whole-body vital energy.",
                        "desc_np": "हातका औंलाहरूले हल्का दबाब दिई ऊर्जा प्रवाहलाई सन्तुलित पार्ने।"
                    }
                ],
                "duration": "40 Mins",
                "physiological_action_en": "Bio-Electrical Meridian Stimulation & Endorphin Release",
                "physiological_action_np": "स्नायु उत्तेजना तथा प्राकृतिक दुखाइ निवारण",
                "primary_indication_en": "Bell's Palsy, Paralysis, Severe Chronic Pain, Migraines",
                "primary_indication_np": "पक्षघात, मुख बाङ्गेको, माइग्रेन, नसा दुखाइ",
                "icon": "needle",
                "order": 9,
                "related_slugs": ["physiotherapy", "reflexology", "integrated-treatment"]
            },
            {
                "slug": "reflexology",
                "name_en": "Reflexology",
                "name_np": "रिफ्लेक्सोलोजी",
                "summary_en": "Therapeutic pressure applied to plantar neuro-vascular reflex zones connecting to internal organs.",
                "summary_np": "पैताला र हत्केलाका विशेष विन्दुहरूमा दबाब दिएर भित्री अंगहरूलाई स्वस्थ र सक्रिय बनाउने विधि।",
                "hero_description_en": "The feet and hands house dense concentrations of neuro-vascular reflex zones corresponding to every vital organ, gland, and joint in the human body. Clinical Reflexology applies precise alternating thumb and finger pressure techniques to stimulate visceral blood circulation, disperse crystalline lactic deposits, and promote autonomic balance.",
                "hero_description_np": "हाम्रो पैताला र हत्केलामा शरीरका सबै भित्री अंगहरूसँग जोडिएका हजारौं स्नायु विन्दुहरू हुन्छन्। रिफ्लेक्सोलोजी थेरापीमा ती विन्दुहरूमा वैज्ञानिक तरिकाले दबाब दिई रक्तसञ्चार तेज पारिन्छ, जमेको फोहोर फालिन्छ र अंगहरूलाई पुनः सक्रिय बनाइन्छ। यसले पैताला पोल्ने, झम्झमाउने र थकाइ तुरुन्त मेटाउँछ।",
                "conditions_treated_en": [
                    "Peripheral Neuropathy & Numb Extremities",
                    "Plantar Fasciitis & Heel Spur Discomfort",
                    "Sluggish Lymphatic Flow & Lower Limb Edema",
                    "Chronic Congestive Headaches & Sinusitis",
                    "Digestive Stagnation & Constipation"
                ],
                "conditions_treated_np": [
                    "खुट्टा पोल्ने, झम्झमाउने तथा नसा सुन्निने",
                    "कुर्कुच्चा तथा पैतालाको दुखाइ (Plantar Fasciitis)",
                    "खुट्टा सुन्निने र कमजोर रक्तसञ्चार",
                    "पिनास तथा पुरानो टाउको दुखाइ",
                    "पाचन गडबडी र पेटको समस्या"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Botanical Foot Soak",
                        "title_np": "हर्बल पादस्नान",
                        "desc_en": "Warm footbath infused with Himalayan rock salts and essential oils to soften tissues.",
                        "desc_np": "तातो पानी र हिमाली जडीबुटीमा खुट्टा डुबाएर मांशपेशी नरम बनाउने।"
                    },
                    {
                        "step": 2,
                        "title_en": "Reflex Zone Diagnostic Mapping",
                        "title_np": "विन्दु पहिचान",
                        "desc_en": "Careful palpation to identify pain nodules, crystal deposits, and energy blocks.",
                        "desc_np": "पैतालाका संवेदनशिल र कडा भएका विन्दुहरूको परीक्षण।"
                    },
                    {
                        "step": 3,
                        "title_en": "Systematic Plantar Articulation",
                        "title_np": "वैज्ञानिक दबाब विधि",
                        "desc_en": "Rhythmic thumb-walking and pressure point stimulation along reflex arcs.",
                        "desc_np": "औंलाहरूको सहयोगमा निश्चित लयमा रिफ्लेक्स विन्दुहरू थिच्ने।"
                    },
                    {
                        "step": 4,
                        "title_en": "Cooling Herbal Refreshment",
                        "title_np": "शीतलीकरण तथा आराम",
                        "desc_en": "Light application of soothing herbal camphor and menthol balm to ground vitality.",
                        "desc_np": "चिसो हर्बल मलम लगाएर पैतालालाई पूर्ण आराम र ताजगी दिने।"
                    }
                ],
                "duration": "35 Mins",
                "physiological_action_en": "Reflex Neuro-Vascular Stimulation & Lymph Drainage",
                "physiological_action_np": "रिफ्लेक्स स्नायु सक्रियता तथा रक्तसञ्चार सुधार",
                "primary_indication_en": "Plantar Pain, Peripheral Neuropathy, Fatigue",
                "primary_indication_np": "पैताला दुखाइ, खुट्टा पोल्ने, थकान",
                "icon": "foot",
                "order": 10,
                "related_slugs": ["hydrotherapy", "acupuncture-acupressure", "relaxation"]
            },
            {
                "slug": "manipulation",
                "name_en": "Manipulation (Massage)",
                "name_np": "मसाज",
                "summary_en": "Classical Abhyanga and clinical myofascial manipulation with warm medicated herbal oils.",
                "summary_np": "औषधीय तातो तेलद्वारा मांशपेशी खुकुलो बनाउने, दुखाइ हटाउने र रक्तसञ्चार बढाउने क्लिनिकल मसाज।",
                "hero_description_en": "Clinical Manipulation (Therapeutic Massage) integrates time-tested Ayurvedic Abhyanga effleurage with modern myofascial release. Administered by skilled physical therapists using warm medicated herbal oils tailored to your constitution, this therapy dissolves stubborn adhesions, flushes metabolic wastes, nourishes skeletal joints, and calms the central nervous system.",
                "hero_description_np": "हाम्रो क्लिनिकल मसाज केवल साधारण मालिस होइन, यो एक पूर्ण चिकित्सकीय पद्धति हो। बिरामीको शारीरिक समस्या अनुसार छनोट गरिएका तातो औषधीय तेलमार्फत दक्ष थेरापिस्टहरूले मांशपेशीका गाँठा फुकाउने, रक्तसञ्चार सुधार गर्ने र नसाहरूलाई बलियो बनाउने उपचार गर्दछन्। यसले ढाड र कम्मरको दुखाइ तत्काल कम गर्छ।",
                "conditions_treated_en": [
                    "Chronic Myofascial Pain & Muscle Spasms",
                    "Cervical & Lumbar Spinal Stiffness",
                    "Sluggish Peripheral Circulation & Fatigue",
                    "Postural Muscle Shortening & Adhesions",
                    "Nervous Exhaustion & Chronic Fatigue Syndrome"
                ],
                "conditions_treated_np": [
                    "मांशपेशीको कडापन, बाउँडिने र सुन्निने",
                    "ढाड, कम्मर र गर्धनको कडा दुखाइ",
                    "कमजोर रक्तसञ्चार र शरीर गल्ने",
                    "लामो समय बस्दा हुने शारीरिक असन्तुलन",
                    "मानसिक थकान तथा स्नायु कमजोरी"
                ],
                "how_it_works": [
                    {
                        "step": 1,
                        "title_en": "Medicated Oil Selection",
                        "title_np": "औषधीय तेल छनोट",
                        "desc_en": "Warm botanical formulation chosen based on your doshic balance and pain site.",
                        "desc_np": "रोग र प्रकृतिका आधारमा उपयुक्त तातो औषधीय तेलको छनोट।"
                    },
                    {
                        "step": 2,
                        "title_en": "Full-Body Effleurage & Warming",
                        "title_np": "समानुपातिक मालिस",
                        "desc_en": "Long, flowing rhythmic strokes in the direction of venous blood flow.",
                        "desc_np": "मुटु र रगतको बहाव अनुसार पूरै शरीरमा तेल पुर्‍याउने।"
                    },
                    {
                        "step": 3,
                        "title_en": "Deep Myofascial Kneading",
                        "title_np": "गहिरो मांशपेशी उपचार",
                        "desc_en": "Targeted pressure and friction to break stubborn scar tissue and muscle trigger knots.",
                        "desc_np": "दुखेको ठाउँ र कडा भएका मांशपेशीका गाँठाहरू खुकुलो बनाउने।"
                    },
                    {
                        "step": 4,
                        "title_en": "Herbal Steam (Swedana) Integration",
                        "title_np": "हर्बल बाफ (स्वेदन)",
                        "desc_en": "Gentle medicated steam to open cutaneous pores and facilitate deep herbal absorption.",
                        "desc_np": "औषधीय बाफ दिएर पसिनामार्फत विकार फाल्ने र शरीर हलुका बनाउने।"
                    }
                ],
                "duration": "50 Mins",
                "physiological_action_en": "Myofascial Release, Lymphatic Clearance & Vata Pacification",
                "physiological_action_np": "मांशपेशी विश्राम, रक्तसञ्चार सुधार तथा वात शान्ति",
                "primary_indication_en": "Muscle Spasms, Back Pain, Joint Stiffness, Sciatica",
                "primary_indication_np": "ढाड-कम्मर दुखाइ, मांशपेशी कडापन, नसा च्यापिएको",
                "icon": "hands",
                "order": 11,
                "related_slugs": ["physiotherapy", "hydrotherapy", "herbal-therapy"]
            }
        ]

        # Phase 1: Create or update all 11 Service objects
        services_by_slug = {}
        for item in services_data:
            related_slugs = item.pop("related_slugs", [])
            service, created = Service.objects.update_or_create(
                slug=item["slug"],
                defaults=item
            )
            services_by_slug[item["slug"]] = (service, related_slugs)
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} service: {service.name_en} ({service.slug})"))

        # Phase 2: Link related services
        for slug, (service, related_slugs) in services_by_slug.items():
            related_objs = []
            for r_slug in related_slugs:
                if r_slug in services_by_slug:
                    related_objs.append(services_by_slug[r_slug][0])
            if related_objs:
                service.related_services.set(related_objs)
                self.stdout.write(f"Linked {len(related_objs)} related services to {service.name_en}")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(services_data)} clinical services."))
