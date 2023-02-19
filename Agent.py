from PIL import Image
from twoSolver import solveTwo
from threeSolver import solveThree
import numpy as np
import math

class Agent:

    def __init__(self):
        pass        

    def Solve(self, problem):
        figures = problem.figures
        if "D" in figures.keys():
            print(problem.name)
            return solveThree(figures)
        else:
            return solveTwo(figures)
