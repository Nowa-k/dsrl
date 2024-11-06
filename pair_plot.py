import re
import sys
import csv
import os.path
import LowMathLib
import matplotlib.pyplot as plt
from math import *

class Pair_plot:
    def __init__(self):
        self.argv = sys.argv
        self.column = []
        self.x_feature = 0
        self.y_feature = 0
        self.data = {}
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
                        
                        self.data['Ravenclaw'] = {}
                        self.data['Slytherin'] = {}
                        self.data['Gryffindor'] = {}
                        self.data['Hufflepuff'] = {}
                        
                        for house in self.data :
                            for header in headers:
                                self.data[house][header] = []

                        for line in csvreader:
                            for index, value in enumerate(line):
                                if is_digit(value) and line[1] in ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']:
                                    value = float(value)
                                    self.data[line[1]][headers[index]].append(value)
                                elif not value and line[1] in ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']:
                                    self.data[line[1]][headers[index]].append(float("nan"))
                else:
                    print("[Error] Vous ne disposez pas des permissions nécessairess pour lire ce fichier.")
                    sys.exit()
            else:
                print("[Error] Le fichier est introuvable. Etes-vous sûrs du chemin d'accès?")
                sys.exit()

    def makeScatterMatrix(self):
        size = 0
        for house, house_data in self.data.items():
            for header, values in house_data.items():
                if header not in ['Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                    size += 1
            break
        i = 1
        plt.style.use('classic')
        fig = plt.figure(figsize=(24,13))
        for house, house_data in self.data.items():
            for header_axis, values_axis in house_data.items():
                if header_axis not in ['Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                    for header_ordo, values_ordo in house_data.items():
                        if header_ordo not in ['Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                            ax = fig.add_subplot(size, size, i)
                            if (i <= size):
                                ax.set_title(header_ordo[0:9])
                            if (i % size == 1):
                                ax.set_ylabel(header_axis[0:7])
                            ax.set_yticklabels([])
                            ax.set_xticklabels([])
                            fill_scatter_plot(ax, self.data, header_axis, header_ordo)
                            i += 1
            break
        plt.show()

def fill_scatter_plot(ax, data, class_1, class_2):
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    colors = ['orange', 'green','blue','red']
    for house, color in zip(houses, colors):
        ax.scatter(data[house][class_1], data[house][class_2], color=color)

def is_digit(chaine):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, chaine))

if __name__ == "__main__":
    PAIR = Pair_plot()
    PAIR.parser()
    PAIR.makeScatterMatrix()