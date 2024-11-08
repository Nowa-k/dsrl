import re
import sys
import csv
import json
import os.path
import LowMathLib
import numpy as np
import pandas as pd

class Predict:
    def __init__(self):
        self.data = {}
        self.argv = sys.argv
        self.predictions = []
        self.lib = LowMathLib.LowMathLib()
        self.classes = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"]

    def parser(self):
        if len(self.argv) < 2 or len(self.argv) > 3:
            print("[Command] ./python3 logreg_predict.py [ARG REQUIRED] [PATH TO]/dataset_test.csv [ARG REQUIRED] weighs file")
            sys.exit()
        elif len(self.argv) == 3:
            if os.path.basename(self.argv[1]) == "dataset_test.csv":
                if os.path.exists(self.argv[1]) or os.path.exists(self.argv[2]):
                    if os.access(self.argv[1], os.R_OK) and os.access(self.argv[2], os.R_OK):
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
                print("[Error] Le nom du fichier doit être: 'dataset_test.csv'")
                sys.exit()

    def predict(self):
        X = self.data[self.classes].to_numpy()
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        lib = LowMathLib.LowMathLib()
        with open(self.argv[2], "r") as f:
            weights = json.load(f)
        for i in range(X.shape[0]):
            probs = {cls: lib.sigmoid(np.dot(X[i], np.array(weights))) for cls, weights in weights.items()}
            self.predictions.append(max(probs, key=probs.get))

    def normalization(self):
        lib = LowMathLib.LowMathLib()
        for classe in self.classes:
            min_val = self.lib.ft_min(self.data[classe])
            max_val = self.lib.ft_max(self.data[classe])
            self.data[classe] = (self.data[classe] - min_val) / (max_val - min_val)
    
    def output(self):
        with open('houses.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Index', 'Hogwarts House'])
            for i in range(len(self.predictions)):
                writer.writerow([str(i), self.predictions[i]])

if __name__ == "__main__":
    PREDICT = Predict()
    PREDICT.parser()
    PREDICT.normalization()
    PREDICT.predict()
    PREDICT.output()