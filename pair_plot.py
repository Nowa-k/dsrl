import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully with shape {data.shape}")
        data = data.drop("Index", axis=1)
        data = data.drop("Flying", axis=1)
        data = data.drop("Arithmancy", axis=1)
        data = data.drop("Care of Magical Creatures", axis=1)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def display_pair_plot(data, hue_column=None):
    try:
        sns.pairplot(data, hue=hue_column, corner=True)
        plt.show()
    except Exception as e:
        print(f"Error generating pair plot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    file_path = 'data.csv'
    target_column = 'target'
    
    data = load_data("datasets/dataset_train.csv")
    display_pair_plot(data, hue_column="Hogwarts House")
