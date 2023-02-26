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
                print("you win")
                open('Output.txt','a',encoding='utf-8').writelines("You win\n")
                return 0
            elif (self.firstCube == self.secondCube) and (self.board.map[self.secondCube]==1):
                print("You lose")
                open('Output.txt','a',encoding='utf-8').writelines("You lose\n")
                return 0
            else:
                print("can't solve")
                open('Output.txt','a',encoding='utf-8').writelines("Can't Solve\n")
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
        return 1