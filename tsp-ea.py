from functools import total_ordering
from glob import glob
import math
import random
from random import randint
from re import T
import  matplotlib.pyplot  as plt

adj_list = {}
random.seed()

class EA:

    def __init__(self, generations, filename, p_size, parent_scheme, survivor_scheme, offsprings, iterations, mutation_rate):
        self.generations = generations
        self.filename = filename
        self.p_size = p_size
        self.parent_scheme = parent_scheme
        self.survivor_scheme = survivor_scheme
        self.offsprings = offsprings
        self.iterations = iterations
        self.mutation_rate = mutation_rate

    def generation_counter(self):
        for i in range(self.iterations):
            self.make_adj_list()
            p = self.make_population(adj_list)

            for g in range(self.generations):
                p2 = self.make_offspring(p)
                new_p = {}
                if self.survivor_scheme == "truncation":
                    new_p = self.truncation_scheme(p2, new_p)

                elif self.survivor_scheme == "random":
                    new_p = self.random_scheme(p2, new_p)

                elif self.survivor_scheme == "rbs":
                    new_p = self.rbs_scheme(p2, new_p)

                elif self.survivor_scheme == "fps":
                    new_p = self.fps_scheme(p2, new_p)
                p = new_p

            #in each iterations (after some generations)
            a = sorted(p.values(), key = lambda x: x[0], reverse = True) #https://stackoverflow.com/questions/55365106/sorting-a-list-with-sub-lists-in-python/55365159
            best_value = a.pop()       

        # after running some iterations, print the best fitness value 
        a = sorted(p.values(), key = lambda x: x[0], reverse = True) #https://stackoverflow.com/questions/55365106/sorting-a-list-with-sub-lists-in-python/55365159
        best_value = a.pop()

        print("Best distance so far:", best_value[0])
            
    def make_adj_list(self):
        node = {}
        f = open(self.filename, "r")

        for x in range(4):
            next(f)
        length = f.readline().split()[2]

        for x in range(2):
            next(f)

        for line in range(int(length)):
            l = f.readline().split()
            n = int(l[0])
            x_c = float(l[1])
            y_c = float(l[2])
            node[n] = [x_c, y_c]

        dict_length = len(node.keys())

        for x in range(1, dict_length + 1):
            adj_list[x] = []
            for y in range(1, dict_length + 1):
                if y != x:
                    temp = [y, round(math.sqrt((node[x][0] - node[y][0])**2 + (node[x][1] - node[y][1])**2))]
                    adj_list[x].append(temp)

        return adj_list

    def make_population(self, adj_list): 
        population = {}

        for y in range(1, self.p_size + 1): #create population
            dict_length = len(adj_list.keys())
            l = []
            r = randint(1, dict_length) #start from a random node
            i = []
            l.append(r) #random node is the first node
            fitness = 0

            for x in range(1, dict_length):
                r2 = randint(0, (dict_length - 2))
                while adj_list[r][r2][0] in l:
                    r2 = randint(0, (dict_length - 2))
                fitness = adj_list[r][r2][1] + fitness
                r = adj_list[r][r2][0]
                l.append(r)
            i.extend((fitness, l))
            population[y] = i
                 
        return population

    def rbs_scheme(self, population, total_parent):
        new_p = {}
        new_f = {}
        l = []
        rank_sum = 0

        if self.survivor_scheme == "rbs":
            a = sorted(population.items(), key = lambda x: x[1])
            for x in range(len(a)):
                rank_sum = x + 1 + rank_sum
                
            for x in range(1, len(a) + 1):
                new_f[x] = (a[x-1][0], x/rank_sum)
                
            for x in range(len(a)):
                rank_sum = new_f[x + 1][1] + rank_sum
                l.append((a[x][0], rank_sum))

            p3 = population.copy()
            for y in range(self.offsprings):
                r_f = random.random()
                if r_f <= l[0][1]:
                    del(p3[l[0][0]])
                    del(l[0])
                else:
                    for x in range(len(population)-y-1):
                        if r_f >= l[x][1]:
                            if r_f < l[x + 1][1]:
                                del(p3[l[x][0]])
                                del(l[x])
            count = 1
            for x in p3.values():
                new_p[count] = x
                count = count + 1

            return new_p

        elif self.parent_scheme == "rbs":
            a = sorted(population.items(), key = lambda x: x[1], reverse = True)
            for x in range(1,len(a)+1):
                rank_sum = x + rank_sum

            for x in range(1, len(a) + 1):
                new_p[x] = (a[x-1][0], x/rank_sum)
                
            for x in range(len(a)):
                rank_sum = new_p[x + 1][1] + rank_sum
                l.append((a[x][0], rank_sum))

            for y in range(2):
                r_f = random.random()
                if r_f <= l[0][1]:
                    total_parent.append(population[l[0][0]])
                else:
                    for x in range(len(l)):
                        if r_f >= l[x][1]:
                            if r_f < l[x + 1][1]:
                                total_parent.append(population[l[x][0]])
            return total_parent

    def truncation_scheme(self, population, total_parent):

        if self.survivor_scheme == "truncation":
            new_p = {}
            a = sorted(population.values(), key = lambda x: x[0]) #https://stackoverflow.com/questions/55365106/sorting-a-list-with-sub-lists-in-python/55365159
            for x in range(self.offsprings):
                a.pop()
        
            for x in range(1, self.p_size + 1):
                new_p[x] = a[x-1]

            return new_p

        elif self.parent_scheme == "truncation":
            a = sorted(population.values(), key = lambda x: x[0], reverse = True)
            total_parent.append(a[len(a)-1])
            total_parent.append(a[len(a)-2])

            return total_parent

    def random_scheme(self, population, total_parent):

        if self.survivor_scheme == "random":
            new_p = {}
            a = list(population.values())
            for x in range(self.offsprings):
                r2 = randint(0,len(a)- 1)
                a.pop(r2)

            for x in range(1,self.p_size + 1):
                new_p[x] = a[x-1]

            return new_p

        elif self.parent_scheme == "random":
            total_parent = random.sample(list(population.values()), 2) #generate two random parents from the population

            return total_parent

    def fps_scheme(self, population, total_parent):
        new_p = {}
        temp_p = []
        new_f = []
        new_sum = 0
        f_sum = 0

        for x in range(1,len(population.keys())+1):
            f_sum = population[x][0] + f_sum

        for x, y in population.items():
            temp_p.append((x, y[0]/f_sum))

        for x in range(len(temp_p)):
            new_sum = temp_p[x][1] + new_sum
            new_f.append((temp_p[x][0], new_sum))

        if self.survivor_scheme == "fps":
            p3 = population.copy()
            for y in range(self.offsprings):
                r_f = random.random()
                if r_f <= new_f[0][1]:
                    del(p3[new_f[0][0]])
                    del(new_f[0])
                else:
                    for x in range(len(population)-y-1):
                        if r_f >= new_f[x][1]:
                            if r_f < new_f[x + 1][1]:
                                del(p3[new_f[x][0]])
                                del(new_f[x])
            count = 1
            for x in p3.values():
                new_p[count] = x
                count = count + 1

            return new_p

        elif self.parent_scheme == "fps":
            for y in range(2):
                r_f = random.random()
                if r_f <= new_f[0][1]:
                    total_parent.append(population[0+1])
                else:
                    for x in range(len(new_f)):
                        if r_f >= new_f[x][1]:
                            if r_f < new_f[x + 1][1]:
                                total_parent.append(population[x + 1])
            return total_parent

    def make_offspring(self, population):
        
        for n in range(round(self.offsprings/2)): #create 10 offsprings
            total_offspring = []
            total_parent = []

            if self.parent_scheme == "truncation":
                total_parent = self.truncation_scheme(population, total_parent)
            
            elif self.parent_scheme == "random":
                total_parent = self.random_scheme(population, total_parent)

            elif self.parent_scheme == "rbs":
                total_parent = self.rbs_scheme(population, total_parent)
            
            elif self.parent_scheme == "fps":
                total_parent = self.fps_scheme(population, total_parent)

            midpoint = round(len(total_parent[0][1])/3) 
            start = midpoint 
            end = (midpoint + midpoint) 
            total_offspring = []
            for x in range(2):
                o = []
                if x == 1:
                    v = 0
                elif x == 0:
                    v = 1
        
                o = total_parent[x][1][start:end]
                t = total_parent[v][1][end:] + total_parent[v][1][:end]

                temp = []
                for i in t:
                    if i  not in o:
                        temp.append(i)
            
                o.extend(temp[:start])
                o = temp[start:] + o
                total_offspring.append(o)

            total_offspring = self.mutation(total_offspring)

            for x in range(2):
                fitness = 0
                for n in range(len(total_offspring[x])-1): 
                    for s in adj_list[total_offspring[x][n]]:
                        if s[0] == total_offspring[x][n+1]:
                            fitness = s[1] + fitness
        
                o2 = []
                o2.extend((fitness, total_offspring[x]))
                population[len(population.keys())+1] = o2
        
        return population
        
    def mutation(self, total_offspring):
        o = random.randint(0, len(total_offspring)-1)
        m = random.random()
        s1 = 0
        s2 = 0
        if m <= self.mutation_rate:
        #do mutation
            while s1 == s2:
                s1 = randint(0, len(total_offspring[o])-1) #two random indexes
                s2 = randint(0, len(total_offspring[o])-1)
            
            q = total_offspring[o][s1] #SWAP 
            total_offspring[o][s1] = total_offspring[o][s2]
            total_offspring[o][s2] = q

        return total_offspring
            
if __name__ == '__main__':

    tsp = EA(200,"qa194.tsp", 300, "truncation", "fps", 500, 1, 0.7)
    tsp.generation_counter()
