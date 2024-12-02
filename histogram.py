import re
import sys
import csv
import os.path
import LowMathLib
import matplotlib.pyplot as plt
from math import *

class Histogram:
    
    def __init__(self):
        self.res = {}
        self.data = {}
        self.column = []
        self.classe = ""
        self.argv = sys.argv

    # Parse data
    def parser(self):
        if len(self.argv) < 2 or len(self.argv) > 2:
            print("[Command] ./python3 histogram.py [ARG REQUIRED] file.csv")
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
                        
                        # Add the data for each house and each classe
                        for line in csvreader:
                            for index, value in enumerate(line):
                                if is_digit(value) and line[1] in ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']:
                                    value = float(value)
                                    self.data[line[1]][headers[index]].append(value)
                else:
                    print("[Error] Vous ne disposez pas des permissions nécessairess pour lire ce fichier.")
                    sys.exit()
            else:
                print("[Error] Le fichier est introuvable. Etes-vous sûrs du chemin d'accès?")
                sys.exit()

    # Draw the Histogram                    
    def makeHistogram(self):
        self.classe = get_classe(self.data)
        histogram = []
        for house, house_data in self.data.items():
            house_value = []
            for header, values in house_data.items():
                if self.classe == header:
                    histogram.append(values)

        plt.title(self.classe, fontsize=14)
        plt.hist(histogram, stacked=True, color=['orange', 'green','blue','red'])
        plt.xlabel("Notes")
        plt.ylabel("Nombres d'élèves")
        plt.show()

# Get the class with a homogeneous score
def get_classe(data):
    lib = LowMathLib.LowMathLib()
    min_ = lib.ft_std_dev(data['Ravenclaw']['Index'])
    for key, value in data.items():
        for key_value, value_value in value.items():
            if key_value not in ['Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand']:
                try:
                    tmp = lib.ft_std_dev(value_value)
                    if min_ > tmp:
                        min_ = tmp
                        feature = key_value
                except:
                    continue
    return feature            

def is_digit(chaine):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, chaine))

# Main
if __name__ == "__main__":
    HIST = Histogram()
    HIST.parser()
    HIST.makeHistogram()
