import asyncio
import pandas as pd
from urllib.parse import quote
from playwright.async_api import async_playwright

EXCEL_FILE = "menukit_whatsapp_outreach.xlsx"

DELAY_BETWEEN_MESSAGES = 30
WHATSAPP_LOAD_WAIT = 8

SKIP_NUMBERS = {
    "7540040234",
    "8186057777",
    "7708814391",
    "9514959861",
    "8148987007",
    "8015621160",
    "9342500428",
    "9500236621",
    "9952590703",
    "9159361212",
    "9842118990",
    "8870477079",
    "9894940933",
    "7867877878",
}

message = """
உங்கள் Restaurant-க்கு தினமும் Customers வராங்க.

ஆனா ஒரு பெரிய Problem இருக்கு:

சாப்பிடுறாங்க → Bill Pay பண்றாங்க → போறாங்க → அப்படியே மறந்துடுறாங்க. 👻

அந்த Customers-ஐ உங்கள் Restaurant-க்கு திரும்பவும் வர வைக்க முடிஞ்சா? 🔥

அதுக்காகத்தான் MenuKit 🚀

இது வெறும் Digital Menu மட்டும் கிடையாது.

உங்கள் Restaurant-க்கான Customer Management Platform.

📱 Digital Menu
👤 Customer Details
🎯 Offers & Promotions
🔁 பழைய Customers-ஐ மீண்டும் கொண்டு வருதல்
📊 Customer Insights
⚡ Menu-வை உடனுக்குடன் Update செய்யலாம்

ஒருமுறை வந்த Customer-ஐ மீண்டும் மீண்டும் வரக்கூடிய Customer-ஆ மாற்றுங்கள். ❤️

நாங்கள் தற்போது Restaurants-ஐ MenuKit-ல் onboard செய்து வருகிறோம்.

உங்கள் Restaurant-க்கு ஒரு Quick Demo காட்டட்டுமா? 👀

Interested? 🔥
"""


async def main():

    df = pd.read_excel(EXCEL_FILE)

    async with async_playwright() as p:

        # Visible browser for initial WhatsApp login
        browser = await p.chromium.launch(
            headless=False
        )

        context = await browser.new_context()

        page = await context.new_page()

        # Open WhatsApp ONCE
        await page.goto("https://web.whatsapp.com")

        print("📱 Waiting for WhatsApp Web...")

        # First time: scan QR manually
        await page.wait_for_timeout(15000)

        print("✅ WhatsApp Web loaded")

        for _, row in df.iterrows():

            phone = str(row["Mobile Number"]).strip()

            if phone.endswith(".0"):
                phone = phone[:-2]

            restaurant = str(row["Business Name"]).strip()

            if phone in SKIP_NUMBERS:
                print(f"⏭️ SKIPPED → {restaurant} | {phone}")
                continue

            text = message.format(
                restaurant=restaurant
            )

            print(
                f"📤 Sending → "
                f"{restaurant} | {phone}"
            )

            url = (
                "https://web.whatsapp.com/send?"
                f"phone=91{phone}"
                f"&text={quote(text)}"
            )

            # SAME TAB
            await page.goto(url)

            await page.wait_for_timeout(
                WHATSAPP_LOAD_WAIT * 1000
            )

            # Press Enter to send
            await page.keyboard.press("Enter")

            print(
                f"✅ Sent → "
                f"{restaurant} | {phone}"
            )

            await page.wait_for_timeout(
                DELAY_BETWEEN_MESSAGES * 1000
            )

        print("🏁 Finished")

        await browser.close()


asyncio.run(main())