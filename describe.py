import sys
import csv
import statistics
from tabulate import tabulate

class LowMathLib:
    @staticmethod
    def ft_min(tab):
        min = tab[0]
        for i in tab:
            if i <= min:
                min = i
        return min

    @staticmethod
    def ft_max(tab):
        max = tab[0]
        for i in tab:
            if i >= max:
                max = i
        return max

    @staticmethod
    def ft_mean(values):
            return sum(values) / len(values) if values else 0

    @staticmethod
    def ft_std_dev(values):
            mean_val = LowMathLib.ft_mean(values)
            variance = sum((x - mean_val) ** 2 for x in values) / (len(values) - 1) if len(values) > 1 else 0
            return variance ** 0.5
    
    @staticmethod
    def ft_median(values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2
        else:
            return sorted_values[mid]
        
    @staticmethod
    def ft_quartiles(values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        q1_pos = (n + 3) // 4 - 1
        q3_pos = (3 * n + 1) // 4 - 1

        q1 = sorted_values[int(q1_pos)]
        q3 = sorted_values[int(q3_pos)]

        return q1, q3
        
class Describe:
    
    def __init__(self):
        self.column = []
        self.argv = sys.argv
        self.data = {}
        self.res = {}

    def parser(self): 
        if len(self.argv) != 2:
            print("[Error] Il faut uniquement un argument ...")
            sys.exit()
            
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
        
    def response(self):
        lib = LowMathLib()
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
                
                stats = {
                    'Count': count,
                    'Mean': mean,
                    'Std': std_dev,
                    'Min': min_val,
                    '25%': q1,
                    '50%': median,
                    '75%': q3,
                    'Max': max_val
                }

                self.res[column] = stats
                
    
    def printRes(self):
        header, count, mean, std, min, q1, q2, q3, max = [""], ["Count"], ["Mean"], ["Std"], ["Min"], ["25%"], ["50%"], ["75%"], ["Max"]
        
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
                
        print(tabulate([header, count, mean, std, min, q1, q2, q3, max]))

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
