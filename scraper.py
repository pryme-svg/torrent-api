import re
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}


def shorten(magnet):
    url = "http://mgnet.me/api/create?&format=json&opt=&m={}".format(magnet)
    e = requests.get(url).json()
    return e['shorturl']


def convertBytes(num):
    step_unit = 1000.0
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


def get(url):
    return requests.get(url, headers=headers)


def toInt(value):
    return int(value.replace(',', ''))


def search1337x(query, limit=3):
    torrents = []
    source = get(f"http://1337x.to/search/{query}/1/").text
    soup = BeautifulSoup(source, 'lxml')
    i = 0
    for tr in soup.select("tbody > tr"):
        a = tr.select("td.coll-1 > a")[1]
        torrent = get("http://1337x.to{}".format(a['href'])).text
        torrent = BeautifulSoup(torrent, 'lxml')
        e = torrent.find('a', href=re.compile(r"^magnet"))
        torrents.append({
            "name": a.text,
            "seeds": int(tr.select("td.coll-2")[0].text),
            "leeches": int(tr.select("td.coll-3")[0].text),
            "size": str(tr.select("td.coll-4")[0].text).split('B', 1)[0] + "B",
            "uploader": tr.select("td.coll-5 > a")[0].text,
            "link": f"http://1337x.to{a['href']}",
            "magnet": e['href'],
            "shortlink": shorten(e['href'])
        })

        if limit is not None:
            if i >= limit:
                break
            i += 1
    return torrents


def searchTPB(query):
    torrents = []
    resp_json = get(f"http://apibay.org/q.php?q={query}&cat=100,200,300,400,600").json()
    if(resp_json[0]["name"] == "No results returned"):
        return torrents

    for t in resp_json:
        torrents.append({
            "name": t["name"],
            "seeds": toInt(t["seeders"]),
            "leeches": toInt(t["leechers"]),
            "size": convertBytes(int(t["size"])),
            "uploader": t["username"],
            "link": f"http://apibay.org/t.php?id={t['id']}"})
    return torrents


def searchRarbg(query):
    torrents = []
    source = get(
        f"http://rargb.to/search/?search={query}"
        "&category[]=movies&category[]=tv&category[]=games&"
        "category[]=music&category[]=anime&category[]=apps&"
        "category[]=documentaries&category[]=other"
    ).text
    soup = BeautifulSoup(source, "lxml")
    for tr in soup.select("tr.lista2"):
        tds = tr.select("td")
        torrents.append({
            "name": tds[1].a.text,
            "seeds": toInt(tds[5].font.text),
            "leeches": toInt(tds[6].text),
            "size": tds[4].text,
            "uploader": tds[7].text,
            "link": f"http://rargb.to{tds[1].a['href']}"})
    return torrents


def searchEttv(query):
    torrents = []
    source = get(f"http://www.ettvcentral.com/torrents-search.php?search={query}").text
    soup = BeautifulSoup(source, "lxml")
    for tr in soup.select("table > tr"):
        tds = tr.select("td")
        torrents.append({
            "name": tds[1].a.text,
            "seeds": toInt(tds[5].font.b.text),
            "leeches": toInt(tds[6].font.b.text),
            "size": tds[3].text,
            "uploader": tds[7].a.text,
            "link": f"http://www.ettvdl.com{tds[1].a['href']}"
        })
    return torrents
