import requests
import sys
import csv
from bs4 import BeautifulSoup
import time
from datetime import datetime

class Google():
  def request(self, url):
    html = ''
    response = requests.get(url, headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36'})
    try: 
        response.raise_for_status()
        html = response.content
    except requests.exceptions.HTTPError as e: 
        self.request(url)
        print(e)
    return html

  def getUrl(self,html, text):
    soup = BeautifulSoup(html)
    url = soup.select_one('a:contains("{}")'.format(text))['href']
    return url

  def writeToCsv(self, filename, data):
      with open(filename + '.csv', 'w', newline='', encoding='utf8') as file:
          writer = csv.writer(file)
          writer.writerow(data[0].keys())
          for item in data:
              writer.writerow(item.values())  

  def averageData(self, data , row):
    now = datetime.now() 
    total = 0
    minValue = 9999999
    maxValue = 0
    count = 0
    for item in data:
      total = total + item['PRECO CANAL']
      count = count + 1
      if float(item['PRECO CANAL']) > maxValue:
        maxValue = item['PRECO CANAL']

      if float(item['PRECO CANAL']) < minValue:
        minValue = item['PRECO CANAL'] 

    result = {
      'PRODUTO': row[1],
      'EAN': row[0],
      'PRECO REF':row[2],
      'MIN':minValue,
      'MAX':maxValue,
      'MEDIA': str(total / count),
      'QTDE SELLER':count,
      'DATA':now.strftime("%x")
    }
    return result


  def getData(self, url, rw):
    now = datetime.now() 
    data = []
    start = 0
    more = True
    while more:
      html = self.request('https://www.google.com.br' + url)
      soup = BeautifulSoup(html)
      url = url.replace('&prds=','&prds=start:' + str(start) + ',')
      rows = soup.find_all('tr', attrs={'class': 'sh-osd__offer-row'})
      for row in rows:  
            price = row.find('table').select('td')[1]
            seller = row.find('span')
            if hasattr(price, 'text'):
              price = float(price.text.replace("R$\u00A0","").replace('.','').replace(',','.'))
              status = 'IGUAL'
              if price > float(rw[2]):
                status = 'MAIS CARO'
              elif price < float(rw[2]):
                status = 'MAIS BARATO'
              gap = str(abs(round(((price * 100) / float(rw[2])) - 100,2)))
              data.append({
                'PRODUTO': rw[1],
                'EAN': rw[0],
                'CANAL':'google',
                'VENDEDOR':seller.text,
                'PRECO REF':rw[2],
                'PRECO CANAL':price,
                'GAP':gap,
                'STATUS':status,
                'DATA':now.strftime("%x"),
                'HORA':now.strftime("%X")
              })
      start = start + 25
      existMore = soup.find('button', attrs={'class': 'sh-fp__pagination-button'})
      if not existMore:
        more = False
      pass
    return data