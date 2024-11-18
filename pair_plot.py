import re
import sys
import csv
import os.path
import LowMathLib
import matplotlib.pyplot as plt
from math import *

class Pair_plot:
    def __init__(self):
        self.res = {}
        self.data = {}
        self.column = []
        self.header = []
        self.x_feature = 0
        self.y_feature = 0
        self.argv = sys.argv
    
    # Parse data
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

    # Calculate all the similarities for each classes
    def makeScatterMatrix(self):
        size = 0
        for house, house_data in self.data.items():
            for header, values in house_data.items():
                if header not in ['Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                    size += 1
            break
        i = 1
        plt.style.use('classic')
        fig = plt.figure(figsize=(45,30))
        for house, house_data in self.data.items():
            axis = 0
            for header_axis, values_axis in house_data.items():
                if header_axis not in ['Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                    ordo = 0
                    for header_ordo, values_ordo in house_data.items():
                        if header_ordo not in ['Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                            ax = fig.add_subplot(size, size, i)
                            if axis == ordo:
                                ax.set_title(header_ordo, fontsize=20)
                            if ordo > axis:
                                ax.set_visible(False)
                            if (i % size == 1):
                                ax.set_ylabel(header_axis[0:9], fontsize=20)
                            ax.set_yticklabels([])
                            ax.set_xticklabels([])
                            if header_axis != header_ordo:
                                fill_scatter_plot(ax, self.data, header_axis, header_ordo)
                            else:
                                fill_histogram(ax, self.data, header_axis)
                            i += 1
                            ordo += 1
                    axis += 1
            break
        plt.show()

# Draw the Histograms
def fill_histogram(ax, data, classe):
    histogram = []
    for house, house_data in data.items():
        house_value = []
        for header, values in house_data.items():
            if classe == header:
                histogram.append(values)

    ax.hist(histogram, stacked=True, color=['orange', 'green','blue','red'])

# Draw the scatters
def fill_scatter_plot(ax, data, class_1, class_2):
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    colors = ['orange', 'green','blue','red']
    for house, color in zip(houses, colors):
        ax.scatter(data[house][class_1], data[house][class_2], s=4, color=color)

def is_digit(chaine):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, chaine))

# Main
if __name__ == "__main__":
    PAIR = Pair_plot()
    PAIR.parser()
    PAIR.makeScatterMatrix()