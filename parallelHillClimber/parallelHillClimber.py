
from solution import SOLUTION
import constants as c
import copy
import os
import re

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        os.system("rm body*.urdf")
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm fitness_curve.txt")
        self.parents = {}
        self.nextAvailableID = 0
        self.currGeneration = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        best = max([self.parents[i].fitness for i in self.parents])
        f = open(f"fitness_curve.txt", "a")
        f.write(f"{self.currGeneration} {best}\n")
        f.close()
        self.currGeneration += 1

        for currentGeneration in range(c.numberOfGenerations):
            print(currentGeneration)
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children:
            self.children[i].Mutate()

    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()

    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
        best = max([self.parents[i].fitness for i in self.parents])
        f = open(f"fitness_curve.txt", "a")
        f.write(f"{self.currGeneration} {best}\n")
        f.close()
        self.currGeneration += 1

    def Print(self):
        print("\n")
        for i in self.parents:
            print(self.parents[i].fitness, self.children[i].fitness)
        print("\n")

    def Show_Best(self):
        best = self.parents[0].fitness
        index = 0
        for i in self.parents:
            if self.parents[i].fitness > best:
                best = self.parents[i].fitness
                index = i
        os.system("python simulate.py GUI 0")
        self.parents[index].Start_Simulation("GUI")
        id = self.parents[index].myID
        for file in os.listdir():
            if re.search("^body.*urdf", file) and not file == f"body{id}.urdf" and not file == f"body0.urdf":
                os.system(f"rm {file}")
            elif re.search("^brain.*nndf", file) and not file == f"brain{id}.nndf" and not file == f"brain0.nndf":
                os.system(f"rm {file}")