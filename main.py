import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}



url = 'https://glycemic-index.net/baguette-white/'
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

product = soup.find('h1', class_='entry-title').text.strip()

nutrition = soup.find("div", class_="entry-content clear", itemprop="text")
for table in nutrition.find_all('table'):
    table.decompose()

text = nutrition.get_text()

kcal = re.search(r"(\d+)\s*kcal", text).group(1)
proteins = re.search(r"(\d+\.\d+)\s*grams?\s+of\s+proteins", text).group(1)
carbohydrates = re.search(r"(\d+\.\d+)\s*grams?\s+of\s+carbohydrates", text).group(1)
fats = re.search(r"(\d+\.\d+)\s*grams?\s+of\s+fats", text).group(1)


df = pd.DataFrame({'Product': [product],
                   'kcal': [kcal],
                   'proteins': [proteins],
                   'carbohydrates': [carbohydrates],
                   'fats': [fats]})

df.to_csv('nutrition.csv', index=False, sep='\t')

# print(product)
# print("kcal:", kcal)
# print("proteins:", proteins)
# print("carbohydrates:", carbohydrates)
# print("fats:", fats)

# calories = re.findall(r'Calories \(kcal\)(\d+)', text)
# proteins = re.findall(r'Proteins \(g\)(\d+.\d+)', text)
# carbohydrates = re.findall(r'Carbohydrates \(g\)(\d+.\d+)', text)
# fats = re.findall(r'Fats \(g\)(\d+.\d+)', text)
#
# print("Calories:", calories[0])
# print("Proteins:", proteins[0])
# print("Carbohydrates:", carbohydrates[0])
# print("Fats:", fats[0])
