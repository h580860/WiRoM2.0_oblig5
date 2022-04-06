from math import sqrt
import heapq

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tree:
    # def __init__(self, robot):
    def __init__(self):
        pass


def euclidean_distance(start, finish):
    return sqrt((finish.x - start.x) ** 2 + (finish.y - start.y) ** 2)


def cost_function(start, finish):
    return euclidean_distance(start, finish)


def prim_allocation(Vt, Vr, c):
    '''
    Parameters
    ----------
    Vt : list
        Vertices corresponding to the locations of the robots
    Vr : list
        Vertices corresponding to the locations of the targets
    c : function
        Cost function C
    '''
    # forest = []
    forest = {}
    # Step 1
    for robot in Vr:
        # Construct a tree
        # forest.append(Tree(robot))
        forest[robot] = Tree()
    # Step 2
    while Vt:
        break


if __name__ == '__main__':
    # example graph from the paper
    r1 = Vertex(1, 8)
    r2 = Vertex(4, 7)
    robot_locations = [r1, r2]
    g1 = Vertex(1, 0)
    g2 = Vertex(0, 4)
    g3 = Vertex(1, 12)
    g4 = Vertex(4, 12)
    targets = [g1, g2, g3, g4]

    print("Prim Allocation")
