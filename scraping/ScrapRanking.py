import requests
from bs4 import BeautifulSoup

url = 'https://www.shanghairanking.com/rankings/gras/2023/RS0102'

reponse = requests.get(url)
if reponse.ok:
    print('rep1 ok')
    soup = BeautifulSoup(reponse.text, 'lxml')
    tds = soup. findAll('tr', {'class': 'data-v-ae1ab4a8'})
    datas = [(str(td) + '\n\n') for td in tds]
    print(datas)
else:
    print('rep1 not ok')