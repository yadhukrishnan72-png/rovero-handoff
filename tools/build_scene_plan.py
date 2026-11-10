#!/usr/bin/env python3
"""Builds destination-art/scene-plan.xlsx: one row per destination (country or region group) with the scene type and
landmark proposed for its artwork. The owner reviews/edits this sheet; the scene generator will read it later.

Usage: python tools/build_scene_plan.py --plans destination-art/esim-plans-....xlsx --out destination-art/scene-plan.xlsx
"""
import argparse
import collections

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

TYPES = {
    'tropical-island': 'Palms, turquoise sea, beach, sailboats',
    'desert': 'Dunes, rock arches, mud-brick or stone landmarks',
    'savanna': 'Acacia or baobab trees, wildlife silhouettes, open plains',
    'alpine': 'Snow peaks, pines, chalets or mountain monasteries',
    'steppe': 'Wide grassland, yurts or horses, distant mountains',
    'boreal-forest': 'Pine forest, lake, red cabins, optional aurora',
    'city-skyline': 'Modern towers by the water at dusk',
    'fjord-coast': 'Cliffs, narrow bay, lighthouse or fishing houses',
    'volcanic': 'Volcano cone, glowing crater, black rock and sea',
    'rainforest': 'Dense tropical trees, river or waterfall, mist',
    'mediterranean': 'White and terracotta houses on hills above the sea',
    'farmland': 'Rolling fields, windmill or barn, hedgerows',
    'old-town': 'Historic spires, domes and rooftops with a landmark',
    'arctic': 'Icebergs, ice cap, northern lights',
}

# code: (name, scene type, landmark / motif, note)
C = {
    'AD': ('Andorra', 'alpine', 'Pyrenees valley village with a Romanesque bell tower', ''),
    'AE': ('United Arab Emirates', 'city-skyline', 'Burj Khalifa and dhow on the creek', ''),
    'AF': ('Afghanistan', 'alpine', 'Hindu Kush peaks and a mountain valley', 'Neutral landscape only'),
    'AG': ('Antigua and Barbuda', 'tropical-island', 'Sailboats in a harbour (sailing capital)', ''),
    'AI': ('Anguilla', 'tropical-island', 'White-sand beach and a sailing boat', ''),
    'AL': ('Albania', 'mediterranean', 'Riviera coast below rugged mountains', ''),
    'AM': ('Armenia', 'alpine', 'Stone hilltop monastery in mountains', 'Mount Ararat is a national symbol but lies in Turkey; kept out'),
    'AO': ('Angola', 'savanna', 'Calandula waterfalls and baobab', ''),
    'AR': ('Argentina', 'alpine', 'Patagonian granite peaks (Fitz Roy)', ''),
    'AT': ('Austria', 'alpine', 'Alpine village with an onion-dome church', ''),
    'AU': ('Australia', 'city-skyline', 'Sydney Opera House and harbour', ''),
    'AW': ('Aruba', 'tropical-island', 'Wind-bent divi-divi tree on a beach', ''),
    'AX': ('Aland Islands', 'fjord-coast', 'Archipelago with a red windmill', ''),
    'AZ': ('Azerbaijan', 'city-skyline', 'Baku Flame Towers', ''),
    'BA': ('Bosnia and Herzegovina', 'old-town', 'Mostar old bridge (Stari Most) over the river', ''),
    'BB': ('Barbados', 'tropical-island', 'Palm beach with a coral-stone lighthouse', ''),
    'BD': ('Bangladesh', 'rainforest', 'Delta river with a wooden boat and mangroves', ''),
    'BE': ('Belgium', 'old-town', 'Atomium and Brussels guild houses', ''),
    'BF': ('Burkina Faso', 'savanna', 'Sahel plain with a baobab and round huts', ''),
    'BG': ('Bulgaria', 'old-town', 'Alexander Nevsky Cathedral domes, Rila mountains behind', ''),
    'BH': ('Bahrain', 'city-skyline', 'World Trade Center towers and a pearl-diving dhow', ''),
    'BJ': ('Benin', 'savanna', 'Stilt houses of Ganvie on a lake', ''),
    'BL': ('Saint Barthelemy', 'tropical-island', 'Yachts in a small harbour', ''),
    'BM': ('Bermuda', 'tropical-island', 'Pastel houses and Gibbs Hill lighthouse', ''),
    'BN': ('Brunei', 'old-town', 'Golden mosque dome beside a water village', 'Religious building as landmark; confirm'),
    'BO': ('Bolivia', 'alpine', 'Uyuni salt-flat mirror with a llama', ''),
    'BQ': ('Caribbean Netherlands', 'tropical-island', 'Flamingos in a salt lake, windswept shore', 'Bonaire, Saba, Sint Eustatius'),
    'BR': ('Brazil', 'tropical-island', 'Christ the Redeemer above Rio bay and Sugarloaf', 'Religious statue as landmark; confirm'),
    'BS': ('Bahamas', 'tropical-island', 'Turquoise shallows and a small boat', ''),
    'BT': ('Bhutan', 'alpine', 'Tiger\'s Nest cliff monastery', ''),
    'BW': ('Botswana', 'savanna', 'Elephants crossing the Okavango at dusk', ''),
    'BY': ('Belarus', 'boreal-forest', 'Primeval forest and a European bison', ''),
    'BZ': ('Belize', 'tropical-island', 'Cayes, reef water and a sailboat', ''),
    'CA': ('Canada', 'alpine', 'Rocky Mountain lake with a canoe and maple tree', ''),
    'CD': ('Democratic Republic of the Congo', 'rainforest', 'Congo River rainforest with an okapi', ''),
    'CF': ('Central African Republic', 'savanna', 'Forest-edge savanna with elephants', ''),
    'CG': ('Republic of the Congo', 'rainforest', 'River and dense rainforest canopy', ''),
    'CH': ('Switzerland', 'alpine', 'Matterhorn above a chalet village', ''),
    'CI': ('Cote d\'Ivoire', 'tropical-island', 'Lagoon palms and Abidjan skyline', ''),
    'CL': ('Chile', 'alpine', 'Torres del Paine towers over a lake', ''),
    'CM': ('Cameroon', 'volcanic', 'Mount Cameroon above rainforest', ''),
    'CN': ('China', 'alpine', 'Great Wall on a ridge with a pagoda', ''),
    'CO': ('Colombia', 'rainforest', 'Cocora valley wax palms in mist', ''),
    'CR': ('Costa Rica', 'rainforest', 'Arenal volcano above rainforest with a toucan', ''),
    'CV': ('Cabo Verde', 'volcanic', 'Pico do Fogo above a black-sand bay', ''),
    'CW': ('Curacao', 'tropical-island', 'Pastel Willemstad waterfront houses', ''),
    'CY': ('Cyprus', 'mediterranean', 'Rocky coves and a stone harbour', ''),
    'CZ': ('Czechia', 'old-town', 'Prague Castle spires and Charles Bridge', ''),
    'DE': ('Germany', 'old-town', 'Brandenburg Gate', ''),
    'DK': ('Denmark', 'old-town', 'Nyhavn coloured harbour houses', ''),
    'DM': ('Dominica', 'rainforest', 'Waterfall in lush rainforest', ''),
    'DO': ('Dominican Republic', 'tropical-island', 'Palm-lined beach and a colonial tower', ''),
    'DZ': ('Algeria', 'desert', 'Sahara dunes and a Tassili rock formation', ''),
    'EC': ('Ecuador', 'volcanic', 'Cotopaxi cone above Andean highlands', ''),
    'EE': ('Estonia', 'old-town', 'Tallinn medieval towers and rooftops', ''),
    'EG': ('Egypt', 'desert', 'Pyramids of Giza', ''),
    'ES': ('Spain', 'old-town', 'Sagrada Familia spires', ''),
    'ET': ('Ethiopia', 'alpine', 'Simien mountain cliffs with a gelada baboon', ''),
    'FI': ('Finland', 'boreal-forest', 'Lake, red cabin and northern lights', ''),
    'FJ': ('Fiji', 'tropical-island', 'Palm islet and an outrigger canoe', ''),
    'FO': ('Faroe Islands', 'fjord-coast', 'Grass-roof houses and a waterfall into the sea', ''),
    'FR': ('France', 'old-town', 'Eiffel Tower', ''),
    'GA': ('Gabon', 'rainforest', 'Rainforest meeting a beach, with a forest elephant', ''),
    'GB': ('United Kingdom', 'old-town', 'Big Ben (Elizabeth Tower) and the Thames', ''),
    'GD': ('Grenada', 'tropical-island', 'Spice-island bay with a sailboat', ''),
    'GE': ('Georgia', 'alpine', 'Caucasus peak above a hilltop stone church', ''),
    'GF': ('French Guiana', 'rainforest', 'Rocket on a launch pad above rainforest', ''),
    'GG': ('Guernsey', 'fjord-coast', 'Cliffs and a lighthouse', ''),
    'GH': ('Ghana', 'tropical-island', 'Palm beach with a fishing boat and Independence Arch', ''),
    'GI': ('Gibraltar', 'mediterranean', 'Rock of Gibraltar above the bay', ''),
    'GL': ('Greenland', 'arctic', 'Icebergs in a fjord with colourful houses', ''),
    'GM': ('Gambia', 'savanna', 'River with a pirogue and palms', ''),
    'GN': ('Guinea', 'rainforest', 'Highland waterfall in green hills', ''),
    'GP': ('Guadeloupe', 'tropical-island', 'Butterfly-shaped islands, palms and beach', ''),
    'GR': ('Greece', 'mediterranean', 'Santorini white houses and blue domes', ''),
    'GT': ('Guatemala', 'volcanic', 'Tikal temple above jungle, volcano behind', ''),
    'GU': ('Guam', 'tropical-island', 'Cliffs and a palm beach', ''),
    'GW': ('Guinea-Bissau', 'tropical-island', 'Bijagos islands, mangroves and a canoe', ''),
    'GY': ('Guyana', 'rainforest', 'Kaieteur Falls in rainforest', ''),
    'HK': ('Hong Kong', 'city-skyline', 'Victoria Harbour skyline with a junk boat', 'Neutral: no flags'),
    'HN': ('Honduras', 'tropical-island', 'Caribbean reef island and a Mayan stela', ''),
    'HR': ('Croatia', 'mediterranean', 'Dubrovnik walls and terracotta roofs', ''),
    'HT': ('Haiti', 'tropical-island', 'Mountain citadel above the coast', ''),
    'HU': ('Hungary', 'old-town', 'Parliament building on the Danube', ''),
    'ID': ('Indonesia', 'tropical-island', 'Balinese split gate and palms at sunset', 'Done in pilot'),
    'IE': ('Ireland', 'farmland', 'Green fields, stone walls and a round tower', ''),
    'IL': ('Israel', 'mediterranean', 'Mediterranean coast and desert hills', 'Neutral: no flags, no religious or contested symbols'),
    'IM': ('Isle of Man', 'fjord-coast', 'Laxey Wheel and a lighthouse', ''),
    'IN': ('India', 'old-town', 'Taj Mahal', ''),
    'IQ': ('Iraq', 'desert', 'Date palms by the river and Ziggurat of Ur', ''),
    'IS': ('Iceland', 'volcanic', 'Glacier, black beach and northern lights', ''),
    'IT': ('Italy', 'old-town', 'Colosseum', ''),
    'JE': ('Jersey', 'fjord-coast', 'Corbiere lighthouse on rocks', ''),
    'JM': ('Jamaica', 'tropical-island', 'Palm cove with a waterfall and sailboat', ''),
    'JO': ('Jordan', 'desert', 'Petra Treasury in the canyon', ''),
    'JP': ('Japan', 'volcanic', 'Mount Fuji, torii gate and cherry blossom', 'Done in pilot'),
    'KE': ('Kenya', 'savanna', 'Giraffes and acacia under Mount Kenya', 'Done in pilot'),
    'KG': ('Kyrgyzstan', 'steppe', 'Yurt by a mountain lake and horses', ''),
    'KH': ('Cambodia', 'rainforest', 'Angkor Wat towers at sunrise', ''),
    'KN': ('Saint Kitts and Nevis', 'tropical-island', 'Fortress above a palm coast', ''),
    'KR': ('South Korea', 'city-skyline', 'Seoul skyline with N Seoul Tower and a palace roof', ''),
    'KW': ('Kuwait', 'city-skyline', 'Kuwait Towers and dhows', ''),
    'KY': ('Cayman Islands', 'tropical-island', 'Seven Mile Beach with palms', ''),
    'KZ': ('Kazakhstan', 'steppe', 'Baiterek tower above the steppe', ''),
    'LA': ('Laos', 'rainforest', 'Kuang Si waterfall and a Luang Prabang temple roof', ''),
    'LC': ('Saint Lucia', 'tropical-island', 'The Pitons rising from the sea', ''),
    'LI': ('Liechtenstein', 'alpine', 'Vaduz Castle above the Rhine valley', ''),
    'LK': ('Sri Lanka', 'tropical-island', 'Sigiriya rock and stilt fishermen', ''),
    'LR': ('Liberia', 'tropical-island', 'Palm coast and surf', ''),
    'LS': ('Lesotho', 'alpine', 'Mountain kingdom with round thatched huts', ''),
    'LT': ('Lithuania', 'old-town', 'Trakai island castle on a lake', ''),
    'LU': ('Luxembourg', 'old-town', 'Adolphe Bridge and the old town', ''),
    'LV': ('Latvia', 'old-town', 'Riga old town spires', ''),
    'LY': ('Libya', 'desert', 'Leptis Magna Roman columns in the dunes', ''),
    'MA': ('Morocco', 'desert', 'Ait Benhaddou kasbah and palms', ''),
    'MC': ('Monaco', 'city-skyline', 'Harbour with yachts and tiered buildings', ''),
    'MD': ('Moldova', 'farmland', 'Vineyard rows at sunset', ''),
    'ME': ('Montenegro', 'mediterranean', 'Bay of Kotor between mountains', ''),
    'MF': ('Saint Martin', 'tropical-island', 'Palm beach and a small boat', ''),
    'MG': ('Madagascar', 'savanna', 'Avenue of baobabs at sunset', ''),
    'MK': ('North Macedonia', 'alpine', 'Lake Ohrid with a cliff-side church', ''),
    'ML': ('Mali', 'desert', 'Great Mosque of Djenne (mud-brick)', 'Religious building as landmark; confirm'),
    'MN': ('Mongolia', 'steppe', 'Gers and horses on endless grassland', ''),
    'MO': ('Macao', 'city-skyline', 'Ruins of St. Paul\'s facade and towers', 'Neutral: no flags'),
    'MQ': ('Martinique', 'tropical-island', 'Volcano above a palm bay', ''),
    'MR': ('Mauritania', 'desert', 'Dunes with a camel caravan', ''),
    'MS': ('Montserrat', 'volcanic', 'Soufriere Hills volcano above green coast', ''),
    'MT': ('Malta', 'mediterranean', 'Valletta bastions and honey-stone domes', ''),
    'MU': ('Mauritius', 'tropical-island', 'Le Morne mountain above a lagoon', ''),
    'MV': ('Maldives', 'tropical-island', 'Overwater villas over turquoise water', ''),
    'MW': ('Malawi', 'tropical-island', 'Lake Malawi with a dhow-style boat and baobab', ''),
    'MX': ('Mexico', 'rainforest', 'Chichen Itza pyramid in the jungle', ''),
    'MY': ('Malaysia', 'city-skyline', 'Petronas Towers', ''),
    'MZ': ('Mozambique', 'tropical-island', 'Dhow sailing off a palm coast', ''),
    'NC': ('New Caledonia', 'tropical-island', 'Lagoon and a traditional hut', ''),
    'NE': ('Niger', 'desert', 'Agadez mud-brick minaret and dunes', 'Religious building as landmark; confirm'),
    'NG': ('Nigeria', 'savanna', 'Zuma Rock monolith in the savanna', ''),
    'NI': ('Nicaragua', 'volcanic', 'Concepcion volcano on Ometepe in a lake', ''),
    'NL': ('Netherlands', 'farmland', 'Windmill and tulip fields', ''),
    'NO': ('Norway', 'fjord-coast', 'Fjord with red cabins and northern lights', ''),
    'NP': ('Nepal', 'alpine', 'Himalaya peaks and a stupa with prayer flags', ''),
    'NR': ('Nauru', 'tropical-island', 'Small island with a pinnacle-rock shore', ''),
    'NZ': ('New Zealand', 'fjord-coast', 'Milford Sound with Mitre Peak', ''),
    'OM': ('Oman', 'desert', 'Fort above Muscat bay with a dhow', ''),
    'PA': ('Panama', 'city-skyline', 'Skyline with a ship in the Panama Canal', ''),
    'PE': ('Peru', 'alpine', 'Machu Picchu terraces and a llama', ''),
    'PF': ('French Polynesia', 'tropical-island', 'Overwater bungalows below Mount Otemanu', ''),
    'PG': ('Papua New Guinea', 'rainforest', 'Bird-of-paradise in rainforest', ''),
    'PH': ('Philippines', 'tropical-island', 'Limestone karst lagoon and a banca boat', ''),
    'PK': ('Pakistan', 'alpine', 'Karakoram peaks above the Hunza valley', ''),
    'PL': ('Poland', 'old-town', 'Colourful old town square houses and a tower', ''),
    'PR': ('Puerto Rico', 'tropical-island', 'El Morro fort on the sea cliff', ''),
    'PT': ('Portugal', 'old-town', 'Belem Tower and a yellow Lisbon tram', ''),
    'PY': ('Paraguay', 'farmland', 'Rolling plains and a Jesuit mission ruin', ''),
    'QA': ('Qatar', 'city-skyline', 'Doha skyline with a dhow', ''),
    'RE': ('Reunion', 'volcanic', 'Piton de la Fournaise crater above the coast', ''),
    'RO': ('Romania', 'alpine', 'Carpathian castle (Peles) above pine forest', ''),
    'RS': ('Serbia', 'old-town', 'Belgrade fortress at the river confluence', ''),
    'RU': ('Russia', 'old-town', 'Colourful onion domes of St. Basil\'s Cathedral', ''),
    'RW': ('Rwanda', 'rainforest', 'Virunga volcanoes and a mountain gorilla', ''),
    'SA': ('Saudi Arabia', 'desert', 'Riyadh Kingdom Centre and desert dunes', ''),
    'SC': ('Seychelles', 'tropical-island', 'Granite boulders and palms on a beach', ''),
    'SD': ('Sudan', 'desert', 'Pyramids of Meroe in the desert', ''),
    'SE': ('Sweden', 'boreal-forest', 'Lake with a red cottage and pines', ''),
    'SG': ('Singapore', 'city-skyline', 'Marina Bay Sands and Supertrees', ''),
    'SI': ('Slovenia', 'alpine', 'Lake Bled with its island church', ''),
    'SK': ('Slovakia', 'alpine', 'Spis Castle and the High Tatras', ''),
    'SL': ('Sierra Leone', 'tropical-island', 'Palm beach and mountain backdrop', ''),
    'SM': ('San Marino', 'alpine', 'Three Towers on Mount Titano', ''),
    'SN': ('Senegal', 'savanna', 'Baobab and the pink lake', ''),
    'SR': ('Suriname', 'rainforest', 'Paramaribo wooden colonial buildings and rainforest', ''),
    'SS': ('South Sudan', 'savanna', 'Nile wetlands with a shoebill', ''),
    'SV': ('El Salvador', 'volcanic', 'Santa Ana volcano above a crater lake', ''),
    'SZ': ('Eswatini', 'savanna', 'Hills with traditional beehive huts', ''),
    'TC': ('Turks and Caicos Islands', 'tropical-island', 'Grace Bay beach and a sailboat', ''),
    'TD': ('Chad', 'desert', 'Ennedi rock arch in the desert', ''),
    'TG': ('Togo', 'tropical-island', 'Palm-fringed Gulf of Guinea coast', ''),
    'TH': ('Thailand', 'tropical-island', 'Wat Arun above a longtail boat', ''),
    'TJ': ('Tajikistan', 'alpine', 'Pamir peaks and a turquoise lake', ''),
    'TN': ('Tunisia', 'mediterranean', 'Sidi Bou Said blue-and-white town', ''),
    'TO': ('Tonga', 'tropical-island', 'Palm islet and a humpback whale', ''),
    'TR': ('Turkey', 'old-town', 'Cappadocia fairy chimneys and hot-air balloons', 'Chosen as neutral; Istanbul mosques avoided'),
    'TT': ('Trinidad and Tobago', 'tropical-island', 'Scarlet ibis over mangroves', ''),
    'TW': ('Taiwan', 'city-skyline', 'Taipei 101 over mountains', 'Neutral: no flags'),
    'TZ': ('Tanzania', 'savanna', 'Kilimanjaro behind an acacia tree', ''),
    'UA': ('Ukraine', 'farmland', 'Sunflower field and a windmill', 'Neutral: no flags or military imagery'),
    'UG': ('Uganda', 'rainforest', 'Source of the Nile falls and a gorilla', ''),
    'US': ('United States', 'city-skyline', 'Statue of Liberty and the Manhattan skyline', ''),
    'UY': ('Uruguay', 'tropical-island', 'Punta del Este hand sculpture on the beach', ''),
    'UZ': ('Uzbekistan', 'old-town', 'Registan tiled domes at dusk', 'Religious-style architecture; confirm'),
    'VA': ('Vatican City', 'old-town', 'St. Peter\'s dome above a plaza', 'Religious building is the landmark; confirm'),
    'VC': ('Saint Vincent and the Grenadines', 'tropical-island', 'Sailboats among small cays', ''),
    'VE': ('Venezuela', 'rainforest', 'Angel Falls from a tepui', ''),
    'VG': ('British Virgin Islands', 'tropical-island', 'The Baths granite boulders', ''),
    'VN': ('Vietnam', 'fjord-coast', 'Ha Long Bay limestone karst with a junk boat', ''),
    'VU': ('Vanuatu', 'volcanic', 'Mount Yasur glowing above the shore', ''),
    'WS': ('Samoa', 'tropical-island', 'Open fale hut on a palm beach', ''),
    'XK': ('Kosovo', 'alpine', 'Mountain valley landscape', 'Neutral landscape only: no flags or symbols'),
    'YE': ('Yemen', 'desert', 'Shibam mud-brick towers', 'Neutral architecture only'),
    'YT': ('Mayotte', 'tropical-island', 'Lagoon with an islet and reef', ''),
    'ZA': ('South Africa', 'alpine', 'Table Mountain over Cape Town bay', ''),
    'ZM': ('Zambia', 'savanna', 'Victoria Falls with a rainbow', ''),
    'ZW': ('Zimbabwe', 'savanna', 'Balancing rocks and baobab', ''),
}

# code: (name, scene type, landmarks / motifs, note)
R = {
    'EU': ('Europe', 'old-town', 'Eiffel Tower, Colosseum, Big Ben skyline', 'Plain "Europe" group (plans range 32-40 areas)'),
    'EU-42': ('Europe (42 areas)', 'old-town', 'Eiffel Tower, Brandenburg Gate, windmill', ''),
    'EU-43': ('Europe + Morocco (43 areas)', 'old-town', 'Eiffel Tower, Colosseum and a Moroccan kasbah', ''),
    'EU-30': ('Europe + Turkey (30 areas)', 'old-town', 'Big Ben, Cappadocia balloons, Colosseum', ''),
    'EU-31': ('Europe (31 areas)', 'old-town', 'Sagrada Familia, Prague spires, windmill', ''),
    'EU-33': ('Europe (33 areas)', 'old-town', 'Eiffel Tower, Santorini domes, Big Ben', ''),
    'EU-35': ('Europe (35 areas)', 'old-town', 'Colosseum, Brandenburg Gate, Tallinn towers', 'Includes Ukraine, Moldova, San Marino, Vatican'),
    'EU-7': ('Balkans (7 areas)', 'mediterranean', 'Dubrovnik walls, Mostar bridge, Bay of Kotor', ''),
    'AF-21': ('Africa (21 areas)', 'savanna', 'Pyramids, acacia tree, palms (as in the Africa pilot)', 'Done in pilot'),
    'AF-29': ('Africa (29 areas)', 'savanna', 'Baobab avenue, Kilimanjaro, acacia', ''),
    'AS-12': ('Asia (12 areas)', 'city-skyline', 'Skylines of Hong Kong and Singapore with a pagoda', ''),
    'AS-14': ('Asia (14 areas)', 'old-town', 'Taj Mahal, Wat Arun, Fuji', ''),
    'AS-21': ('Asia (21 areas)', 'old-town', 'Taj Mahal, Fuji, Angkor Wat, Petronas Towers', ''),
    'AS-20': ('Asia-Pacific (20 areas)', 'city-skyline', 'Opera House, Marina Bay Sands, Fuji', 'Includes Australia, New Zealand, Israel, Kuwait, Saudi Arabia'),
    'AS-7': ('Southeast Asia (7 areas)', 'rainforest', 'Angkor Wat, longtail boat, palms', ''),
    'SEA-8': ('Southeast Asia (8 areas)', 'rainforest', 'Wat Arun, Angkor Wat, Ha Long karst', ''),
    'SGMYVNTHID-5': ('Southeast Asia (5 areas)', 'tropical-island', 'Marina Bay Sands, Petronas Towers, Bali gate', ''),
    'SGMYTH-3': ('Singapore, Malaysia & Thailand', 'city-skyline', 'Marina Bay Sands, Petronas Towers, Wat Arun', ''),
    'SGMY-2': ('Singapore & Malaysia', 'city-skyline', 'Marina Bay Sands and Petronas Towers', ''),
    'CA-4': ('Central Asia (4 areas)', 'steppe', 'Registan domes, yurt, Baiterek tower', ''),
    'AS-5': ('Central & South Asia (5 areas)', 'steppe', 'Registan domes, Karakoram peaks, Sigiriya rock', ''),
    'SAS-6': ('South Asia (6 areas)', 'alpine', 'Himalaya, Taj Mahal, stupa with prayer flags', ''),
    'CN-3': ('Greater China (3 areas)', 'city-skyline', 'Hong Kong skyline, Great Wall, Macao ruins', 'Neutral: no flags'),
    'CNHK-2': ('China & Hong Kong', 'city-skyline', 'Great Wall and Victoria Harbour', 'Neutral: no flags'),
    'CNJPKR-3': ('China, Japan & Korea', 'alpine', 'Great Wall, Mount Fuji, Seoul tower', ''),
    'JPKR-2': ('Japan & Korea', 'volcanic', 'Mount Fuji, torii gate, N Seoul Tower', ''),
    'AUNZ-2': ('Australia & New Zealand', 'fjord-coast', 'Opera House and Milford Sound', ''),
    'AUKUS-3': ('Australia, UK & USA', 'city-skyline', 'Opera House, Big Ben, Statue of Liberty', ''),
    'OCE-8': ('Oceania (8 areas)', 'tropical-island', 'Opera House, overwater bungalows, outrigger canoe', ''),
    'CB-25': ('Caribbean & South America (25 areas)', 'tropical-island', 'Christ the Redeemer, palm beach, Machu Picchu', ''),
    'SA-18': ('Latin America (18 areas)', 'alpine', 'Christ the Redeemer, Machu Picchu, palms', ''),
    'SA-6': ('South America (6 areas)', 'alpine', 'Fitz Roy peaks, Christ the Redeemer, Machu Picchu', ''),
    'NA-3': ('North America (3 areas)', 'city-skyline', 'Statue of Liberty, Rockies with maple, Chichen Itza', ''),
    'USCA-2': ('USA & Canada', 'city-skyline', 'Statue of Liberty and a Rocky Mountain lake with a maple', ''),
    'BI-2': ('UK & Ireland', 'farmland', 'Big Ben and a round tower with green fields', ''),
    'IESI-2': ('Ireland & Slovenia', 'farmland', 'Round tower and Lake Bled church', 'Unusual pairing; confirm the name'),
    'SAAEQAKWOMBH-6': ('Gulf states (6 areas)', 'city-skyline', 'Burj Khalifa, Kuwait Towers, Doha dhow', ''),
    'ME-6': ('Gulf & Iraq (6 areas)', 'desert', 'Burj Khalifa, Doha skyline, date palms', ''),
    'ME-5': ('Middle East (5 areas)', 'desert', 'Doha skyline, Kuwait Towers, desert dunes', 'Includes Israel; neutral desert/skyline only'),
    'ME-12': ('Middle East & North Africa (12 areas)', 'desert', 'Pyramids, Petra, Burj Khalifa', ''),
    'ME-13': ('Middle East (13 areas)', 'desert', 'Petra, Burj Khalifa, Cappadocia balloons', ''),
    'GL-120': ('Global (120 areas)', 'old-town', 'Horizon with a plane and small Eiffel, pyramid, Fuji, Statue icons', ''),
    'GL-139': ('Global (139 areas)', 'old-town', 'Horizon with a plane and small Taj Mahal, Opera House, Christ icons', ''),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plans', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    ws = openpyxl.load_workbook(a.plans, read_only=True, data_only=True).worksheets[0]
    plans = collections.Counter()
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[11] is not None:
            plans[r[11]] += 1
    known = set(C) | set(R)
    assert set(plans) == known, (sorted(set(plans) - known), sorted(known - set(plans)))
    assert all(t in TYPES for _, t, _, _ in list(C.values()) + list(R.values()))

    wb = openpyxl.Workbook()
    sh = wb.active
    sh.title = 'Scenes'
    head = ['Code', 'Kind', 'Name', 'Scene type', 'Landmark / motif', 'Notes', 'Plans in file', 'OK? (type yes / change)']
    sh.append(head)
    rows = [(c, 'Country') + v for c, v in sorted(C.items(), key=lambda kv: kv[1][0])]
    rows += [(c, 'Region') + v for c, v in sorted(R.items(), key=lambda kv: kv[1][0])]
    for code, kind, name, typ, mark, note in rows:
        sh.append([code, kind, name, typ, mark, note, plans[code], ''])

    bold = Font(bold=True, color='FFFFFF')
    for c in sh[1]:
        c.font = bold
        c.fill = PatternFill('solid', fgColor='6415FE')
        c.alignment = Alignment(vertical='center', wrap_text=True)
    for i, w in enumerate([12, 10, 36, 18, 62, 46, 12, 22], 1):
        sh.column_dimensions[get_column_letter(i)].width = w
    for row in sh.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical='top', wrap_text=True)
        if row[1].value == 'Region':
            for c in row:
                c.fill = PatternFill('solid', fgColor='F1EAFF')
    sh.freeze_panes = 'D2'
    sh.auto_filter.ref = f'A1:H{sh.max_row}'
    dv = DataValidation(type='list', formula1='"' + ','.join(TYPES) + '"', allow_blank=False)
    sh.add_data_validation(dv)
    dv.add(f'D2:D{sh.max_row}')

    ty = wb.create_sheet('Scene types')
    ty.append(['Scene type', 'What the base scene shows', 'Destinations using it'])
    use = collections.Counter(t for _, t, _, _ in list(C.values()) + list(R.values()))
    for t, d in TYPES.items():
        ty.append([t, d, use[t]])
    for c in ty[1]:
        c.font = bold
        c.fill = PatternFill('solid', fgColor='6415FE')
    for i, w in enumerate([20, 70, 22], 1):
        ty.column_dimensions[get_column_letter(i)].width = w

    wb.save(a.out)
    print(f'{len(C)} countries + {len(R)} regions = {len(rows)} rows -> {a.out}')
    for t, n in sorted(use.items(), key=lambda kv: -kv[1]):
        print(f'  {t:16s}{n}')


if __name__ == '__main__':
    main()
