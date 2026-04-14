import requests
from bs4 import BeautifulSoup
import random

TIMEOUT = 8

# =========================
# FUENTE 1: ProxyScrape
# =========================
def get_proxies_proxyscrape():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&country=AR&protocol=http&timeout=5000"
    try:
        r = requests.get(url, timeout=10)
        return [f"http://{p.strip()}" for p in r.text.split("\n") if p.strip()]
    except:
        return []

# =========================
# FUENTE 2: Free-Proxy.cz
# =========================
def get_proxies_freeproxycz():
    url = "http://free-proxy.cz/es/proxylist/country/AR/all/ping/all"
    proxies = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("table tr")

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) > 1:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append(f"http://{ip}:{port}")
    except:
        pass
    return proxies

# =========================
# TEST REAL (IP + NAVEGACIÓN)
# =========================
def test_proxy(proxy):
    try:
        # 1. verificar IP Argentina
        r = requests.get(
            "https://ipinfo.io/json",
            proxies={"http": proxy, "https": proxy},
            timeout=TIMEOUT
        )

        if r.json().get("country") != "AR":
            return False

        # 2. verificar navegación real
        r2 = requests.get(
            "https://www.google.com",
            proxies={"http": proxy, "https": proxy},
            timeout=TIMEOUT
        )

        if r2.status_code == 200:
            return True

        return False

    except:
        return False

# =========================
# SISTEMA PRINCIPAL
# =========================
def get_all_proxies():
    proxies = []
    proxies += get_proxies_proxyscrape()
    proxies += get_proxies_freeproxycz()

    proxies = list(set(proxies))

    print(f"📊 Total proxies recolectados: {len(proxies)}")
    return proxies

def get_working_proxy():
    proxies = get_all_proxies()
    random.shuffle(proxies)

    for p in proxies[:50]:  # más intentos
        print(f"🧪 Testing real: {p}")
        if test_proxy(p):
            print(f"✅ Proxy FUNCIONAL: {p}")
            return p

    print("❌ No hay proxy funcional")
    return None
