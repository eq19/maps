import subprocess

for i in ['binance', 'binancecoinm', 'binanceusdm', 'bitbank', 'bitflyer', 'btcbox', 'coincheck', 'huobijp', 'liquid', 'zaif']:
    subprocess.run(f'freqtrade list-pairs --print-csv --one-column --exchange {i}', shell=True)
