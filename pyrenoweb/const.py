API_URL_DATA = ".renoweb.dk/Legacy/JService.asmx/GetAffaldsplanMateriel_mitAffald"
API_URL_SEARCH = ".renoweb.dk/Legacy/JService.asmx/Adresse_SearchByString"

NON_SUPPORTED_ITEMS = [
    "Asbest",
    "Beholderservice",
    "Bestillerordning",
]

SUPPORTED_ITEMS = {
    "restaffaldmadaffald": ["Restaffald-Madaffald", "Rest/mad", "Restaffald", "Rest - Mad", "Rest-/Madaffald", "Mad- og restaffald", "Mad/rest"],
    "dagrenovation": ["Dagrenovation"],
    "glas": ["Industri Genbrugeligt"],
    "metalglas": ["Glas og metal", "Metal-Glas", "Glas/Metal"],
    "pappi": ["Plast MDK og papir", "PAPPI", "Plast/MD-karton/PP"],
    "farligtaffald": ["Farligt affald", "Miljøkasser"],
    "farligtaffaldmiljoboks": ["Farligt affald/Miljøboks"],
    "flis": ["Flis"],
    "genbrug": ["Tekstiler", "Genbrug"],
    "jern": ["Jern"],
    "papir": ["Papir", "Papir 660 L"],
    "papirmetal": ["Papir & Metal", "Papir/metal"],
    "pap": ["Pap"],
    "plastmetal": ["Plast & Metal", "Plast, metal & MDK 660L", "Plast/MDK"],
    "storskrald": ["Storskrald"],
    "storskraldogtekstilaffald": ["Storskrald og tekstilaffald"],
    "haveaffald": ["Haveaffald, flishugning", "Haveaffald"],
}

ICON_LIST = {
    "restaffaldmadaffald": "mdi:trash-can",
    "dagrenovation": "mdi:trash-can",
    "glas": "liquor",
    "metalglas": "mdi:glass-fragile",
    "pappi": "mdi:recycle",
    "farligtaffald": "mdi:biohazard",
    "farligtaffaldmiljoboks":"mdi:biohazard",
    "flis": "mdi:tree",
    "genbrug": "mdi:recycle",
    "jern": "mdi:bucket",
    "papir": "mdi:file",
    "papirmetal": "mdi:delete-empty",
    "pap": "mdi:note",
    "plastmetal": "mdi:trash-can-outline",
    "storskrald": "mdi:table-furniture",
    "storskraldogtekstilaffald": "mdi:table-furniture",
    "haveaffald": "mdi:leaf",
}

NAME_LIST = {
    "restaffaldmadaffald": "Rest & Madaffald",
    "dagrenovation": "Dagrenovation",
    "glas": "Glas",
    "metalglas": "Metal & Glas",
    "pappi": "Papir & Plast",
    "farligtaffald": "Farligt affald",
    "farligtaffaldmiljoboks":"Farligt affald & Miljøboks",
    "flis": "Flis",
    "genbrug": "Genbrug",
    "jern": "Jern",
    "papir": "Papir",
    "papirmetal": "Papir & Metal",
    "pap": "Pap",
    "plastmetal": "Plast & Metal",
    "storskrald": "Storskrald",
    "storskraldogtekstilaffald": "Storskrald & Tekstilaffald",
    "haveaffald": "Haveaffald",
}


MUNICIPALITIES_LIST = {
    "aabenraa": "aabenraa",
    "aalborg": "aalborg",
    "albertslund": "albertslund",
    "allerød": "alleroed",
    "assens": "assens",
    "ballerup": "ballerup",
    "billund": "billund",
    "bornholm": "bornholm",
    "brøndby": "brondby",
    "brønderslev": "bronderslev",
    "dragør": "dragoer",
    "egedal": "egedal",
    "esbjerg": "esbjerg",
    "fanø": "fanoe",
    "favrskov": "favrskov",
    "faxe": "faxe",
    "fredensborg": "fredensborg",
    "fredericia": "fredericia",
    "frederiksberg": "frederiksberg",
    "frederikshavn": "frederikshavn",
    "frederikssund": "frederikssund",
    "furesø": "furesoe",
    "gentofte": "gentofte",
    "gladsaxe": "gladsaxe",
    "glostrup": "glostrup",
    "greve": "greve",
    "gribskov": "gribskov",
    "guldborgsund": "guldborgsund",
    "haderslev": "haderslev",
    "halsnæs": "halsnaes",
    "hedensted": "hedensted",
    "helsingør": "helsingor",
    "herlev": "herlev",
    "herning": "herning",
    "hillerød": "hillerod",
    "hjørring": "hjoerring",
    "holbæk": "holbæk",
    "holstebro": "holstebro",
    "horsens": "horsens",
    "hvidovre": "hvidovre",
    "høje-taastrup": "htk",
    "hørsholm": "horsholm",
    "ikast-brande": "ikast-brande",
    "ishøj": "ishoj",
    "jammerbugt": "jammerbugt",
    "kalundborg": "kalundborg",
    "kerteminde": "kerteminde",
    "kolding": "kolding",
    "køge": "koege",
    "læsø": "laesoe",
    "lolland": "lolland",
    "lyngby-taarbæk": "ltf",
    "lyngby": "ltf",
    "taarbæk": "ltf",
    "mariagerfjord": "mariagerfjord",
    "middelfart": "middelfart",
    "morsø": "morsø",
    "norddjurs": "norddjurs",
    "nordfyns": "nordfyns",
    "nyborg": "nyborg",
    "næstved": "naestved",
    "odder": "odder",
    "odense": "odense",
    "odsherred": "odsherred",
    "randers": "randers",
    "rebild": "rebild",
    "ringkøbing-skjern": "rksk",
    "ringkøbing": "rksk",
    "skjern": "rksk",
    "ringsted": "ringsted",
    "roskilde": "roskilde",
    "rødovre": "rk",
    "samsø": "samsoe",
    "silkeborg": "silkeborg",
    "skanderborg": "skanderborg",
    "skive": "skive",
    "slagelse": "slagelse",
    "solrød": "solrod",
    "sorø": "soroe",
    "stevns": "stevns",
    "struer": "struer",
    "svendborg": "svendborg",
    "syddjurs": "syddjurs",
    "tårnby": "taarnby",
    "thisted": "thisted",
    "tønder": "toender",
    "vallensbæk": "vallensbaek",
    "varde": "varde",
    "vejen": "vejen",
    "vejle": "vejle",
    "vesthimmerland": "vesthimmerland",
    "viborg": "viborg",
    "vordingborg": "vordingborg"
}

MUNICIPALITIES_ARRAY = list(MUNICIPALITIES_LIST.keys())
