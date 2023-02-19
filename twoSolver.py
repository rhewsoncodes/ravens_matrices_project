import numpy as np
from UtilityFunctions import getMatrix, returnClosestAnswer, splitQuestionAnswer
from PIL import Image

def twoDifferential(question):
        imageMatrices = {}
        for key in question.keys():
            imageMatrices[key] = getMatrix(question[key].visualFilename)
        hDiff = (imageMatrices["A"] - imageMatrices["B"])
        vDiff = (imageMatrices["A"] - imageMatrices["C"])
        return vDiff, hDiff

def twoVertical(question, vDiff):
        vFrame = getMatrix(question["B"].visualFilename)
        return vFrame + vDiff

def twoHorizontal(question, hDiff):
        hFrame = getMatrix(question["C"].visualFilename)
        return hFrame + hDiff

def twoBoth(question, vDiff, hDiff):
        vhFrame = getMatrix(question["A"].visualFilename)
        return vhFrame + vDiff + hDiff

def isVerticalFlip(question):
        aFrame = getMatrix(question["A"].visualFilename)
        cFrame = getMatrix(question["C"].visualFilename)
        aFlipped = np.flipud(aFrame)
        h = np.mean(np.absolute(aFlipped - cFrame))
        if h < 1:
            return np.flipud(getMatrix(question["B"].visualFilename))
        return None

def isHorizontalFlip(question):
        aFrame = getMatrix(question["A"].visualFilename)
        bFrame = getMatrix(question["B"].visualFilename)
        aFlipped = np.fliplr(aFrame)
        h = np.mean(np.absolute(aFlipped - bFrame))
        if h < 1:
            return np.fliplr(getMatrix(question["C"].visualFilename))
        return None
    
def isRotateHorizontal(question):
        aFrame = getMatrix(question["A"].visualFilename)
        bFrame = getMatrix(question["B"].visualFilename)
        aRotated = np.rot90(aFrame, 1)
        h = np.mean(np.absolute(aRotated - bFrame))
        if h < 1:
            return np.rot90(getMatrix(question["C"].visualFilename))
        return None

def catchAll(question, answer):
        vDiff, hDiff = twoDifferential(question)
        answers = []
        for option in answer.keys():
            methodGuesses = []
            optionFrame = getMatrix(answer[option].visualFilename)
            methodGuesses.append(twoVertical(question, vDiff))
            methodGuesses.append(twoHorizontal(question, hDiff))
            methodGuesses.append(twoBoth(question, vDiff, hDiff))
            methodScores = [np.sum(np.absolute(optionFrame - guess)) for guess in methodGuesses]
            answers.append(min(methodScores))

        return np.argmin(answers) + 1
        
def solveTwo(problem):
    question, answer = splitQuestionAnswer(problem)
    vFlipGuess = isVerticalFlip(question)
    hFlipGuess = isHorizontalFlip(question)
    rotateGuess = isRotateHorizontal(question)

    if np.any(vFlipGuess): 
        return returnClosestAnswer(vFlipGuess, answer)
    if np.any(hFlipGuess): 
        return returnClosestAnswer(hFlipGuess, answer)
    if np.any(rotateGuess):
        return returnClosestAnswer(rotateGuess, answer)

    return catchAll(question, answer)
        