import webbrowser
import datetime
import time
import tempfile
import os
from cryptography.fernet import Fernet
import pyautogui

chave = b'aLnLEwboui6Lfa3NWgYLk0_suDi53AAXZBFsh_o56Pg='
fernet = Fernet(chave)

with open('formulariosolicitacaopagamento-16b35458658e.json', 'rb') as f:
    conteudo_criptografado = f.read()
conteudo_descriptografado = fernet.decrypt(conteudo_criptografado)

with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.json') as temp_json:
    temp_json.write(conteudo_descriptografado)
    caminho_arquivo_temp = temp_json.name
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = caminho_arquivo_temp

import script

cabecalho = script.planilha.row_values(1)
data_atual = datetime.date.today().strftime('%d/%m/%Y')

mensagens_por_diretoria = {}

for linha in script.dados:
    if linha.get('DATA DE ENVIO AO BANCO') == data_atual:
        diretoria = linha.get('DIRETORIA')
        if diretoria not in ['DOE', 'DOB', 'DPH', 'DAF', 'SUJUR']:
            continue

        if diretoria not in mensagens_por_diretoria:
            mensagens_por_diretoria[diretoria] = []

        mensagens_por_diretoria[diretoria].append(linha)

for diretoria, linhas in mensagens_por_diretoria.items():
    if diretoria == 'DOE':
        nome = 'Conceição'
        telefone = '+558184459945'
    elif diretoria == 'DOB':
        nome = 'Conceição'
        telefone = '+558184459945'
    elif diretoria in ['DPH', 'DAF', 'SUJUR']:
        nome = 'Conceição'
        telefone = '+558184459945'
    else:
        continue

    mensagem = f'Olá, {nome} %0A'
    mensagem += f'Diretoria: {diretoria} %0A%0A'

    for linha in linhas:
        mensagem += f'----- %0A'
        mensagem += f'Remessa: {linha.get("REMESSA/OFÍCIO")} %0A'
        mensagem += f'Empresa: {linha.get("EMPRESA")} %0A'
        mensagem += f'CNPJ: {linha.get("CNPJ")} %0A'
        mensagem += f'OBS: {linha.get("OBS")} %0A%0A'
        mensagem += f'Valor: {linha.get("VALOR")} %0A'
        mensagem += f'Data de envio ao banco: {linha.get("DATA DE ENVIO AO BANCO")} %0A'
        mensagem += f'Período: {linha.get("PERÍODO")} %0A%0A'

    webbrowser.open(f'https://web.whatsapp.com/send?phone={telefone}&text={mensagem}')
    time.sleep(9)
    pyautogui.hotkey('ctrl', 'w')
