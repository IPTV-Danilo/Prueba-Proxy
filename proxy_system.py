import requests
from bs4 import BeautifulSoup
import random

TIMEOUT = 5

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
# FUENTE 2: Proxy5
# =========================
def get_proxies_proxy5():
    url = "https://proxy5.net/free-proxy/argentina"
    proxies = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("table tbody tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 1:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append(f"http://{ip}:{port}")
    except:
        pass
    return proxies

# =========================
# FUENTE 3: Free-Proxy.cz
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
# TESTEO REAL (AR)
# =========================
def test_proxy(proxy):
    try:
        r = requests.get(
            "https://ipinfo.io/json",
            proxies={"http": proxy, "https": proxy},
            timeout=TIMEOUT
        )
        return r.json().get("country") == "AR"
    except:
        return False

# =========================
# SISTEMA PRINCIPAL
# =========================
def get_all_proxies():
    proxies = []

    print("🔎 Obteniendo ProxyScrape...")
    proxies += get_proxies_proxyscrape()

    print("🔎 Obteniendo Proxy5...")
    proxies += get_proxies_proxy5()

    print("🔎 Obteniendo FreeProxy...")
    proxies += get_proxies_freeproxycz()

    # eliminar duplicados
    proxies = list(set(proxies))

    print(f"📊 Total proxies recolectados: {len(proxies)}")
    return proxies

def get_working_proxy():
    proxies = get_all_proxies()
    random.shuffle(proxies)

    for p in proxies[:40]:  # probamos más proxies
        print(f"🧪 Testing: {p}")
        if test_proxy(p):
            print(f"✅ Proxy ARG válido: {p}")
            return p

    print("❌ No se encontró proxy válido")
    return None
