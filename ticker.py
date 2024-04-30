import re

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Ticker:
    def __init__(self, info):
        self.name = info["name"]
        self.symbol = info["symbol"]
        self.url = info["url"]
        self.price = info["price"]
        self.change = info["change"]
        self.change_percent = info["change_percent"]

    def __str__(self):
        return f"{self.name} ([{self.symbol}](<{self.url}>))\n{self.price} {self.change} {self.change_percent}"


def lookup(symbol):
    # yahoo will return inaccurate data without a useragent
    # platform is specified because yahoo displays the name inconsistently between pc and mobile
    ua = UserAgent(platforms=["pc"]).random

    symbol = symbol.upper()  # yahoo requires symbols in uppercase
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = httpx.get(url, headers={"User-Agent": ua})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        header = soup.find(attrs={"data-testid": re.compile(r"^quote-hdr")})
        info = {
            "name": header.find("h1").string.rsplit(maxsplit=1)[0],
            "symbol": symbol,
            "url": url,
            "price": header.find(
                attrs={"data-field": re.compile(r"^regularMarketPrice")}
            ).string,
            "change": header.find(
                attrs={"data-field": re.compile(r"^regularMarketChange")}
            ).string,
            "change_percent": header.find(
                attrs={"data-field": re.compile(r"^regularMarketChangePercent")}
            ).string,
        }
        return Ticker(info)
    else:
        return f'Unable to lookup "{symbol}"'
