from datetime import datetime


def main():
    nome = datetime.today().strftime('%d-%m-%Y')
    arquivoFonte = open("C:\\Users\\pcc\\Rastreio\\logs\\main.log","r")
    arquivoDestino = open("C:\\Users\\pcc\\Rastreio\\logs\\" + nome +".log","w")
    for linha in arquivoFonte:
        if("telegram.ext.updater" not in linha and "apscheduler.scheduler" not in linha):
            arquivoDestino.write(linha)
main()