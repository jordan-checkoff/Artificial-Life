import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

length = 1
width = 1
height = 1

x = 0
y = 0
z = 0.5

for j in range(5):
  for k in range(5):
    curr = 0
    for i in range(10):
      pyrosim.Send_Cube(name="Box", pos=[j,k,curr + 0.9**i*length/2], size=[0.9**i*length,0.9**i*width,0.9**i*height])
      curr += 0.9**i

pyrosim.End()
