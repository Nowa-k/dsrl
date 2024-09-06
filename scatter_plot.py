import re
import sys
import csv
import matplotlib.pyplot as plt
from math import *

class Scatter_plot:
    def __init__(self):
        self.column = []
        self.argv = sys.argv
        self.data = {}
        self.res = {}
        
    def parser(self):
        print("[Command] ./python3 scatter_plot.py [ARG REQUIRED] file.csv")
        if len(self.argv) != 2:
            print("[Error] Need 1 or 2 args ...")
            sys.exit()
            
        with open('datasets/dataset_short.csv', 'r') as file:
            csvreader = csv.reader(file)
            headers = next(csvreader)
            for header in headers:
                self.data[header] = []
            
            for line in csvreader:
                for index, value in enumerate(line):
                    if is_digit(value):
                        self.data[headers[index]].append(ceil(float(value)))
        
    def makeScatter(self):
        x_feature = 'Astronomy'
        y_feature = 'Flying'
        min_length = min(len(self.data[x_feature]), len(self.data[y_feature]))

        plt.scatter(self.data[x_feature][:min_length], self.data[y_feature][:min_length])

        plt.title(f"Relation entre {x_feature} et {y_feature}")
        plt.xlabel(x_feature)
        plt.ylabel(y_feature)

        plt.show()
        
def is_digit(chaine):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, chaine))

if __name__ == "__main__":
    SCAT = Scatter_plot()
    SCAT.parser()
    SCAT.makeScatter()