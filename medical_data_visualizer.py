import warnings

# Suppress all FutureWarning warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Suppress UserWarning warnings
warnings.filterwarnings("ignore", category=UserWarning)

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
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature.
    grouped = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=grouped, kind='bar')
    g.set_axis_labels('variable', 'total')
    g.set_titles('Cardio: {col_name}')
    # Get the figure for the output
    fig = plt.gcf()
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    df['id'] = df.index
    columns = pd.Series(['id', 'age', 'sex', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol',
       'gluc', 'smoke', 'alco', 'active', 'cardio', 'overweight'])

    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                (df['height'] >= df['height'].quantile(0.025)) &
                (df['height'] <= df['height'].quantile(0.975)) &
                (df['weight'] >= df['weight'].quantile(0.025)) &
                (df['weight'] <= df['weight'].quantile(0.975))
                ]
    # Calculate the correlation matrix
    df_heat = df_heat[columns]
    correlation =df_heat.corr()
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(correlation, dtype=bool))
    corr = correlation.where(~mask)

    # Set up the matplotlib figure
    fig, ax = plt.subplots()
    
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, square=True, linewidths=0.5, annot=True, fmt="0.1f")

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
