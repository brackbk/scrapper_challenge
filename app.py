#from scripts import forms
from flask import Flask, request
from scrap import Scrap
import sys
import os 
import json
import csv

app = Flask(__name__)
# ======== Roteamento =========================================================== #
# -------- Index ------------------------------------------------------------- #
@app.route('/')
def index():
    data = {}
    scrap = Scrap()
    with open('produtos.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        resultAvg = []
        for row in readCSV:
            try:
                html = scrap.request('http://www.google.com.br/search?tbm=shop&q={}&tbs=vw:g'.format(str(row[0]))) 
                url = scrap.getUrl(html, 'Comparar')
                data = scrap.getData(url.replace('?q','/online?q'), row)
                resultAvg.append(scrap.averageData(data, row))
                if data: 
                    filename = row[0]
                    scrap.writeToCsv(filename, data)  
            except Exception as e: 
                print('nao foi possivel captar dados:' + e)
                pass
    if resultAvg:
        filename = 'media produtos'
        scrap.writeToCsv(filename, resultAvg)
    return json.dumps({
        'analiseCompleta': data,
        'analiseResumida': resultAvg
    })


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")