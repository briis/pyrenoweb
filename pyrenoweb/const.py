BASE_URL = "https://servicesgh.renoweb.dk/v1_13"
DAWA_URL = "https://dawa.aws.dk/kommuner"

DEFAULT_TIMEOUT = 10
NO_WASTE_SCHEDULE_TIMESTAMP = 1767135600

TYPE_RESIDUAL = ["Restaffald-Madaffald", "Dagrenovation"]
TYPE_GLASS = ["Glas", "Glas Papir"]
TYPE_METAL_GLASS = ["Metal-Glas"]
TYPE_METAL = ["Jern"]
TYPE_PAPER = ["Papir", "Pap"]
TYPE_PLASTIC = ["Plast"]
TYPE_PLASTIC_METAL = ["Plast Metal"]
TYPE_STORSKRALD = ["Storskrald"]
TYPE_HAVEAFFALD = ["Haveaffald"]

WASTE_LIST = [
    {"type": "Restaffald-Madaffald", "icon": "mdi:trash-can"},
    {"type": "Metal-Glas", "icon": "mdi:glass-fragile"},
    {"type": "PAPPI", "icon": "mdi:recycle"},
    {"type": "Farligt affald", "icon": "mdi:biohazard"},
    {"type": "Tekstiler", "icon": "mdi:hanger"},
]

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
