import asyncio
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright
import pandas as pd

# Expanded search queries across key Madurai neighborhoods to reach 500+ records quickly
AREAS = [
    "KK Nagar Madurai",
    "Anna Nagar Madurai",
    "Simmakkal Madurai",
    "West Masi Street Madurai",
    "Town Hall Road Madurai",
    "Mattuthavani Madurai",
    "Periyar Madurai",
    "Goripalayam Madurai",
    "Pasumalai Madurai",
    "Tallakulam Madurai",
    "Thiruparankundram Madurai",
    "Bye Pass Road Madurai",
]

CATEGORIES = ["restaurants", "cafes", "hotels", "retailers", "supermarkets"]

# Generate full localized query list
QUERIES = [f"{cat} in {area}" for area in AREAS for cat in CATEGORIES]

OUTPUT_FILE = "madurai_500_businesses.xlsx"
TARGET_PER_QUERY = 35


def append_to_excel(business_data, file_path):
    """Appends scraped records directly to the Excel file in real-time."""
    df_new = pd.DataFrame([business_data])

    if not os.path.exists(file_path):
        df_new.to_excel(file_path, index=False, engine="openpyxl")
    else:
        try:
            with pd.ExcelWriter(
                file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay"
            ) as writer:
                # Read existing sheet to find next empty row
                try:
                    df_existing = pd.read_excel(file_path)
                    start_row = len(df_existing) + 1
                    df_new.to_excel(
                        writer,
                        index=False,
                        header=False,
                        startrow=start_row,
                    )
                except Exception:
                    df_new.to_excel(file_path, index=False)
        except PermissionError:
            print(
                f"\n[WARNING] Please close '{file_path}' in Excel! Data saved to fallback file."
            )
            fallback_file = f"madurai_businesses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df_new.to_excel(fallback_file, index=False)


async def scrape_google_maps():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )

        page = await context.new_page()
        page.set_default_navigation_timeout(60000)
        page.set_default_timeout(8000)

        # Track seen (Name, Phone) combinations in memory to avoid duplicate entries
        seen_keys = set()
        total_saved = 0

        print(f"Starting real-time extraction into '{OUTPUT_FILE}'...")

        for index, query in enumerate(QUERIES, start=1):
            print(f"\n[{index}/{len(QUERIES)}] Query: {query}...")

            search_url = (
                f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            )

            try:
                await page.goto(search_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(1800)
            except Exception as e:
                print(f"Navigation issue for '{query}'. Moving to next...")
                continue

            feed_selector = 'div[role="feed"]'
            try:
                await page.wait_for_selector(feed_selector, timeout=8000)
            except Exception:
                print(f"Feed panel omitted for '{query}'. Skipping...")
                continue

            scrollable_div = page.locator(feed_selector)

            # Fast scrolling pass
            previous_count = 0
            for _ in range(10):
                await scrollable_div.evaluate(
                    "node => node.scrollBy(0, 1500)"
                )
                await page.wait_for_timeout(800)

                items = await page.locator('a[href*="/maps/place/"]').all()
                if (
                    len(items) == previous_count
                    or len(items) >= TARGET_PER_QUERY
                ):
                    break
                previous_count = len(items)

            place_links = await page.locator('a[href*="/maps/place/"]').all()

            for item in place_links:
                try:
                    aria_label = await item.get_attribute("aria-label")
                    maps_link = await item.get_attribute("href")

                    if not aria_label:
                        continue

                    name = aria_label

                    await item.click()
                    await page.wait_for_timeout(900)

                    # 1. Extract Phone Number
                    phone = "N/A"
                    phone_locator = page.locator(
                        'button[data-tooltip*="phone"], button[data-item-id*="phone"]'
                    )
                    if await phone_locator.count() > 0:
                        phone_raw = await phone_locator.first.inner_text()
                        phone = phone_raw.replace("\n", " ").strip()

                    if phone == "N/A":
                        content = await page.content()
                        phone_match = re.search(
                            r"(\+91[\s\-]?[0-9]{5}[\s\-]?[0-9]{5}|0[0-9]{2,4}[\s\-]?[0-9]{6,8})",
                            content,
                        )
                        if phone_match:
                            phone = phone_match.group(1)

                    # 2. Extract Address
                    address = "N/A"
                    addr_locator = page.locator(
                        'button[data-item-id="address"]'
                    )
                    if await addr_locator.count() > 0:
                        addr_raw = await addr_locator.first.inner_text()
                        address = addr_raw.replace("\n", " ").strip()

                    # 3. Extract Website Link (directly from button attribute, no site visits)
                    website = "N/A"
                    website_locator = page.locator(
                        'a[data-item-id="authority"], a[aria-label*="website"]'
                    )
                    if await website_locator.count() > 0:
                        website_url = (
                            await website_locator.first.get_attribute("href")
                        )
                        if website_url:
                            website = website_url

                    # Check for duplicates using (Name, Phone) key
                    record_key = (name.lower(), phone.strip())
                    if record_key in seen_keys:
                        continue

                    seen_keys.add(record_key)

                    # Prepare row record
                    record = {
                        "Category/Query": query,
                        "Name": name,
                        "Phone": phone,
                        "Address": address,
                        "Website": website,
                        "Google Maps Link": maps_link if maps_link else "N/A",
                    }

                    # Append directly to Excel file on disk
                    append_to_excel(record, OUTPUT_FILE)
                    total_saved += 1
                    print(
                        f" Saved #{total_saved}: {name} | Phone: {phone}"
                    )

                except Exception:
                    continue

        await browser.close()
        print(
            f"\n Done! Scraped & wrote {total_saved} unique records live into '{OUTPUT_FILE}'."
        )


if __name__ == "__main__":
    asyncio.run(scrape_google_maps())