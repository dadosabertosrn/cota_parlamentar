import requests
from requests_consts import YEAR2PARAMS
import argparse
import os

def maybeCreateDir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def getVereadoresIds():
    from bs4 import BeautifulSoup
    import requests

    url = "https://www.cmnat.rn.gov.br/vereadores/"

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    ids = []
    soup = BeautifulSoup(html_content, "lxml")
    links = soup.find_all("a")
    for link in links:
        if "https://www.cmnat.rn.gov.br/vereadores/" in link['href']:
            ids.append(link['href'].split('/')[-1])
    return ids



parser = argparse.ArgumentParser()
parser.add_argument("-fp", "--outputPath", required = True)
parser.add_argument("--year", required = True)
args = parser.parse_args()


params = YEAR2PARAMS[args.year]
url = params["url"]

outputPath = args.outputPath
maybeCreateDir(outputPath)

vereadoresIds = getVereadoresIds()


for month_id in params["months_ids"]:
    for vereador_id in vereadoresIds:
        postValues = {
            'mes_id' : month_id,
            'vereador_id' : vereador_id
        }

        # print(postValues)

        r = requests.post(url, data=postValues)

        content_type = r.headers['content-type']

        # print(r.content)

        if 'pdf' in content_type:
            print(f'[OK] {url}: {month_id} {vereador_id}')
            file = open(os.path.join(outputPath, "cota_{}_{}_{}.pdf".format(args.year, month_id, vereador_id)), "wb")
            file.write(r.content)
            file.close()
        else:
            print(f'[Fail] {url}: {month_id} {vereador_id}')
