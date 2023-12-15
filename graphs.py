#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:33:40 2022

@author: tom
"""

# on définit les graphe comme des liste d'adjacence

from tkinter import *
import random
import math as m
import time

#graph = [[2, 7, 11], [3, 4, 9, 10], [5, 8, 0], [10, 1, 4, 6],
#         [3, 1, 6], [2], [3, 10, 4], [0], [2], [10, 1], [3, 1, 6, 9], [0]]
#graph = [[1, 2, 3, 4, 5], [0, 2, 3, 4, 6], [0, 1, 3, 4, 7], [0, 1, 2, 4, 8], [0, 1, 2, 3, 9],
#            [0, 6, 9], [1, 7, 5], [2, 8, 6], [3, 9, 7], [4, 5, 8]]
#graph = [[1, 2, 3, 4, 5], [0, 2, 3, 4, 6], [0, 1, 3, 4, 7], [0, 1, 2, 4, 8], [0, 1, 2, 3, 9],
#            [0, 6, 7, 8, 9], [1, 5, 7, 8, 9], [2, 5, 6, 8, 9], [3, 5, 6, 7, 9], [4, 5, 6, 7, 8]]
graph = [[1, 2], [2], [3, 0], [0]]
 
def sup(l, x):
    l.remove(x)
    return l


#random graph
#graph = [sup(list(set([random.randrange(10) for _ in range(random.randrange(10))]+[i])), i) for i in range(10)]
#print(graph)



def distance(x, y):
    return m.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def norme(x):
    return distance(x, [0, 0])


class Graph:
    def __init__(self, g):
        """dico_pos est de la forme : (x, y, vx , vy, cercle, text)"""
        self.window = Tk()
        self.window.title("graphe")

        self.g = g

        self.canevas = Canvas(self.window, width=800, height=800, bg="white")
        self.canevas.grid(column=0, row=0)

        self.dico_pos = {}
        self.dico_arrete = {}

        for i in range(len(g)):
            continuer = True
            while continuer:
                continuer = False
                x, y = random.randint(100, 700), random.randint(100, 700)
                for k in self.dico_pos:
                    a, b = self.dico_pos[k][0]
                    if distance([a, b], [x, y]) < 100:
                        continuer = True
                        break

                for k in self.g[i]:
                    try:
                        if distance(self.dico_pos[k][0], self.dico_pos[i][0]) > 100:
                            continuer = True
                            break
                    except KeyError:
                        pass

            self.dico_pos[i] = [[x, y], [0, 0]]  # position vitesse
        
        
        
        for i in range(len(self.g)):
            x, y = self.dico_pos[i][0]
            cercle = self.canevas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='#4A7A8C')
            etiquette = self.canevas.create_text(x, y, text=str(i), fill="black", font=("arial", 15))
            self.dico_pos[i].append(cercle)
            self.dico_pos[i].append((etiquette))

        self.tracer()

        self.window.bind('<f>', self.actualise)
        self.window.bind('<p>', self.perturber)
        self.window.bind('<s>', self.start)
        

        self.window.mainloop()

    def effacer(self):
        """
        for i in self.canevas.find_all():
            self.canevas.delete(i)
        self.canevas.update()
        """

        for i in self.dico_arrete:
            self.canevas.delete(self.dico_arrete[i][0])

    def tracer(self):
        for i in range(len(self.g)):
            for k in self.g[i]:
                x1, y1 = self.dico_pos[i][0]
                x2, y2 = self.dico_pos[k][0]
                arrete = self.canevas.create_line(x1, y1, x2, y2, fill='#4A7A8C')
                self.dico_arrete[(i, k)] = [arrete, [x1, y1], [x2, y2]]

    
    def perturber(self, p):
        for i in self.dico_pos:
            self.dico_pos[i][1][0] += random.randrange(-100, 110)
            self.dico_pos[i][1][1] += random.randrange(-100, 110)
        
    def actualise(self, f):
        """on applique le pfd a chaque itératio"""

        for i in range(len(self.g)):
            x1, y1 = self.dico_pos[i][0]
            # calcul des forces
            dvx, dvy = 0, 0
            for k in self.g[i]:
                x2, y2 = self.dico_pos[k][0]
                d = distance([x1, y1], [x2, y2])
                vec = [(x2 - x1) / d, (y2 - y1) / d]
                dvx -= 0.1 * vec[0] * 5 * (60 - d)
                dvy -= 0.1 * vec[1] * 5 * (60 - d)

            # pour séparer les composante conexe 
            for k in range(len(self.g)):
                if k != i:
                    x2, y2 = self.dico_pos[k][0]
                    d = distance([x1, y1], [x2, y2])
                    if d < 200:
                        vec = [(x2 - x1) / d, (y2 - y1) / d]
                        dvx -= 0.1 * vec[0] * (15000 / (d))
                        dvy -= 0.1 * vec[1] * (15000 / (d))

            # on le raproche du centre
            # avec un ressort de longueur a vide nulle au centre

            d = distance([x1, y1], [400, 400])
            if d > 270:
                vec = [(x1 - 300) / d, (y1 - 300) / d]
                dvx += 0.1 * vec[0] * 1 * ( - d)
                dvy += 0.1 * vec[1] * 1 * ( - d)

            # frotement 
            dvx -= 0.1 * self.dico_pos[i][1][0]
            dvy -= 0.1 * self.dico_pos[i][1][1]

            # on actualise
            vx, vy = self.dico_pos[i][1]
            self.dico_pos[i][1] = [vx + dvx, vy + dvy]

        for i in range(len(self.g)):
            vx, vy = self.dico_pos[i][1]
            dx, dy = 0.1 * vx, 0.1 * vy
            x, y = self.dico_pos[i][0]
            self.dico_pos[i][0] = [x + dx, y + dy]
            self.canevas.move(self.dico_pos[i][2], dx, dy)
            self.canevas.move(self.dico_pos[i][3], dx, dy)

        self.effacer()
        self.tracer()

    def start(self, s=None):
        self.actualise(None)
        if sum(norme(self.dico_pos[i][1]) for i in self.dico_pos.keys())/len(self.dico_pos) > 5:
            #print(sum(norme(self.dico_pos[i][1]) for i in self.dico_pos.keys())/len(self.dico_pos))
            self.canevas.after(100, self.start)    



    def energie(self, e):
        res = 0
        for i in self.dico_arrete:
            for k in self.dico_arrete:
                if k != i:
                    def f(t, u, v):
                        return [t * u[0] * (1 - t) * v[0], t * u[1] + (1 - t) * v[1]]

                    for x in range(2, 9):
                        for t in range(2, 9):
                            tmp1 = f(1 / x, self.dico_arrete[i][1], self.dico_arrete[i][2])
                            tmp2 = f(1 / t, self.dico_arrete[k][1], self.dico_arrete[k][2])
                            
                            if norme([tmp1[0] - tmp2[0], tmp1[1] - tmp2[1]]) < 1:
                                res += 1
        print(res)
        return res-30

    def permute(self):
        i = random.randrange(len(self.g))
        continuer = True
        while continuer:
            continuer = False
            x, y = random.randint(100, 500), random.randint(100, 500)
            for k in self.dico_pos:
                a, b = self.dico_pos[k][0]
                if distance([a, b], [x, y]) < 50:
                    continuer = True

        self.dico_pos[i] = [[x, y], [0, 0]]

    def recuit_simule(self, T0, iteration):
        en = self.energie()
        T = T0
        for i in range(iteration):
            tmp = self.g
            self.permute()
            self.effacer()
            self.tracer()
            e = self.energie()
            # print(en, e)
            if e < en:
                en = e
            else:
                p = m.exp((en - e) / T)
                a = random.random()
                if a >= p:
                    self.g = tmp
                else:
                    en = e
            T = T * 0.99
    
    


if __name__ == "__main__":
    g = Graph(graph)
    # g = Graph([[1, 2], [3, 4], [5, 6], [], [], [], []])
    #g = Graph([[1, 2, 3, 4, 5, 6, 7, 8], [0, 2, 3, 4, 5, 6, 7, 8], [0, 1, 3, 4, 5, 6, 7, 8], [0, 1, 2, 4, 5, 6, 7, 8], [0, 1, 2, 3, 5, 6, 7, 8], [0, 1, 2, 3, 4, 6, 7, 8], [0, 1, 2, 3, 4, 5, 7, 8], [0, 1, 2, 3, 4, 5, 6, 8], [0, 1, 2, 3, 4, 5, 6, 7]])
    #g = Graph([[1], [2], [3], [4], [5], [0]])

