from PIL import Image
import numpy as np
import math

class Agent:

    def __init__(self):
        self.questionNumber = 1

    def getMatrix(self, myImage):
        image = Image.open(myImage)
        imageNP = np.array(image)

        return imageNP

    def twoDifferential(self, question):
        imageMatrices = {}
        for key in question.keys():
            imageMatrices[key] = self.getMatrix(question[key].visualFilename)
        hDiff = (imageMatrices["A"] - imageMatrices["B"])
        vDiff = (imageMatrices["A"] - imageMatrices["C"])
        return vDiff, hDiff

    def twoVertical(self, question, vDiff):
        vFrame = self.getMatrix(question["B"].visualFilename)
        return vFrame + vDiff

    def twoHorizontal(self, question, hDiff):
        hFrame = self.getMatrix(question["C"].visualFilename)
        return hFrame + hDiff

    def twoBoth(self, question, vDiff, hDiff):
        vhFrame = self.getMatrix(question["A"].visualFilename)
        return vhFrame + vDiff + hDiff

    def twoFlipVertical(self, question):
        vFrame = self.getMatrix(question["B"].visualFilename)
        return np.flipud(vFrame)

    def twoFlipHorizontal(self, question):
        hFrame = self.getMatrix(question["C"].visualFilename)
        return np.fliplr(hFrame)
        
    def solveTwo(self, problem):
        question, answer = self.splitQuestionAnswer(problem)
        vDiff, hDiff = self.twoDifferential(question)
        answers = []
        for option in answer.keys():
            methodGuesses = []
            optionFrame = self.getMatrix(answer[option].visualFilename)
            methodGuesses.append(self.twoVertical(question, vDiff))
            methodGuesses.append(self.twoHorizontal(question, hDiff))
            methodGuesses.append(self.twoBoth(question, vDiff, hDiff))
            methodScores = [np.sum(np.absolute(optionFrame - guess)) for guess in methodGuesses]
            answers.append(min(methodScores))
        self.questionNumber += 1
        return np.argmin(answers) + 1



            

    def solveThree(self, problem):
        return 1


        
    
    
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
        figures = problem.figures
        if "D" in figures.keys():
            return self.solveThree(figures)
        else:
            return self.solveTwo(figures)
