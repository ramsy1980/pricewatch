from requests_html import HTMLSession

class ItemOutOfStockError(Exception):
    pass


class ItemPriceConversionError(Exception):
    pass


def filter_result(result: str) -> str:
    if result.isdigit():
        return result
    else:
        return "0"


class Request:

    @classmethod
    def scrape(
            cls,
            url: str,
            css_selector: str,
            out_of_stock_css_selector: str = None,
            enable_javascript: bool = False
    ) -> float:
        session = HTMLSession()

        r = session.get(url)

        if enable_javascript:
            r.html.render(sleep=5)

        if out_of_stock_css_selector is not None:
            out_of_stock = r.html.find(out_of_stock_css_selector, first=True)

        if out_of_stock is not None:
            raise ItemOutOfStockError("Item is out of stock")
        else:
            try:
                element_text = r.html.find(css_selector, first=True).text
                split_price = list(map(filter_result, element_text.split(" ")))
                price = float(".".join(split_price))

                return price
            except:
                raise ItemPriceConversionError("Unable to convert price")
