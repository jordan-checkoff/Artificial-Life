
import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, ID):
        self.myID = ID

    def Start_Simulation(self, method):
        self.Create_World()
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
        pyrosim.Send_Cube(name="Box", pos=[-5,5,0.5], size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        self.num_links = random.randint(2, 10)
        self.sensor_locs = []
        pyrosim.Start_URDF("body.urdf")

        length = random.random() * 2
        is_sensor = random.randint(0,1)
        self.sensor_locs.append(is_sensor)
        color = [0,1,0,1, "sensor"] if is_sensor==1 else [0, 1, 1, 1, "not"]
        pyrosim.Send_Cube(name="0", pos=[0,0,0.5], size=[length, random.random()/2 + 0.5, random.random()/2 + 0.5], color=color)
        pyrosim.Send_Joint( name = "0_1" , parent= "0" , child = "1" , type = "revolute", position = [-length/2,0,0.5], jointAxis = "0 0 1")

        for i in range(1, self.num_links):
            length = random.random() * 2
            is_sensor = random.randint(0,1)
            self.sensor_locs.append(is_sensor)
            color = [0,1,0,1, "sensor"] if is_sensor==1 else [0, 1, 1, 1, "not"]
            pyrosim.Send_Cube(name=f"{i}", pos=[-length/2,0,0], size=[length, random.random()/2 + 0.5, random.random()/2 + 0.5], color=color)
            if i < self.num_links - 1:
                pyrosim.Send_Joint( name = f"{i}_{i+1}" , parent= f"{i}" , child = f"{i+1}" , type = "revolute", position = [-length,0,0], jointAxis = "0 0 1")

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        curr = 0
        for i in range(len(self.sensor_locs)):
            if self.sensor_locs[i] == 1:
                pyrosim.Send_Sensor_Neuron(name = curr , linkName = str(curr))
                curr += 1

        num_sensor_neurons = len([x for x in self.sensor_locs if x==1])

        for i in range(self.num_links - 1):
            pyrosim.Send_Motor_Neuron( name = i + num_sensor_neurons , jointName = f"{i}_{i+1}")


        self.weights = numpy.random.rand(num_sensor_neurons,self.num_links-1) * 2 - 1

        for currentRow in range(len([x for x in self.sensor_locs if x==1])):
            for currentColumn in range(self.num_links - 1):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow, targetNeuronName = currentColumn + num_sensor_neurons, weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID