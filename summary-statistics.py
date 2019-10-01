# -*- coding: utf-8 -*-
"""SummaryStatistics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Es3e1N6CgWlZJgF49p5Vrjhdze47nMyy
"""

# Import dependencies
import pandas as pd
from scipy.linalg import svd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import seaborn as sns
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D

# Download data
#!wget https://web.stanford.edu/~hastie/ElemStatLearn/datasets/SAheart.data

df = pd.read_csv("SouthAfrica.csv", sep=",")
df

"""Standardiserer data og konverterer 'present' og 'absent' til 1 og 0"""

df2 = df.copy()
df2["famhist"] = 1 * (df2["famhist"] == "Present")
cols = ["sbp", "tobacco", "ldl", "adiposity", "typea", "obesity", "alcohol", "age"]
#df2[cols] = (df2[cols] - df2[cols].mean(0)) / df2[cols].std(0)
#df2["age"] = df2["age"] / df2["age"].max(0)
df2 = df2.drop("row.names", 1)

print(df2["chd"].sum())

cols2 = ["sbp", "tobacco", "ldl", "adiposity", "famhist", "typea", "obesity", "alcohol", "age"]
noa = np.size(cols2)

def Statistics(X,noa):
    for i in range(1,noa):
        stat = []
        x = X[cols2[i]]
        stat.append(x.mean())
        stat.append(x.var())
        stat.append(np.median(x))
        stat.append(x.max())
        stat.append(x.min())
        print(stat)
        
a = round(df.drop(['row.names','chd'],1).describe().drop('count'),2)
a.to_latex(index=True)

"""Statistikkerne printes i kolonner
1. kolonne: mean
2. kolonne: varians
3. kolonne: median
4. kolonne: max værdi
4. kolonne: min værdi
"""

#print('Calculate statistics')
#Statistics(df2, noa)

np.corrcoef(df["adiposity"],df["age"])

chd = df2['chd']

"""Histogrammerne plottes"""

def gaussian(x, mean, amplitude, standard_deviation):
    return amplitude * np.exp( - ((x - mean) / standard_deviation) ** 2)
X = df.drop(['row.names','chd'],1);
X["famhist"] = 1 * (X["famhist"] == "Present")
titles = ['Systolic Blood Pressure', 'Cumultative Tobacco', 'Low density lipoprotein cholesterol', 'Adiposity','History of family heart disease', 'Type A behaviour' ,'Obesity', 'Current alcohol consumption', 'Age']
labels = ['mmHG', 'Cumultative Tobacco in kg', 'mmMol / L','BAI', 'Present / absent', 'TypeA Behaviour scale (1-100)', 'BMI', 'Grams of pure alcohol within the last 30 days', 'Age']
def histogram(X,noa):
    fig = plt.figure(figsize=[10,10])
    fig.subplots_adjust(hspace=0.5)
    fig.subplots_adjust(wspace=0.5)
    for i in range(noa):
        Xplot = X.iloc[:,i]
        plt.subplot(3,3,i+1)
        plt.hist(Xplot,bins=20, zorder = 3,alpha = 0.8);
        plt.title(titles[i])
        plt.grid(linestyle = '--', zorder = 0, axis = 'y', alpha =0.8)
        plt.xlabel(labels[i])
    plt.subplot(3,3,9)
    plt.suptitle("Histograms of the attributes")
    plt.show()

histogram(X, len(X.iloc[1,:]))

x = df['typea']
plt.hist(x,bins=20, zorder = 3,alpha = 0.8)
plt.grid(linestyle = '--', zorder = 0, axis = 'y')
plt.show()
sns.distplot(x, norm_hist = True)
plt.grid(linestyle = '--', zorder = 0, axis = 'y')

"""Fortolkning af boxplots:

sbp: højreskæv fordeling

Idl: højreskæv fordeling

obesity: tilnærmelsesvist normalfordelt

typea: tilnærmelsesvist normalfordelt

adioposity: tilnærmelsesvist normalfordelt med en stor spredning

age: Somewhat uniformt???

alcohol og tobacco: chi^2 eller F-fordeling m. 2 frihedsgrader

CHD, famhist: diskrete variable

Boxplots
"""

def boxPlot(X):
    fig = plt.figure(figsize=[15,15])
    fig.subplots_adjust(hspace=.5)
    for i in range(0,noa):
        plt.subplot(3,3,i+1)
        box = plt.boxplot(X[cols2[i]])
        box['boxes'][0].set(color='C0')
        plt.xticks(range(0),cols2)
        plt.title(cols2[i])
        plt.ylabel(labels[i])
        plt.grid(linestyle = "--")

    plt.suptitle("Boxplot of attributes")
    plt.show()
boxPlot(df2)



"""Her ser adiposity ud til at være normalfordelt

Resten ser ud til at være henholdsvis højre- eller venstreskæv

Bortset fra de diskrete værdier selvfølgelig ;-)

Kan vi evt. sige noget om outliers
"""