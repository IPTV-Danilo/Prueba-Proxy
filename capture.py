import asyncio
from playwright.async_api import async_playwright
from proxy_system import get_working_proxy
from m3u_generator import generar_m3u

URL = "https://streamtpnew.com/global1.php?stream=espn"

async def intentar_captura(proxy):
    try:
        print(f"🌐 Usando proxy: {proxy}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                proxy={"server": proxy} if proxy else None
            )

            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                locale="es-AR"
            )

            page = await context.new_page()

            m3u8_links = []

            # capturar requests
            page.on("request", lambda request: (
                m3u8_links.append(request.url)
                if ".m3u8" in request.url else None
            ))

            print("🌍 Abriendo página...")
            await page.goto(URL, timeout=60000)

            # esperar carga del player
            await page.wait_for_timeout(15000)

            await browser.close()

            return list(set(m3u8_links))

    except Exception as e:
        print(f"❌ Error con proxy {proxy}: {e}")
        return []


async def main():
    print("🚀 Iniciando captura...")

    for intento in range(5):
        print(f"\n🔁 Intento {intento + 1}")

        proxy = get_working_proxy()

        if not proxy:
            print("❌ No se encontró proxy válido")
            continue

        links = await intentar_captura(proxy)

        if links:
            print("\n🎯 M3U8 ENCONTRADOS:")
            for l in links:
                print(l)

            generar_m3u(links)
            return

    print("\n💣 No se pudo capturar ningún m3u8")


if __name__ == "__main__":
    asyncio.run(main())
