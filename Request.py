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
from datetime import datetime, timedelta
load_dotenv()

now = datetime.now()
if os.getenv("DATACONSULTA") != '':
    DataAlt = os.getenv("DATACONSULTA")
else:
    DaltaAlt = now.strftime("%Y-%m-%d")

#pega data do arquivo .env e e subtrai 30 dias padrão para usar na dataini
dataConsultaAnt = DataAlt
ToDate = datetime.strptime(dataConsultaAnt, "%Y-%m-%d")
dataconsultaAntIni = ToDate - timedelta(days=30)
dataconsultaAntIniStr = dataconsultaAntIni.strftime("%Y-%m-%d") 

#pega data atual para gravar no arquivo .env quando concluir a consulta
dataconsulta = now.strftime("%Y-%m-%d")

base_url = 'https://apix.toqweb.com.br:2004/rel/maxus/kpi/'


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

    #todos os endpoints usados na consulta estão usando a mesma classeDTO para não dar erro e poder passar todos os campos previamente no body
    body = {
            'TipoConsulta' : '', 
            'Ordem' : '',
            'Detalhado' : False,
            'DataAlt' : dataConsultaAnt,
            'DataIni' : dataconsultaAntIniStr,
            'DataFim' : dataConsultaAnt,
        }

    api_response = requests.post(url, json=body, headers=headers)

    if api_response.status_code == 200:
            
            print("Solicitação bem-sucedida!")
            set_env_variable('DATACONSULTA', dataconsulta)

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
                print(f"Dados salvos em {file} no formato adequado para Excel!")
        
            except Exception as e:
                print(f"Erro ao processar os dados CSV: {e}")
                print("Conteúdo recebido:")
                print(api_response.text[:500]) 
    else:
        print(f"Falha ao acessar a API: {api_response.status_code}")
        print("Resposta:", api_response.text)

print('Consulta Finalizada!')