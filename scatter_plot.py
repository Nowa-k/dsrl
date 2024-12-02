import re
import sys
import csv
import matplotlib.pyplot as plt
from math import *

class Scatter_plot:
    def __init__(self):
        self.column = []
        self.x_feature = 0
        self.y_feature = 0
        self.data = {}
        self.res = {}
        self.header = []
        
    def setArg(self):
        try :
            self.x_feature = self.header.index(sys.argv[1])
            self.y_feature = self.header.index(sys.argv[2])
        except ValueError:
            print("This classe doesn't exist")
            sys.exit()
           
    def parser(self):
        print("[Command] ./python3 scatter_plot.py [ARG REQUIRED] Classes Classes")
        print("[Classes] Arithmancy, Astronomy, Herbology, Defense Against the Dark Arts, Divination, Muggle Studies, Ancient Runes, History of Magic, Transfiguration, Potions, Care of Magical Creatures, Charms, Flying")
        if len(sys.argv) != 3:
            print("[Error] You need 2 args")
            sys.exit()
            
        with open('datasets/dataset_test.csv', 'r') as file:
            csvreader = csv.reader(file)
            headers = next(csvreader)
            
            for header in headers:
                self.header.append(header)
                self.data[header] = []
            
            self.setArg()
            for line in csvreader:
                if line[self.x_feature] and is_digit(line[self.x_feature]) and line[self.y_feature] and is_digit(line[self.y_feature]):
                    self.data[headers[self.x_feature]].append(float(line[self.x_feature]))
                    self.data[headers[self.y_feature]].append(float(line[self.y_feature]))
        
    def makeScatter(self):
        plt.scatter(self.data[self.header[self.x_feature]], self.data[self.header[self.y_feature]])

        plt.title(f"Relation entre {self.header[self.x_feature]} et {self.header[self.y_feature]}")
        plt.xlabel(self.header[self.x_feature])
        plt.ylabel(self.header[self.y_feature])

        plt.show()
        
def is_digit(chaine):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, chaine))

if __name__ == "__main__":
    SCAT = Scatter_plot()
    SCAT.parser()
    SCAT.makeScatter()