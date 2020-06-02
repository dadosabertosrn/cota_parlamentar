from tika import parser
from dateutil.parser import parser as date_parser
from PortugueseParserInfo import PortugueseParserInfo




class DocumentParser():

    def __init__(self):
        self.portDateParser = date_parser(info = PortugueseParserInfo())


    def isDate(self, token):
        try:
            day, month, year = token.split('/')
            day = int(day)
            year = int(year)
            return True
        except:
            return False


    def getLineClassification(self, line):
        if len(line) == 0:
            return "none"

        hasVereador = "Vereador(a):" in line
        hasRSOnPos = len(line) > 1 and line[-2] == "R$"
        firstIsDate = self.isDate(line[0])

        if hasVereador and hasRSOnPos:
            return "total"
        if hasVereador and not hasRSOnPos:
            return "title"
        if hasRSOnPos and firstIsDate:
            return "detail"
        if hasRSOnPos and not firstIsDate:
            return "issue"

        return "none"


    def getInfoFromTitle(self, line):
        info = dict()

        name = []
        nameStart = False
        for i in range(len(line)):
            if nameStart:
                name.append(line[i])
            elif line[i] == 'Vereador(a):':
                nameStart = True

        info["nameVereador"] = " ".join(name)
        info["yearDocument"] = line[0].split('/')[1]
        info["monthDocument"] = line[0].split('/')[0]

        return info


    def getInfoFromIssue(self, line):
        # last two are "R$" and "float"
        info = dict()
        info["issueDesc"] = " ".join(line[:-2])
        info["issueCost"] = float(line[-1])

        return info


    def getInfoFromDetail(self, line):
        info = dict()

        info["date"] = self.portDateParser.parse(line[0])
        info["cupomNumbr"] = int(line[1])
        info["cpfCnpj"] = line[2]
        info["fundament"] = line[3]
        info["desc"] = " ".join(line[4:-2])
        info["detailCost"] = float(line[-1])

        return info


    def parse(self, filePath):
        raw = parser.from_file(filePath)
        lines = raw['content'].split('\n')

        info = {
            "issues": []
        }

        currentDetails = []
        for line in lines:
            # qual a classe da linha?
            line = line.split(' ')
            line = [x for x in line if len(x) > 0]

            group = self.getLineClassification(line)
            if group == "title":
                info.update(self.getInfoFromTitle(line))
            elif group == "issue":
                info["issues"].append(self.getInfoFromIssue(line))
            elif group == "detail":
                if "details" not in info["issues"][-1]:
                    info["issues"][-1]["details"] = []

                info["issues"][-1]["details"].append(
                    self.getInfoFromDetail(line)
                )

        return info
