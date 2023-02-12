from random import choice
from time import sleep
import requests

def proxy_generator():
    """
    From https://github.com/dbertho/spamcity/blob/main/spamcity.py
    Returns a random proxy from a proxy list
    """
    response1 = requests.get("https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
                             timeout=3
                             )
    response2 = requests.get("https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/ultrafast.txt",
                             timeout=3
                             )
    response3 = requests.get("https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
                             timeout=3
                             )
    response4 = requests.get("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                             timeout=3
                             )
    response5 = requests.get("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
                             timeout=3
                             )
    response6 = requests.get("https://raw.githubusercontent.com/rx443/proxy-list/main/online/https.txt",
                             timeout=3
                             )
    response7 = requests.get("https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
                             timeout=3
                             )
    lines = response1.text.splitlines()
    lines.extend(response2.text.splitlines())
    lines.extend(response3.text.splitlines())
    lines.extend(response4.text.splitlines())
    lines.extend(response5.text.splitlines())
    lines.extend(response6.text.splitlines())
    lines.extend(response7.text.splitlines())
    test_proxy = choice(list(lines))
    test_proxy = {"https": test_proxy}
    return test_proxy

def rand_proxy():
    """
    Test proxies from proxy_generator
    and return the first random proxy which is working
    """
    proxy = False
    while True:
        test_proxy = proxy_generator()
        try:
            sleep(1)
            response = requests.get('https://api.myip.com/', proxies=test_proxy, timeout=5)
            print(response.json())
            if response.status_code == 200:
                proxy = test_proxy
                break
        except Exception:
            print("Proxy is not responding, trying another one")
        if proxy:
            break
    #print(proxy)
    return proxy
