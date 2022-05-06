from datetime import datetime
import data_base

def main():
    id = datetime.today().strftime('%d-%m-%Y')
    log = open("C:\\Users\\pcc\\Rastreio\\logs\\" + id +".log","r")
    content = []
    for x in log:
        content.append(x)
    data_base.insertLog(id,"data_base",content)
    log.close()
main()