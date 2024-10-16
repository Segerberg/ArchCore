from bs4 import BeautifulSoup

with open('metadata_crosswalk.html') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    tr = soup.find_all('tr')
    for t in tr:
        tds = soup.find_all('td')
        print(tds[0])