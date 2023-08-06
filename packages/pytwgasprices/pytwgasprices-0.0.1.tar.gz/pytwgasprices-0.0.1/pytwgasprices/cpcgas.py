import requests
import bs4

CPC_WEBSITE_URL = 'https://www.cpc.com.tw'

def get_cpc_gas_info():
    """
    Fetch the latest gas prices from CPC official website.
    """
    response = requests.get(CPC_WEBSITE_URL)

    if response.ok:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        gas_tags = soup.select('.today_price_info')
        return [(tag.select_one('.name').text, tag.select_one('.price').text) for tag in gas_tags]

if __name__ == '__main__':
    print(get_cpc_gas_info())
