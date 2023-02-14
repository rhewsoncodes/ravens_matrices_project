from PIL import Image
import numpy as np
import math

class Agent:

    def __init__(self):
        self.questionNumber = 0

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

    def isVerticalFlip(self, question):
        aFrame = self.getMatrix(question["A"].visualFilename)
        cFrame = self.getMatrix(question["C"].visualFilename)
        aFlipped = np.flipud(aFrame)
        h = np.mean(np.absolute(aFlipped - cFrame))
        if h < 1:
            return np.flipud(self.getMatrix(question["B"].visualFilename))
        return None

    def isHorizontalFlip(self, question):
        aFrame = self.getMatrix(question["A"].visualFilename)
        bFrame = self.getMatrix(question["B"].visualFilename)
        aFlipped = np.fliplr(aFrame)
        h = np.mean(np.absolute(aFlipped - bFrame))
        if h < 1:
            return np.fliplr(self.getMatrix(question["C"].visualFilename))
        return None
    
    def isRotateHorizontal(self, question):
        aFrame = self.getMatrix(question["A"].visualFilename)
        bFrame = self.getMatrix(question["B"].visualFilename)
        aRotated = np.rot90(aFrame, 1)
        h = np.mean(np.absolute(aRotated - bFrame))
        if h < 1:
            return np.rot90(self.getMatrix(question["C"].visualFilename))
        return None

    def catchAll(self, question, answer):
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

        return np.argmin(answers) + 1

    def returnClosestAnswer(self, frame, answer):
        answerArrays = {}
        for option in answer.keys():
            answerArrays[option] = self.getMatrix(answer[option].visualFilename)
        return np.argmin([np.sum(np.absolute(frame-answerArrays[option])) for option in answer.keys()]) + 1

        
    def solveTwo(self, problem):
        question, answer = self.splitQuestionAnswer(problem)
        vFlipGuess = self.isVerticalFlip(question)
        hFlipGuess = self.isHorizontalFlip(question)
        rotateGuess = self.isRotateHorizontal(question)

        if np.any(vFlipGuess):
            print(self.questionNumber, "V FLIP") 
            return self.returnClosestAnswer(vFlipGuess, answer)
        if np.any(hFlipGuess):
            print(self.questionNumber, "H FLIP") 
            return self.returnClosestAnswer(hFlipGuess, answer)
        if np.any(rotateGuess):
            print(self.questionNumber, "ROTATE")
            return self.returnClosestAnswer(rotateGuess, answer)

        return self.catchAll(question, answer)
        
        




            

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
            self.questionNumber += 1
            return self.solveThree(figures)
        else:
            self.questionNumber += 1
            return self.solveTwo(figures)
