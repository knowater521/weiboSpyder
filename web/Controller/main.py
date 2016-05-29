import xlrd
import datetime
from web.Model.database import Lab,db
data = xlrd.open_workbook('/Volumes/RamDisk/FinalData.xls')
table = data.sheets()[0]
nrows = table.nrows
for i in range(1, nrows):
    uid = table.cell(i, 1).value
    time = datetime.datetime.fromtimestamp(table.cell(i, 8).value/1000)
    text = table.cell(i, 11).value
    new = Lab(uid,text,time)
    db.session.add(new)

db.session.commit()
