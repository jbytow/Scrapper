import pandas as pd
import requests
import re
import time
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

main_url = 'https://glycemic-index.net/glycemic-index-chart/'
page_main = requests.get(main_url, headers=headers)
soup_main = BeautifulSoup(page_main.content, 'html.parser')

table = soup_main.find('table', class_='tftable')

product_urls = []

for row in table.find_all('tr'):
    link = row.find('a')
    if link:
        product_urls.append(link['href'])

print(product_urls)

product_list = []
kcal_list = []
proteins_list = []
carbohydrates_list = []
fats_list = []

for url in product_urls:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    time.sleep(2)

    product = soup.find('h1', class_='entry-title').text.strip()

    nutrition = soup.find("div", class_="entry-content clear", itemprop="text")
    for table in nutrition.find_all('table'):
        table.decompose()

    text = nutrition.get_text()

    kcal = re.search(r"(\d+)\s*kcal", text).group(1)
    proteins = re.search(r"(\d+\.\d+)\s*grams?\s+of\s+proteins", text).group(1)
    carbohydrates = re.search(r"(\d+\.\d+)\s*grams?\s+of\s+carbohydrates", text).group(1)
    fats = re.search(r"(\d+\.\d+)\s*grams?\s+of\s+fats", text).group(1)

    product_list.append(product)
    kcal_list.append(kcal)
    proteins_list.append(proteins)
    carbohydrates_list.append(carbohydrates)
    fats_list.append(fats)

df = pd.DataFrame({'Product': product_list,
                   'kcal': kcal_list,
                   'proteins': proteins_list,
                   'carbohydrates': carbohydrates_list,
                   'fats': fats_list})

df.to_csv('nutrition.csv', index=False, sep='\t')

