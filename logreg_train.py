import re
import sys
import csv
import json
import os.path
import LowMathLib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Train:
    def __init__(self):
        self.data = {}
        self.weights = {}
        self.argv = sys.argv
        self.lib = LowMathLib.LowMathLib()
        self.classes = ["Astronomy", "Herbology", "Defense Against the Dark Arts", "Ancient Runes", "Charms"]

    # Parse arguments
    def parser(self):
        if len(self.argv) < 2 or len(self.argv) > 2:
            print("[Command] ./python3 logreg_predict.py [ARG REQUIRED] [PATH TO]/dataset_train.csv")
            sys.exit()
        elif len(self.argv) == 2:
            if os.path.basename(self.argv[1]) == "dataset_train.csv":
                if os.path.exists(self.argv[1]):
                    if os.access(self.argv[1], os.R_OK):
                        self.data = pd.read_csv(self.argv[1])
                        for classe in self.classes:
                            parsed_data = []
                            for i in range(len(self.data[classe])):
                                if str(self.data[classe][i]) != "nan":
                                    parsed_data.append(self.data[classe][i])
                            for i in range(len(self.data[classe])):
                                if str(self.data[classe][i]) == "nan":
                                    self.data.loc[i, classe] = self.lib.ft_mean(parsed_data)
                    else:
                        print("[Error] Vous ne disposez pas des permissions nécessairess pour lire ce fichier.")
                        sys.exit()
                else:
                    print("[Error] Le fichier est introuvable. Etes-vous sûrs du chemin d'accès?")
                    sys.exit()
            else:
                print("[Error] Le nom du fichier doit être: 'dataset_train.csv'")
                sys.exit()

    #Calc the precision of the algorythm
    def calc_precision(self):
        predictions = []
        precisionData = []
        total = 0
        X = self.data[self.classes].to_numpy()
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        lib = LowMathLib.LowMathLib()
        with open("weights.json", "r") as f:
            weights = json.load(f)
        with open("datasets/dataset_train.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] in ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']:
                    precisionData.append(row[1])
        for i in range(X.shape[0]):
            probs = {cls: lib.sigmoid(np.dot(X[i], np.array(weights))) for cls, weights in weights.items()}
            predictions.append(max(probs, key=probs.get))
        for i in range(len(predictions)):
            if predictions[i] == precisionData[i]:
                total += 1
        print((total / len(predictions)) * 100)

    # Normalize informations to be between 0 and 1
    def normalization(self):
        lib = LowMathLib.LowMathLib()
        for classe in self.classes:
            min_val = self.lib.ft_min(self.data[classe])
            max_val = self.lib.ft_max(self.data[classe])
            self.data[classe] = (self.data[classe] - min_val) / (max_val - min_val)

    # Train the AI with gradiant descent function
    def train(self):
        lib = LowMathLib.LowMathLib()
        X = self.data[self.classes].to_numpy()
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        houses = self.data['Hogwarts House'].unique()
        for house in houses:
            y = (self.data['Hogwarts House'] == house).astype(int).values
            weight = np.zeros(X.shape[1])
            weight = gradient_descent(X, y, weight, 0.025, 2500)
            self.weights[house] = weight.tolist()
    
    # Write weights in a json
    def output(self):
        with open("weights.json", "w") as f:
            json.dump(self.weights, f)

# The Gradient Descent logic
def gradient_descent(X, y, weight, alpha, iterations):
    lib = LowMathLib.LowMathLib()
    m = len(y)
    for i in range(iterations):
        h = lib.sigmoid(X.dot(weight))
        gradient = (1 / m) * X.T.dot(h - y)
        weight -= alpha * gradient
    return weight

# Main
if __name__ == "__main__":
    TRAIN = Train()
    TRAIN.parser()
    TRAIN.normalization()
    TRAIN.train()
    TRAIN.output()
    #TRAIN.calc_precision()