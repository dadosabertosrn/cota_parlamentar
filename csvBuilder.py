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

with open(outputPath, "w") as csvOuput:
    for documentPath in os.listdir(documentsFolder):
        documentPath = os.path.join(documentsFolder, documentPath)

        print(dp.parse(documentPath))
