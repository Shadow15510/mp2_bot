from bs4 import BeautifulSoup
import json
import os
import requests
import time


def get_cdp_rss():
    lasttime = requests.get(f"https://odyssee.pythonanywhere/read/{os.environ['api_token']}").text
    lasttime = time.strptime(lastime, "%a, %d %b %Y %H:%M:%S")


    payload = {"login": os.environ["cdp_login"], "motdepasse": os.environ["cdp_password"], "connexion": 1}

    r = requests.post("https://cahier-de-prepa.fr/mp2-malherbe/ajax.php", data=payload)
    cookies = {"CDP_SESSION": r.cookies["CDP_SESSION"]}

    cdp = requests.get("https://cahier-de-prepa.fr/mp2-malherbe/rss/2d2f630bda45d7b1d0c3/rss.xml", cookies=cookies)

    cdp = BeautifulSoup(cdp.text, features="html5lib")
    cdp = cdp.find_all("item")

    rss = []
    for item in cdp:
        item_time = item.select_one("pubDate").text
        item_time = time.strptime(item_time[: item_time.find("+")], "%a, %d %b %Y %H:%M:%S ")

        times = []
        if item_time >= lasttime:
            times.append(item_time)
            title = item.select_one("title").text
            link = item.text.splitlines()[2]
            rss.append((
                title[9: title.find("]]>", 10)],
                link.strip()
            ))

    if rss:
        lasttime = max(times)
        requests.get(f"https://odyssee.pythonanywhere/read/{os.environ['api_token']}/{time.strftime('%a, %d %b %Y %H:%M:%S', lasttime)}")

        return rss
    

