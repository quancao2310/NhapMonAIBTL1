from numpy import sin as sin
from numpy import cos as cos
from numpy import pi as pi
class Setting:
    def __init__(self):
        self.cellWidth = 40
        self.alpha = pi/3
        self.dx=self.cellWidth*cos(self.alpha)
        self.dy=self.cellWidth*sin(self.alpha)
        self.color = ['#630900','#FA9363','#C3CCD7','#4DC726']
        self.cubeColor = 'black'
        self.boardSize = 13
        self.screenWidth = int((self.boardSize+2)*self.cellWidth+(self.boardSize+1)*self.dx)
        self.screenHeight = int((self.boardSize+4)*self.dy)