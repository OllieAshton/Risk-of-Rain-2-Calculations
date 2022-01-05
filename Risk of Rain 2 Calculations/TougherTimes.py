import plotly.express as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

### READING IN THE DATA ###
df = pd.read_csv('/mnt/f/Projects/Risk of Rain 2 Calculations/percentages_toughertimes.csv',delimiter=',').values

### FITTING THE DATA ###
def log_fun(x,a,b,c,d): return (a/(b*x+c))+1
par,cov = curve_fit(log_fun,df[:,0],df[:,1])

### SIMULATING THE PERCENTAGE OF HITS ARE BLOCKED WITH R CLOVERS AND N TEDDIES ###
def hit_loop(rr,nn,hits):
    '''
    Calculates the percentage chance of a hit occuring using random number generation per hit\n
    rr = Number of 57 Leaf Clovers\n
    nn = Number of Tougher Times\n
    hits = Number of attacks that have occured\n
    '''
    lst1=[]
    for r in range(rr):
        for n in range(nn):
            ii=0
            lst = []
            while ii<=hits:
                nh=0 #hit
                p = log_fun(n,*par)
                rando = np.random.random()
                if p>rando:
                    nh=1 #not hit
                elif p<=rando:
                    for _ in range(r):
                        p = log_fun(n,*par)
                        rando = np.random.random()
                        if p>rando:
                            nh=1 #not hit
                            break      

                lst.append(nh)
                ii+=1
            lst1.append(np.array([r,n,sum(lst)/ii]))
    lst1 = np.array(lst1)
    arr = np.empty([rr,nn])
    for iii in range(len(lst1)):
        arr[int(lst1[iii,0]),int(lst1[iii,1])] = lst1[iii,2]

    return arr

r = 10 #Number of 57 Leaf Clovers
n = 100 #Number of Tougher Times
hits = 1e10 #Number of attacks
fig = plt.imshow(hit_loop(r,n,hits),
    labels = dict(x = 'Number of Tougher Times',
                y = 'Number of 57 Leaf Clovers',
                color = 'Percentage Chance of Block'),
    aspect = 'auto',
    title = f'For {hits} Attacks')
fig.write_image(f'Risk of Rain 2 Calculations/hit_loop {r} clovers {n} teddy {hits} hits'+'.png')
