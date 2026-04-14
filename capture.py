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
                user_agent="Mozilla/5.0",
                locale="es-AR"
            )

            page = await context.new_page()

            m3u8_links = []

            # capturar requests
            page.on("request", lambda request: (
                m3u8_links.append(request.url)
                if ".m3u8" in request.url else None
            ))

            # capturar responses
            page.on("response", lambda response: (
                m3u8_links.append(response.url)
                if ".m3u8" in response.url else None
            ))

            print("🌍 Abriendo página...")
            await page.goto(URL, timeout=60000, wait_until="domcontentloaded")

            # esperar carga
            await page.wait_for_timeout(25000)

            await browser.close()

            return list(set(m3u8_links))

    except Exception as e:
        print(f"❌ Error con proxy {proxy}: {e}")
        return []


async def main():
    print("🚀 Iniciando captura...")

    all_links = []

    for intento in range(7):  # más intentos
        print(f"\n🔁 Intento {intento + 1}")

        proxy = get_working_proxy()

        if not proxy:
            print("❌ No se encontró proxy válido")
            continue

        links = await intentar_captura(proxy)

        if links:
            all_links.extend(links)

    all_links = list(set(all_links))

    if all_links:
        print("\n🎯 M3U8 ENCONTRADOS:")
        for l in all_links:
            print(l)

        generar_m3u(all_links)
    else:
        print("\n💣 NO SE ENCONTRARON M3U8")
        generar_m3u([])


if __name__ == "__main__":
    asyncio.run(main())
