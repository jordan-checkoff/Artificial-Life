
import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
from tree import TREE

class SOLUTION:

    def __init__(self, ID):
        self.myID = ID

    def Start_Simulation(self, method):
        # self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        # os.system("python simulate.py " + method + " " + str(self.myID) + " &")
        os.system("python simulate.py " + method + " " + str(self.myID) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system(f"rm fitness{self.myID}.txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[-5,5,0.5], size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        self.tree = TREE()
        self.tree.construct_body()


    def Generate_Brain(self):
        self.tree.construct_brain(self.myID)

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID