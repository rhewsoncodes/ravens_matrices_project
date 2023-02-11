from PIL import Image
import numpy as np
import math

class Agent:

    def __init__(self):
        pass

    def simplifyMatrix(self, myImage, height, width):
        image = Image.open(myImage)
        imageNP = np.array(image)
        dimensions = imageNP.shape
        imageMatrix = np.zeros((height, width))
        for i in range(height):
            heightStart = int(dimensions[0]/height * i)
            heightEnd = int(heightStart + dimensions[0]/height)
            for x in range(width):
                widthStart = int(dimensions[1]/width * i)
                widthEnd = int(widthStart + dimensions[1]/width)
                imageMatrix[i][x] = np.mean(imageNP[heightStart:heightEnd, widthStart:widthEnd])
        return imageMatrix
        
    
    
    def splitQuestionAnswer(self, problem):
        question = {}
        answer = {}

        for image in problem.keys():
            if image.isdigit():
                answer[image] = problem[image]
            else:
                question[image] = problem[image]

        return question, answer
    
    def Solve(self, problem):
        pass
