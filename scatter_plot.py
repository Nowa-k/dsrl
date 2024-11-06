import re
import sys
import csv
import os.path
import LowMathLib
import matplotlib.pyplot as plt
from math import *

class Scatter_plot:
    def __init__(self):
        self.argv = sys.argv
        self.column = []
        self.feature1 = 0
        self.feature2 = 0
        self.data = {}
        self.rawdata = {}
        self.res = {}
        self.header = []
        
    def parser(self):
        if len(self.argv) < 2 or len(self.argv) > 2:
            print("[Command] ./python3 scatter_plot.py [ARG REQUIRED] file.csv")
            sys.exit()
        elif len(self.argv) == 2:
            if os.path.exists(self.argv[1]):
                if os.access(self.argv[1], os.R_OK):   
                    with open(self.argv[1], 'r') as file:
                        csvreader = csv.reader(file)
                        headers = next(csvreader)

                        self.rawdata['Ravenclaw'] = {}
                        self.rawdata['Slytherin'] = {}
                        self.rawdata['Gryffindor'] = {}
                        self.rawdata['Hufflepuff'] = {}
                        
                        for house in self.rawdata:
                            for header in headers:
                                self.data[header] = []
                                self.rawdata[house][header] = []

                        for line in csvreader:
                            for index, value in enumerate(line):
                                if is_digit(value):
                                    value = float(value)
                                    self.data[headers[index]].append(value)
                                    if line[1] in ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']:
                                        self.rawdata[line[1]][headers[index]].append(value)
                                elif not value:
                                    self.data[headers[index]].append(float("nan"))
                                    if line[1] in ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']:
                                        self.rawdata[line[1]][headers[index]].append(float("nan"))
                else:
                    print("[Error] Vous ne disposez pas des permissions nécessairess pour lire ce fichier.")
                    sys.exit()
            else:
                print("[Error] Le fichier est introuvable. Etes-vous sûrs du chemin d'accès?")
                sys.exit()

    def find_similar_features(self):
        max_corr = 0
        features = []
        similar_pair = (None, None)
        lib = LowMathLib.LowMathLib()
        
        for feature in self.data.keys():
            if feature not in ['Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                features.append(feature)
        for i in range(len(features)):
            for j in range(len(features)):
                if (i != j):
                    corr = abs(lib.calculate_correlation(self.data[features[i]], self.data[features[j]]))
                    if corr > max_corr:
                        max_corr = corr
                        similar_pair = (features[i], features[j])
        self.feature1 = similar_pair[0]
        self.feature2 = similar_pair[1]

    def makeScatter(self):
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(1,1,1)
        houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
        colors = ['orange', 'green','blue','red']
        for house, color in zip(houses, colors):
            ax.scatter(self.rawdata[house][self.feature1], self.rawdata[house][self.feature2], color=color)
        plt.title(f'Scatter plot of {self.feature1} vs {self.feature2}')
        plt.xlabel(self.feature1)
        plt.ylabel(self.feature2)
        plt.grid(True)
        plt.show()

def is_digit(chaine):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, chaine))

if __name__ == "__main__":
    SCAT = Scatter_plot()
    SCAT.parser()
    SCAT.find_similar_features()
    SCAT.makeScatter()