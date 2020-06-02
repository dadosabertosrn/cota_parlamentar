# Cota Parlamentar da Câmara Municipal de Natal/RN

![CMN](https://cmnat.rn.gov.br/assets/site/img/logo-camara-sem-slogan.png)

Projeto para abertura de dados das cotas parlamentares. Atualmente encontram-se em formato PDF por ano nos endereços abaixo:

- Ano 2020: [https://cmnat.rn.gov.br/verbas-2020](https://cmnat.rn.gov.br/verbas-2020)
- Ano 2019: [https://cmnat.rn.gov.br/verbas-2019](https://cmnat.rn.gov.br/verbas-2019)
- Ano 2018: [https://cmnat.rn.gov.br/verbas-2018](https://cmnat.rn.gov.br/verbas-2018)
- Ano 2017: [https://cmnat.rn.gov.br/verbas-2017](https://cmnat.rn.gov.br/verbas-2017)

## Features

- Python

## Getting Started

## Instalation

```bash
pip install beautifulsoup4
```

## Usage

Foram desenvolvidos 2 scripts:
### `pdfsDownloader.py`
Esse script faz o download dos PDFs relacionados às cotas do ano passado por argumento  
```bash
python pdfsDownloader.py -fp PDFS_FOLDER --year YEAR
```
`PDFS_FOLDER`: pasta em que os PDFs serão salvos  
`YEAR`: ano das cotas relacionadas aos PDFs a serem salvos. Valores aceitos: `2017` a `2020`  

### `csvBuilder.py`
Esse script gera um CSV com os detalhamentos dos gastos a partir dos PDFs salvos  
```bash
python csvBuilder.py -fp PDFS_FOLDER -op OUT
```
`PDFS_FOLDER`: pasta em que os PDFs estão salvos  
`OUT`: arquivo de saída. É sugerido adicionar `.csv` como extensão  

## Support

Caso tenha algma dúvida, sugestão ou crítica, basta abrir um issue: [https://github.com/dadosabertosrn/cota_parlamentar/issues](https://github.com/dadosabertosrn/cota_parlamentar/issues)

## Roadmap



## Contributing

Primeiramente é bom abrir um issue descrito acima, informando o que se deseja fazer, depois faça um *fork*, abra uma nova *branch* com a nova *feature* e faça o *pull request*.

## Authors and acknowledgment

| [![](https://avatars1.githubusercontent.com/u/26348952?s=300)@pauloamed](https://github.com/pauloamed) | [![](https://avatars0.githubusercontent.com/u/8619309?s=350)@georgemaia](https://github.com/georgemaia) | [![](https://avatars3.githubusercontent.com/u/13808?s=300)@fredericopranto](https://github.com/fredericopranto) | [![](https://avatars3.githubusercontent.com/u/8407904?s=300)@ja0n](https://github.com/ja0n) |
| --- | --- | --- | --- | 

## Project Status

Em desenvolvimento...

## License

## Changelog

### 0.0.1  - 01/06/2020
- Primeira implementação

