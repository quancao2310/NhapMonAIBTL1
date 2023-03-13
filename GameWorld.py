from Visualize import Game
from Setting import *
import pygame as pg
import numpy as np
from MonteCarloTreeSearch import MonterCarloTreeSearch
from BlindSearch import BlindSearch
from A_star import A_star

class Board:
    def __init__(self, game):
        self.map = game.testCase[0]
        self.buttonList = game.testCase[2]
        self.screen = game.screen
        self.color = game.setting.color
        self.cellWidth = game.setting.cellWidth
        self.alpha = game.setting.alpha
        self.dx = game.setting.dx
        self.dy = game.setting.dy
        self.basePoint = (self.cellWidth,3*self.dy)
    def draw(self):
        for cell, value in self.map.items():
            points = [
                        (self.basePoint[0]+cell[0]*self.dx+cell[1]*self.cellWidth,self.basePoint[1]+cell[0]*self.dy),
                        (self.basePoint[0]+cell[0]*self.dx+(cell[1]+1)*self.cellWidth,self.basePoint[1]+cell[0]*self.dy),
                        (self.basePoint[0]+(cell[0]+1)*self.dx+(cell[1]+1)*self.cellWidth,self.basePoint[1]+(cell[0]+1)*self.dy),
                        (self.basePoint[0]+(cell[0]+1)*self.dx+cell[1]*self.cellWidth,self.basePoint[1]+(cell[0]+1)*self.dy)
                    ]
            pg.draw.polygon(self.screen,self.color[value],points)
            for i in range (0,4):
                pg.draw.line(self.screen,self.color[0],points[i],points[(i+1)%4])
        for buttonKey, buttonValue in self.buttonList.items():
            if buttonValue[0]==1:
                point = (self.basePoint[0]+buttonKey[0]*self.dx+buttonKey[1]*self.cellWidth + self.cellWidth/2 + self.dx/2,self.basePoint[1]+buttonKey[0]*self.dy+self.dy/2)
                pg.draw.circle(self.screen,pg.Color(self.color[4]),point,self.dy/2)
            elif buttonValue[0]==2:
                points = [
                    (self.basePoint[0]+buttonKey[0]*self.dx+buttonKey[1]*self.cellWidth,self.basePoint[1]+buttonKey[0]*self.dy),
                    (self.basePoint[0]+buttonKey[0]*self.dx+(buttonKey[1]+1)*self.cellWidth,self.basePoint[1]+buttonKey[0]*self.dy),
                    (self.basePoint[0]+(buttonKey[0]+1)*self.dx+(buttonKey[1]+1)*self.cellWidth,self.basePoint[1]+(buttonKey[0]+1)*self.dy),
                    (self.basePoint[0]+(buttonKey[0]+1)*self.dx+buttonKey[1]*self.cellWidth,self.basePoint[1]+(buttonKey[0]+1)*self.dy)
                    ]
                pg.draw.line(self.screen,pg.Color(self.color[5]),points[0],points[2])
                pg.draw.line(self.screen,pg.Color(self.color[5]),points[1],points[3])
            elif buttonValue[0]==3:
                point = (self.basePoint[0]+buttonKey[0]*self.dx+buttonKey[1]*self.cellWidth + self.cellWidth/2 + self.dx/2,self.basePoint[1]+buttonKey[0]*self.dy+self.dy/2)
                pg.draw.circle(self.screen,pg.Color(self.color[1]),point,self.dy/2)
                pg.draw.circle(self.screen,pg.Color(self.color[2]),point,self.dy/4)
class Cube:
    def __init__(self, game):
        self.firstCube = game.testCase[1][0]
        self.secondCube = game.testCase[1][1]
        self.board = game.board
        self.color = game.setting.cubeColor
    def __draw(self,points):
        pg.draw.polygon(self.board.screen,pg.Color(self.color),points)
        for i in range (0,4):
            pg.draw.line(self.board.screen,pg.Color(self.board.color[0]),points[i],points[(i+1)%4])
    def isNotSplit(self):
        if self.firstCube == self.secondCube:
            return True
        if self.firstCube[0] == self.secondCube[0] and np.abs(self.firstCube[1]-self.secondCube[1])<=1:
            return True
        if self.firstCube[1] == self.secondCube[1] and np.abs(self.firstCube[0]-self.secondCube[0])<=1:
            return True
        return False
            
    def __blindSearchMove(self):
        solver = BlindSearch(self,self.board)
        ans = solver.solve()
        return ans
    
    def __a_starMove(self):
        solver = A_star(self,self.board)
        ans = solver.solve()
        return ans

    def __monteCarloTreeSearchMove(self):
        solver = MonterCarloTreeSearch(self,self.board)
        ans = solver.solve()
        return ans

    def draw(self):
        if self.firstCube == self.secondCube:
            points = [
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-2*self.board.cellWidth),
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-2*self.board.cellWidth),
            (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy-2*self.board.cellWidth),
            (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy-2*self.board.cellWidth)
        ]
            self.__draw(points)
            points = [
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-2*self.board.cellWidth),
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-2*self.board.cellWidth),
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy),
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy)
        ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy),
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy),
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-2*self.board.cellWidth),
                (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy-2*self.board.cellWidth)
            ]
            self.__draw(points)
        elif self.firstCube[0]==self.secondCube[0] and np.abs(self.firstCube[1]-self.secondCube[1])==1:
            row = self.firstCube[0]
            minCol = min(self.firstCube[1],self.secondCube[1])
            maxCol = max(self.firstCube[1],self.secondCube[1])
            points = [
                (self.board.basePoint[0]+row*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+row*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+row*self.board.dx+(maxCol+1)*self.board.cellWidth,self.board.basePoint[1]+row*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(row+1)*self.board.dx+(maxCol+1)*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(row+1)*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+(row+1)*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy),
                (self.board.basePoint[0]+(row+1)*self.board.dx+(maxCol+1)*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy),                
                (self.board.basePoint[0]+(row+1)*self.board.dx+(maxCol+1)*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(row+1)*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+row*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+row*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+row*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+row*self.board.dy),
                (self.board.basePoint[0]+(row+1)*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy),
                (self.board.basePoint[0]+(row+1)*self.board.dx+minCol*self.board.cellWidth,self.board.basePoint[1]+(row+1)*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
        elif self.firstCube[1]==self.secondCube[1] and np.abs(self.firstCube[0]-self.secondCube[0])==1:
            col = self.firstCube[1]
            minRow = min(self.firstCube[0],self.secondCube[0])
            maxRow = max(self.firstCube[0],self.secondCube[0])
            points = [
                (self.board.basePoint[0]+minRow*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+minRow*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+minRow*self.board.dx+(col+1)*self.board.cellWidth,self.board.basePoint[1]+minRow*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+(col+1)*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy),
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+(col+1)*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy),                
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+(col+1)*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+minRow*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+minRow*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+minRow*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+minRow*self.board.dy),
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy),
                (self.board.basePoint[0]+(maxRow+1)*self.board.dx+col*self.board.cellWidth,self.board.basePoint[1]+(maxRow+1)*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
        else:
            points = [
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-self.board.cellWidth),
            (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-self.board.cellWidth),
            (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy-self.board.cellWidth),
            (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy-self.board.cellWidth)
        ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+(self.firstCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy),
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy),
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy),
                (self.board.basePoint[0]+(self.firstCube[0]+1)*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.firstCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+self.firstCube[0]*self.board.dx+self.firstCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.firstCube[0]*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+(self.secondCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+self.secondCube[0]*self.board.dx+(self.secondCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+self.secondCube[0]*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+self.secondCube[0]*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.secondCube[0]*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+(self.secondCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+(self.secondCube[1]+1)*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy),
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy)
            ]
            self.__draw(points)
            points = [
                (self.board.basePoint[0]+self.secondCube[0]*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.secondCube[0]*self.board.dy),
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy),
                (self.board.basePoint[0]+(self.secondCube[0]+1)*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+(self.secondCube[0]+1)*self.board.dy-self.board.cellWidth),
                (self.board.basePoint[0]+self.secondCube[0]*self.board.dx+self.secondCube[1]*self.board.cellWidth,self.board.basePoint[1]+self.secondCube[0]*self.board.dy-self.board.cellWidth)
            ]
            self.__draw(points)
    def move(self, mode, dir=0):
        if mode !=1:
            seriesMove = []
            if (mode == 2):
                seriesMove = self.__blindSearchMove()
            elif (mode == 3):
                seriesMove = self.__a_starMove()
            elif (mode == 4):
                seriesMove = self.__monteCarloTreeSearchMove()
            print (seriesMove)
            open('Output.txt','a',encoding='utf-8').writelines(str(seriesMove)+'\n')
            for i in seriesMove:
                self.firstCube, self.secondCube = i
                buttonListKeys = self.board.buttonList.keys()
                if (self.firstCube not in self.board.map.keys()) or (self.secondCube not in self.board.map.keys()) or (self.board.map[self.firstCube]==0) or (self.board.map[self.secondCube]==0):
                    break                   
                if (self.firstCube in buttonListKeys and self.board.buttonList[self.firstCube][0]==1):
                    for j in self.board.buttonList[self.firstCube][1]:
                        if j in self.board.map.keys():
                            self.board.map[j]+=2
                            if self.board.map[j] >=3:
                                self.board.map[j] = 0
                        else:
                            self.board.map[j]=2
                elif ((self.secondCube in buttonListKeys and self.board.buttonList[self.secondCube][0]==1)):
                    for j in self.board.buttonList[self.secondCube][1]:
                        if j in self.board.map.keys():
                            self.board.map[j]+=2
                            if self.board.map[j] >=3:
                                self.board.map[j] = 0
                        else:
                            self.board.map[j]=2
                elif (self.firstCube == self.secondCube and self.firstCube in buttonListKeys and self.board.buttonList[self.firstCube][0]==2):
                    for j in self.board.buttonList[self.firstCube][1]:
                        if j in self.board.map.keys():
                            self.board.map[j]+=2
                            if self.board.map[j] >=3:
                                self.board.map[j] = 0
                        else:
                            self.board.map[j]=2
                elif (self.secondCube in buttonListKeys and self.board.buttonList[self.secondCube][0]==3) and self.firstCube == self.secondCube:
                    [self.firstCube,self.secondCube] = self.board.buttonList[self.secondCube][1]
                self.board.screen.fill(pg.Color(self.board.color[0]))
                self.board.draw()
                self.draw()
                pg.display.update()
                pg.time.delay(1000)
            if (self.firstCube not in self.board.map.keys()) or (self.secondCube not in self.board.map.keys()) or (self.board.map[self.firstCube]==0) or (self.board.map[self.secondCube]==0):
                print("You lose")
                open('Output.txt','a',encoding='utf-8').writelines("You lose\n")
                return 0
            elif ((self.firstCube == self.secondCube) and (self.board.map[self.secondCube]==3)):
                print("You win")
                open('Output.txt','a',encoding='utf-8').writelines("You win\n")
                return 0
            elif (self.firstCube == self.secondCube) and (self.board.map[self.secondCube]==1):
                print("You lose")
                open('Output.txt','a',encoding='utf-8').writelines("You lose\n")
                return 0
            else:
                print("Can't solve")
                open('Output.txt','a',encoding='utf-8').writelines("Can't solve\n")
                return 0
                    
        else:
            if self.firstCube == self.secondCube:
                if dir == 'w':
                    self.firstCube = (self.firstCube[0]-2,self.firstCube[1])
                    self.secondCube = (self.secondCube[0]-1,self.secondCube[1])
                elif dir == 's':
                    self.firstCube = (self.firstCube[0]+1,self.firstCube[1])
                    self.secondCube =(self.secondCube[0]+2,self.secondCube[1])
                elif dir == 'a':
                    self.firstCube = (self.firstCube[0],self.firstCube[1]-2)
                    self.secondCube =(self.secondCube[0],self.secondCube[1]-1)
                elif dir == 'd':
                    self.firstCube = (self.firstCube[0],self.firstCube[1]+1)
                    self.secondCube =(self.secondCube[0],self.secondCube[1]+2)
            elif self.firstCube[0]==self.secondCube[0]:
                if dir == 'w':
                    self.firstCube = (self.firstCube[0]-1,self.firstCube[1])
                    self.secondCube = (self.secondCube[0]-1,self.secondCube[1])
                elif dir == 's':
                    self.firstCube = (self.firstCube[0]+1,self.firstCube[1])
                    self.secondCube =(self.secondCube[0]+1,self.secondCube[1])
                elif dir == 'a':
                    self.firstCube = (self.firstCube[0],self.firstCube[1]-1)
                    self.secondCube =(self.secondCube[0],self.secondCube[1]-2)
                elif dir == 'd':
                    self.firstCube = (self.firstCube[0],self.firstCube[1]+2)
                    self.secondCube =(self.secondCube[0],self.secondCube[1]+1)
            elif self.firstCube[1]==self.secondCube[1]:
                if dir == 'w':
                    self.firstCube = (self.firstCube[0]-1,self.firstCube[1])
                    self.secondCube = (self.secondCube[0]-2,self.secondCube[1])
                elif dir == 's':
                    self.firstCube = (self.firstCube[0]+2,self.firstCube[1])
                    self.secondCube =(self.secondCube[0]+1,self.secondCube[1])
                elif dir == 'a':
                    self.firstCube = (self.firstCube[0],self.firstCube[1]-1)
                    self.secondCube =(self.secondCube[0],self.secondCube[1]-1)
                elif dir == 'd':
                    self.firstCube = (self.firstCube[0],self.firstCube[1]+1)
                    self.secondCube =(self.secondCube[0],self.secondCube[1]+1)
            else:
                pass
            buttonListKeys = self.board.buttonList.keys()
            if (self.firstCube in buttonListKeys and self.board.buttonList[self.firstCube][0]==1):
                for i in self.board.buttonList[self.firstCube][1]:
                    if i in self.board.map.keys():
                        self.board.map[i]+=2
                        if self.board.map[i] >=3:
                            self.board.map[i] = 0
                    else:
                        self.board.map[i]=2
            elif ((self.secondCube in buttonListKeys and self.board.buttonList[self.secondCube][0]==1)):
                for i in self.board.buttonList[self.secondCube][1]:
                    if i in self.board.map.keys():
                        self.board.map[i]+=2
                        if self.board.map[i] >=3:
                            self.board.map[i] = 0
                    else:
                        self.board.map[i]=2
            elif (self.firstCube == self.secondCube and self.firstCube in buttonListKeys and self.board.buttonList[self.firstCube][0]==2):
                for i in self.board.buttonList[self.firstCube][1]:
                    if i in self.board.map.keys():
                        self.board.map[i]+=2
                        if self.board.map[i] >=3:
                            self.board.map[i] = 0
                    else:
                        self.board.map[i]=2
            elif ((self.secondCube in buttonListKeys and self.board.buttonList[self.secondCube][0]==3) and self.firstCube == self.secondCube):
                    [self.firstCube,self.secondCube] = self.board.buttonList[self.secondCube][1]
        return 1

