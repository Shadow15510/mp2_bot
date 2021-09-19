from bs4 import BeautifulSoup
import json
import os
import requests
import time


def get_cdp_rss():
    # Récupération de la dernière date
    lasttime = requests.get(f"https://odyssee.pythonanywhere.com/read/{os.environ['api_token']}").text
    lasttime = time.strptime(lasttime, "%d:%m:%H:%M")

    # Connexion au site et stockage du cookie de connexion
    payload = {"login": os.environ["cdp_login"], "motdepasse": os.environ["cdp_password"], "connexion": 1}
    r = requests.post("https://cahier-de-prepa.fr/mp2-malherbe/ajax.php", data=payload)
    cookies = {"CDP_SESSION": r.cookies["CDP_SESSION"]}

    # Requête sur les flux RSS
    cdp = requests.get("https://cahier-de-prepa.fr/mp2-malherbe/recent", cookies=cookies)
    cdp = BeautifulSoup(cdp.text, features="html5lib")
    cdp = cdp.find_all("article", {"class": "recents"})

    rss, doc_times = [], []
    for document in cdp:
        pub_date, description = document.select("p")
        pub_date = pub_date.text

        doc_time = time.strptime(pub_date, "Publication le %d/%m à %Hh%M")

        if doc_time > lasttime:
            doc_times.append(doc_time)

            title = document.select_one("a")
            description

            rss.append((
                title.text,
                pub_date[12:],
                description.text.replace("\xa0", " ").split(", "),
                f"https://cahier-de-prepa.fr/mp2-malherbe/{title['href']}"
            ))

    if rss:
        lasttime = max(doc_times)
        requests.get(f"https://odyssee.pythonanywhere.com/send/{os.environ['api_token']}/{time.strftime('%d:%m:%H:%M', lasttime)}")
        return rss