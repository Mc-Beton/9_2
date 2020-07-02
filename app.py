from flask import Flask, render_template, request, redirect
import csv
from collections import OrderedDict
import requests
import json
from decimal import Decimal, getcontext



app = Flask(__name__)

getcontext().prec = 2
result=[]
data_cur=[]
cod=[]

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_json = response.json()
data = data_json[0]

with open('kantor.csv', 'w', newline='') as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data.get('rates'):
        writer.writerow(i)

with open('kantor.csv', newline='') as csvfile:
    data_j = csv.DictReader(csvfile)
    for i in data_j:
        data_cur.append(dict(OrderedDict(i)))

for i in data_cur:
    j=i.get('code')
    cod.append(j)

@app.route("/kantor/", methods=['GET', 'POST'])
def exchange():
    
    if request.method =='GET':
       
        return render_template("kantor.html", sro=cod)

    if request.method == 'POST':
        try:
            data = request.form
            cur = data.get('currency')
            amo = data.get('amount')
            amo_num = float(amo)
        
            for i in data_cur:
                if cur == i.get('code'):
                    bi = i.get('bid')

            bi_num = float(bi)
            result.clear()

            x = Decimal(amo_num*bi_num)
            output = round(x,2)
            result.append(output)

            return render_template("calcu_res.html", result=result)

        except:
            return render_template("kantor.html", sro=cod)


if __name__ == '__main__':
    app.run(debug=True)