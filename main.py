import webbrowser
import datetime
import time
import tempfile
import os
from cryptography.fernet import Fernet
import pyautogui
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread
import os

chave = b'aLnLEwboui6Lfa3NWgYLk0_suDi53AAXZBFsh_o56Pg='
fernet = Fernet(chave)

with open('formulariosolicitacaopagamento-16b35458658e.json', 'rb') as f:
    conteudo_criptografado = f.read()
conteudo_descriptografado = fernet.decrypt(conteudo_criptografado)

with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.json') as temp_json:
    temp_json.write(conteudo_descriptografado)
    caminho_arquivo_temp = temp_json.name
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = caminho_arquivo_temp


file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    filename=file,
    scopes=scopes
)
client = gspread.authorize(creds)
print(client)

planilha_completa = client.open_by_key('1MQbo9Q55HyRGgJsYrhm5t5mjd3idmHe0zUdvhgYSFYU')
planilha = planilha_completa.get_worksheet(0)
dados = planilha.get_all_records()


cabecalho = planilha.row_values(1)
data_atual = datetime.date.today().strftime('%d/%m/%Y')

mensagens_por_diretoria = {}

for linha in dados:
    if linha.get('DATA DE ENVIO AO BANCO') == '14/04/2025':
        diretoria = linha.get('DIRETORIA')
        if diretoria not in mensagens_por_diretoria:
            mensagens_por_diretoria[diretoria] = []
        mensagens_por_diretoria[diretoria].append(linha)


for diretoria, linhas in mensagens_por_diretoria.items():
    if diretoria == 'DOE':
        telefone = '+558194994938'

    elif diretoria == 'DOHDU':
        telefone = '+558199004886'

    elif diretoria == 'DPH':
        telefone = '+558188458189'

    elif diretoria == 'SUJUR':
        telefone = '+553499610569'
    else:
        continue

    mensagem = f'Diretoria: {diretoria} %0A%0A'

    for linha in linhas:
        mensagem += f'----- %0A'
        mensagem += f'Remessa: {linha.get("REMESSA/ OFÍCIO")} %0A'
        mensagem += f'Empresa: {linha.get("EMPRESA")} %0A'
        mensagem += f'CNPJ: {linha.get("CNPJ")} %0A'
        mensagem += f'OBS: {linha.get("OBS")} %0A%0A'
        mensagem += f'Valor: {linha.get("VALOR")} %0A'
        mensagem += f'Data de envio ao banco: {linha.get("DATA DE ENVIO AO BANCO")} %0A'
        mensagem += f'Período: {linha.get("PERÍODO")} %0A%0A'
        
        webbrowser.open(f'https://web.whatsapp.com/send?phone={telefone}&text={mensagem}')
        time.sleep(6)
        pyautogui.hotkey('ctrl', 'w')
