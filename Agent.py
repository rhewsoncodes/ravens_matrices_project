from PIL import Image
from twoSolver import solveTwo
from threeSolver import solveThree
import numpy as np
import math

class Agent:

    def __init__(self):
        self.questionNumber = 0            

    def Solve(self, problem):
        figures = problem.figures
        if "D" in figures.keys():
            self.questionNumber += 1
            return solveThree(figures)
        else:
            self.questionNumber += 1
            return solveTwo(figures)
