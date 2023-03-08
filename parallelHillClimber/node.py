import random

class NODE:

    def __init__(self, name, parent, rng):
        self.name = name
        self.size = [random.random(), random.random(), random.random()]
        self.attachments = [None] * 6
        self.add_link(parent)
        self.generate_position(parent)
        self.is_sensor = random.randint(0, 1)
        self.axes = rng.integers(0, 2, size=6, endpoint=True)

    def has_children(self):
        count = 0
        for attachment in self.attachments:
            if attachment:
                count += 1
                if count == 2:
                    return True
        return False

    def full(self):
        if len(set(self.attachments)) == 1 and self.attachments[0]:
            return True
        return False

    def get_empty_pos(self):
        start = random.randint(0, 5)
        while self.attachments[start]:
            start = (start + 1) % 6
        return start
    
    def add_link(self, parent):
        if parent:
            pos = parent.get_empty_pos()
            parent.attachments[pos] = self
            self.parent_side = 5 - pos
            self.attachments[self.parent_side] = parent
        else:
            self.parent_side = None

    def generate_position(self, parent):
        if parent == None:
            self.pos = [0, 0, random.random()]
        elif self.parent_side == 0:
            self.pos = [parent.pos[0] - parent.size[0]/2 - self.size[0]/2, parent.pos[1], parent.pos[2]]
        elif self.parent_side == 1:
            self.pos = [parent.pos[0], parent.pos[1] - parent.size[1]/2 - self.size[1]/2, parent.pos[2]]
        elif self.parent_side == 2:
            self.pos = [parent.pos[0], parent.pos[1], parent.pos[2] - parent.size[2]/2 - self.size[2]/2]
        elif self.parent_side == 3:
            self.pos = [parent.pos[0], parent.pos[1], parent.pos[2] + parent.size[2]/2 + self.size[2]/2]
        elif self.parent_side == 4:
            self.pos = [parent.pos[0], parent.pos[1] + parent.size[1]/2 + self.size[1]/2, parent.pos[2]]
        else:
            self.pos = [parent.pos[0] + parent.size[0]/2 + self.size[0]/2, parent.pos[1], parent.pos[2]]

    def get_relative_joint_position(self, face, reference):
        absolute_pos = self.get_absolute_joint_position(face)
        return get_relative_location(absolute_pos, reference)

    def get_absolute_joint_position(self, face):
        if face == 0 : return [self.pos[0] + self.size[0]/2, self.pos[1], self.pos[2]]
        if face == 1 : return [self.pos[0], self.pos[1] + self.size[1]/2, self.pos[2]]
        if face == 2 : return [self.pos[0], self.pos[1], self.pos[2] + self.size[2]/2]
        if face == 3 : return [self.pos[0], self.pos[1], self.pos[2] - self.size[2]/2]
        if face == 4 : return [self.pos[0], self.pos[1] - self.size[1]/2, self.pos[2]]
        if face == 5 : return [self.pos[0] - self.size[0]/2, self.pos[1], self.pos[2]]

    def get_relative_position(self, reference):
        return get_relative_location(self.pos, reference)

    def is_root(self):
        return self.parent_side is None

    def is_parent_face(self, i):
        if not self.is_root() and self.parent_side == i:
            return True
        else:
            return False
        
    def is_underground(self):
        return self.pos[2] - self.size[2] / 2 < 0
    
    def delete(self):
        parent = self.attachments[self.parent_side]
        parent.attachments[5 - self.parent_side] = None

    def get_min_max(self):
        return  { 'min_x': self.pos[0] - self.size[0] / 2,
        'max_x': self.pos[0] + self.size[0] / 2,
        'min_y': self.pos[1] - self.size[1] / 2,
        'max_y': self.pos[1] + self.size[1] / 2,
        'min_z': self.pos[2] - self.size[2] / 2,
        'max_z': self.pos[2] + self.size[2] / 2}


## https://stackoverflow.com/questions/6008206/detect-overlapping-of-rectangular-prisms

    def overlaps(self, node):
        pos_a = self.get_min_max()
        pos_b = node.get_min_max()
        if pos_a['min_x'] < pos_b['max_x'] and pos_a['max_x'] > pos_b['min_x']:
            if pos_a['min_y'] < pos_b['max_y'] and pos_a['max_y'] > pos_b['min_y']:
                if pos_a['min_z'] < pos_b['max_z'] and pos_a['max_z'] > pos_b['min_z']:
                    return True
        
def get_relative_location(pos, reference):
    return [pos[0] - reference[0], pos[1] - reference[1], pos[2] - reference[2]]