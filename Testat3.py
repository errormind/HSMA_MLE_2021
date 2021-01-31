#!/usr/bin/python3

import sys
import numpy as np

def take_second(ele):
    return ele[1]

class population:
    """a population of packaging units"""
    def __init__(self, psize=10, plength = 100, c=0.025):
        np.random.seed(9) #for repeatability
        self.c = c
        self.p = [[np.random.randint(2,size=plength),0,0] for _ in range(psize)] #population with [bits, fitness, Pr]
        self.v = [np.random.randint(1,10) for _ in range(plength+1)] #volumina of boxes (1..10)
        self.newp = [] #new population with [bits, fitness, Pr]
        self.r = 4
        self.m = 4

    def evolve(self):
        """evolves the population to next generation"""
        self.update_fitness()
        self.survivor()
        self.crossover()
        self.mutation()
        self.p = self.newp
        self.update_fitness()
        self.newp = sorted(self.p, key=take_second)
        for x in self.newp:
            print("%.2f" % x[1], end=" ")
        else:
            print("",end="\n")
        self.newp=[]

    def selectHypo(self):
        """better use (numpy Gewichtete Zufallsauswahl)"""
        rand = np.random.randint(0,85)/100 #0 .. 0.85
        start = np.random.randint(1,10)
        num = 0
        for ge in range(-start, len(self.p)-start):
            num += self.p[ge][2]
            if num > rand:
                break
        return ge
            
    def survivor(self):
        """select r=4 for new population"""
        for _ in range(self.r):
            self.newp.append(self.p[self.selectHypo()]) 

    def crossover(self):
        """creates 10-r=6 paired genes"""
        mother = self.selectHypo()
        father = self.selectHypo()
        crosspoint = np.random.randint(0,100)
        for _ in range((10-self.r)//2):
            self.newp.append([np.concatenate((self.p[father][0][crosspoint:],self.p[mother][0][:crosspoint])),0,0])
            self.newp.append([np.concatenate((self.p[mother][0][crosspoint:],self.p[father][0][:crosspoint])),0,0])
        
    def mutation(self):
        """mutates genes"""
        for x in range(self.m):
            gene = 0-self.selectHypo()
            bit = np.random.randint(0,100)
            gene = np.random.randint(0,10)
            try:
                self.newp[gene - x][0][bit] ^= True         
            except IndexError:
                print(gene, x, bit)
                self.newp[gene + x][0][bit] ^= True

    def update_fitness(self):
        fitGes = 0
        """update fitness of population"""
        for i,_ in enumerate(self.p):
            w = 0 #weight of santas bag by candidate i
            for x,box in enumerate(self.v):
                #iterate over boxes
                if self.p[i][0][x] == True:
                    #if "put in box" is true 
                    if w + box <= 100:
                        w += box
                    else:
                        break
            self.p[i][1] = np.e**(-self.c*(100-w)**2) 
        for gene in self.p:
            fitGes += gene[1]
        for gene in self.p:
            gene[2] = gene[1]/fitGes                

def main(args):
    pop = population()
    for x in range(50):
        pop.evolve()
        if sorted(pop.p, key=take_second)[0][1] > 0.975:
            print(x)
            break
   
if __name__== "__main__":
    main(sys.argv[1:])
