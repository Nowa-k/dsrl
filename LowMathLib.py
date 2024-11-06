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