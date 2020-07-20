from tika import parser
from dateutil.parser import parser as date_parser
from PortugueseParserInfo import PortugueseParserInfo




class DocumentParser():

    def __init__(self):
        self.portDateParser = date_parser(info = PortugueseParserInfo())


    def isDate(self, token):
        '''
        Funcao que retorna se token passado representa uma data
        '''
        try:
            day, month, year = token.split('/')
            day = int(day)
            year = int(year)
            return True
        except:
            return False


    def isMonthYear(self, token):
        '''
        Funcao que retorna se token passado esta no formato Mes/Ano
        '''
        try:
            month, year = token.split('/')
            year = int(year)
            return month in ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        except:
            return False


    def getLineClassification(self, line):
        '''
        Funcao para indicar classe da linha passada
        As classes sao:
            - title: titulo do documento
            - issue: declaracao do gasto
            - detail: detalhamento do gasto
            - total: total do que foi gasto
            - none: nao tem classe, nao tem importancia
        '''
        if len(line) == 0:
            return "none"

        hasVereador = "Vereador(a):" in line # checa se a string "Vereador(a):" esta presente na lihnha
        hasMonthYear = self.isMonthYear(line[0]) # checa se o primeiro token da linha esta no formato Mes/Ano
        hasRSOnPos = len(line) > 1 and line[-2] == "R$" # checa se tem um cifrao no penultimo token da linha
        firstIsDate = self.isDate(line[0]) # checa se o primeiro token da linha eh uma data

        # atribui a classe de acordo com o que foi extraido sobre a linha
        if hasVereador and hasRSOnPos:
            return "total"
        #if hasVereador and not hasRSOnPos and hasMonthYear:
        if hasVereador and not hasRSOnPos:
            return "title"
        if hasRSOnPos and firstIsDate:
            return "detail"
        if hasRSOnPos and not firstIsDate and not hasVereador:
            return "issue"

        return "none"


    def getInfoFromTitle(self, line):
        '''
        Funcao para extrair informacao de class "title"
        '''
        info = dict()

        name = []
        nameStart = False
        for i in range(len(line)):
            if nameStart:
                name.append(line[i])
            elif line[i] == 'Vereador(a):':
                nameStart = True

        info["nameVereador"] = " ".join(name)
        #info["yearDocument"] = line[0].split('/')[1]
        #info["monthDocument"] = line[0].split('/')[0]
        # aqui, 2018 e 12 são números arbitrários
        # não sei se remover esses dois atributos quebra alguma coisa no código
        # não estão sendo imprimidos no csv
        info["yearDocument"] = 2018 # a sugestao é não usar isso e pegar do nome do arquivo
        info["monthDocument"] = 12 # a sugestao é não usar isso e pegar do nome do arquivo

        return info


    def getInfoFromIssue(self, line):
        '''
        Funcao para extrair informacao de class "issue"
        '''
        # last two are "R$" and "float"
        info = dict()
        info["issueDesc"] = " ".join(line[:-2])
        info["issueCost"] = float(line[-1])

        return info


    def getInfoFromDetail(self, line):
        '''
        Funcao para extrair informacao de class "detail"
        '''
        info = dict()

        try:
            info["dateDatetime"] = self.portDateParser.parse(line[0])
        except:
            info["dateStr"] = line[0]

        info["reciptId"] = line[1]
        info["cpfCnpj"] = line[2]
        info["fundament"] = line[3]
        info["desc"] = " ".join(line[4:-2])
        info["detailCost"] = float(line[-1])

        return info


    def parse(self, filePath):

        # usnado o tika para extrair o texto do arquivo PDF passado
        raw = parser.from_file(filePath)
        lines = raw['content'].split('\n')

        # inicializando o dicionario que ira armazenar os dados extraidos
        info = {
            "issues": []
        }


        for line in lines: # para cada linha do PDF

            # separa a string usando split por ' '
            line = line.split(' ')
            # corta as linhas vazias
            line = [x for x in line if len(x) > 0]

            # recupera a classe da linha
            group = self.getLineClassification(line)

            # se for um titulo ou issue, extrai info da linha
            if group == "title": info.update(self.getInfoFromTitle(line))
            elif group == "issue": info["issues"].append(self.getInfoFromIssue(line))
            elif group == "detail": # se for um detalhamento, adiciona a lista de detalhamentos da issue corrente
                if "details" not in info["issues"][-1]:
                    info["issues"][-1]["details"] = []

                info["issues"][-1]["details"].append(
                    self.getInfoFromDetail(line)
                )

        return info
