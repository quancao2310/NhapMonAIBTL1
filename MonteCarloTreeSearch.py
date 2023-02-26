from GameWorld import *

class MonterCarloTreeSearch:
    def __init__(self,cube,board):
        self.board = board.map
        self.firstCube = cube.firstCube
        self.secondCube = cube.secondCube
        ### board is a dictionary with key is a tuple of (row, col)
        ### value is a type of the brick 
        ### 0 for no brick, 1 for weak brick, 2 is normal brick, 3 is a win hole in game
        ### a tuple (row,col) is a position of firstCube
        ### a tuple (row,col) is a position of secondCube
        ### Note that when the cube is vertical firstCube == secondCube
        ### when the cube is horizontal the firstCube is always on the left or
        #  on the top of secondCube 
    def solve(self): 
        ### return a array of tupple is the position of each first and second Cube
        ### for example: [[(1,1),(1,2)],[(1,3),(1,3)]]
        return [[]]