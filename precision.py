import re
import sys
import csv
import json
import os.path
import LowMathLib
import numpy as np
import pandas as pd

class Precision:
    def __init__(self):
        self.wieghts = {}
        self.argv = sys.argv
        self.predictions = []
        self.realValues = []
        self.lib = LowMathLib.LowMathLib()
        self.classes = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"]

    # Parse arguments
    def parser(self):
        if len(self.argv) != 3:
            print("[Command] ./python3 precision.py [ARG REQUIRED] [PATH TO]/dataset_train.csv [ARG REQUIRED] weighs file")
            sys.exit()
        else:
            if os.path.basename(self.argv[1]) == "dataset_train.csv":
                if os.path.exists(self.argv[1]) or os.path.exists(self.argv[2]):
                    if os.access(self.argv[1], os.R_OK) and os.access(self.argv[2], os.R_OK):
                        self.data = pd.read_csv(self.argv[1])
                        self.realValues = self.data["Hogwarts House"]
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

    # Predicct the houses with the trained data
    def predict(self):
        X = self.data[self.classes].to_numpy()
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        lib = LowMathLib.LowMathLib()
        with open(self.argv[2], "r") as f:
            weights = json.load(f)
        for i in range(X.shape[0]):
            probs = {cls: lib.sigmoid(np.dot(X[i], np.array(weights))) for cls, weights in weights.items()}
            self.predictions.append(max(probs, key=probs.get))

    # Normalize informations to be between 0 and 1
    def normalization(self):
        lib = LowMathLib.LowMathLib()
        for classe in self.classes:
            min_val = self.lib.ft_min(self.data[classe])
            max_val = self.lib.ft_max(self.data[classe])
            self.data[classe] = (self.data[classe] - min_val) / (max_val - min_val)
    
    # Write the results in houses.csv
    def output(self):
        errors = 0
        for i in range(len(self.realValues)):
            if (self.realValues[i] != self.predictions[i]):
                errors += 1
        pourcent = ((len(self.realValues) - errors) * 100) / len(self.realValues)
        print(f"The precision of the algo is: {pourcent}%")

# Main
if __name__ == "__main__":
    PRECISION = Precision()
    PRECISION.parser()
    PRECISION.normalization()
    PRECISION.predict()
    PRECISION.output()