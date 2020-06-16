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
for i in data.get('rates'):
    data_cur.append(i)

for i in data_cur:
    j=i.get('code')
    cod.append(j)

@app.route("/kantor/", methods=['GET', 'POST'])
def exchange():
    if request.method =='GET':
        items=cod
        return render_template("kantor.html", items=items)

    if request.method == 'POST':

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



if __name__ == '__main__':
    app.run(debug=True)