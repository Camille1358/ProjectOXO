import requests
from bs4 import BeautifulSoup

url = 'https://www.shanghairanking.com/rankings/gras/2023/RS0102'

reponse = requests.get(url)
if reponse.ok:
    print('rep1 ok')
    soup = BeautifulSoup(reponse.text)
    data = soup.find('td data-v-ae1ab4a8 class')
    print(data)
else:
    print('rep1 not ok')