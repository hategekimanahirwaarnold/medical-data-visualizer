import warnings

# Suppress all FutureWarning warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Suppress UserWarning warnings
warnings.filterwarnings("ignore", category=UserWarning)

import ssl
import urllib.request

# Dsable ssl certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# begin code after disabling
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv', index_col=0)

# Add 'overweight' column
df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2 > 25).astype(int)

# Normalize data for 'cholesterol' and 'gluc'
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    # print("The df_cat used to melt: \n", df_cat)
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature.
    grouped = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    gr = df_cat.groupby(['cardio', 'variable', 'value']).size()
    # print("Grouped data up to size: \n",gr,"\n Grouped data up to reset_index()\n", grouped)
    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=grouped, kind='bar')
    g.set_axis_labels('Variables', 'Total')
    g.set_titles('Cardio: {col_name}')
    # Get the figure for the output
    # fig =  plt.show()
    fig = plt
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    df['id'] = df.index
    columns = pd.Series(['id', 'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol',
       'gluc', 'smoke', 'alco', 'active', 'cardio', 'overweight'])

    # Clean the data
    df_heat = df
    df_heat.columns = columns
    # Calculate the correlation matrix
    corr =df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    corr = corr.where(~mask)


    # Set up the matplotlib figure
    fig, ax = plt.subplots()
    

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, annot=True, fmt=".1f", vmax=1, vmin=-1)

    # plt.show()
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
