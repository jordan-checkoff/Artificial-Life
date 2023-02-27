import numpy

steps = 1000
sleep = 1/500

frontAmplitude = numpy.pi / 4
frontFrequency = 10
frontPhaseOffset = numpy.pi
frontMaxForce = 50

backAmplitude = numpy.pi / 2
backFrequency = 10
backPhaseOffset = numpy.pi
backMaxForce = 50

numberOfGenerations = 10
populationSize = 2

numSensorNeurons = 13
numMotorNeurons = 12

motorJointRange = 0.25