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
        "sub_units": []
    },
    {
        "name": "Kilogram",
        "short_name": "Kg",
        "description": "Weight in kilograms",
        "sub_units": [
            {"name": "g", "factor": 0.001},
            {"name": "mg", "factor": 0.000001}
        ]
    },
    {
        "name": "Gram",
        "short_name": "g",
        "description": "Weight in grams",
        "sub_units": []
    },
    {
        "name": "Liter",
        "short_name": "L",
        "description": "Volume in liters",
        "sub_units": [
            {"name": "mL", "factor": 0.001}
        ]
    },
    {
        "name": "Milliliter",
        "short_name": "mL",
        "description": "Volume in milliliters",
        "sub_units": []
    },
    {
        "name": "Meter",
        "short_name": "m",
        "description": "Length in meters",
        "sub_units": [
            {"name": "cm", "factor": 0.01},
            {"name": "mm", "factor": 0.001}
        ]
    },
    {
        "name": "Centimeter",
        "short_name": "cm",
        "description": "Length in centimeters",
        "sub_units": []
    },
    {
        "name": "Box",
        "short_name": "Box",
        "description": "Box package",
        "sub_units": []
    },
    {
        "name": "Packet",
        "short_name": "Pkt",
        "description": "Packet",
        "sub_units": []
    },
    {
        "name": "Bottle",
        "short_name": "Btl",
        "description": "Bottle",
        "sub_units": []
    },
    {
        "name": "Can",
        "short_name": "Can",
        "description": "Can",
        "sub_units": []
    },
    {
        "name": "Bag",
        "short_name": "Bag",
        "description": "Bag",
        "sub_units": []
    },
    {
        "name": "Dozen",
        "short_name": "Doz",
        "description": "12 pieces",
        "sub_units": []
    },
    {
        "name": "Pack",
        "short_name": "Pack",
        "description": "Pack",
        "sub_units": []
    },
    {
        "name": "Set",
        "short_name": "Set",
        "description": "Set of items",
        "sub_units": []
    },
]



ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

