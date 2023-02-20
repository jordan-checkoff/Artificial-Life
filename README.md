# Artificial-Life

## Morphospace
My simulator creates creatures with the following morphologies:
* Each creature contains between 5-10 links
* Each link is a rectangular prism with each dimension between 0-1 units
* Each link can have at most one joint on each of its faces
* Two links that connect at a joint do so at the center of two of their faces

My simulator creates creatures with the following neural networks:
* Links are randomly assigned as sensor neurons or not
* Every joint is a motor neuron
* There is a synapse with a randomly generated weight connecting each sensor neuron to each motor neuron

## Method
In order to randomly design a creature without any overlapping links, I created a Tree class and a Node class to first represent the creature's morphology with a tree, where each node represents one of the creature's links. This allowed me to develop a random hierarchy of parent-child relationships, which worked nicely with the parent-child relationships of pyrosim's joints. Once complete, I iterated over the tree to add in each link, joint and neuron. This is represented in the following diagram.

![alt text](/diagram.png)

### Creating the tree representation
Upon initialization, the Tree class randomly generates a tree for representing the creature's morphology using the following algorithm:
1. The Tree creates a root node, which is initalized with a random position and size, and creates a list called self.nodes with it as the sole item.
2. A random number between 5 and 10 is chosen for the number of additional nodes to add.
3. To add a new node, a random node is first chosen from self.nodes. This will be the parent of the new node.
4. If the parent node is already connected to 6 other nodes (one on each face), return to step 3 to pick a new parent.
5. Generate a new node with a random size and a random position such that it is connected to the parent node on a randomly chosen face
6. If this new node is underground or overlaps with any other node, return to step 5 to redesign the node.
7. Add the new node to self.nodes.
8. Repeat steps 3-7 based on the number selected in step 2.

### Creating the body and brain from the tree representation
Once the tree is complete, the body and brain can be created with pyrosim using the following algorithm:
1. To add each link and join, call the Send_Cube function for the root node. For each child of the root node, use Send_Link to add the appropriate joint and repeat for that child.
2. To add the sensor neurons, iterate over self.nodes. If the node is assigned to be a sensor neuron, call Send_Sensor_Neuron for the link reprsented by that node.
3. To add the motor neurons, iterate over self.nodes. For all nodes, call Send_Motor_Neuron for the joint comprised of that node and its parent.
4. To add the synapses, call Send_Synapse for each pair of sensor and motor neurons

## Sources
This project was developed with the help of the Ludobots course on reddit: https://www.reddit.com/r/ludobots/
