import scrapy
from scrapy.exceptions import CloseSpider
from ..items import EbayItem
from urllib.parse import parse_qsl, urlparse, urlencode


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['www.ebay.com']
    start_urls = []

    custom_settings = {"DOWNLOAD_DELAY": 1,
                       "USER_AGENT": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    def __init__(self, url="", linkId=1, **kwargs):
        parsed_url = urlparse(url)
        params = dict(parse_qsl(parsed_url.query))
        params['_stpos'] = "37338"
        params['_fcid'] = "1"
        params.pop("_trksid", None)
        params.pop("_sop", None)
        encoded_params = urlencode(params)
        final_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{encoded_params}"
        self.start_urls = [final_url]
        self.sourceLinkId = linkId

    def parse(self, response):
        prods = response.xpath(
            "//ul[contains(@class,'srp-results')]/li")
        if len(prods) == 0:
            raise CloseSpider("empty result")
        for prod in prods:
            if "srp-river-answer--REWRITE_START" in prod.xpath(".//@class").get():
                break
            elif "s-item" in prod.xpath(".//@class").get():
                item = EbayItem()
                item['task'] = self.sourceLinkId
                item['title'] = prod.xpath(
                    ".//div[@class='s-item__title']/span/text()"
                ).get(default="N/A")
                item['condition'] = prod.xpath(
                    ".//*/span[@class='SECONDARY_INFO']/text()"
                ).get(default="")
                item['price'] = prod.xpath(
                    ".//span[@class='s-item__price']/text()"
                ).get(default="N/A")
                prOp = prod.xpath(
                    ".//span[contains(@class, 's-item__purchase-options')]/text()"
                ).get()
                if prOp is None:
                    prOp = prod.xpath(
                        ".//span[contains(@class, 's-item__purchaseOptionsWithIcon')]/text()"
                    ).get()
                    if prOp is None:
                        if prod.xpath(".//span[contains(@class, 's-item__bidCount')]/text()").get():
                            prOp = "Auction"
                item['sell'] = prOp
                shipping = prod.xpath(
                    ".//span[contains(@class, 's-item__shipping')]/text()").get()
                if not shipping:
                    shipping = prod.xpath(
                        ".//span[contains(@class, 's-item__freeXDays')]/span/text()"
                    ).get()
                if not shipping:
                    shipping = prod.xpath(
                        ".//span[contains(@class, 's-item__localDelivery')]/text()"
                    ).get(default="")
                item['shipping'] = shipping.replace(",", " ")
                item['url'] = prod.xpath(
                    ".//a[@class='s-item__link']/@href"
                ).get().split("?")[0]
                item['prodId'] = prod.xpath(
                    ".//a[@class='s-item__link']/@href"
                ).get().split("itm/")[-1].split("?")[0]
                yield item
        _next = response.xpath(
            "//a[contains(@class, 'pagination__next')]/@href"
        ).get()
        if _next is None:
            raise CloseSpider("No Next Page.")
        yield scrapy.Request(url=_next)
        pass
