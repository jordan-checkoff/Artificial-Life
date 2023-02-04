
import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, ID):
        self.weights = numpy.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1
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
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,0.5], size=[2,0.5,0.5])

        pyrosim.Send_Joint( name = "Torso_FrontLeftLeg" , parent= "Torso" , child = "FrontLeftLeg" , type = "revolute", position = [-0.5,-0.25,0.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeftLeg", pos=[0,-0.25,0], size=[0.2,0.5,0.2])
        pyrosim.Send_Joint( name = "Torso_MiddleLeftLeg" , parent= "Torso" , child = "MiddleLeftLeg" , type = "revolute", position = [0,-0.25,0.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="MiddleLeftLeg", pos=[0,-0.25,0], size=[0.2,0.5,0.2])
        pyrosim.Send_Joint( name = "Torso_BackLeftLeg" , parent= "Torso" , child = "BackLeftLeg" , type = "revolute", position = [0.5,-0.25,0.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeftLeg", pos=[0,-0.25,0], size=[0.2,0.5,0.2])
        
        pyrosim.Send_Joint( name = "Torso_FrontRightLeg" , parent= "Torso" , child = "FrontRightLeg" , type = "revolute", position = [-0.5,0.25,0.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontRightLeg", pos=[0,0.25,0], size=[0.2,0.5,0.2])
        pyrosim.Send_Joint( name = "Torso_MiddleRightLeg" , parent= "Torso" , child = "MiddleRightLeg" , type = "revolute", position = [0,0.25,0.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="MiddleRightLeg", pos=[0,0.25,0], size=[0.2,0.5,0.2])
        pyrosim.Send_Joint( name = "Torso_BackRightLeg" , parent= "Torso" , child = "BackRightLeg" , type = "revolute", position = [0.5,0.25,0.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackRightLeg", pos=[0,0.25,0], size=[0.2,0.5,0.2])
        
        pyrosim.Send_Joint( name = "FrontLeftLeg_FrontLeftFoot", parent= "FrontLeftLeg" , child = "FrontLeftFoot" , type = "revolute", position = [0,-0.5,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeftFoot", pos=[0,0,-0.25], size=[0.2,0.2,0.5])
        pyrosim.Send_Joint( name = "MiddleLeftLeg_MiddleLeftFoot", parent= "MiddleLeftLeg" , child = "MiddleLeftFoot" , type = "revolute", position = [0,-0.5,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="MiddleLeftFoot", pos=[0,0,-0.25], size=[0.2,0.2,0.5])
        pyrosim.Send_Joint( name = "BackLeftLeg_BackLeftFoot", parent= "BackLeftLeg" , child = "BackLeftFoot" , type = "revolute", position = [0,-0.5,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeftFoot", pos=[0,0,-0.25], size=[0.2,0.2,0.5])

        pyrosim.Send_Joint( name = "FrontRightLeg_FrontRightFoot", parent= "FrontRightLeg" , child = "FrontRightFoot" , type = "revolute", position = [0,0.5,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontRightFoot", pos=[0,0,-0.25], size=[0.2,0.2,0.5])
        pyrosim.Send_Joint( name = "MiddleRightLeg_MiddleRightFoot", parent= "MiddleRightLeg" , child = "MiddleRightFoot" , type = "revolute", position = [0,0.5,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="MiddleRightFoot", pos=[0,0,-0.25], size=[0.2,0.2,0.5])
        pyrosim.Send_Joint( name = "BackRightLeg_BackRightFoot", parent= "BackRightLeg" , child = "BackRightFoot" , type = "revolute", position = [0,0.5,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackRightFoot", pos=[0,0,-0.25], size=[0.2,0.2,0.5])
        
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "MiddleLeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "BackLeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "FrontRightLeg")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "MiddleRightLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "BackRightLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "FrontLeftFoot")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "MiddleLeftFoot")
        pyrosim.Send_Sensor_Neuron(name = 9 , linkName = "BackLeftFoot")
        pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "FrontRightFoot")
        pyrosim.Send_Sensor_Neuron(name = 11 , linkName = "MiddleRightFoot")
        pyrosim.Send_Sensor_Neuron(name = 12 , linkName = "BackRightFoot")

        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "Torso_FrontLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "Torso_MiddleLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "Torso_BackLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "Torso_FrontRightLeg")
        pyrosim.Send_Motor_Neuron( name = 17 , jointName = "Torso_MiddleRightLeg")
        pyrosim.Send_Motor_Neuron( name = 18 , jointName = "Torso_BackRightLeg")
        pyrosim.Send_Motor_Neuron( name = 19 , jointName = "FrontLeftLeg_FrontLeftFoot")
        pyrosim.Send_Motor_Neuron( name = 20 , jointName = "MiddleLeftLeg_MiddleLeftFoot")
        pyrosim.Send_Motor_Neuron( name = 21 , jointName = "BackLeftLeg_BackLeftFoot")
        pyrosim.Send_Motor_Neuron( name = 22 , jointName = "FrontRightLeg_FrontRightFoot")
        pyrosim.Send_Motor_Neuron( name = 23 , jointName = "MiddleRightLeg_MiddleRightFoot")
        pyrosim.Send_Motor_Neuron( name = 24 , jointName = "BackLeftLeg_BackLeftFoot")


        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID