import webbrowser
import datetime
import time
import tempfile
import os
from cryptography.fernet import Fernet

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

for i, linha in enumerate(script.dados, start=2):
    if linha.get('DATA DE ENVIO AO BANCO') == data_atual:
        if linha.get('DIRETORIA') == 'DOE':
            nome = 'Conceição'
            telefone = '+5581991492389'
        elif linha.get('DIRETORIA') == 'DOB':
            nome = 'Conceição'
            telefone = '+5581998772704'
        elif linha.get('DIRETORIA') == 'DPH':
            nome = ''
            telefone = '+'
        elif linha.get('DIRETORIA') == 'DAF':
            nome = ''
            telefone = '+'
        elif linha.get('DIRETORIA') == 'SUJUR':
            nome = ''
            telefone = '+'
        else:
            continue

        webbrowser.open(f'https://web.whatsapp.com/send?phone={telefone}&text=Olá {nome}, esta é uma mensagem automática :)')
        time.sleep(7)
