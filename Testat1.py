#!/usr/bin/python3

import numpy as np 
import random



def create_distances(num):
    """generate matrix with distances"""
    x = np.zeros((num,num))
    for i in range(num):
        for j in range(num):
            if i == j:
            #distance from city a to city a is 0 
                x[i][j] = 0
            else:
            #append same distance from a to b and b to a
                x[i][j] = random.randint(00,10)
                x[j][i] = x[i][j]
    return x

def swap(jour):
    """swap two random cities in journey"""
    a = random.randint(0,y-1)
    b = random.randint(0,y-1)
    jour[a], jour[b] = jour[b], jour[a]
    return jour

def calc_len_journey(jour):
    """calculate length of journey"""
    e = 0
    for i in range(len(jour)-1):
        e += x[jour[i-1]-1][jour[i]-1]
    return e



    
if __name__=='__main__':
    cities = 10
    x = create_distances(cities)
    journey = []
    y = 10

    while len(journey) < 10:
    # append 10 random cities to journey
        city = random.randint(1,cities)
        if city not in journey:
            journey.append(city)
    #print(x)

    for i in range(100):
        # calculate length of journey, swap and recalculate journey
        # save journey if length smaller
        way = calc_len_journey()
        #print(way,journey)
        alte_journey = journey[:] #copy
        journey = swap(journey)
        new_way = calc_len_journey()
        #print("new ",new_way,journey)
        if not new_way < way:
            journey = alte_journey[:]
            #print("old %d was shorter than %d"%(way,new_way))
            way = calc_len_journey()
        print(way)
    






  
