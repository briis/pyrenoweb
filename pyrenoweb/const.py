API_URL_DATA = ".renoweb.dk/Legacy/JService.asmx/GetAffaldsplanMateriel_mitAffald"
API_URL_SEARCH = ".renoweb.dk/Legacy/JService.asmx/Adresse_SearchByString"

BASE_URL = "https://servicesgh.renoweb.dk/v1_13"
DAWA_URL = "https://dawa.aws.dk/kommuner"

DEFAULT_TIMEOUT = 10

TYPE_RESIDUAL = ["Restaffald-Madaffald", "Dagrenovation"]
TYPE_GLASS = ["Glas", "Glas Papir"]
TYPE_METAL_GLASS = ["Metal-Glas"]
TYPE_METAL = ["Jern"]
TYPE_PAPER = ["Papir", "Pap"]
TYPE_PLASTIC = ["Plast"]
TYPE_PLASTIC_METAL = ["Plast Metal"]
TYPE_STORSKRALD = ["Storskrald"]
TYPE_HAVEAFFALD = ["Haveaffald"]

ICON_LIST = {
    "Restaffald-Madaffald": "mdi:trash-can",
    "Dagrenovation": "mdi:trash-can",
    "Metal-Glas": "mdi:glass-fragile",
    "PAPPI": "mdi:recycle",
    "Farligt affald": "mdi:biohazard",
    "Tekstiler": "mdi:hanger",
    "Jern": "mdi:bucket",
    "Papir": "mdi:file",
    "Pap": "mdi:note",
    "Plast Metal": "mdi:trash-can-outline",
    "Storskrald": "mdi:table-furniture",
    "Haveaffald": "mdi:leaf",
}

NAME_LIST = {
    "Restaffald-Madaffald": "Rest og madaffald",
    "Dagrenovation": "Dagrenovation",
    "Metal-Glas": "Meta og glas",
    "PAPPI": "Papir og plast",
    "Farligt affald": "Farligt affald",
    "Tekstiler": "Tekstiler",
    "Jern": "Jern",
    "Papir": "Papir",
    "Pap": "Pap",
    "Plast Metal": "Plast og metal",
    "Storskrald": "Storskrald",
    "Haveaffald": "Haveaffald",
}
MUNICIPALITIES_LIST = {
    "aabenraa": "aabenraa",
    "aalborg": "aalborg",
    "aarhus": "aarhus",
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
    "københavn": "kk",
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

class color:
    """Defines colors used for Terminal Output."""

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
