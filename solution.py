
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
        self.tree = TREE()


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
        self.tree.construct_body(self.myID)


    def Generate_Brain(self):
        self.tree.construct_brain(self.myID)

    def Mutate(self):
        choice = random.randint(0,6)
        if choice == 0 and len(self.tree.nodes) > 3:
            self.tree.delete_node()
        elif choice == 1:
            self.tree.add_node()
        else:
            self.tree.update_weights()

    def Set_ID(self, ID):
        self.myID = ID