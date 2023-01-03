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
