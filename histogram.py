import re
import sys
import csv
import matplotlib.pyplot as plt
from math import *

class Histogram:
    
    def __init__(self):
        self.column = []
        self.argv = sys.argv
        self.data = {}
        self.res = {}
        if len(self.argv) == 3 and sys.argv[2] in ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']:
            self.classe = sys.argv[2]
        else :
            self.classe = 'Arithmancy'

    def parser(self):
        print("[Command] ./python3 histogram.py [ARG REQUIRED] file.csv [ARG OPTIONNAL] Classes")
        print("[Classes] Arithmancy, Astronomy, Herbology, Defense Against the Dark Arts, Divination, Muggle Studies, Ancient Runes, History of Magic, Transfiguration, Potions, Care of Magical Creatures, Charms, Flying")
        if len(self.argv) != 2 and len(self.argv) != 3:
            print("[Error] Need 1 or 2 args ...")
            sys.exit()
            
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
                        self.data[line[1]][headers[index]].append(ceil(value))
                        
    def makeHistogram(self):
        histogram = {}
        for house, house_data in self.data.items():
            for header, values in house_data.items():
                if self.classe == header:
                    histogram[house] = values
 
        plt.hist(histogram["Ravenclaw"], bins=20, alpha=0.5, label='Ravenclaw', color='blue')
        plt.hist(histogram["Slytherin"], bins=20, alpha=0.5, label='Slytherin', color='red')
        plt.hist(histogram["Gryffindor"], bins=20, alpha=0.5, label='Gryffindor', color='yellow')
        plt.hist(histogram["Hufflepuff"], bins=20, alpha=0.5, label='Hufflepuff', color='green')
        
        plt.xlabel("Values")
        plt.ylabel("Frequence")
        plt.legend(title="Maisons de Poudlard", title_fontsize='13', loc='upper right')
        plt.title(self.classe, fontsize=14)
        plt.show()
            

def is_digit(chaine):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, chaine))

# Main
if __name__ == "__main__":
    HIST = Histogram()
    HIST.parser()
    HIST.makeHistogram()
