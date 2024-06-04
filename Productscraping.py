
import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin


def get_html(baseurl,page):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
    response = httpx.get(baseurl + str(page),headers=headers,follow_redirects=True)
    try:
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"\nHTTP Exception for {exc.request.url} - {exc} .Page Limit Exceeded")
        return False
    #print(response.status_code)
    html = HTMLParser(response.text)
    return html

def extract(html,sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        if sel=="span[data-ui=full-price]":
            try:
                return html.css_first("span[data-ui=compare-at-price]").text()
            except:
                return None
        return None


#print(html.css_first('title').text())

def parse_page(html):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    #print(products)
    items = []
    for product in products:
        item = {
            "name":product.css_first(".Xpx0MUGhB7jSm5UvK2EY").text(),
            "full price":extract(product,"span[data-ui=full-price]"),#product.css_first("span[data-ui=sale-price]").text()
            "discount price":extract(product,"span[data-ui=sale-price]"),
            "savings":extract(product,"div[data-ui=savings-percent-variant2]")
            }
        yield item
        #items.append(item)
    #return items

def main():
    baseurl = "https://www.rei.com/c/mens-workout-clothing?page="
    products = []
    for i in range(1,11):
        print(f"\nGathering Page {i}")
        html = get_html(baseurl,i)
        if html is False:
            break
        data = parse_page(html)
        for item in data:
            print(item)
            products.append(item)
        time.sleep(2)
    #print(products)

if __name__ == "__main__":
    main()