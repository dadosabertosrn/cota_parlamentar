import argparse
import os
import re

from DocumentParser import DocumentParser


# tratando argumetnos passados por linha de comando
parser = argparse.ArgumentParser()
parser.add_argument("-fp", "--folderPath", required = True)
parser.add_argument("-op", "--outputPath", required = True)
args = parser.parse_args()

documentsFolder = args.folderPath
outputPath = args.outputPath

# init do nosso parser
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
    # escrita de cabecalho
    csvOuput.write("cnpj_cpf;congressperson_name;document_number;document_type;document_value;issue_date;month;state;subquota_description;supplier;total_net_value;year\n")

    # para cada arquivo na pasta passada por parametro
    for documentPath in os.listdir(documentsFolder):
        # extrai o ano e o mês do nome do arquivo
        # Motivo: os pdf's de 2018 não contém o mês/ano na seção "title"
        yearfile = os.path.basename(documentPath) # nome do arquivo
        yearfile = yearfile[5:9] # 4 dígitos referentes ao ano
        monthfile = os.path.basename(documentPath)
        monthfile = monthfile[10:12] # 2 dígitos referentes ao mês
        # o nome do arquivo em 2018 é mal formatado: o mês 13 equivale a janeiro, 
        # o mês 14, fevereiro e assim por diante. Há um 13º mês com pagamentos feitos 
        # em 2019; por isso, no arquivo aparecem 13 meses
        # além disso, 2019 só inclui um dígito para os meses abaixo de 2010 (setembro é 9, não 09)
        # por isso, incluo a restrição yearfile == 2018. 
        if (yearfile == "2018"):
            if (int(monthfile) > 12): 
                monthfile = int(monthfile) - 12
        if (yearfile == "2019"):
            monthfile = re.sub("\_", "", monthfile)
                

        # recupera path completo do arquivo
        documentPath = os.path.join(documentsFolder, documentPath)

        # log para indicar qual arquivo esta sendo processado
        print(">> File being processed: " + documentPath)

        # extraindo informacoes de parsing
        parsedInfo = dp.parse(documentPath)

        # para cada detalhamento de cada issue, imprimo uma linha no CSV
        if "issues" not in parsedInfo: continue
        for issue in parsedInfo["issues"]:
            if "details" not in issue: continue
            for detail in issue["details"]:
                line = [
                    detail["cpfCnpj"],
                    parsedInfo["nameVereador"],
                    detail["reciptId"],
                    0,
                    detail["detailCost"],
                    detail["dateDatetime"].strftime("%d/%m/%y") if "dateDatetime" in detail else detail["dateStr"],
                    #parsedInfo["monthDocument"], # sugestao: pegar do nome do arquivo
                    monthfile,
                    "RN",
                    issue["issueDesc"],
                    detail["desc"],
                    issue["issueCost"],
                    #issue["issueCost"], # estava duplicado
                    #parsedInfo["yearDocument"], # sugestao: pegar do nome do arquivo
                    yearfile,
                ]

                line = ";".join([str(x) for x in line])
                csvOuput.write(line + "\n")
