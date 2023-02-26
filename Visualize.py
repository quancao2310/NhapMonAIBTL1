from Setting import *
from GameWorld import *
from TestCaseConfig import TestCase
import pygame as pg
class Game:
    def __init__(self, setting):
        pg.init()
        self.setting = setting
        self.screen = pg.display.set_mode((setting.screenWidth,setting.screenHeight))
        self.clock = pg.time.Clock()
        self.testCase = 0
        self.board = 0
        self.cube = 0
    def loadTestCase(self, testCase):
        self.testCase = testCase
        self.board = Board(self)
        self.cube = Cube(self)

    def chooseMode(self):
        message = """Please choose mode:
        Press 1 to play by your self
        Press 2 to test blind search algorithm
        Press 3 to test A* algorithm
        Press 4 to test Monte Carlo Tree Search algorithm
        press 0 to quit
        """
        font = pg.font.SysFont(None, 30)
        lines = message.split('\n')
        text = []
        for line in lines:
            text.append(font.render(line, True, pg.Color('White')))
        total_height = sum([text[i].get_height() for i in range(len(text))])
        self.screen.fill(pg.Color(self.setting.color[0]))
        y = (self.setting.screenHeight - total_height) // 2
        for i in range(len(text)):
            x = self.setting.dx
            self.screen.blit(text[i], (x, y))
            y += text[i].get_height()
        pg.display.update()
        looping=True
        while looping:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    looping = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        return 1
                    elif event.key == pg.K_2:
                        return 2
                    elif event.key == pg.K_3:
                        return 3
                    elif event.key == pg.K_4:
                        return 4
                    elif event.key == pg.K_0:
                        return 0
        return 0

    def gameStart(self, mode):
        looping = True
        if mode == 0:
            looping = False
        while looping:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    looping = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        looping = self.cube.move(mode,'w')
                    elif event.key == pg.K_s:
                        looping = self.cube.move(mode,'s')
                    elif event.key == pg.K_d:
                        looping = self.cube.move(mode,'d')
                    elif event.key == pg.K_a:
                        looping = self.cube.move(mode,'a')
             
            self.screen.fill(self.setting.color[0])
            if (self.cube.firstCube not in self.board.map.keys()) or (self.cube.secondCube not in self.board.map.keys()) or (self.board.map[self.cube.firstCube]==0) or (self.board.map[self.cube.secondCube]==0):
                print("You lose")
                looping=False
            elif ((self.cube.firstCube == self.cube.secondCube) and (self.board.map[self.cube.secondCube]==3)):
                print("You win")
                looping=False
            elif (self.cube.firstCube == self.cube.secondCube) and (self.board.map[self.cube.firstCube]==1):
                print("You lose")
                looping=False
            if mode != 1:
                looping = self.cube.move(mode)
            self.board.draw()
            self.cube.draw()
            pg.display.update()
            self.clock.tick(60)
        pg.time.delay(1000)

            
            

def main():
    testboard1 = {
            (0, 0):2,(0, 1):2,(0, 2):2,
            (1, 0):2,(1, 1):2,(1, 2):2,(1, 3):2,(1, 4):2,(1, 5):2,
            (2, 0):2,(2, 1):2,(2, 2):2,(2, 3):2,(2, 4):2,(2, 5):2,(2, 6):2,(2, 7):2,(2, 8):2,
            (3, 1):2,(3, 2):2,(3, 3):2,(3, 4):2,(3, 5):2,(3, 6):2,(3, 7):2,(3, 8):2,(3, 9):2,
            (4, 5):2,(4, 6):2,(4, 7):3,(4, 8):2,(4, 9):2,
            (5, 6):2,(5, 7):2,(5, 8):2
            }
    cubePos = [(1,1),(1,1)]
    setting=Setting()
    testCase = TestCase('Input.txt')
    pg.display.set_caption("Visualization")
    game = Game(setting)
    mode = game.chooseMode()
    while testCase.isNotEmpty():
        game.loadTestCase(testCase.getTestCase())
        game.gameStart(mode)
if __name__ == "__main__":
    main()
