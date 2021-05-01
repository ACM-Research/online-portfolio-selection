from datetime import datetime
import csv
data = []
with open('./merged/ABBV_AMC_BGS_GME_NHI_WMT_XOM.csv') as csvf:
    r = csv.reader(csvf)
    for i,row in enumerate(r):
        if not i:
            data.append(['time', 'ask', 'bid', 'ticker'])
            continue
        data.append([row[0], row[1], row[4], row[-1]])
        data[-1][0] = int(datetime.strptime(data[-1][0], '%Y-%m-%d').timestamp()) * 1000000000
print(data)

with open('./merged/ABBV-AMC-BGS-GME-NHI-WMT-XOM.csv', 'w') as outcsv:
    w = csv.writer(outcsv)
    for row in data:
        w.writerow(row)
