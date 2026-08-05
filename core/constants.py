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


SHOP_CATEGORIES_MAPPING = {
    "Decor / Handicrafts": [
        {"name": "Wall Decor", "description": "Wall decor and art"},
        {"name": "Showpieces", "description": "Showpieces and artifacts"},
        {"name": "Candles", "description": "Candles and home fragrance"},
        {"name": "Pottery", "description": "Pottery and ceramic items"},
        {"name": "Furnishings", "description": "Home furnishings"},
        {"name": "Lighting", "description": "Lamps and decorative lighting"},
        {"name": "Festive", "description": "Festive decorations"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Groceries / Kirana": [
        {"name": "Grains", "description": "Rice, wheat, and grains"},
        {"name": "Pulses", "description": "Dals and pulses"},
        {"name": "Spices", "description": "Spices and masalas"},
        {"name": "Oils", "description": "Cooking oils and ghee"},
        {"name": "Snacks", "description": "Packaged snacks and munchies"},
        {"name": "Beverages", "description": "Tea, coffee, and drinks"},
        {"name": "Household", "description": "Cleaning and household supplies"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Pharmacies": [
        {"name": "Medicines", "description": "Prescription and OTC medicines"},
        {"name": "Supplements", "description": "Vitamins and health supplements"},
        {"name": "Baby Care", "description": "Baby food and care products"},
        {"name": "Personal Care", "description": "Personal hygiene and care"},
        {"name": "Ayurvedic", "description": "Ayurvedic and herbal medicines"},
        {"name": "Devices", "description": "Medical devices and monitors"},
        {"name": "Surgical", "description": "Surgical supplies and dressings"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Bakeries": [
        {"name": "Breads", "description": "Fresh breads and buns"},
        {"name": "Cakes", "description": "Cakes and pastries"},
        {"name": "Pastries", "description": "Pastries and tarts"},
        {"name": "Cookies", "description": "Biscuits and cookies"},
        {"name": "Sweets", "description": "Bakery sweets and confectioneries"},
        {"name": "Ingredients", "description": "Baking ingredients and supplies"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Electronics / Mobile": [
        {"name": "Mobiles", "description": "Smartphones and mobile phones"},
        {"name": "Accessories", "description": "Mobile and tech accessories"},
        {"name": "Wearables", "description": "Smartwatches and fitness bands"},
        {"name": "Computers", "description": "Laptops, desktops, and peripherals"},
        {"name": "Appliances", "description": "Electronic appliances"},
        {"name": "Spares", "description": "Electronic spare parts"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Food Stores": [
        {"name": "Ghee", "description": "Pure ghee and butter"},
        {"name": "Pickles", "description": "Traditional pickles and chutneys"},
        {"name": "Spices", "description": "Specialty spices and seasonings"},
        {"name": "Dry Fruits", "description": "Nuts and dry fruits"},
        {"name": "Snacks", "description": "Traditional snacks and savories"},
        {"name": "Sweets", "description": "Traditional sweets and mithai"},
        {"name": "Drinks", "description": "Specialty drinks and syrups"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Homemade Organic": [
        {"name": "Organic Foods", "description": "Certified organic food items"},
        {"name": "Millets", "description": "Millets and ancient grains"},
        {"name": "Herbal", "description": "Herbal teas and formulations"},
        {"name": "Skincare", "description": "Organic skincare products"},
        {"name": "Soaps", "description": "Handmade and organic soaps"},
        {"name": "Oils", "description": "Cold pressed and organic oils"},
        {"name": "Honey", "description": "Natural and raw honey"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Stationery": [
        {"name": "Notebooks", "description": "Notebooks, diaries, and pads"},
        {"name": "Writing", "description": "Pens, pencils, and markers"},
        {"name": "Art Supplies", "description": "Paints, brushes, and craft materials"},
        {"name": "Office Supplies", "description": "Staplers, clips, and office items"},
        {"name": "School Supplies", "description": "School stationery items"},
        {"name": "Files", "description": "Files, folders, and binders"},
        {"name": "Printing", "description": "Paper and printing supplies"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Fashion / Lifestyle": [
        {"name": "Womenswear", "description": "Women's clothing and apparel"},
        {"name": "Menswear", "description": "Men's clothing and apparel"},
        {"name": "Kidswear", "description": "Kids and children's clothing"},
        {"name": "Accessories", "description": "Fashion accessories and belts"},
        {"name": "Jewellery", "description": "Fashion and fine jewellery"},
        {"name": "Footwear", "description": "Fashion footwear"},
        {"name": "Watches", "description": "Wristwatches and smartwatches"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Boutiques / Textiles": [
        {"name": "Sarees", "description": "Traditional and designer sarees"},
        {"name": "Kurtis", "description": "Kurtis and tunics"},
        {"name": "Lehengas", "description": "Lehengas and ethnic wear"},
        {"name": "Blouses", "description": "Readymade blouses and tops"},
        {"name": "Dupattas", "description": "Dupattas and stoles"},
        {"name": "Fabrics", "description": "Unstitched dress materials and fabrics"},
        {"name": "Tailoring", "description": "Tailoring materials and services"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Home Appliances": [
        {"name": "Kitchen Appliances", "description": "Mixers, grinders, and kitchen tools"},
        {"name": "Laundry", "description": "Washing machines and irons"},
        {"name": "Purifiers", "description": "Water and air purifiers"},
        {"name": "Cookware", "description": "Pots, pans, and cookware"},
        {"name": "Lighting", "description": "Home lighting and bulbs"},
        {"name": "Spares", "description": "Appliance spare parts"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Toys / Gifts": [
        {"name": "Toys", "description": "Action figures, cars, and toys"},
        {"name": "Games", "description": "Board games and puzzles"},
        {"name": "Soft Toys", "description": "Plush and soft toys"},
        {"name": "Party Supplies", "description": "Balloons and party decorations"},
        {"name": "Stationery", "description": "Gift stationery and cards"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Footwear / Leather": [
        {"name": "Mens Footwear", "description": "Men's shoes and sandals"},
        {"name": "Womens Footwear", "description": "Women's shoes and heels"},
        {"name": "Kids Footwear", "description": "Children's shoes and boots"},
        {"name": "Sports Shoes", "description": "Athletic and sports shoes"},
        {"name": "Sandals", "description": "Sandals, slippers, and floaters"},
        {"name": "Leather Goods", "description": "Leather products and accessories"},
        {"name": "Crocks", "description": "Clogs, crocs, and casual slides"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Bags / Trolleys": [
        {"name": "Backpacks", "description": "Casual and tech backpacks"},
        {"name": "Handbags", "description": "Women's handbags and totes"},
        {"name": "Trolleys", "description": "Luggage and trolley bags"},
        {"name": "Laptop Bags", "description": "Laptop sleeves and bags"},
        {"name": "School Bags", "description": "School backpacks"},
        {"name": "Travel Bags", "description": "Duffle and travel bags"},
        {"name": "Wallets", "description": "Wallets and cardholders"},
        {"name": "Belt", "description": "Leather and fabric belts"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Sports / Fitness": [
        {"name": "Equipment", "description": "Sports and gym equipment"},
        {"name": "Sportswear", "description": "Athletic wear and jerseys"},
        {"name": "Footwear", "description": "Sports shoes and cleats"},
        {"name": "Supplements", "description": "Protein and fitness supplements"},
        {"name": "Accessories", "description": "Sports accessories and guards"},
        {"name": "Yoga", "description": "Yoga mats and accessories"},
        {"name": "Outdoor", "description": "Camping and outdoor gear"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Pet Shops": [
        {"name": "Pet Food", "description": "Dog, cat, and pet food"},
        {"name": "Treats", "description": "Pet treats and chews"},
        {"name": "Toys", "description": "Pet toys and chewables"},
        {"name": "Grooming", "description": "Pet shampoos and grooming tools"},
        {"name": "Accessories", "description": "Collars, leashes, and beds"},
        {"name": "Health", "description": "Pet healthcare and wellness"},
        {"name": "Aquarium", "description": "Fish food and aquarium supplies"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ],
    "Bookstores": [
        {"name": "Fiction", "description": "Novels and fiction books"},
        {"name": "Non-Fiction", "description": "Biographies and self-help"},
        {"name": "Academic", "description": "Textbooks and academic reference"},
        {"name": "Children", "description": "Children's storybooks and activity books"},
        {"name": "Magazines", "description": "Magazines and periodicals"},
        {"name": "Regional", "description": "Regional language books"},
        {"name": "Stationery", "description": "Bookmarks, pens, and reading accessories"},
        {"name": "GENERAL", "description": "General products"},
        {"name": "OTHERS", "description": "Miscellaneous products"}
    ]
}

# Alias mapping for backwards compatibility and single-word lookup
SHOP_CATEGORIES_MAPPING["GROCERY"] = SHOP_CATEGORIES_MAPPING["Groceries / Kirana"]
SHOP_CATEGORIES_MAPPING["ELECTRONICS"] = SHOP_CATEGORIES_MAPPING["Electronics / Mobile"]
SHOP_CATEGORIES_MAPPING["CLOTHING"] = SHOP_CATEGORIES_MAPPING["Fashion / Lifestyle"]
SHOP_CATEGORIES_MAPPING["PHARMACY"] = SHOP_CATEGORIES_MAPPING["Pharmacies"]
SHOP_CATEGORIES_MAPPING["RESTAURANT"] = SHOP_CATEGORIES_MAPPING["Food Stores"]
SHOP_CATEGORIES_MAPPING["BAKERY"] = SHOP_CATEGORIES_MAPPING["Bakeries"]
SHOP_CATEGORIES_MAPPING["SUPERMARKET"] = SHOP_CATEGORIES_MAPPING["Groceries / Kirana"]
SHOP_CATEGORIES_MAPPING["GENERAL"] = [
    {"name": "GENERAL", "description": "General products"},
    {"name": "OTHERS", "description": "Miscellaneous products"}
]

# Build default categories from union of all product categories
all_cats = []
seen = set()
for cat_list in SHOP_CATEGORIES_MAPPING.values():
    for item in cat_list:
        if item['name'] not in seen:
            seen.add(item['name'])
            all_cats.append(item)

DEFAULT_CATEGORIES = all_cats


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

