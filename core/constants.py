ENV_PREFIX="UTILS_"
SERVICE_NAME='utils'


DEFAULT_UI_IDS = [
    {
        "entity_type": "PRODUCT",
        "prefix": "PRD",
    },
    {
        "entity_type": "STOCKMOVEMENT",
        "prefix": "STM",
    },
    {
        "entity_type": "PURCHASE",
        "prefix": "PUR",
    },
    {
        "entity_type": "SUPPLIER",
        "prefix": "SUP",
    },
    {
        "entity_type": "CUSTOMER",
        "prefix": "CUS",
    },
    {
        "entity_type": "EMPLOYEE",
        "prefix": "EMP",
    },
    {
        "entity_type": "SHOP",
        "prefix": "SHP",
    },
    {
        "entity_type": "ORDER",
        "prefix": "ORD",
    },
]


DEFAULT_CATEGORIES = [
    {"name": "GENERAL", "description": "General products"},
    {"name": "FOOD", "description": "Food items"},
    {"name": "BEVERAGES", "description": "Drinks and beverages"},
    {"name": "SNACKS", "description": "Snacks and chips"},
    {"name": "FRUITS", "description": "Fresh fruits"},
    {"name": "VEGETABLES", "description": "Fresh vegetables"},
    {"name": "DAIRY", "description": "Milk and dairy products"},
    {"name": "BAKERY", "description": "Bread and bakery items"},
    {"name": "MEAT", "description": "Chicken, mutton and meat"},
    {"name": "SEAFOOD", "description": "Fish and seafood"},
    {"name": "FROZEN", "description": "Frozen foods"},
    {"name": "GROCERY", "description": "Daily grocery items"},
    {"name": "HOUSEHOLD", "description": "Household essentials"},
    {"name": "PERSONAL CARE", "description": "Personal care products"},
    {"name": "HEALTH", "description": "Medicines and health products"},
    {"name": "STATIONERY", "description": "Office and school supplies"},
    {"name": "ELECTRONICS", "description": "Electronic items"},
    {"name": "CLOTHING", "description": "Garments and apparel"},
    {"name": "HOME APPLIANCES", "description": "Home appliances"},
    {"name": "OTHERS", "description": "Miscellaneous products"},
]


DEFAULT_UNITS = [
    {
        "name": "Piece",
        "short_name": "Pc",
        "description": "Individual item",
    },
    {
        "name": "Kilogram",
        "short_name": "Kg",
        "description": "Weight in kilograms",
    },
    {
        "name": "Gram",
        "short_name": "g",
        "description": "Weight in grams",
    },
    {
        "name": "Liter",
        "short_name": "L",
        "description": "Volume in liters",
    },
    {
        "name": "Milliliter",
        "short_name": "mL",
        "description": "Volume in milliliters",
    },
    {
        "name": "Meter",
        "short_name": "m",
        "description": "Length in meters",
    },
    {
        "name": "Centimeter",
        "short_name": "cm",
        "description": "Length in centimeters",
    },
    {
        "name": "Box",
        "short_name": "Box",
        "description": "Box package",
    },
    {
        "name": "Packet",
        "short_name": "Pkt",
        "description": "Packet",
    },
    {
        "name": "Bottle",
        "short_name": "Btl",
        "description": "Bottle",
    },
    {
        "name": "Can",
        "short_name": "Can",
        "description": "Can",
    },
    {
        "name": "Bag",
        "short_name": "Bag",
        "description": "Bag",
    },
    {
        "name": "Dozen",
        "short_name": "Doz",
        "description": "12 pieces",
    },
    {
        "name": "Pack",
        "short_name": "Pack",
        "description": "Pack",
    },
    {
        "name": "Set",
        "short_name": "Set",
        "description": "Set of items",
    },
]



ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

