from PIL import Image
import numpy as np
import math

def getMatrix(myImage):
        image = Image.open(myImage)
        imageNP = np.array(image)

        return imageNP

def returnClosestAnswer(frame, answer):
        answerArrays = {}
        for option in answer.keys():
            answerArrays[option] = getMatrix(answer[option].visualFilename)
        return np.argmin([np.sum(np.absolute(frame-answerArrays[option])) for option in answer.keys()]) + 1

def splitQuestionAnswer(problem):
        question = {}
        answer = {}

        for image in problem.keys():
            if image.isdigit():
                answer[image] = problem[image]
            else:
                question[image] = problem[image]

        return question, answer