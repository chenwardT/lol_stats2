VALID_LANE_ROLE_COMBOS = [
    {'lane': 'TOP',    'role': 'DUO'},
    {'lane': 'TOP',    'role': 'DUO_CARRY'},
    {'lane': 'TOP',    'role': 'DUO_SUPPORT'},
    {'lane': 'TOP',    'role': 'NONE'},
    {'lane': 'TOP',    'role': 'SOLO',          'alias': 'Top'},

    {'lane': 'JUNGLE', 'role': 'NONE',          'alias': 'Jungle'},

    {'lane': 'MIDDLE', 'role': 'DUO'},
    {'lane': 'MIDDLE', 'role': 'DUO_CARRY'},
    {'lane': 'MIDDLE', 'role': 'DUO_SUPPORT'},
    {'lane': 'MIDDLE', 'role': 'NONE'},
    {'lane': 'MIDDLE', 'role': 'SOLO',          'alias': 'Middle'},

    {'lane': 'BOTTOM', 'role': 'DUO'},
    {'lane': 'BOTTOM', 'role': 'DUO_CARRY',     'alias': 'ADC'},
    {'lane': 'BOTTOM', 'role': 'DUO_SUPPORT',   'alias': 'Support'},
    {'lane': 'BOTTOM', 'role': 'NONE'},
    {'lane': 'BOTTOM', 'role': 'SOLO'},
]

REGIONS = [
    'BR',   # Brazil
    'EUNE', # Europe Northeast
    'EUW',  # Europe West
    'KR',   # Korea
    'LAN',  # Latin America North
    'LAS',  # Latin America South
    'NA',   # North America
    'OCE',  # Oceania
    'RU',   # Russia
    'TR',   # Turkey
]

TIER_ENUM = {
    'UNRANKED':     0,
    'BRONZE':       1,
    'SILVER':       2,
    'GOLD':         3,
    'PLATINUM':     4,
    'DIAMOND':      5,
    'MASTER':       6,
    'CHALLENGER':   7,
}

TIER_ORDER = [
    'BRONZE',
    'SILVER',
    'GOLD',
    'PLATINUM',
    'DIAMOND',
    'MASTER',
    'CHALLENGER'
]