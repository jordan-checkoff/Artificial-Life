
from parallelHillClimber.solution import SOLUTION
import constants as c
import copy
import os
import re

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        os.system(f"rm body*.urdf")
        os.system(f"rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system(f"rm fitness_curves/fitness_curve_{c.seed}.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        best = max([self.parents[i].fitness for i in self.parents])
        f = open(f"fitness_curves/fitness_curve_{c.seed}.txt", "a")
        f.write(f"0, {best}\n")
        f.close()

        for i in self.parents:
            os.system(f"cp body{self.parents[i].myID}.urdf creatures/body{c.seed}_{i}_{0}.nndf")
            os.system(f"cp brain{self.parents[i].myID}.nndf creatures/brain{c.seed}_{i}_{0}.urdf")

        for currentGeneration in range(c.numberOfGenerations):
            print(currentGeneration + 1)
            self.Evolve_For_One_Generation(currentGeneration + 1)

    def Evolve_For_One_Generation(self, gen):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select(gen)

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

    def Select(self, gen):
        for i in self.parents:
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
        if gen % c.pickle == 0:
            for i in self.parents:
                os.system(f"cp body{self.parents[i].myID}.urdf creatures/body{c.seed}_{i}_{gen}.urdf")
                os.system(f"cp brain{self.parents[i].myID}.nndf creatures/brain{c.seed}_{i}_{gen}.nndf")
        best = max([self.parents[i].fitness for i in self.parents])
        f = open(f"fitness_curves/fitness_curve_{c.seed}.txt", "a")
        f.write(f"{gen}, {best}\n")
        f.close()

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