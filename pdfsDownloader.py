import requests
from requests_consts import YEAR2PARAMS
import argparse
import os

'''
Script para realizar download de PDFs com detalhamento de gastos das cotas parlamentares
'''


def maybeCreateDir(path):
    '''
    Funcao para talvez criar pasta no caminho especificado
    '''
    if not os.path.exists(path):
        os.mkdir(path)


def getVereadoresIds():
    '''
    Funcao para recuperar os ids dos vereadores ativos na camara
    '''
    from bs4 import BeautifulSoup
    import requests

    url = "https://www.cmnat.rn.gov.br/vereadores/" # url com vereadores ativos

    # extraindo HTML do URL passado
    html_content = requests.get(url).text

    # usando bs para parsing de HTML
    soup = BeautifulSoup(html_content, "lxml")

    # recuperando todos as tags <a
    links = soup.find_all("a")

    # extraindo os link com ids dos vereadores ativos
    ids = []
    for link in links:
        if "https://www.cmnat.rn.gov.br/vereadores/" in link['href']:
            ids.append(link['href'].split('/')[-1])
    return ids



# tratamento de argumentos por linha de comando
parser = argparse.ArgumentParser()
parser.add_argument("-fp", "--outputPath", required = True)
parser.add_argument("--year", required = True)
args = parser.parse_args()


outputPath = args.outputPath # caminho onde os PDFs serao salvos
params = YEAR2PARAMS[args.year] # parametros para requisicao POST para o argumento ANO passado

url = params["url"] # URL da requisicao

maybeCreateDir(outputPath) # talvez criando diretorio onde os PDFs serao salvos

vereadoresIds = getVereadoresIds() # recuperando IDs dos vereadores ativos


for month_id in params["months_ids"]: # para cada mes relacionado ao ano passado
    for vereador_id in vereadoresIds: # para cada vereador ativo

        # dicionario com argumentos do request POST
        postValues = {
            'mes_id' : month_id,
            'vereador_id' : vereador_id
        }

        r = requests.post(url, data=postValues) # realizando request POST

        # checnado se um PDF foi retornado
        if 'pdf' in r.headers['content-type']: # se sim, salva num arquivo
            print(f'[OK] {url}: {month_id} {vereador_id}')
            file = open(os.path.join(outputPath, "cota_{}_{}_{}.pdf".format(args.year, month_id, vereador_id)), "wb")
            file.write(r.content)
            file.close()
        else: # senao, emite log de erro
            print(f'[Fail] {url}: {month_id} {vereador_id}')
