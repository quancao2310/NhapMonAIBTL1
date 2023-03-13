from GameWorld import *
from copy import deepcopy
from collections import deque
# test
# board = {
# (0,0):2,(0,1):2,(0,2):2,
# (1,0):2,(1,1):2,(1,2):2,(1,3):2,(1,4):2,(1,5):2,
# (2,0):2,(2,1):2,(2,2):2,(2,3):2,(2,4):2,(2,5):2,(2,6):2,(2,7):2,(2,8):2,
# (3,1):2,(3,2):2,(3,3):2,(3,4):2,(3,5):2,(3,6):2,(3,7):2,(3,8):2,(3,9):2,
# (4,5):2,(4,6):2,(4,7):3,(4,8):2,(4,9):2,
# (5,6):2,(5,7):2,(5,8):2
# }
# firstCube = (1,1)
# secondCube = (1,1)
# button = {
# (2,2):[2,[(5,9),(5,10)]],
# (1,2):[1,[(0,4)]],
# (5,7):[3,[(1,1),(2,2)]]
# }
# end test
# state = (firstCube, secondCube, {newTargetOnBoard})
class Node:
    def __init__(self, state:tuple[tuple, tuple, set[tuple]], parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
    
    def key(self):
        firstCube, secondCube, targets = self.state
        targets = tuple(targets)
        return (firstCube, secondCube, targets)

    def __lt__(self, other):
        return isinstance(other, Node) and self.key() < other.key()
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.key() == other.key()
    
    def __hash__(self):
        return hash(self.key())
    
    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        new_node = Node(next_state, self, action, problem.path_cost(self.path_cost))
        return new_node
    
    def expand(self, problem):
        childNodes = []
        for action in problem.actions(self.state):
            childNodes.append(self.child_node(problem, action))
        return childNodes
    
    def path(self):
        node = self
        path = deque()
        while node:
            path.appendleft(node)
            node = node.parent
        return list(path)
    
    def solution(self):
        path = self.path()
        actions = []
        for node in path[1:]:
            actions.append(node.action)
        return actions

class BlindSearch:
    def __init__(self,cube,board):
        self.board:dict[tuple,int] = board.map.copy() #dict of tuple:int
        self.firstCube:tuple = cube.firstCube #tuple
        self.secondCube:tuple = cube.secondCube #tuple
        self.button:dict[tuple, list] = board.buttonList #dict of tuple:list
        self.initial = (self.firstCube, self.secondCube, set({}))
        goal_tile = list(self.board.keys())[list(self.board.values()).index(3)]
        self.goal = (goal_tile, goal_tile)
        ### board is a dictionary with key is a tuple of (row, col)
        ### value is a type of the brick 
        ### 0 for no brick, 1 for weak brick, 2 is normal brick, 3 is a win hole in game
        ### a tuple (row,col) is a position of firstCube
        ### a tuple (row,col) is a position of secondCube
        ### Note that when the cube is vertical firstCube == secondCube
        ### when the cube is horizontal the firstCube is always on the left or
        #  on the top of secondCube 
        ### button list is dictionary where key is a button position
        #value of key is a list with the first item is type of button, the second is the list of position
        #involve in the activation of button
    # def __init__(self, b, fc, sc, bt):
    #     self.board = b
    #     self.firstCube = fc
    #     self.secondCube = sc
    #     self.button = bt
    # state = (firstCube, secondCube, {newTargetOnBoard})
    
    def goal_test(self, state:tuple[tuple, tuple, set[tuple]]):
        return state[0:2] == self.goal
    
    def __inMap(self, tile:tuple):
        return tile in self.board and self.board[tile] != 0

    def actions(self, state:tuple) -> list:
        fc, sc, targets = state # tuple, tuple, list of tuples
        acts = []
        if fc == sc: # Dung -> Nam
            tmp_list = [
                        [(fc[0]+1, fc[1]), (fc[0]+2, fc[1])], # Down
                        [(fc[0], fc[1]+1), (fc[0], fc[1]+2)], # Right
                        [(fc[0]-2, fc[1]), (fc[0]-1, fc[1])], # Up
                        [(fc[0], fc[1]-2), (fc[0], fc[1]-1)], # Left
                        ]
            for item in tmp_list:
                new_first, new_second = item
                if self.__inMap(new_first) and self.board[new_first] != 0 and self.__inMap(new_second) and self.board[new_second] != 0:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if self.button[btn][0] == 1 and (btn == new_first or btn == new_second):
                            for tar in self.button[btn][1]:
                                if tar not in new_targets:
                                    new_targets.add(tar)
                                else:
                                    new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
        elif fc[0] + 1 == sc[0] and fc[1] == sc[1]: # Nam doc: len xuong -> Dung, trai phai -> Nam doc
            tmp_list = [
                        (sc[0]+1, sc[1]), # Down
                        (fc[0]-1, fc[1]), # Up
                        ]
            for item in tmp_list:
                new_first = item
                new_second = new_first
                if self.__inMap(new_first) and self.board[new_first] > 1:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if btn == new_first:
                            if self.button[btn][0] == 3:
                                new_first = self.button[btn][1][0]
                                new_second = self.button[btn][1][1]
                            else:
                                for tar in self.button[btn][1]:
                                    if tar not in new_targets:
                                        new_targets.add(tar)
                                    else:
                                        new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
            tmp_list = [
                        [(fc[0], fc[1]+1), (sc[0], sc[1]+1)], # Right
                        [(fc[0], fc[1]-1), (sc[0], sc[1]-1)], # Left
                        ]
            for item in tmp_list:
                new_first, new_second = item
                if self.__inMap(new_first) and self.board[new_first] != 0 and self.__inMap(new_second) and self.board[new_second] != 0:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if self.button[btn][0] == 1 and (btn == new_first or btn == new_second):
                            for tar in self.button[btn][1]:
                                if tar not in new_targets:
                                    new_targets.add(tar)
                                else:
                                    new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
        elif fc[0] == sc[0] and fc[1] + 1 == sc[1]: # Nam ngang: len xuong -> Nam ngang, trai phai -> Dung
            tmp_list = [
                        (sc[0], sc[1]+1), # Down
                        (fc[0], fc[1]-1), # Up
                        ]
            for item in tmp_list:
                new_first = item
                new_second = new_first
                if self.__inMap(new_first) and self.board[new_first] > 1:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if btn == new_first:
                            if self.button[btn][0] == 3:
                                new_first = self.button[btn][1][0]
                                new_second = self.button[btn][1][1]
                            else:
                                for tar in self.button[btn][1]:
                                    if tar not in new_targets:
                                        new_targets.add(tar)
                                    else:
                                        new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
            tmp_list = [
                        [(fc[0]+1, fc[1]), (sc[0]+1, sc[1])], # Right
                        [(fc[0]-1, fc[1]), (sc[0]-1, sc[1])], # Left
                        ]
            for item in tmp_list:
                new_first, new_second = item
                if self.__inMap(new_first) and self.board[new_first] != 0 and self.__inMap(new_second) and self.board[new_second] != 0:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if self.button[btn][0] == 1 and (btn == new_first or btn == new_second):
                            for tar in self.button[btn][1]:
                                if tar not in new_targets:
                                    new_targets.add(tar)
                                else:
                                    new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
        else: # Khoi duoc tach ra lam hai
            tmp_list = [
                        [(fc[0]+1, fc[1]), (sc[0], sc[1])], # Down1
                        [(fc[0], fc[1]+1), (sc[0], sc[1])], # Right1
                        [(fc[0]-1, fc[1]), (sc[0], sc[1])], # Up1
                        [(fc[0], fc[1]-1), (sc[0], sc[1])], # Left1
                        [(fc[0], fc[1]), (sc[0]+1, sc[1])], # Down2
                        [(fc[0], fc[1]), (sc[0], sc[1]+1)], # Right2
                        [(fc[0], fc[1]), (sc[0]-1, sc[1])], # Up2
                        [(fc[0], fc[1]), (sc[0], sc[1]-1)], # Left2
                        ]
            for item in tmp_list:
                new_first, new_second = item
                if self.__inMap(new_first) and self.board[new_first] != 0 and self.__inMap(new_second) and self.board[new_second] != 0:
                    if new_first > new_second:
                        new_first, new_second = new_second, new_first
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if self.button[btn][0] == 1 and (btn == new_first or btn == new_second):
                            for tar in self.button[btn][1]:
                                if tar not in new_targets:
                                    new_targets.add(tar)
                                else:
                                    new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
        return acts
    
    def result(self, state, action):
        return action
    
    def path_cost(self, c:int): # g function
        return c + 1
    
    def bfs(self):
        iteration = 0
        node = Node(self.initial)
        if self.goal_test(node.state):
            return node.path()
        q = deque([node])
        visited = set()
        while q:
            node = q.popleft()
            visited.add(node.key())
            iteration += 1
            for tar in node.state[2]:
                if not self.__inMap(tar):
                    self.board[tar] = 2
                else:
                    self.board.pop(tar, None)
            child:Node
            for child in node.expand(self):
                if child.key() not in visited and child not in q:
                    # print(child.key())
                    if self.goal_test(child.state):
                        print("Solution depth:", child.depth)
                        print("Number of iterations:", iteration)
                        return child.path()
                    q.append(child)
            for tar in node.state[2]:
                if self.__inMap(tar):
                    self.board.pop(tar, None)
                else:
                    self.board[tar] = 2
        return None
    
    def solve(self): 
        ### return an array of tuple that is the position of each first and second Cube
        ### for example: [[(1,1),(1,2)],[(1,3),(1,3)]]
        sol = self.bfs()
        if sol:
            res = []
            for node in sol:
                res.append(list(node.state[0:2]))
            return res
        return [[]]
    
# solver = BlindSearch(board, firstCube, secondCube, button)
# print(solver.actions(((2,5), (2,5))))
