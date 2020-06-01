from dateutil.parser import parserinfo


class PortugueseParserInfo(parserinfo):

    def __init__(self):
        super().__init__()

    MONTHS = [("Jan", "Janeiro"),
          ("Feb", "Fevereiro"),      # TODO: "Febr"
          ("Mar", "Março"),
          ("Apr", "Abril"),
          ("May", "Maio"),
          ("Jun", "Junho"),
          ("Jul", "Julho"),
          ("Aug", "Agosto"),
          ("Sep", "Sept", "Setembro"),
          ("Oct", "Outubro"),
          ("Nov", "Novembro"),
          ("Dec", "Dezembro")]
