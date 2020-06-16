import requests
import json
import csv
from collections import OrderedDict

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_json = response.json()
data = data_json[0]

cur_data=[]

for i in data.get('rates'):
    cur_data.append(i)

print(cur_data)
with open('kantor.csv', 'w', newline='') as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data.get('rates'):
        writer.writerow(i)


