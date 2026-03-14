"""
Deal Hunter Pro X — Market Intelligence Module
Based on SA marketplace research 2025-2026
Sources: Gumtree SA, OLX SA, Facebook Marketplace, WeBuyCars, AutoTrader SA,
         BusinessTech, Cars.co.za, World Wide Worx Online Retail Report 2025
"""

# ---------------------------------------------------------------------------
# FAST-MOVING CATEGORIES
# Ranked by demand score (composite of listing volume, sell-through rate,
# buyer search frequency, and average days-on-market data from SA platforms)
# ---------------------------------------------------------------------------

FAST_MOVING_CATEGORIES = {
    'electronics': {
        'rank': 1,
        'avg_days_to_sell': 3,
        'hot_items': [
            'iPhone 13/14/15',
            'Samsung Galaxy S23/S24',
            'MacBook Air M2/M3',
            'PS5 Console',
            'Laptops under R8 000',
            'AirPods / Samsung Galaxy Buds',
            'iPad (any gen)',
            'DJI Drones',
        ],
        'peak_price_range': (500, 18000),  # ZAR
        'top_platforms': ['Facebook Marketplace', 'Gumtree', 'OLX'],
        'demand_score': 95,
        'notes': (
            'Electronics is the single highest-turnover category on SA classifieds. '
            'Flagship phones sell within hours in Joburg/Cape Town. '
            'Laptops under R8 000 are in perpetual demand from students and WFH workers. '
            'PS5 scarcity has eased but premium pre-owned units still sell in <24 hrs.'
        ),
    },

    'vehicles': {
        'rank': 2,
        'avg_days_to_sell': 14,
        'hot_items': [
            'Toyota Hilux (used)',
            'Ford Ranger (used)',
            'VW Polo Vivo',
            'Suzuki Swift',
            'Toyota Fortuner (used)',
            'Toyota Corolla Cross',
            'Chery Tiggo 4',
            'Toyota Starlet',
            'Honda Jazz / Fit',
        ],
        'peak_price_range': (45000, 350000),  # ZAR
        'top_platforms': ['WeBuyCars', 'AutoTrader', 'Gumtree', 'Facebook Marketplace'],
        'demand_score': 90,
        'notes': (
            'WeBuyCars averages 15 000+ vehicle purchases/month (2025). '
            'Bakkies (Hilux, Ranger) dominate both new and used markets. '
            'Fuel-efficient hatchbacks (Swift, Polo Vivo) are top movers for <R200k budget. '
            'Chinese brands (Chery, Haval, GWM) rising fast as rand pressure pushes buyers toward value. '
            'SUVs remain aspirational — Fortuner is SA top used SUV despite high price. '
            'WeBuyCars AI "Blue" now executes purchases autonomously, compressing deal windows.'
        ),
    },

    'furniture': {
        'rank': 3,
        'avg_days_to_sell': 7,
        'hot_items': [
            'Lounge suites / couches',
            'Queen/king bed frames',
            'Dining table sets',
            'Wardrobes',
            'Office chairs (WFH)',
            'Coricraft / Rochester branded items',
        ],
        'peak_price_range': (500, 12000),  # ZAR
        'top_platforms': ['Facebook Marketplace', 'Gumtree', 'OLX'],
        'demand_score': 78,
        'notes': (
            'Furniture sells at ~35-65% off retail on second-hand platforms. '
            'Premium brands (Coricraft, Rochester) retain buyer confidence and command higher prices. '
            'End-of-month listings spike when tenants move. '
            'Flat-pack and branded office furniture popular post-COVID with WFH market. '
            'Facebook Marketplace dominates furniture due to photo-first browsing and local pickup.'
        ),
    },

    'appliances': {
        'rank': 4,
        'avg_days_to_sell': 6,
        'hot_items': [
            'Samsung / LG Fridges',
            'Samsung / Hisense Smart TVs',
            'Washing machines',
            'Defy / Whirlpool stoves',
            'Air conditioners (12 000 BTU)',
            'Generators (Eskom hedge)',
            'Inverters & lithium battery packs',
            'Air fryers',
        ],
        'peak_price_range': (500, 15000),  # ZAR
        'top_platforms': ['Gumtree', 'Facebook Marketplace', 'OLX'],
        'demand_score': 82,
        'notes': (
            'Load-shedding (loadshedding) has created a sustained boom in generators, inverters, '
            'and solar-related appliances — even as Eskom stabilises, buyers remain cautious. '
            'Fridges and washing machines are high-intent purchases (buyers decide quickly). '
            'Smart TVs under R3 500 sell within 2-3 days. '
            'Air fryers have become a lifestyle staple — used ones sell fast at R600-R1 200.'
        ),
    },

    'clothing_fashion': {
        'rank': 5,
        'avg_days_to_sell': 10,
        'hot_items': [
            'Branded sneakers (Nike, Adidas, Jordan)',
            'Designer handbags',
            'Kids clothing bundles',
            'School uniforms',
            'Matric dance / formal wear',
            'Work / office attire',
        ],
        'peak_price_range': (100, 5000),  # ZAR
        'top_platforms': ['Facebook Marketplace', 'Gumtree', 'Yaga'],
        'demand_score': 72,
        'notes': (
            'Clothing volume is very high but margins are thin. '
            'Branded sneakers (especially Jordans and Yeezys) flip quickly and profitably. '
            'Kids clothing bundles (back-to-school Jan, mid-year Jul) spike seasonally. '
            'Yaga SA gaining traction as a fashion-specific resale platform. '
            'Counterfeit risk highest in this category — safety scoring critical.'
        ),
    },

    'power_solar': {
        'rank': 6,
        'avg_days_to_sell': 4,
        'hot_items': [
            'Portable power stations (EcoFlow, Jackery, Bluetti)',
            'Lithium LiFePO4 batteries (100Ah-200Ah)',
            'Victron MPPT charge controllers',
            'Solar panels (100W-400W)',
            'Inverter/UPS combos',
            'Automatic transfer switches',
            'Load-shedding LED lighting kits',
        ],
        'peak_price_range': (800, 45000),  # ZAR
        'top_platforms': ['Gumtree', 'Facebook Marketplace', 'Bidorbuy'],
        'demand_score': 88,
        'notes': (
            'Post-loadshedding normality has reduced panic buying but the market remains large. '
            'Homeowners who over-invested now sell surplus at attractive discounts. '
            'Brand-name portable power stations (EcoFlow DELTA) sell fast at 40-50% off retail. '
            'Victron components retain value exceptionally well. '
            'Strong demand in Cape Town and Joburg suburbs for whole-home backup solutions.'
        ),
    },

    'tools_hardware': {
        'rank': 7,
        'avg_days_to_sell': 8,
        'hot_items': [
            'DeWalt / Makita power tools',
            'Angle grinders',
            'Cordless drill sets',
            'Laser levels',
            'Welding machines',
            'Compressors',
            'Scaffolding / ladders',
        ],
        'peak_price_range': (300, 8000),  # ZAR
        'top_platforms': ['Gumtree', 'Facebook Marketplace', 'Bidorbuy'],
        'demand_score': 68,
        'notes': (
            'Construction boom in Gauteng and Western Cape drives steady tool demand. '
            'Contractors regularly seek to buy/sell job-completion surplus. '
            'DeWalt 18V system commands premium resale value. '
            'Power tools are a theft risk — serial number verification important for safety system.'
        ),
    },

    'garden_outdoor': {
        'rank': 8,
        'avg_days_to_sell': 9,
        'hot_items': [
            'Lawnmowers (petrol)',
            'Outdoor furniture sets',
            'Braai / Weber grills',
            'Garden sheds',
            'Trampoline sets',
            'Above-ground swimming pools',
        ],
        'peak_price_range': (300, 10000),  # ZAR
        'top_platforms': ['Facebook Marketplace', 'Gumtree'],
        'demand_score': 60,
        'notes': (
            'Summer (Oct-Feb) is peak season for outdoor items. '
            'Braai equipment is a SA cultural staple and sells year-round. '
            'Large items benefit from Facebook Marketplace local-pickup model. '
            'Trampolines and pools spike Jan-Feb and then again in Nov pre-summer.'
        ),
    },

    'baby_kids': {
        'rank': 9,
        'avg_days_to_sell': 5,
        'hot_items': [
            'Baby strollers / prams',
            'Cot / crib sets',
            'Baby monitors',
            'Kids bicycles',
            'Educational toys / LEGO sets',
            'Car seats',
        ],
        'peak_price_range': (200, 6000),  # ZAR
        'top_platforms': ['Facebook Marketplace', 'Gumtree'],
        'demand_score': 75,
        'notes': (
            'High-velocity category — parents move items fast as children outgrow them. '
            'Car seats and prams sell within days if priced correctly. '
            'LEGO and branded toy sets have strong collector/resale value. '
            'Safety certification of car seats is a key buyer concern — '
            'our safety system should flag items missing safety compliance info.'
        ),
    },

    'sports_fitness': {
        'rank': 10,
        'avg_days_to_sell': 7,
        'hot_items': [
            'Gym equipment (dumbbells, benches)',
            'Treadmills',
            'Road bicycles',
            'Mountain bikes',
            'Surfboards / bodyboards',
            'Fishing gear',
            'Trail running gear',
        ],
        'peak_price_range': (300, 20000),  # ZAR
        'top_platforms': ['Facebook Marketplace', 'Gumtree', 'Bidorbuy'],
        'demand_score': 65,
        'notes': (
            'New Year resolution spike in Jan for gym equipment. '
            'Mountain biking culture strong in Cape Town / Paarl — bikes sell fast at all price points. '
            'Fishing gear is a top category on Bidorbuy (auction model suits rare/specialist items). '
            'Treadmills are notoriously slow movers unless priced aggressively (>40% off retail).'
        ),
    },

    'books_media': {
        'rank': 11,
        'avg_days_to_sell': 14,
        'hot_items': [
            'University textbooks',
            'Matric study guides',
            'Bestseller novels',
            'Vinyl records',
            'Board games',
            'Video game titles',
        ],
        'peak_price_range': (30, 800),  # ZAR
        'top_platforms': ['Facebook Marketplace', 'Gumtree', 'Bidorbuy'],
        'demand_score': 45,
        'notes': (
            'Low average transaction value but high listing volume. '
            'University textbooks spike Jan and Jul (semester start). '
            'Vinyl records have niche but passionate SA collector market. '
            'Board games and video game titles sell well during December school holidays.'
        ),
    },

    'collectibles_antiques': {
        'rank': 12,
        'avg_days_to_sell': 21,
        'hot_items': [
            'SA coins / Krugerrands',
            'Stamps (SA Post Office sets)',
            'Vintage Springbok rugby memorabilia',
            'Apartheid-era ephemera',
            'Vintage watches',
            'Art (SA artists)',
        ],
        'peak_price_range': (100, 50000),  # ZAR
        'top_platforms': ['Bidorbuy', 'Facebook Marketplace'],
        'demand_score': 50,
        'notes': (
            'Bidorbuy (now Bob Shop) dominates this niche with its auction format. '
            'Krugerrands track gold price — currently high demand. '
            'Springbok rugby memorabilia spikes during Rugby World Cup cycles. '
            'Provenance verification is critical — SA art market has documented forgery issues.'
        ),
    },

    'property_rentals': {
        'rank': 13,
        'avg_days_to_sell': 30,
        'hot_items': [
            'Flatlets / garden cottages to rent',
            'Room rentals',
            'Student accommodation',
            'Commercial space',
        ],
        'peak_price_range': (3500, 25000),  # ZAR/month
        'top_platforms': ['Gumtree', 'Facebook Marketplace', 'Property24'],
        'demand_score': 70,
        'notes': (
            'High demand but slow transaction cycle. '
            'Student accommodation peaks Jan/Feb and Jun/Jul. '
            'Room rentals in Sandton, Rondebosch, Hatfield are hyper-competitive. '
            'Scam risk is very high in this category — advance payment fraud common.'
        ),
    },

    'services': {
        'rank': 14,
        'avg_days_to_sell': 2,  # service inquiries, not physical goods
        'hot_items': [
            'Plumbers',
            'Electricians',
            'Domestic workers',
            'Garden services',
            'IT support / PC repairs',
            'Tutoring (Maths, Science)',
            'Photography',
        ],
        'peak_price_range': (200, 5000),  # ZAR per job
        'top_platforms': ['Gumtree', 'Facebook Marketplace'],
        'demand_score': 55,
        'notes': (
            'Services listings are high volume but hard to automate deal-scoring. '
            'Tutor demand peaks Jan (matric/university intake) and Sep (exam prep). '
            'IT/PC repairs surged with WFH normalisation. '
            'Phase 2 Skills Marketplace can capture this category more effectively.'
        ),
    },

    'musical_instruments': {
        'rank': 15,
        'avg_days_to_sell': 11,
        'hot_items': [
            'Electric guitars',
            'Digital pianos / keyboards',
            'DJ controllers (Pioneer, Denon)',
            'Audio interfaces',
            'Studio monitors',
            'Acoustic guitars',
        ],
        'peak_price_range': (500, 25000),  # ZAR
        'top_platforms': ['Gumtree', 'Facebook Marketplace'],
        'demand_score': 52,
        'notes': (
            'SA music scene (amapiano, Afrobeats) drives demand for DJ gear. '
            'Pioneer DJ controllers retain excellent resale value. '
            'Guitars and keyboards have passionate niche buyer community. '
            'December Christmas gifting spikes this category significantly.'
        ),
    },
}


# ---------------------------------------------------------------------------
# PLATFORM INTELLIGENCE
# ---------------------------------------------------------------------------

PLATFORM_INTELLIGENCE = {
    'facebook_marketplace': {
        'best_categories': [
            'furniture', 'electronics', 'appliances', 'vehicles',
            'clothing_fashion', 'baby_kids', 'garden_outdoor',
        ],
        'monthly_active_users_sa': 14_000_000,  # estimated SA active users 2025
        'avg_response_time_hours': 2,
        'peak_hours': ['07:00-09:00', '12:00-13:00', '18:00-21:00'],  # SAST
        'peak_days': ['Tuesday', 'Thursday', 'Saturday', 'Sunday'],
        'listing_cost': 'Free',
        'boost_available': True,
        'strengths': [
            'Largest active user base in SA',
            'Hyper-local discovery via Maps',
            'Seller profile/reputation visible',
            'Integrated Messenger for negotiation',
            'Photo-first browsing optimised for impulse discovery',
            'Cross-posting to Buy/Sell groups multiplies reach',
        ],
        'weaknesses': [
            'High scam density (17% of users report being defrauded)',
            'No built-in escrow or payment protection',
            'Algorithm changes can reduce organic listing reach',
            'Fake/bot accounts inflate "interested" counts',
            'No search by serial number or item condition grade',
        ],
        'scam_risk_level': 'HIGH',
        'notes': (
            'Dominant platform for fast local deals. '
            'Phishing via WhatsApp links is the #1 reported scam vector. '
            'Sellers should always use Marketplace Messenger — not personal WhatsApp — '
            'for safety audit trail.'
        ),
    },

    'gumtree': {
        'best_categories': [
            'vehicles', 'electronics', 'furniture', 'appliances',
            'property_rentals', 'services', 'tools_hardware',
        ],
        'monthly_active_users_sa': 3_800_000,
        'monthly_buyers': 1_500_000,
        'avg_response_time_hours': 4,
        'peak_hours': ['08:00-10:00', '12:00-14:00', '19:00-21:00'],  # SAST
        'peak_days': ['Monday', 'Wednesday', 'Saturday'],
        'listing_cost': 'Free (basic); R59+ for boost; professional packages available',
        'boost_available': True,
        'strengths': [
            'Most established SA classifieds brand (high trust)',
            'Strong SEO — listings appear in Google search',
            'Category breadth covers services and property',
            'Email alert system for saved searches',
            'Business seller packages with analytics',
        ],
        'weaknesses': [
            'Declining relative to Facebook Marketplace',
            'Older UI/UX compared to competitors',
            'Response rates slower than Facebook',
            'Limited mobile app functionality',
        ],
        'scam_risk_level': 'MEDIUM',
        'notes': (
            '3.8M visits/month, 1.5M active buyers. '
            'Phishing scam (fake payment confirmation links) widely reported 2022-2025. '
            'Best for vehicles and property where buyers expect formal listings.'
        ),
    },

    'olx': {
        'best_categories': [
            'electronics', 'clothing_fashion', 'furniture', 'appliances',
        ],
        'monthly_active_users_sa': 1_200_000,  # declining — merging with Bidorbuy into Bob Shop
        'avg_response_time_hours': 6,
        'peak_hours': ['09:00-11:00', '13:00-15:00'],  # SAST
        'peak_days': ['Wednesday', 'Thursday', 'Saturday'],
        'listing_cost': 'Free (paid boosts available)',
        'boost_available': True,
        'strengths': [
            'Simple listing process',
            'Good mobile app',
            'International brand recognition',
        ],
        'weaknesses': [
            'Significantly declining user base vs Gumtree and Facebook Marketplace',
            'Merging into Bob Shop — platform uncertainty',
            'Lower buyer intent than Gumtree',
        ],
        'scam_risk_level': 'MEDIUM',
        'notes': (
            'OLX SA is merging with Bidorbuy to form Bob Shop. '
            'User base has contracted substantially. '
            'Still worth scanning for electronics bargains but response rates are lower.'
        ),
    },

    'webuycars': {
        'best_categories': ['vehicles'],
        'monthly_active_users_sa': 8_700_000,  # website viewers/month
        'monthly_purchases': 15_390,
        'monthly_sales': 15_232,
        'avg_response_time_hours': 1,  # AI-assisted instant valuations
        'peak_hours': ['09:00-11:00', '14:00-17:00'],  # SAST
        'peak_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
        'listing_cost': 'N/A — platform buys directly; consumer-to-dealer model',
        'boost_available': False,
        'strengths': [
            'Largest dedicated used vehicle marketplace in SA',
            'AI-powered ("Blue") instant vehicle valuations',
            'Nationwide presence — multiple physical depots',
            '8.7M website viewers/month',
            'Fast transactions — instant cash offers',
            'No private seller haggling required',
        ],
        'weaknesses': [
            'Vehicles only — single-category platform',
            'Dealer pricing means sellers get less than private sale',
            'Limited to SA geographic coverage',
        ],
        'scam_risk_level': 'LOW',
        'notes': (
            'WeBuyCars is a dealer — scam risk to consumers is low vs peer-to-peer platforms. '
            '12.9% YoY growth in purchases in 2025. '
            'AI "Blue" system now closes some vehicle purchases without human involvement. '
            'Scout Delta should monitor their public listings for deal arbitrage opportunities.'
        ),
    },

    'bidorbuy': {
        'best_categories': [
            'collectibles_antiques', 'tools_hardware', 'sports_fitness',
            'books_media', 'musical_instruments', 'power_solar',
        ],
        'monthly_active_users_sa': 800_000,  # estimated, platform rebranding to Bob Shop
        'avg_response_time_hours': 12,  # auction format — inherently slower
        'peak_hours': ['20:00-22:00'],  # Auctions end in evenings
        'peak_days': ['Sunday', 'Monday'],
        'listing_cost': 'Free to list; success fee applies on sale (2-7%)',
        'boost_available': True,
        'strengths': [
            'Auction format creates price discovery — good for rare/collectible items',
            'Buyer protection program',
            'Large catalogue (3M+ items)',
            'Strong collector and niche community',
            'Merging with OLX (Bob Shop) may boost reach',
        ],
        'weaknesses': [
            'Slower transaction cadence (auction timelines)',
            'Lower traffic than Facebook/Gumtree for everyday items',
            'Rebranding to Bob Shop creates uncertainty',
        ],
        'scam_risk_level': 'LOW-MEDIUM',
        'notes': (
            'Second-hand sales make up ~40% of all Bidorbuy transactions. '
            'Collectibles, coins, stamps, fishing gear, and tools are strongest categories. '
            'Auction sniping in final minutes is common — Scout should monitor closing auctions '
            'for below-market final prices.'
        ),
    },
}


# ---------------------------------------------------------------------------
# PRICE BENCHMARKS
# Realistic SA market prices for deal-scoring (ZAR)
# Format: 'item_key': {'poor': ZAR, 'fair': ZAR, 'good': ZAR, 'excellent': ZAR}
# 'poor'      = damaged / faulty / missing accessories
# 'fair'      = working, heavy wear, original box missing
# 'good'      = working well, minor cosmetic marks, accessories present
# 'excellent' = like new / sealed / full accessories
# ---------------------------------------------------------------------------

PRICE_BENCHMARKS = {
    # --- Smartphones ---
    'iphone_15_pro_max_256gb': {'poor': 12000, 'fair': 16000, 'good': 19000, 'excellent': 22000},
    'iphone_15_pro_128gb':     {'poor': 10000, 'fair': 13500, 'good': 16500, 'excellent': 19500},
    'iphone_15_128gb':         {'poor': 8000,  'fair': 11000, 'good': 14000, 'excellent': 17000},
    'iphone_14_128gb':         {'poor': 6500,  'fair': 8500,  'good': 11000, 'excellent': 13500},
    'iphone_14_pro_128gb':     {'poor': 8000,  'fair': 11000, 'good': 14000, 'excellent': 17000},
    'iphone_13_128gb':         {'poor': 4500,  'fair': 6000,  'good': 7800,  'excellent': 9500},
    'iphone_12_64gb':          {'poor': 2500,  'fair': 3500,  'good': 4500,  'excellent': 5500},
    'iphone_11_64gb':          {'poor': 1800,  'fair': 2500,  'good': 3200,  'excellent': 4000},
    'samsung_s24_ultra_256gb': {'poor': 9000,  'fair': 13000, 'good': 16000, 'excellent': 20000},
    'samsung_s24_256gb':       {'poor': 6000,  'fair': 8500,  'good': 11000, 'excellent': 14000},
    'samsung_s23_ultra_256gb': {'poor': 7000,  'fair': 10000, 'good': 12500, 'excellent': 15000},
    'samsung_s23_256gb':       {'poor': 4500,  'fair': 6500,  'good': 8500,  'excellent': 11000},
    'samsung_a55_128gb':       {'poor': 2500,  'fair': 3500,  'good': 4500,  'excellent': 5500},
    'samsung_a35_128gb':       {'poor': 1800,  'fair': 2500,  'good': 3200,  'excellent': 4000},

    # --- Laptops ---
    'macbook_air_m2_8gb_256gb':    {'poor': 12000, 'fair': 16000, 'good': 20000, 'excellent': 24000},
    'macbook_air_m2_8gb_512gb':    {'poor': 14000, 'fair': 18000, 'good': 23000, 'excellent': 27000},
    'macbook_pro_m3_14in_512gb':   {'poor': 20000, 'fair': 26000, 'good': 32000, 'excellent': 38000},
    'macbook_air_m1_8gb_256gb':    {'poor': 8000,  'fair': 11000, 'good': 14000, 'excellent': 17000},
    'dell_xps_15_i7_16gb_512gb':   {'poor': 8000,  'fair': 12000, 'good': 16000, 'excellent': 20000},
    'dell_xps_13_i5_8gb_256gb':    {'poor': 5000,  'fair': 7500,  'good': 10000, 'excellent': 13000},
    'hp_elitebook_840_g8_i5':      {'poor': 5000,  'fair': 7000,  'good': 9000,  'excellent': 11500},
    'lenovo_thinkpad_x1_carbon':   {'poor': 6000,  'fair': 9000,  'good': 12000, 'excellent': 15000},
    'lenovo_ideapad_i5_8gb_256gb': {'poor': 3000,  'fair': 4500,  'good': 6000,  'excellent': 7500},
    'asus_vivobook_i3_4gb':        {'poor': 1500,  'fair': 2500,  'good': 3500,  'excellent': 4500},

    # --- Tablets ---
    'ipad_pro_12_9_m2_256gb':  {'poor': 9000,  'fair': 13000, 'good': 17000, 'excellent': 21000},
    'ipad_air_m1_64gb':        {'poor': 5000,  'fair': 7000,  'good': 9000,  'excellent': 11000},
    'ipad_10th_gen_64gb':      {'poor': 4000,  'fair': 5500,  'good': 7000,  'excellent': 8500},
    'samsung_tab_s9_ultra':    {'poor': 10000, 'fair': 14000, 'good': 18000, 'excellent': 22000},
    'samsung_tab_s9_256gb':    {'poor': 6000,  'fair': 8500,  'good': 11000, 'excellent': 14000},

    # --- Gaming ---
    'ps5_disc_edition':        {'poor': 6000,  'fair': 8000,  'good': 10000, 'excellent': 12000},
    'ps5_digital_edition':     {'poor': 5000,  'fair': 6500,  'good': 8000,  'excellent': 10000},
    'xbox_series_x':           {'poor': 5500,  'fair': 7000,  'good': 8500,  'excellent': 10500},
    'xbox_series_s':           {'poor': 3000,  'fair': 4000,  'good': 5000,  'excellent': 6500},
    'nintendo_switch_oled':    {'poor': 3000,  'fair': 4000,  'good': 5000,  'excellent': 6500},
    'playstation_4_pro':       {'poor': 2500,  'fair': 3500,  'good': 4500,  'excellent': 5500},

    # --- TVs ---
    'samsung_55in_qled_4k':    {'poor': 4000,  'fair': 6000,  'good': 8000,  'excellent': 11000},
    'samsung_65in_qled_4k':    {'poor': 7000,  'fair': 10000, 'good': 13000, 'excellent': 17000},
    'lg_c3_55in_oled':         {'poor': 8000,  'fair': 12000, 'good': 16000, 'excellent': 20000},
    'hisense_55in_4k':         {'poor': 2500,  'fair': 3500,  'good': 5000,  'excellent': 6500},

    # --- Audio ---
    'airpods_pro_2nd_gen':     {'poor': 1500,  'fair': 2200,  'good': 2900,  'excellent': 3500},
    'sony_wh1000xm5':          {'poor': 2000,  'fair': 3000,  'good': 4000,  'excellent': 5000},
    'bose_quietcomfort_45':    {'poor': 2000,  'fair': 3000,  'good': 4000,  'excellent': 5000},
    'jbl_boombox_3':           {'poor': 1500,  'fair': 2200,  'good': 3000,  'excellent': 4000},

    # --- Power / Solar ---
    'ecoflow_delta_2':         {'poor': 6000,  'fair': 9000,  'good': 12000, 'excellent': 16000},
    'ecoflow_delta_pro':       {'poor': 12000, 'fair': 17000, 'good': 22000, 'excellent': 28000},
    'victron_mppt_100_50':     {'poor': 2000,  'fair': 3000,  'good': 4000,  'excellent': 5000},
    'lifepo4_100ah_12v':       {'poor': 1500,  'fair': 2500,  'good': 3500,  'excellent': 4500},
    'generator_5kva_petrol':   {'poor': 5000,  'fair': 8000,  'good': 11000, 'excellent': 14000},

    # --- Vehicles (representative models) ---
    'toyota_hilux_2020_4x4':   {'poor': 280000, 'fair': 340000, 'good': 400000, 'excellent': 450000},
    'ford_ranger_2021_wildtrak':{'poor': 300000,'fair': 380000, 'good': 440000, 'excellent': 500000},
    'vw_polo_vivo_2020_1_4':   {'poor': 100000, 'fair': 130000, 'good': 155000, 'excellent': 175000},
    'suzuki_swift_2021_1_2':   {'poor': 100000, 'fair': 130000, 'good': 155000, 'excellent': 175000},
    'toyota_fortuner_2020_4x4':{'poor': 380000, 'fair': 460000, 'good': 530000, 'excellent': 600000},
    'toyota_corolla_cross_2022':{'poor': 260000,'fair': 310000, 'good': 360000, 'excellent': 400000},

    # --- Furniture ---
    'coricraft_couch_3seater': {'poor': 2000,  'fair': 4000,  'good': 7000,  'excellent': 12000},
    'queen_bed_frame_wood':    {'poor': 500,   'fair': 1500,  'good': 3000,  'excellent': 5000},
    'dining_table_6seater':    {'poor': 1000,  'fair': 2500,  'good': 5000,  'excellent': 9000},
    'office_desk_gaming':      {'poor': 500,   'fair': 1200,  'good': 2500,  'excellent': 4000},

    # --- Appliances ---
    'samsung_fridge_321l':     {'poor': 1500,  'fair': 2500,  'good': 4000,  'excellent': 6000},
    'samsung_65in_smart_tv':   {'poor': 3000,  'fair': 5000,  'good': 7500,  'excellent': 10000},
    'washing_machine_7kg':     {'poor': 1000,  'fair': 2000,  'good': 3500,  'excellent': 5000},
    'air_fryer_4l':            {'poor': 300,   'fair': 600,   'good': 900,   'excellent': 1400},
    'defy_stove_4plate':       {'poor': 1000,  'fair': 2000,  'good': 3500,  'excellent': 5000},
    'air_conditioner_12kbtu':  {'poor': 1500,  'fair': 2500,  'good': 3500,  'excellent': 5000},
}


# ---------------------------------------------------------------------------
# SEASONAL TRENDS
# Month numbers: 1=Jan, 2=Feb ... 12=Dec
# Score 0-100 per category per month (relative demand index)
# ---------------------------------------------------------------------------

SEASONAL_TRENDS = {
    'electronics': {
        'peak_months': [11, 12, 1],  # Black Friday, December holidays, January (back to school tech)
        'trough_months': [3, 4, 5],
        'monthly_index': {
            1: 80, 2: 65, 3: 55, 4: 50, 5: 50,
            6: 60, 7: 65, 8: 65, 9: 70, 10: 75,
            11: 100, 12: 95,
        },
        'key_events': [
            'Black Friday (Nov) — biggest single electronics spike',
            'December school holidays — gaming, tablets spike',
            'January back-to-school — laptops, calculators, earphones',
            'June/July school holidays — moderate secondary spike',
        ],
    },

    'vehicles': {
        'peak_months': [1, 2, 10, 11],
        'trough_months': [6, 7],
        'monthly_index': {
            1: 90, 2: 85, 3: 75, 4: 65, 5: 60,
            6: 50, 7: 55, 8: 65, 9: 75, 10: 85,
            11: 90, 12: 80,
        },
        'key_events': [
            'January — year-start purchases, new vehicle registrations',
            'October/November — bonus season, year-end upgrades',
            'Winter (Jun/Jul) — slowest period for private vehicle sales',
        ],
    },

    'furniture': {
        'peak_months': [1, 2, 10, 11],
        'trough_months': [5, 6, 7],
        'monthly_index': {
            1: 90, 2: 85, 3: 70, 4: 60, 5: 50,
            6: 45, 7: 50, 8: 60, 9: 65, 10: 80,
            11: 90, 12: 85,
        },
        'key_events': [
            'January — students and new tenants furnishing places',
            'November Black Friday — major furniture retailer sales push second-hand market',
            'End of month — tenants moving spike second-hand listings',
        ],
    },

    'appliances': {
        'peak_months': [11, 12, 1],
        'trough_months': [4, 5],
        'monthly_index': {
            1: 80, 2: 70, 3: 65, 4: 55, 5: 55,
            6: 70, 7: 70, 8: 65, 9: 65, 10: 75,
            11: 100, 12: 90,
        },
        'key_events': [
            'Black Friday (Nov) — biggest appliance deals of the year',
            'Winter (Jun/Jul) — heaters, air conditioners, generators spike',
            'December — gifting season for small appliances',
        ],
    },

    'power_solar': {
        'peak_months': [5, 6, 7, 8],  # Winter + load-shedding anxiety
        'trough_months': [1, 2],
        'monthly_index': {
            1: 50, 2: 45, 3: 55, 4: 65, 5: 85,
            6: 95, 7: 100, 8: 90, 9: 75, 10: 65,
            11: 60, 12: 55,
        },
        'key_events': [
            'Winter months — load-shedding historically worsens, driving demand',
            'Year-round baseline demand remains elevated post-2022 loadshedding crisis',
        ],
    },

    'clothing_fashion': {
        'peak_months': [11, 12, 1],
        'trough_months': [4, 5, 6],
        'monthly_index': {
            1: 85, 2: 70, 3: 60, 4: 50, 5: 50,
            6: 55, 7: 60, 8: 65, 9: 70, 10: 75,
            11: 100, 12: 95,
        },
        'key_events': [
            'November Black Friday — peak fashion search interest (index 89 in 2025)',
            'January — back-to-school uniforms, children clothing bundles',
            'September/October — spring fashion refresh',
            'Matric farewell season (Sep-Oct) — formal wear spike',
        ],
    },

    'baby_kids': {
        'peak_months': [1, 11, 12],
        'trough_months': [5, 6],
        'monthly_index': {
            1: 95, 2: 75, 3: 65, 4: 60, 5: 55,
            6: 55, 7: 65, 8: 65, 9: 70, 10: 75,
            11: 90, 12: 95,
        },
        'key_events': [
            'January — school readiness purchases',
            'December — Christmas gifting season',
            'July — mid-year toy clearouts',
        ],
    },

    'garden_outdoor': {
        'peak_months': [10, 11, 12, 1],  # Southern hemisphere summer
        'trough_months': [5, 6, 7],
        'monthly_index': {
            1: 90, 2: 85, 3: 70, 4: 55, 5: 40,
            6: 35, 7: 40, 8: 50, 9: 65, 10: 85,
            11: 95, 12: 100,
        },
        'key_events': [
            'October/November — summer prep, outdoor furniture, pools',
            'December — peak braai equipment demand',
            'January — post-Christmas pool and garden equipment',
        ],
    },

    'sports_fitness': {
        'peak_months': [1, 9, 10],
        'trough_months': [5, 6, 7],
        'monthly_index': {
            1: 100, 2: 80, 3: 65, 4: 55, 5: 50,
            6: 50, 7: 55, 8: 65, 9: 80, 10: 85,
            11: 75, 12: 70,
        },
        'key_events': [
            'January — New Year resolution gym equipment purchases',
            'September/October — spring outdoor activity ramp-up',
            'Comrades Marathon (May) — running gear spike',
            'Two Oceans Marathon (April) — trail running gear spike',
        ],
    },

    'collectibles_antiques': {
        'peak_months': [11, 12],
        'trough_months': [2, 3],
        'monthly_index': {
            1: 60, 2: 50, 3: 50, 4: 55, 5: 60,
            6: 65, 7: 70, 8: 65, 9: 65, 10: 70,
            11: 90, 12: 85,
        },
        'key_events': [
            'Rugby World Cup years — Springbok memorabilia peaks',
            'Heritage Day (24 Sep) — SA cultural collectibles awareness',
            'December — collectors making year-end acquisitions',
        ],
    },
}


# ---------------------------------------------------------------------------
# SCAM RED FLAGS
# Used by the safety scoring engine to weight risk scores
# ---------------------------------------------------------------------------

SCAM_RED_FLAGS = {
    'price_anomaly': {
        'description': 'Price is significantly below market benchmark',
        'risk_weight': 30,
        'threshold_pct_below_market': 40,  # >40% below "poor" benchmark triggers flag
        'notes': (
            '"When the offer seems too good to be true, it usually is." '
            'Phantom listings at deep discounts are the most common SA scam entry point.'
        ),
    },
    'advance_payment_demand': {
        'description': 'Seller demands payment before item is inspected or confirmed',
        'risk_weight': 40,
        'notes': (
            'SAPS and multiple consumer protection orgs warn this is the #1 red flag. '
            'Especially prevalent in vehicle and property listings.'
        ),
    },
    'external_link_in_listing': {
        'description': 'Listing contains links to external URLs (phishing risk)',
        'risk_weight': 35,
        'notes': (
            'Gumtree SA and Facebook Marketplace both issued formal warnings '
            'about phishing links sent via WhatsApp/email posing as payment confirmations.'
        ),
    },
    'whatsapp_redirect_early': {
        'description': 'Seller immediately redirects off-platform to WhatsApp',
        'risk_weight': 25,
        'notes': 'Legitimate sellers are patient with in-app messaging initially.',
    },
    'new_account_high_value': {
        'description': 'Account created <30 days ago listing high-value item',
        'risk_weight': 30,
        'notes': 'Scam accounts are disposable; new profiles selling R5000+ items are high risk.',
    },
    'no_profile_picture': {
        'description': 'Seller has no profile picture or minimal profile information',
        'risk_weight': 15,
    },
    'refuses_meetup': {
        'description': 'Seller refuses in-person inspection or meetup',
        'risk_weight': 35,
        'notes': (
            'Phantom listings (non-existent products) always refuse inspection. '
            'SAPS documented case: R10 000 paid for non-existent vehicle in Midrand.'
        ),
    },
    'overpayment_scam_pattern': {
        'description': 'Buyer claims to have overpaid and requests refund',
        'risk_weight': 45,
        'notes': 'Targets sellers. Fake payment screenshots sent; refund request is the scam.',
    },
    'counterfeit_risk_category': {
        'description': 'Category has documented high counterfeit incidence',
        'risk_weight': 20,
        'high_risk_categories': ['clothing_fashion', 'collectibles_antiques', 'musical_instruments'],
        'notes': 'Designer clothing, perfume, jewellery, signed memorabilia are primary targets.',
    },
    'recycled_listing_text': {
        'description': 'Listing description matches known scam scripts',
        'risk_weight': 40,
        'notes': (
            'Organised scam networks use near-identical message patterns and recycled scripts. '
            'NLP pattern matching can detect these with >80% accuracy.'
        ),
    },
    'multiple_platforms_same_item': {
        'description': 'Same item listed simultaneously on multiple platforms (potential double-sell)',
        'risk_weight': 20,
    },
    'stolen_goods_indicator': {
        'description': 'No serial number, IMEI blocked, or known theft pattern',
        'risk_weight': 50,
        'notes': (
            'Power tools and electronics are primary stolen goods categories in SA. '
            'IMEI check integration planned for Phase 2.'
        ),
    },
}


# ---------------------------------------------------------------------------
# DEAL VALUE SCORING FORMULA PARAMETERS
# ---------------------------------------------------------------------------

DEAL_SCORE_WEIGHTS = {
    'price_vs_benchmark': 40,     # % weight: how good the price is vs market
    'category_demand':    20,     # % weight: demand score of the category
    'platform_trust':     15,     # % weight: platform scam risk adjustment
    'seller_profile':     10,     # % weight: account age, listings history
    'listing_quality':    10,     # % weight: photos, description completeness
    'urgency_signals':     5,     # % weight: "moving house", "urgent sale" keywords
}

PLATFORM_TRUST_MULTIPLIERS = {
    'webuycars':          1.0,    # highest trust (dealer)
    'bidorbuy':           0.95,
    'gumtree':            0.90,
    'olx':                0.87,
    'facebook_marketplace': 0.82, # lowest trust (highest scam incidence)
}
