import requests
import bs4

FPCC_WEBSITE_URL = 'http://www.fpcc.com.tw/tc/affiliate.php'

def get_fpcc_gas_info():
    """
    Fetch the latest gas prices from FPCC official website.
    """
    response = requests.get(FPCC_WEBSITE_URL)

    if response.ok:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        classes_to_parse = ('.GasPrice3', '.GasPrice2', '.GasPrice1', '.GasPrice4',)
        gas_tags = [soup.select_one(c) for c in classes_to_parse]
        gas_infos = [(tag.select_one('h3').text.strip().replace('\n', '').replace(' ', ''), 
                      tag.select_one('.pricing').text.replace('$', '')) for tag in gas_tags]
        return gas_infos

if __name__ == '__main__':
    print(get_fpcc_gas_info())
