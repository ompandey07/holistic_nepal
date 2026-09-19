"""
Structured catalog data for Holistic Herbs products.
Contains rich botanical profiles, specifications, DFTQC government licensing,
authentic Nepali descriptions, ingredients, and daily usage guidelines.
"""

PRODUCTS_CATALOG = {
    "herbs-aloe-vera": {
        "slug": "herbs-aloe-vera",
        "name": "Herbs Aloe Vera",
        "category": "Digestion & Liver",
        "category_group": "Nutraceutical",
        "contain": "500mg × 60 Capsules",
        "price": 990,
        "price_formatted": "Rs 990.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-005",
        "short_desc": "Maintains liver health, improves digestion and strengthens natural immunity.",
        "image": "Medicine/Herbs Aloe Vera.png",
        "gallery_images": [
            "Medicine/Herbs Aloe Vera.png",
            "Images/NUTRACEUTICAL BG REMOVED.png",
            "Images/BEVEREGE BG REMOVED.png",
            "Images/PERSONAL CARE BG REMOVED.png",
        ],
        "highlights": [
            "Maintains optimal liver health and detoxification",
            "Improves digestive system and nutrient absorption",
            "Strengthens hair roots and keeps skin hydrated",
            "Reduces risk of cholesterol and heart-related complications",
            "Pure vegetarian capsules with zero synthetic fillers"
        ],
        "nepali_desc": """कोलेस्ट्रोल र मुटु रोगको जोखिम न्यूनीकरण र मधुमेहको उपचार तथा रोकथाम गर्न मद्दत गर्ने एलोभेराले कलेजोलाई स्वस्थ तथा सक्रिय राख्छ, शरीर सुगठित र क्रियाशील बनाउँछ । आँखाका रोग र ती रोगका संक्रमणहरू विरुद्ध लड्न, काटेका तथा पोलेका घाउको पीडा कम गरी निको पार्न तथा छाला, कपाल, यौनांग स्वस्थ राख्न मद्दत गर्छ । कोषको फोहोर सफा गरी पाचन शक्ति बढाउनका साथै रोगप्रतिरोध क्षमता बढाउँछ ।""",
        "english_desc": """Formulated with concentrated Aloe barbadensis leaf extract grown in the fertile mid-hills of Nepal. Renowned for centuries in Ayurvedic medicine as 'Ghritkumari', this pure botanical formulation assists natural cellular cleansing, nurtures the gastrointestinal lining, and maintains peak hepatic function without harsh laxative effects.""",
        "suggested_use": "Take 1 to 2 capsules twice daily with lukewarm water after meals, or as recommended by an Ayurvedic physician.",
        "ingredients": "Pure Aloe Vera (Aloe barbadensis Miller) leaf extract 500mg, Vegetarian capsule shell.",
        "caution": "Consult your physician prior to use if you are pregnant, nursing, or undergoing clinical treatment."
    },
    "herbs-glucosamine": {
        "slug": "herbs-glucosamine",
        "name": "Herbs Glucosamine",
        "subtitle": "(Joint Care)",
        "category": "Joint Care",
        "category_group": "Nutraceutical",
        "contain": "500mg × 90 Capsules",
        "price": 1490,
        "price_formatted": "Rs 1,490.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-012",
        "short_desc": "Reduces joint pain, repairs cartilage and strengthens bone flexibility.",
        "image": "Medicine/Herbs Glucosamine.jpeg",
        "gallery_images": [
            "Medicine/Herbs Glucosamine.jpeg",
            "Images/NUTRACEUTICAL BG REMOVED.png",
            "Images/PERSONAL CARE BG REMOVED.png",
        ],
        "highlights": [
            "Reduces chronic joint pain and inflammatory stiffness",
            "Stimulates natural cartilage regeneration and bone strength",
            "Restores synovial joint lubrication for fluid movement",
            "Protects knees, hips, and spinal discs from age-related wear"
        ],
        "nepali_desc": """जोर्नीको दुखाइ कम गर्न, खिइएको हड्डी तथा कार्टिलेजलाई बलियो बनाउन ग्लुकोसामाइन अत्यन्त प्रभावकारी मानिन्छ । यसले जोर्नीहरूको प्राकृतिक लचिलोपन बढाउँछ, हिँडडुल गर्दा हुने कटकट आवाज र पीडा कम गर्छ र सक्रिय जीवनशैली अपनाउन मद्दत गर्दछ । खेलाडी तथा उमेर ढल्केका व्यक्तिहरूका लागि यो अत्यन्त लाभदायक छ ।""",
        "english_desc": """Engineered to deliver high-potency bioavailable Glucosamine coupled with synergized Himalayan bone-nourishing herbal co-factors. Acts directly on worn synovial fluid and cartilage matrix to ease stiffness and safeguard bone structural integrity over long-term daily usage.""",
        "suggested_use": "Take 1 capsule twice daily with meals or warm water. Recommended for a continuous minimum cycle of 60 to 90 days for lasting joint renewal.",
        "ingredients": "Glucosamine Sulfate Potassium Chloride 500mg, Himalayan Boswellia serrata resin extract, Cellulose vegetarian shell.",
        "caution": "People allergic to shellfish or pregnant mothers should consult a doctor before consumption."
    },
    "herbs-ginkgo-biloba": {
        "slug": "herbs-ginkgo-biloba",
        "name": "Herbs Ginkgo Biloba",
        "subtitle": "(Antioxidant)",
        "category": "Brain & Memory",
        "category_group": "Nutraceutical",
        "contain": "500mg × 90 Capsules",
        "price": 2150,
        "price_formatted": "Rs 2,150.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-009",
        "short_desc": "Protects brain health, enhances memory focus, and fights depression and migraines.",
        "image": "Medicine/Herbs Gingko Biloba.png",
        "gallery_images": [
            "Medicine/Herbs Gingko Biloba.png",
            "Images/NUTRACEUTICAL BG REMOVED.png",
            "Images/BEVEREGE BG REMOVED.png",
        ],
        "highlights": [
            "Improves cerebral micro-circulation and cognitive clarity",
            "Sharpen memory recall and mental alertness",
            "Soothes severe migraines, tension headaches, and vertigo",
            "Powerful cellular antioxidant protection against oxidative stress"
        ],
        "nepali_desc": """जिन्कगो बिलोबाले मस्तिष्कमा अक्सिजन र रगतको सञ्चार सुधारेर स्मरणशक्ति र मानसिक एकाग्रता बढाउँछ । यसले मानसिक थकान, तनाव, डिप्रेसन, अनिद्रा र माइग्रेन जस्ता समस्याहरूबाट प्राकृतिक रूपमा मुक्ति दिलाउन सहयोग गर्दछ । विद्यार्थी, बौद्धिक काम गर्ने व्यक्तिहरू तथा वृद्धवृद्धाहरूका लागि यो उत्तम मस्तिष्क टनिक हो ।""",
        "english_desc": """Extracted from the ancient Ginkgo tree renowned for its remarkable neuroprotective flavonoid glycosides and terpene lactones. Stimulates healthy peripheral and cerebral blood flow, promoting sustained mental clarity, memory sharpness, and soothing neurovascular migraine triggers.""",
        "suggested_use": "Take 1 capsule twice daily in the morning and afternoon with water.",
        "ingredients": "Standardized Ginkgo Biloba leaf extract (24% Flavonoid Glycosides, 6% Terpene Lactones) 500mg.",
        "caution": "Do not take concurrently with prescription blood thinners without professional medical consultation."
    },
    "herbs-green-coffee-beans": {
        "slug": "herbs-green-coffee-beans",
        "name": "Herbs Green Coffee",
        "subtitle": "(Weight Care)",
        "category": "Weight Care",
        "category_group": "Nutraceutical",
        "contain": "500mg × 90 Capsules",
        "price": 3200,
        "price_formatted": "Rs 3,200.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-017",
        "short_desc": "Natural weight care formulation, burns body fat and accelerates metabolism.",
        "image": "Medicine/Herbs Green Coffee Beans.png",
        "gallery_images": [
            "Medicine/Herbs Green Coffee Beans.png",
            "Images/BEVEREGE BG REMOVED.png",
            "Images/NUTRACEUTICAL BG REMOVED.png",
        ],
        "highlights": [
            "Rich in Chlorogenic Acid to block fat synthesis",
            "Accelerates basal metabolic rate naturally without jitters",
            "Regulates post-meal blood glucose spikes",
            "Suppresses unhealthy appetite cravings and emotional snacking"
        ],
        "nepali_desc": """नरोस्ट गरिएका शुद्ध काँचो कफी बिन्समा रहेको क्लोरोजेनिक एसिडले शरीरको अनावश्यक बोसो पगाल्न र तौल सन्तुलन गर्न मद्दत गर्छ । यसले ग्लुकोज अवशोषणलाई नियन्त्रण गरी मेटाबोलिजम वृद्धि गर्छ र शरीरलाई बिना कमजोरी दिनभर ऊर्जावान बनाइराख्छ ।""",
        "english_desc": """Crafted from unroasted raw green coffee beans rich in pristine Chlorogenic acids that would otherwise be destroyed by high roasting temperatures. Naturally moderates glucose release into the bloodstream while prompting the body to burn stored adipocytes for daily energy.""",
        "suggested_use": "Take 1 capsule 30 minutes before breakfast and 1 capsule 30 minutes before lunch with a large glass of warm water.",
        "ingredients": "Raw Green Coffee Bean Extract (Coffea arabica, min. 50% Chlorogenic Acid) 500mg.",
        "caution": "Contains mild natural caffeine. Avoid taking close to bedtime."
    },
    "herbs-green-tea": {
        "slug": "herbs-green-tea",
        "name": "Herbs Green Tea",
        "subtitle": "(Ganoderma & Ginseng Blended)",
        "category": "Beverages & Tea",
        "category_group": "Beverages",
        "contain": "2.5g × 50 Bags",
        "price": 540,
        "price_formatted": "Rs 540.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-021",
        "short_desc": "Cleanses blood, flushes bodily toxins and aids everyday digestion.",
        "image": "Medicine/Herbs Green Tea.jpeg",
        "gallery_images": [
            "Medicine/Herbs Green Tea.jpeg",
            "Medicine/Herbs Leaf Tea.jpeg",
            "Images/BEVEREGE BG REMOVED.png",
        ],
        "highlights": [
            "Blended with pure Ganoderma and wild Ginseng roots",
            "Flushes metabolic toxins and cleanses internal organs",
            "Calms stomach acid and accelerates post-meal digestion",
            "Rich in epigallocatechin gallate (EGCG) antioxidants"
        ],
        "nepali_desc": """शुद्ध हिमालयन अर्गानिक हरियो चियापत्ती, गानोडर्मा च्याउ र जिनसेंगको समिश्रणबाट बनेको यो चिया एन्टिअक्सिडेन्टको उत्तम स्रोत हो । यसले रगत शुद्ध गर्न, मुटुलाई स्वस्थ राख्न, पाचन शक्ति सुधार्न र छालामा प्राकृतिक चमक ल्याउन सहयोग गर्छ ।""",
        "english_desc": """Hand-plucked tender green tea shoots from Himalayan high-altitude estates, synergistically fortified with wild Ganoderma lucidum (Reishi) and Panax Ginseng. Imparts an earthy, delicate aroma that soothes the gut and cleanses cellular debris without astringency.""",
        "suggested_use": "Dip one tea bag in freshly boiled hot water (80-85°C) for 3 to 5 minutes. Enjoy warm without milk or refined sugar.",
        "ingredients": "Himalayan Camellia sinensis green tea leaves, Ganoderma lucidum extract, Panax Ginseng root.",
        "caution": "Store in a cool, moisture-proof container once opened."
    },
    "herbs-black-coffee": {
        "slug": "herbs-black-coffee",
        "name": "Herbs Black Coffee",
        "subtitle": "(Herbal Energy Sachets)",
        "category": "Vitality & Energy",
        "category_group": "Beverages",
        "contain": "4.5g × 20 Sachets",
        "price": 1000,
        "price_formatted": "Rs 1,000.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-024",
        "short_desc": "Relieves stress, eliminates fatigue and sustains physical stamina.",
        "image": "Medicine/Herbs Black Coffee.jpeg",
        "gallery_images": [
            "Medicine/Herbs Black Coffee.jpeg",
            "Images/BEVEREGE BG REMOVED.png",
            "Medicine/Herbs Leaf Tea.jpeg",
        ],
        "highlights": [
            "Zero added sugar, 100% natural herbal vitality blend",
            "Relieves physical and cognitive burnout in minutes",
            "Enhanced with adaptogenic herbs to buffer stress cortisol",
            "Smooth, rich roasted aroma with clean finishing notes"
        ],
        "nepali_desc": """उत्कृष्ट स्वाद र सुगन्ध भएको यो ब्ल्याक कफीले दिनभरिको तनाव र थकान मेटाएर तुरुन्तै नयाँ स्फूर्ति दिन्छ । यसमा मिसाइएका दुर्लभ जडीबुटीहरूले मुटुको गतिलाई असर नगरी शारीरिक स्ट्यामिना र एकाग्रता बढाउँछन् । चिनी नभएकोले मधुमेहका बिरामीहरूका लागि पनि उपयुक्त छ ।""",
        "english_desc": """Premium roasted Arabica beans blended with select adaptogens including Himalayan Cordyceps and Ashwagandha. Designed for high performers seeking razor-sharp clarity, emotional balance, and sustained stamina without the jitters or crash of generic commercial coffee.""",
        "suggested_use": "Empty one sachet into 150ml of freshly boiled water. Stir well and consume hot in the morning or midday slump.",
        "ingredients": "Micro-ground Arabica Coffee, Cordyceps sinensis extract, Ashwagandha root extract.",
        "caution": "Keep in an airtight pouch away from direct heat."
    },
    "herbs-toothpaste": {
        "slug": "herbs-toothpaste",
        "name": "Herbs Toothpaste",
        "subtitle": "(Natural Dental Care)",
        "category": "Oral Care",
        "category_group": "Personal Care",
        "contain": "50g Tube",
        "price": 170,
        "price_formatted": "Rs 170.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-032",
        "short_desc": "Protects enamel, stops gum bleeding and permanently cures bad breath.",
        "image": "Medicine/Herbs Toothpaste 50 Gm.png",
        "gallery_images": [
            "Medicine/Herbs Toothpaste 50 Gm.png",
            "Medicine/Herbs Toothpaste 100 Gm.png",
            "Images/PERSONAL CARE BG REMOVED.png",
        ],
        "highlights": [
            "100% fluoride-free and SLS-free gentle botanical paste",
            "Clove and Neem extracts fight oral bacteria and plaque",
            "Strengthens tooth enamel and eliminates cold/hot sensitivity",
            "Long-lasting natural Himalayan peppermint freshness"
        ],
        "nepali_desc": """ल्वाङ, निम, बबुल र पुदिना जस्ता प्राचीन औषधीय जडीबुटीबाट निर्मित यो हर्बल टुथपेस्टले दाँतलाई किरा लाग्नबाट बचाउँछ । गिजाबाट रगत आउने, सुन्निने र मुखबाट दुर्गन्ध आउने समस्यालाई जरैदेखि निर्मूल पारी दाँतलाई प्राकृतिक रूपमा सेतो र बलियो बनाउँछ ।""",
        "english_desc": """Formulated according to time-tested Ayurvedic dental principles. Harnesses the astringent and antiseptic prowess of Eugenia caryophyllus (Clove) and Azadirachta indica (Neem) to maintain healthy oral microbiome, soothe gum inflammation, and shield natural tooth enamel.""",
        "suggested_use": "Brush thoroughly with a pea-sized amount at least twice daily, or after meals.",
        "ingredients": "Purified water, Calcium carbonate, Clove bud oil, Neem bark extract, Babool extract, Mentha piperita.",
        "caution": "Safe for children above 3 years under parental supervision."
    },
    "herbs-massage-oil": {
        "slug": "herbs-massage-oil",
        "name": "Herbs Massage Oil",
        "subtitle": "(Deep Muscle Pain Relief)",
        "category": "Body Ritual",
        "category_group": "Personal Care",
        "contain": "100ml Bottle",
        "price": 440,
        "price_formatted": "Rs 440.00",
        "dftqc_no": "DFTQC No.: 01-25-76-18-036",
        "short_desc": "Reduces joint stiffness, backache, and deep muscle pain.",
        "image": "Medicine/Herbs Massage Oil.jpeg",
        "gallery_images": [
            "Medicine/Herbs Massage Oil.jpeg",
            "Images/PERSONAL CARE BG REMOVED.png",
            "Medicine/Herbs Massage Oil.jpeg",
        ],
        "highlights": [
            "Deep penetrating warm herbal formula for immediate relief",
            "Sesame base infused with 16 wild Himalayan herbs",
            "Alleviates frozen shoulders, lower back pain, and sciatica",
            "Smooth glide for therapeutic Ayurvedic Abhyanga massage"
        ],
        "nepali_desc": """१६ भन्दा बढी दुर्लभ जडीबुटीहरूको मिश्रणबाट परम्परागत विधिद्वारा पकाइ तयार पारिएको यो मालिस तेलले बाथ, जोर्नी दुखाइ, ढाड दुखाइ, नसा च्यापिएको र मांशपेशीको कडापनमा तुरुन्तै आराम पुर्‍याउँछ । यसले छालामा गहिरोसँग सोसिएर रक्तसञ्चार तेज बनाउँछ ।""",
        "english_desc": """Prepared through slow Ayurvedic decoction where unrefined black sesame oil is infused with Wintergreen, Camphor, Eucalyptus, and wild mountain herbs. Generates deep warming relief that penetrates dense joint capsules and soothes strained myofascial tissue.""",
        "suggested_use": "Apply warm oil generously over the affected joint or muscular area. Massage gently with circular motions for 10 to 15 minutes before bedtime.",
        "ingredients": "Til Taila (Sesame oil base), Gandhapura (Wintergreen), Karpura (Camphor), Nilgiri (Eucalyptus), Himalayan pine oil.",
        "caution": "For external application only. Do not apply over open lacerations or mucous membranes."
    }
}




def get_all_products():
    """
    Return a list of all products from the backend database (ProductSetup),
    enriched with rich catalog metadata (gallery, highlights, bilingual desc, ratings).
    Fallback to static PRODUCTS_CATALOG if DB is uninitialized.
    """
    try:
        from django.utils.text import slugify
        from admin_panel.models import ProductSetup
        db_products = list(ProductSetup.objects.select_related('PRODUCT_CATEGORY', 'PRODUCT_UNIT').order_by('id'))
    except Exception:
        db_products = []

    if not db_products:
        # Fallback to static catalog
        products = []
        for idx, (p_slug, p) in enumerate(PRODUCTS_CATALOG.items(), start=1):
            p_copy = dict(p)
            p_copy['id'] = p_copy.get('id', idx)
            p_copy['db_id'] = p_copy.get('db_id', idx)
            if 'gallery_images' not in p_copy or not p_copy['gallery_images']:
                p_copy['gallery_images'] = [p_copy['image']]
            img = p_copy.get('image', '')
            p_copy['image_url'] = img if (img.startswith('/') or img.startswith('http')) else f"/static/{img}"
            p_copy['price_display'] = f"Rs {int(p_copy['price']):,}" if p_copy.get('price') else "Rs 0"
            p_copy['detail_url'] = f"/product/{p_copy['slug']}/"
            products.append(p_copy)
        return products

    from django.utils.text import slugify
    products = []
    seen_slugs = set()
    for db_p in db_products:
        base_slug = getattr(db_p, 'PRODUCT_SLUG', None) or slugify(db_p.PRODUCT_NAME) or f"product-{db_p.id}"
        catalog_meta = {}
        for cat_slug, cat_val in PRODUCTS_CATALOG.items():
            if cat_val.get('name', '').strip().lower() == db_p.PRODUCT_NAME.strip().lower() or cat_slug == base_slug:
                catalog_meta = cat_val
                base_slug = cat_val.get('slug', cat_slug)
                break

        slug = base_slug
        counter = 1
        while slug in seen_slugs:
            counter += 1
            slug = f"{base_slug}-{counter}"
        seen_slugs.add(slug)

        aliases = [slug, base_slug, slugify(db_p.PRODUCT_NAME), str(db_p.id)]

        # Determine image_url
        if db_p.PRODUCT_IMAGE:
            try:
                image_url = db_p.PRODUCT_IMAGE.url
            except Exception:
                image_url = f"/media/{db_p.PRODUCT_IMAGE}"
        elif catalog_meta.get('image'):
            cat_img = catalog_meta['image']
            image_url = cat_img if (cat_img.startswith('/') or cat_img.startswith('http')) else f"/static/{cat_img}"
        else:
            image_url = "/static/Images/NUTRACEUTICAL BG REMOVED.png"

        # Gallery images
        gallery_images = []
        if catalog_meta.get('gallery_images'):
            for g in catalog_meta['gallery_images']:
                g_url = g if (g.startswith('/') or g.startswith('http')) else f"/static/{g}"
                gallery_images.append(g_url)
        if not gallery_images:
            gallery_images = [image_url]
        elif image_url not in gallery_images:
            gallery_images.insert(0, image_url)

        # Price formatting
        price_num = float(db_p.PRODUCT_PRICE) if db_p.PRODUCT_PRICE is not None else float(catalog_meta.get('price', 0))
        price_formatted = f"Rs {price_num:,.2f}"
        price_display = f"Rs {int(price_num):,}" if price_num.is_integer() else price_formatted

        # Category and Unit
        cat_name = db_p.PRODUCT_CATEGORY.CATEGORY_NAME if db_p.PRODUCT_CATEGORY else catalog_meta.get('category', 'Ayurvedic Remedies')
        unit_name = db_p.PRODUCT_UNIT.UNIT_NAME if db_p.PRODUCT_UNIT else 'Standard Pack'
        unit_symbol = db_p.PRODUCT_UNIT.UNIT_SYMBOL if db_p.PRODUCT_UNIT else ''
        contain = catalog_meta.get('contain') or (f"{unit_symbol} ({unit_name})" if unit_symbol else unit_name)

        # Descriptions (strip all HTML tags)
        import html
        import re
        from django.utils.html import strip_tags
        raw_desc = db_p.PRODUCT_DESCRIPTION or catalog_meta.get('short_desc') or catalog_meta.get('english_desc') or ''
        clean_desc = html.unescape(strip_tags(raw_desc)).replace('\xa0', ' ').strip()
        short_desc = getattr(db_p, 'short_desc', None) or catalog_meta.get('short_desc') or (clean_desc[:110] + ('...' if len(clean_desc) > 110 else ''))
        english_desc = short_desc or clean_desc
        nepali_desc = short_desc or clean_desc

        # Highlights (extract clean action bullets, stripping all HTML)
        highlights = catalog_meta.get('highlights')
        if not highlights:
            feat_source = getattr(db_p, 'PRODUCT_KEY_FEATURES', None) or raw_desc
            if feat_source:
                formatted_feat = re.sub(r'</?(?:p|li|div|br\s*/?|h[1-6])[^>]*>', '\n', feat_source, flags=re.IGNORECASE)
                clean_feat = html.unescape(strip_tags(formatted_feat)).replace('\xa0', ' ')
                lines = [l.strip(' -*•\r\t') for l in clean_feat.split('\n') if l.strip(' -*•\r\t')]
            else:
                lines = []
            highlights = lines[:5] if lines else [
                "100% Pure authentic Himalayan herbal formulation",
                "Processed under strict traditional Ayurvedic standards",
                "Lab verified for chemical purity and active botanicals",
                "Zero artificial additives, preservatives or harsh chemicals"
            ]

        prod_data = {
            "id": db_p.id,
            "db_id": db_p.id,
            "slug": slug,
            "name": db_p.PRODUCT_NAME,
            "category": cat_name,
            "category_group": catalog_meta.get('category_group', 'Nutraceutical'),
            "contain": contain,
            "price": price_num,
            "price_formatted": price_formatted,
            "price_display": price_display,
            "dftqc_no": catalog_meta.get('dftqc_no', 'DFTQC Verified Formulation'),
            "rating": db_p.avg_rating,
            "reviews_count": getattr(db_p, 'reviews_count', 0),
            "avg_rating_stars": db_p.avg_rating_stars,
            "short_desc": short_desc,
            "english_desc": english_desc,
            "nepali_desc": nepali_desc,
            "suggested_use": catalog_meta.get('suggested_use', 'Take 1 serving twice daily with lukewarm water after meals, or as recommended by an Ayurvedic specialist.'),
            "ingredients": catalog_meta.get('ingredients', f"Pure extract of {db_p.PRODUCT_NAME}."),
            "caution": catalog_meta.get('caution', 'Consult your physician prior to use if pregnant, nursing, or undergoing clinical treatment.'),
            "image": image_url,
            "image_url": image_url,
            "gallery_images": gallery_images,
            "highlights": highlights,
            "detail_url": f"/product/{slug}/",
            "aliases": aliases,
        }
        products.append(prod_data)

    return products


def get_product_by_slug(slug):
    """Retrieve a single product by its slug, alias, or db ID."""
    all_prods = get_all_products()
    for p in all_prods:
        if p['slug'] == slug or slug in p.get('aliases', []):
            return p
    clean_req = slug.replace('-', ' ').strip().lower()
    for p in all_prods:
        if p['name'].strip().lower() == clean_req:
            return p
    if str(slug).isdigit():
        prod_id = int(slug)
        for p in all_prods:
            if p.get('id') == prod_id or p.get('db_id') == prod_id:
                return p
    return None
