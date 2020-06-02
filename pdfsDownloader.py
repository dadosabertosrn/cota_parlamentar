import requests

url = "https://www.cmnat.rn.gov.br/vereadores/verbas"
postValues = {
'vereador_id' : 13,
'mes_id': 25
}


r = requests.post(url, data=postValues)


file = open("resp_content.pdf", "wb")
file.write(r.content)
file.close()


content_type = response.headers['content-type']

if 'pdf' in content_type:
    print(f'[OK] {url}')
    f.write(response.content)
else:
    print(f'[Fail] {url}')
