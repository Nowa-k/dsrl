import sys
import csv
import os.path
import statistics
import LowMathLib
from tabulate import tabulate
        
class Describe:
    
    def __init__(self):
        self.column = []
        self.argv = sys.argv
        self.data = {}
        self.res = {}

    def parser(self):
        #Check for number of arguments
        if len(self.argv) < 2:
            print("[Error] Il faut un argument (le dataset à lire).")
            sys.exit()
        elif len(self.argv) > 2:
            print("[Error] Il faut uniquement un argument ...")
            sys.exit()
        
        #Check if the file exists
        if os.path.exists(self.argv[1]):
            #Check if we have the perms to read the file
            if os.access(self.argv[1], os.R_OK):
                with open(self.argv[1], 'r') as file:
                    csvreader = csv.reader(file)
                    headers = next(csvreader)
                    for header in headers:
                        self.data[header] = []
                    
                    for line in csvreader:
                        for index, value in enumerate(line):
                            try:
                                self.data[headers[index]].append(float(value))
                            except ValueError:
                                self.data[headers[index]].append(value)
            else:
                print("[Error] Vous ne disposez pas des permissions nécessairess pour lire ce fichier.")
                sys.exit()  
        else:
            print("[Error] Le fichier est introuvable. Etes-vous sûrs du chemin d'accès?")
            sys.exit()
        
    def response(self):
        lib = LowMathLib.LowMathLib()
        stats = {}
        for column, values in self.data.items():
            values = verifyChunk(values)
            if values is not None and values != []:
                count = round(len(values), 3)
                mean = round(lib.ft_mean(values), 3)
                std_dev = round(lib.ft_std_dev(values), 3) if count > 1 else 0
                min_val = round(lib.ft_min(values), 3)
                max_val = round(lib.ft_max(values), 3)
                q1, q3 = lib.ft_quartiles(values)
                median = round(lib.ft_median(values), 3)
                under_mean = lib.ft_underMean(values, mean)
                over_mean = lib.ft_overMean(values, mean)
                
                stats = {
                    'Count': count,
                    'Mean': mean,
                    'Std': std_dev,
                    'Min': min_val,
                    '25%': q1,
                    '50%': median,
                    '75%': q3,
                    'Max': max_val,
                    'underMean': under_mean,
                    'overMean': over_mean
                }

                self.res[column] = stats
                
    
    def printRes(self):
        header, count, mean, std, min, q1, q2, q3, max, underMean, overMean = [""], ["Count"], ["Mean"], ["Std"], ["Min"], ["25%"], ["50%"], ["75%"], ["Max"], ["underMean"], ["overMean"]
        
        for res, value in self.res.items():
            header = header + [(f"{res}")]
            for n, v in value.items():
                match n:
                    case 'Count':
                        count = count + [f"{v}"]
                    case 'Mean':
                        mean = mean + [f"{v}"]
                    case 'Std':
                        std = std + [f"{v}"]
                    case 'Min':
                        min = min + [f"{v}"]
                    case '25%':
                        q1 = q1 + [f"{v}"]
                    case '50%':
                        q2 = q2 + [f"{v}"]
                    case '75%':
                        q3 = q3 + [f"{v}"]
                    case 'Max':
                        max = max + [f"{v}"]
                    case 'underMean':
                        underMean = underMean + [f"{v}"]
                    case 'overMean':
                        overMean = overMean + [f"{v}"]
                
        print(tabulate([header, count, mean, std, min, q1, q2, q3, max, underMean, overMean]))

def verifyChunk(values):
    values = [x for x in values if x not in ('', None)]

    for value in values:
        if isinstance(value, float) is not True:
            return
    return values    

# Main
if __name__ == "__main__":
    DSLR = Describe()
    DSLR.parser()
    DSLR.response()
    DSLR.printRes()
