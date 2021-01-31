#!/usr/bin/python3

import numpy as np 
import random

def create_distances(num):
    """create distances between cities"""
    x=np.zeros((num, num))
    for i in range(num):
        for j in range(num):
            if i == j:
                x[i][j] = 0
            else:
                x[i][j] = random.random() * 100
                x[j][i] = x[i][j]
    return x

def swap(jour):
    """swap two cities in journey"""
    a = random.randint(0,y-1)
    b = random.randint(0,y-1)
    jour[a], jour[b] = jour[b], jour[a]
    return jour

def dist(jour):
    """calculate journey distance"""
    d = 0
    for i in range(len(jour)-1):
        d += x[jour[i-1]-1][jour[i]-1]
    return d
    
    
if __name__ == __main__:
    #create distances
    cities = 100
    y = 100
    x = create_distances(cities)

    #create journey
    journey = []
    while len(journey) < cities:
        city = random.randint(1,cities)
        if city not in journey:
            journey.append(city)
    #print(x)

    T = 30
    factor = 0.99
    T_init = T
    way = dist()#dist calc #cost0

    for i in range(100):
        T = T * factor
        old_journey = journey[:]#save old journey
        journey = swap()#journey swap
        new_way = dist()#new dist calc
        print(i, "\ndist:", way, "\nnew dist:", new_way)
        if new_way < way:
            way = new_way.copy()
        elif random.random() < np.exp((way-new_way)/T):
            way = new_way
        else:
            journey = old_journey[:]#copy old journey
        if np.exp((way-new_way)/T) < 0 or np.exp((way-new_way)/T) > 1:
            print("~~~~~~~~~~~~Error, probability not between 0 an d 1:", np.exp((way-new_way)/T))
