from bs4 import BeautifulSoup
import requests

url = "http://10.0.0.17/"

page = requests.get(url)

soup = BeautifulSoup(page.content,'html.parser')

rows = soup.find_all('tr')

output = str(rows[0])[8:-10]

print(output)