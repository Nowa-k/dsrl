import sys
import csv
import os.path
import LowMathLib
import numpy as np
import pandas as pd

class Train:
    def __init__(self):
        self.argv = sys.argv
        self.data = {}
        self.target_data = []
        self.prediction_vars = []
        self.weights = []

    def parser(self):
        if len(self.argv) < 2 or len(self.argv) > 2:
            print("[Command] ./python3 logreg_predict.py [ARG REQUIRED] [PATH TO]/dataset_train.csv")
            sys.exit()
        elif len(self.argv) == 2:
            if os.path.basename(self.argv[1]) == "dataset_train.csv":
                if os.path.exists(self.argv[1]):
                    if os.access(self.argv[1], os.R_OK):
                        self.data = pd.read_csv(self.argv[1], index_col = "Index")
                        self.data = self.data.dropna()
                        target_data = np.array(self.data["Hogwarts House"])
                        prediction_vars = np.array(self.data[["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"]])
                        self.target_data = target_data
                        self.prediction_vars = prediction_vars
                    else:
                        print("[Error] Vous ne disposez pas des permissions nécessairess pour lire ce fichier.")
                        sys.exit()
                else:
                    print("[Error] Le fichier est introuvable. Etes-vous sûrs du chemin d'accès?")
                    sys.exit()
            else:
                print("[Error] Le nom du fichier doit être: 'dataset_train.csv'")
                sys.exit()

    def normalization(self):
        lib = LowMathLib.LowMathLib()
        np.apply_along_axis(lib.min_max, 0, self.prediction_vars)

    def handle_nans(self):
        col_mean = np.nanmean(self.prediction_vars, axis=0)
        inds = np.where(np.isnan(self.prediction_vars))
        self.prediction_vars[inds] = 0

    def train(self):
        lib = LowMathLib.LowMathLib()
        X = np.insert(self.prediction_vars, 0, 1, axis=1)
        for house in np.unique(self.target_data):
            current_house_vs_all = np.where(self.target_data == house, 1, 0)
            w = np.ones(X.shape[1])
            for _ in range(1000):
                output = np.dot(X, w)
                errors = current_house_vs_all - lib.sigmoid(output)
                gradient = np.dot(X.T, errors)
                w += 0.1 * gradient
            self.weights.append((w, house))
    
    def output(self):
        with open('weights.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Hogwarts House', 'Arithmancy Weight', 'Astronomy Weight', 'Herbology Weight', 'Defense Against the Dark Arts Weight', 'Divination Weight', 'Muggle Studies Weight', 'Ancient Runes Weight', 'History of Magic Weight', 'Transfiguration Weight', 'Potions Weight', 'Care of Magical Creatures Weight', 'Charms Weight', 'Flying Weight'])
            for values, key in self.weights:
                line = [key]
                for value in values:
                    line.append(str(value))
                writer.writerow(line)

if __name__ == "__main__":
    TRAIN = Train()
    TRAIN.parser()
    TRAIN.handle_nans()
    TRAIN.normalization()
    TRAIN.train()
    TRAIN.output()