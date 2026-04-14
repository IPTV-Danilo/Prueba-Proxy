import requests
from bs4 import BeautifulSoup
import random

TIMEOUT = 5

def get_proxies_proxyscrape():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&country=AR&protocol=http&timeout=5000"
    try:
        r = requests.get(url, timeout=10)
        return [f"http://{p.strip()}" for p in r.text.split("\n") if p.strip()]
    except:
        return []

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

def get_working_proxy():
    proxies = get_proxies_proxyscrape()
    random.shuffle(proxies)

    for p in proxies[:20]:  # probar solo algunos
        print(f"Testing proxy: {p}")
        if test_proxy(p):
            print(f"✔ Proxy OK: {p}")
            return p

    return None
