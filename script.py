from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread
import os

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
