import numpy as np

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

    @staticmethod
    def ft_underMean(values, mean):
        count = 0
        for value in values:
            if value < mean:
                count += 1
        return count

    @staticmethod
    def ft_overMean(values, mean):
        count = 0
        for value in values:
            if value > mean:
                count += 1
        return count

    @staticmethod
    def calculate_correlation(x, y):
        valid_pairs = [(xi, yi) for xi, yi in zip(x, y) if xi == xi and yi == yi]

        if len(valid_pairs) < 2:
            return None
        
        x_filtered, y_filtered = zip(*valid_pairs)
        n = len(x_filtered)

        mean_x = sum(x_filtered) / n
        mean_y = sum(y_filtered) / n

        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x_filtered, y_filtered))
        denominator_x = sum((xi - mean_x) ** 2 for xi in x_filtered) ** 0.5
        denominator_y = sum((yi - mean_y) ** 2 for yi in y_filtered) ** 0.5

        if denominator_x == 0 or denominator_y == 0:
            return None

        return numerator / (denominator_x * denominator_y)

    @staticmethod
    def cost(X, y, theta):
        m = len(y)
        h = sigmoid(X.dot(theta))
        return (-1 / m) * (y.T.dot(np.log(h)) + (1 - y).T.dot(np.log(1 - h)))

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))