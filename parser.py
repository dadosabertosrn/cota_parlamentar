from tika import parser
from dateutil.parser import parse as date_parse

def isDate(token):
    try:
        day, month, year = token.split('/')
        day = int(day)
        year = int(year)
        return True
    except:
        return False


def getLineClass(line):
    if len(line) == 0:
        return "none"

    hasVereador = "Vereador(a):" in line
    hasRSOnPos = len(line) > 1 and line[-2] == "R$"
    firstIsDate = isDate(line[0])

    if hasVereador and hasRSOnPos:
        return "total"
    if hasVereador and not hasRSOnPos:
        return "title"
    if hasRSOnPos and firstIsDate:
        return "detail"
    if hasRSOnPos and not firstIsDate:
        return "section"

    return "none"



def getInfoFromTitle(title):
    info = dict()

    name = []
    nameStart = False
    for i in range(len(title)):
        if nameStart:
            name.append(title[i])
        elif title[i] == 'Vereador(a):':
            nameStart = True

    info["nameVereador"] = " ".join(name)
    info["dateDocument"] = title[0]

    return info


def getInfoFromSection(section):
    # last two are "R$" and "float"
    info = dict()
    info["desc"] = " ".join(section[:-2])
    info["val"] = float(section[-1])

    return info


def getInfoFromDetail(detail):
    info = dict()

    info["date"] = detail[0]
    info["cupomNumbr"] = detail[1]
    info["cpfCnpj"] = detail[2]
    info["fundament"] = detail[3]
    info["desc"] = " ".join(detail[4:-2])
    info["val"] = detail[-1]

    return info





raw = parser.from_file('file')
lines = raw['content'].split('\n')

info = dict()
for line in lines:
    # qual a classe da linha?
    line = line.split(' ')
    line = [x for x in line if len(x) > 0]

    group = getLineClass(line)
    if group == "title":
        info.update(getInfoFromTitle(line))

    if group == "none": continue

    print(group)
    if group == "title":
        print(getInfoFromTitle(line))
    elif group == "section":
        print(getInfoFromSection(line))
    elif group == "detail":
        print(getInfoFromDetail(line))
