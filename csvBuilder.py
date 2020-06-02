import argparse
import os

from DocumentParser import DocumentParser

parser = argparse.ArgumentParser()
parser.add_argument("-fp", "--folderPath", required = True)
parser.add_argument("-op", "--outputPath", required = True)
args = parser.parse_args()

documentsFolder = args.folderPath
outputPath = args.outputPath

dp = DocumentParser()

"""
cnpj_cpf: O conteúdo deste dado representa o CNPJ ou o CPF do emitente do documento fiscal, quando se tratar do uso da cota em razão do reembolso despesas comprovadas pela emissão de documentos fiscais.
congressperson_name: Nome adotado pelo Parlamentar ao tomar posse do seu mandato. Compõe-se de dois elementos: um prenome e o nome; dois nomes; ou dois prenomes, salvo, a juízo do Presidente da Casa legislativa, que poderá alterar essa regra para que não ocorram confusões.
document_number: numero do documento (num da nota fiscal)
document_type: 0 (Zero), para Nota Fiscal; 1 (um), para Recibo; e 2, para Despesa no Exterior.
document_value: valor na nota
issue_date: data de emissao
month: mes
state: estado
subquota_description: descricao
supplier: contratado
total_net_value: valor liquido
year: ano

"""

with open(outputPath, "w") as csvOuput:
    csvOuput.write("cnpj_cpf;congressperson_name;document_number;document_type;document_value;issue_date;month;state;subquota_description;supplier;total_net_value;year\n")

    for documentPath in os.listdir(documentsFolder):
        documentPath = os.path.join(documentsFolder, documentPath)

        parsedInfo = dp.parse(documentPath)

        for issue in parsedInfo["issues"]:
            for detail in issue["details"]:
                line = [
                    detail["cpfCnpj"],
                    parsedInfo["nameVereador"],
                    detail["cupomNumbr"],
                    0,
                    detail["detailCost"],
                    detail["date"].strftime("%d/%m/%y"),
                    parsedInfo["monthDocument"],
                    "RN",
                    issue["issueDesc"],
                    detail["desc"],
                    issue["issueCost"],
                    issue["issueCost"],
                    parsedInfo["yearDocument"],
                ]

                line = ";".join([str(x) for x in line])
                csvOuput.write(line + "\n")
