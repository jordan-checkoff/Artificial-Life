from node import NODE
from random import randint, random, seed
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class TREE:

    def __init__(self):
        self.rng = numpy.random.default_rng(c.seed)
        seed(c.seed)
        self.root = NODE(0, None)
        while self.root.is_underground():
            self.root = NODE(0, None)
        self.nodes = [self.root]
        self.num_nodes = randint(5, 10)
        self.next_node = self.num_nodes
        for i in range(1, self.num_nodes):
            rand = randint(0, i-1)
            parent = self.nodes[rand]
            while parent.full():
                parent = self.nodes[randint(0, i-1)]
            newnode = NODE(i, parent)
            while newnode.is_underground() or self.overlaps(newnode):
                newnode.delete()
                newnode = NODE(i, parent)
            self.nodes.append(newnode)
        self.num_sensor_neurons = len([node.name for node in self.nodes if node.is_sensor])
        self.weights = self.rng.random(size=(self.num_sensor_neurons, self.num_nodes)) * 2 - 1
        self.axes = self.rng.integers(0, 2, size=6, endpoint=True)

    def add_node(self):
        rand = randint(0, self.num_nodes - 1)
        parent = self.nodes[rand]
        while parent.full():
            parent = self.nodes[randint(0, self.num_nodes - 1)]
        newnode = NODE(self.next_node, parent)
        while newnode.is_underground() and self.overlaps(newnode):
            newnode.delete()
            newnode = NODE(self.next_node, parent)
        self.nodes.append(newnode)
        self.next_node += 1
        self.num_nodes += 1
        if newnode.is_sensor:
            self.num_sensor_neurons += 1
            self.weights = numpy.append(self.weights, self.rng.random(size=(1, self.num_nodes-1)) * 2 - 1, axis=0)
            self.weights = numpy.append(self.weights, self.rng.random(size=(self.num_sensor_neurons, 1)) * 2 - 1, axis=1)
        else:
            self.weights = numpy.append(self.weights, self.rng.random(size=(self.num_sensor_neurons, 1)) * 2 - 1, axis=1)

    def delete_node(self):
        random_node = randint(0, self.num_nodes - 1)
        while self.nodes[random_node].has_children() or self.nodes[random_node].is_root():
            random_node = randint(0, self.num_nodes - 1)
        sensor_pos = [node.name for node in self.nodes if node.is_sensor].index(self.nodes[random_node].name) if self.nodes[random_node].is_sensor else 0
        self.nodes[random_node].delete()
        done = self.nodes.pop(random_node)
        self.num_nodes -= 1
        if done.is_sensor:
            self.num_sensor_neurons -= 1
            self.weights = numpy.delete(self.weights, sensor_pos, 0)
        self.weights = numpy.delete(self.weights, random_node, 1)


    def update_weights(self):
        self.weights[randint(0,self.num_sensor_neurons - 1), randint(0,self.num_nodes - 1)] = random() * 2 - 1

    def construct_body(self, myId):
        pyrosim.Start_URDF(f"body{myId}.urdf")
        construct_helper(self.root, [0,0,0], self.axes)
        pyrosim.End()

    def overlaps(self, newnode):
        for node in self.nodes:
            if newnode.overlaps(node):
                return True
        return False
    
    def construct_brain(self, myId):
        pyrosim.Start_NeuralNetwork(f"brain{myId}.nndf")
        sensor_neurons = [node.name for node in self.nodes if node.is_sensor]

        self.i = 0

        for neuron in sensor_neurons:
            pyrosim.Send_Sensor_Neuron(name = self.i, linkName = str(neuron))
            self.i += 1

        self.add_motor_neurons(self.root)

        for currentRow in range(len(sensor_neurons)):
            for currentColumn in range(self.num_nodes):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow, targetNeuronName = currentColumn + len(sensor_neurons), weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()



    def add_motor_neurons(self, node):
        for i in range(6):
            if node.is_parent_face(i):
                continue
            if node.attachments[i]:
                child = node.attachments[i]
                pyrosim.Send_Motor_Neuron( name = f"{self.i}" , jointName = f"{node.name}_{child.name}")
                self.i += 1
                self.add_motor_neurons(node.attachments[i])


def construct_helper(node, reference, axes):
    color = [0,1,0,1, "sensor"] if node.is_sensor == 1 else [0, 1, 1, 1, "not"]
    pyrosim.Send_Cube(name=f"{node.name}", pos=node.get_relative_position(reference), size=node.size, color=color)
    for i in range(6):
        if node.is_parent_face(i):
            continue
        if node.attachments[i]:
            child = node.attachments[i]
            relative_joint_position = node.get_relative_joint_position(i, reference)
            absolute_joint_position = node.get_absolute_joint_position(i)
            axis = ["1 0 0", "0 1 0", "0 0 1"][axes[i]]
            pyrosim.Send_Joint( name = f"{node.name}_{child.name}" , parent= f"{node.name}" , child = f"{child.name}" , type = "revolute", position = relative_joint_position, jointAxis = axis)
            construct_helper(child, absolute_joint_position, axes)