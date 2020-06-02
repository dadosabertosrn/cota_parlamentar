import requests
from requests_consts import YEAR2PARAMS
import argparse
import os

def maybeCreateDir(path):
    if not os.path.exists(path):
        os.mkdir(path)


parser = argparse.ArgumentParser()
parser.add_argument("-fp", "--outputPath", required = True)
parser.add_argument("--year", required = True)
args = parser.parse_args()

params = YEAR2PARAMS[args.year]
url = params["url"]

outputPath = args.outputPath
maybeCreateDir(outputPath)


for month_id in params["months_ids"]:
    for i in range(1, 100):
        postValues = {
            'mes_id' : month_id,
            'vereador_id' : str(i)
        }

        # print(postValues)

        r = requests.post(url, data=postValues)

        content_type = r.headers['content-type']

        # print(r.content)

        if 'pdf' in content_type:
            print(f'[OK] {url}: {month_id} {str(i)}')
            file = open(os.path.join(outputPath, "cota_{}_{}_{}.pdf".format(args.year, month_id, i)), "wb")
            file.write(r.content)
            file.close()
        else:
            print(f'[Fail] {url}: {month_id} {str(i)}')
