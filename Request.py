import os
import sys
import csv
import io
import requests
import pandas as pd
from PegarToken import pegartoken
from env_utils import set_env_variable
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

if os.getenv("DATACONSULTA") != '':
    DataAlt = os.getenv("DATACONSULTA")
else:
    print('Data de alteração inválida, preencha o campo para consulta')

now = datetime.now()
dataConsulta = now.strftime("%Y-%m-%d") #("%d/%m/%Y")

base_url = 'http://localhost:2004/rel/maxus/kpi/' #'https://api.toqweb.com.br:2004'

#url_BiTitulos = 'http://localhost:2004/rel/maxus/kpi/TitulosPagos'


urls = [
    'VendasBiEmpresa',
    'VendasBiOPV',
    'BalanceteBiMes',
    'VendasBiProduto',
    'TitulosPagos'
]

for url_final in urls:

    url = base_url+url_final

    tokenRetorno = pegartoken.token

    headers = {
            'Authorization': f'Bearer {tokenRetorno}',
            'xformat' : 'csv'
        }

    body = {
            # 'TipoConsulta': '', 
            # 'DataAlt': DataAlt,
            'DataIni': '2024-11-01',
            'DataFim' : DataAlt
        }

    api_response = requests.post(url, json=body, headers=headers)

    if api_response.status_code == 200:
            
            print("Solicitação bem-sucedida!")

            file = url_final +".csv"
        
            try:
                csv_data = api_response.content.decode('latin-1') 
                
                df = pd.read_csv(
                    io.StringIO(csv_data), 
                    sep=';', 
                    decimal=',',  
                    engine='python' 
                )
                print(df.head())  
                
                df.to_csv(file, sep=';', decimal=',', index=False, encoding='utf-8-sig')
                print("Dados salvos em 'dados_excel.csv' no formato adequado para Excel!")
        
            except Exception as e:
                print(f"Erro ao processar os dados CSV: {e}")
                print("Conteúdo recebido:")
                print(api_response.text[:500]) 
    else:
        print(f"Falha ao acessar a API: {api_response.status_code}")
        print("Resposta:", api_response.text)