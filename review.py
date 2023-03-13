from simulator.simulation import SIMULATION
import sys

solutionID = sys.argv[1]

simulation = SIMULATION('GUI', solutionID, "creatures/")
simulation.Run()