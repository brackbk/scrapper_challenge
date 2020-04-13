#from scripts import forms
from flask import Flask, request
from google import Google
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
    google = Google()
    with open('produtos.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        resultAvg = []
        for row in readCSV:
            try:
                html = google.request('http://www.google.com.br/search?tbm=shop&q={}&tbs=vw:g'.format(str(row[0]))) 
                url = google.getUrl(html, 'Comparar')
                data = google.getData(url.replace('?q','/online?q'), row)
                resultAvg.append(google.averageData(data, row))
                if data: 
                    filename = row[0]
                    google.writeToCsv(filename, data)  
            except Exception as e: 
                print('nao foi possivel captar dados:' + str(e))
                pass
    if resultAvg:
        filename = 'media_produtos'
        google.writeToCsv(filename, resultAvg)
    return json.dumps({
        'analiseCompleta': data,
        'analiseResumida': resultAvg
    })


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")