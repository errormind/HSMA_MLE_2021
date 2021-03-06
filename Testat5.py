#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import math

def get_NN(x,y):
    """create list of distances"""
    dist = [(math.sqrt(((pointx-x)**2+(pointy-y)**2)),ident) for cla in clas for (pointx,pointy,ident) in cla]
    # sort by distance (dist[0])
    dist = sorted(dist) 
    b = 0
    a = 0
    # look at first k elemtents
    for i in range(k):
        if dist[i][1] == -1:
            a += 1
        else:
            b += 1
    # define class
    if a > b:
        clasA.append((x,y,-1))
    else:
        clasB.append((x,y,1))

def draw():
    """draw data from file to plot"""
    # read data
    with open('spiral.txt','r') as datei:
        # every line
        for i, line in enumerate(datei):
            # divide line
            line=line.split(";")
            # string to float
            if "\n" in line[2]:
                line[2] = float(line[2][:-1])
            line[1] = float(line[1])
            line[0] = float(line[0])
            # append spiral points to class
            if line[2] == -1:
                clasA.append((line[0],line[1],line[2]))
            elif line[2] == 1:
                clasB.append((line[0],line[1],line[2]))
        
        # check points in plot for nearest neighbor
        da = 150
        for x in range(-da, da):
            for y in range(-da, da):
                xx = x/100
                yy = y/100
                get_NN(xx,yy)
                
        # PLOT
        plt.ylabel('spirale')
        plt.axis([-2, 2, -2, 2])
        plt.grid(True)
        for (x,y,i) in classA:
            plt.plot(x, y, 'o', markersize=1, color="lightblue")
        for (x,y,i) in classB:
            plt.plot(x, y, 'o', markersize=1, color="salmon")
        for (x,y,i) in clasA:
            plt.plot(x, y, 'b+')
            pass
        for (x,y,i) in clasB:
            plt.plot(x, y, 'r+')
            pass
        
if __name__=='__main__':
    clasA = []
    clasB = []
    clas = [clasA,clasB]
    k = 51 # change for different scenarios
    draw()
    plt.show() 
