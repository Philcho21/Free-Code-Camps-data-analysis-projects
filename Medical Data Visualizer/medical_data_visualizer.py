import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Read data from file
df = pd.read_csv('medical_examination.csv')

# calculate BMI and use it to determine if a person is overweight
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2)).apply(lambda x: 0 if x > 25 else 1)

# Normalising glucose and cholesterol data to 0 and 1
df[['gluc', 'cholesterol']] = df[['gluc', 'cholesterol']].apply(lambda x: x.map(lambda y: 0 if y == 1 else 1))

# Define a categorical plot function
def draw_cat_plot():
    #Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke',
    #'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'],value_vars= ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'
    df_cat = df_cat.groupby(['variable', 'value', 'cardio']).size().reset_index(name='total')
    
    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar')

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # Remove the outliers
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
            (df['height'] >= df['height'].quantile(0.025)) &
            (df['height'] <= df['height'].quantile(0.975)) &
            (df['weight'] >= df['weight'].quantile(0.025)) &
            (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(18, 12))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, fmt='.1f', mask=mask, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={'shrink': .5})

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
