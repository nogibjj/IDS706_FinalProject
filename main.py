import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def loadDf(path):
    df = pd.read_csv(path)
    df.columns = ['Year','Age','Name','Movie','Movie2']
    return df


def describeData(df):
    return df.describe()

def plotData(df):
    
    plt.figure(figsize=(10,10))
    x = df['Year']
    y = df['Age']
    color= np.array([np.random.randint(0,100) for _ in range(df.shape[0])])
    plt.scatter(x,y,c=color,cmap='viridis',s=100)
    plt.xlabel("year")
    plt.ylabel("age")
    plt.colorbar()
    plt.show()
    plt.savefig("./scatterfig.png")

