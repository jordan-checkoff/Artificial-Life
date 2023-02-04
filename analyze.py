import numpy
import matplotlib.pyplot as plt

frontLegSensorValues = numpy.load("./data/frontLegSensorValues.npy")
backLegSensorValues = numpy.load("./data/backLegSensorValues.npy")

plt.plot(frontLegSensorValues, label="Front Leg", linewidth=3)
plt.plot(backLegSensorValues, label="Back Leg")
plt.legend()
plt.show()