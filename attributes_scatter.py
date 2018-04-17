import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# load dataframe containing height, weight, and pos on all active nba players
df = pd.read_csv("example_csvs/nba_physical_attr.csv")

# create seaborn scatter plot labelling data pts based on position
sns.lmplot('height(cm)', 'weight(kg)', data=df, hue='position', fit_reg=False, markers=['x','o','.','*','p'])
plt.title("NBA Player Height Versus Weight by Position")
plt.show()
