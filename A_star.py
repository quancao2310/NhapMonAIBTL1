from GameWorld import *
from copy import deepcopy
from collections import deque
from heapq import *
class A_star:
    """
    The model of the Bloxorz problem and A* Search implementation to solve it.
    """
    def __init__(self,cube,board):
        """
        The board is a dictionary. Each key is a tuple of 2 integers (row, col) that represent the coordinate
        of a tile on the board. The value of the key is an integer which represent its tile type.
        There are 3 tile types: 1 - weak tile, 2 - normal tile, 3 - goal tile.
        If a coordinate has a value of 0 or it does not appear in the dictionary, it will be
        seen as if there is no tile on that coordinate.

        Each state of the game contains the coordinates of the block (firstCube and secondCube) and a set of tiles
        that is influenced by the buttons. If a button is clicked, the tiles activated will be added to this set 
        and passed down to its children. For the simplification of the problem, the firstCube coordinate will always
        be smaller than the secondCube coordinate. The initial state contains the initial coordinates and an empty set.
        
        The button/switch list is a dictionary. Each key is the position of the button (a tuple of 2 integers) 
        and its value is a list of 2 items. The first item is the type of button: 1 - soft button (X shape), 
        2 - heavy button (O shape), 3 - teleport button (() shape). The second item is the list of position influenced
        by that button.
        """
        self.board = board.map.copy()
        self.firstCube = cube.firstCube
        self.secondCube = cube.secondCube
        self.button = board.buttonList
        self.initial = (self.firstCube, self.secondCube, set({}))
        goal_tile = list(self.board.keys())[list(self.board.values()).index(3)]
        self.goal = (goal_tile, goal_tile)
    
    def __goal_test(self, state):
        return state[0:2] == self.goal
    
    def __in_board(self, tile:tuple):
        return tile in self.board and self.board[tile] != 0
    
    def child_states(self, state:tuple[tuple, tuple, set[tuple]]) -> list:
        fc, sc, targets = state
        acts = []
        if fc == sc: # Standing -> Lying
            tmp_list = [
                        [(fc[0]+1, fc[1]), (fc[0]+2, fc[1])], # Down
                        [(fc[0], fc[1]+1), (fc[0], fc[1]+2)], # Right
                        [(fc[0]-2, fc[1]), (fc[0]-1, fc[1])], # Up
                        [(fc[0], fc[1]-2), (fc[0], fc[1]-1)], # Left
                        ]
            for item in tmp_list:
                new_first, new_second = item
                if self.__in_board(new_first) and self.board[new_first] != 0 and self.__in_board(new_second) and self.board[new_second] != 0:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if self.button[btn][0] == 1 and (btn == new_first or btn == new_second):
                            for tar in self.button[btn][1]:
                                if tar not in new_targets:
                                    new_targets.add(tar)
                                else:
                                    new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
        elif fc[0] + 1 == sc[0] and fc[1] == sc[1]: # Lying vertically: Up Down -> Standing, Left Right -> Lying vertically
            tmp_list = [
                        (sc[0]+1, sc[1]), # Down
                        (fc[0]-1, fc[1]), # Up
                        ]
            for item in tmp_list:
                new_first = item
                new_second = new_first
                if self.__in_board(new_first) and self.board[new_first] > 1:
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
                if self.__in_board(new_first) and self.board[new_first] != 0 and self.__in_board(new_second) and self.board[new_second] != 0:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if self.button[btn][0] == 1 and (btn == new_first or btn == new_second):
                            for tar in self.button[btn][1]:
                                if tar not in new_targets:
                                    new_targets.add(tar)
                                else:
                                    new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
        elif fc[0] == sc[0] and fc[1] + 1 == sc[1]: # Lying horizontally: Up Down -> Lying horizontally, Left Right -> Standing
            tmp_list = [
                        (sc[0], sc[1]+1), # Right
                        (fc[0], fc[1]-1), # Left
                        ]
            for item in tmp_list:
                new_first = item
                new_second = new_first
                if self.__in_board(new_first) and self.board[new_first] > 1:
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
                        [(fc[0]+1, fc[1]), (sc[0]+1, sc[1])], # Down
                        [(fc[0]-1, fc[1]), (sc[0]-1, sc[1])], # Up
                        ]
            for item in tmp_list:
                new_first, new_second = item
                if self.__in_board(new_first) and self.board[new_first] != 0 and self.__in_board(new_second) and self.board[new_second] != 0:
                    new_targets = deepcopy(targets)
                    for btn in self.button:
                        if self.button[btn][0] == 1 and (btn == new_first or btn == new_second):
                            for tar in self.button[btn][1]:
                                if tar not in new_targets:
                                    new_targets.add(tar)
                                else:
                                    new_targets.discard(tar)
                    acts.append((new_first, new_second, new_targets))
        else: # Separation and Teleportation
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
                if self.__in_board(new_first) and self.board[new_first] != 0 and self.__in_board(new_second) and self.board[new_second] != 0:
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
    
    def g(self, node):
        """Return the total cost of the node, which is also its depth in the search tree."""
        return node.depth
    
    def h(self, node):
        """Return the heuristic value from this node to goal. The chosen heuristic function is
        the maximum of Manhattan distances of 2 cubes"""
        fc, sc = node.state[0:2]
        return max(
            abs(fc[0] - self.goal[0][0]) + abs(fc[1] - self.goal[0][1]),
            abs(sc[0] - self.goal[1][0]) + abs(sc[1] - self.goal[1][1])
        )
    
    def h1(self, node):
        fc, sc = node.state[0:2]
        return abs(fc[0] - self.goal[0][0]) + abs(fc[1] - self.goal[0][1]) + abs(sc[0] - self.goal[1][0]) + abs(sc[1] - self.goal[1][1])
    
    def h2(self, node):
        fc, sc = node.state[0:2]
        return np.sqrt((abs(fc[0] - self.goal[0][0]) + abs(fc[1] - self.goal[0][1]))**2 + (abs(sc[0] - self.goal[1][0]) + abs(sc[1] - self.goal[1][1]))**2)
    
    def h_avg(self, node):
        return (self.h(node)+ self.h1(node)+ self.h2(node))/3
    
    def f(self, node):
        """Return estimated score for A* algorithm."""
        return self.g(node) + self.h(node)
    
    def __priority_in_pq(self, pq, node):
        """If the pq (priority queue) contains the node, return f score of that node in the pq.
        Otherwise, return -1, which indicates that the node is not in the pq."""
        for item in pq:
            if node == item[1]:
                return item[0]
        return -1

    def a_star(self):
        iteration = 0
        node = self.Node(self.initial)
        q = []
        heappush(q, (self.f(node), node))
        visited = set()
        while q:
            node = heappop(q)[1]
            iteration += 1
            if self.__goal_test(node.state):
                print("Solution depth:", node.depth)
                print("Number of states traversed:", iteration)
                return node.path()
            visited.add(node.key())
            tmp = {}
            for tar in node.state[2]:
                if not self.__in_board(tar):
                    self.board[tar] = 2
                else:
                    tmp[tar] = self.board[tar]
                    self.board.pop(tar, None)
            for child in node.expand(self):
                priority = self.__priority_in_pq(q, child)
                if child.key() not in visited and priority == -1:
                    heappush(q, (self.f(child), child))
                elif priority != -1 and self.f(child) < priority:
                    q.remove((priority, child))
                    heapify(q)
                    heappush(q, (self.f(child), child))
            for tar in node.state[2]:
                if self.__in_board(tar):
                    self.board.pop(tar, None)
                else:
                    self.board[tar] = tmp[tar]
        return None
    
    def solve(self):
        ### return a array of tupple is the position of each first and second Cube
        ### for example: [[(1,1),(1,2)],[(1,3),(1,3)]]
        sol = self.a_star()
        if sol:
            res = []
            for node in sol:
                res.append(list(node.state[0:2]))
            return res
        return [[]]
    
    def test(self):
        a = self.Node(((1,2), (1,2), {(1,3)}))
        b = self.Node(((1,2), (1,2), {(1,3)}), a)
        print(a == b)

    class Node:
        def __init__(self, state:tuple[tuple, tuple, set[tuple]], parent=None):
            self.state = state
            self.parent = parent
            self.depth = 0
            if parent:
                self.depth = parent.depth + 1
        
        def key(self):
            firstCube, secondCube, targets = self.state
            targets = tuple(targets)
            return (firstCube, secondCube, targets)
        
        def __lt__(self, other):
            if not isinstance(other, A_star.Node):
                raise TypeError("Comparison can only be done for Node instances")
            return self.key() < other.key()

        def __eq__(self, other):
            return isinstance(other, A_star.Node) and self.key() == other.key()
        
        def __hash__(self):
            return hash(self.key())
        
        def child_node(self, next_state):
            return A_star.Node(next_state, self)
        
        def expand(self, problem) -> list:
            childNodes = []
            for child_state in problem.child_states(self.state):
                childNodes.append(self.child_node(child_state))
            return childNodes
        
        def path(self):
            node = self
            path = deque()
            while node:
                path.appendleft(node)
                node = node.parent
            return list(path)
        
