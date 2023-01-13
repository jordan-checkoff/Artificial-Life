import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import random
import matplotlib.pyplot as plt

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

frontLegSensorValues = numpy.zeros(1000)
backLegSensorValues = numpy.zeros(1000)

frontAmplitude = numpy.pi / 4
frontFrequency = 10
frontPhaseOffset = numpy.pi

backAmplitude = numpy.pi / 2
backFrequency = 10
backPhaseOffset = numpy.pi

frontTargetAngles = frontAmplitude * numpy.sin(numpy.linspace(0, 1000, 1000) / 1000 * 2 * numpy.pi * frontFrequency + frontPhaseOffset)

backTargetAngles = backAmplitude * numpy.sin(numpy.linspace(0, 1000, 1000) / 1000 * 2 * numpy.pi * backFrequency + backPhaseOffset)

# plt.plot(targetAngles)
# plt.show()
# exit()

for i in range(1000):
  p.stepSimulation()

  frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
  backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")

  pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b'Torso_FrontLeg',
    controlMode = p.POSITION_CONTROL,
    targetPosition = frontTargetAngles[i],
    maxForce = 50)
  pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b'Torso_BackLeg',
    controlMode = p.POSITION_CONTROL,
    targetPosition = backTargetAngles[i],
    maxForce = 50)

  time.sleep(1/360)

numpy.save("./data/frontLegSensorValues.npy", frontLegSensorValues)
numpy.save("./data/backLegSensorValues.npy", backLegSensorValues)

p.disconnect()
