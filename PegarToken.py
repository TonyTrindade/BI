import os
import requests
from dotenv import load_dotenv
class pegartoken :
    load_dotenv()

    cnpj = os.getenv("CNPJ")

    token_url = (f'https://api.toqweb.com.br:2004/auth/LoginService/LoginCnpj?Cnpj={cnpj}&sKey=ybHF9drnd%26FK%26UA$t*XSDu%23mfehqfg')

    token_response = requests.get(token_url)

    if token_response.ok:
        token = token_response.json().get("Authorization")
        print("Token obtido:", token)
    else:
        print("Erro ao obter o token:", token_response.status_code, token_response.text)
        exit()


