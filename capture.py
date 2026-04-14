import asyncio
from playwright.async_api import async_playwright

URL = "https://streamtpnew.com/global1.php?stream=espn"

async def capture_m3u8():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page = await context.new_page()

        m3u8_links = []

        # escuchar requests
        page.on("request", lambda request: (
            m3u8_links.append(request.url)
            if ".m3u8" in request.url else None
        ))

        print("Abriendo página...")
        await page.goto(URL, timeout=60000)

        # esperar que cargue el player
        await page.wait_for_timeout(15000)

        await browser.close()

        return m3u8_links


async def main():
    links = await capture_m3u8()

    if links:
        print("🎯 M3U8 encontrados:")
        for l in links:
            print(l)
    else:
        print("❌ No se encontró ningún m3u8")


if __name__ == "__main__":
    asyncio.run(main())
