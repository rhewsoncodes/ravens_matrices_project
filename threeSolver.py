import numpy as np
from UtilityFunctions import getMatrix, returnClosestAnswer, splitQuestionAnswer, returnShapes
from PIL import Image


def rowIdentity(question):
    aFrame = getMatrix(question["A"].visualFilename)
    bFrame = getMatrix(question["B"].visualFilename)
    h = np.average(np.absolute(aFrame - bFrame))
    if h < 1:
        return getMatrix(question["G"].visualFilename)
    return None

def columnIdentity(question):
    aFrame = getMatrix(question["A"].visualFilename)
    dFrame = getMatrix(question["D"].visualFilename)
    h = np.average(np.absolute(aFrame - dFrame))
    if h < 1:
        return getMatrix(question["C"].visualFilename)
    return None

def catchAll(question, answer):
    aFrame = int(np.sum(getMatrix(question["A"].visualFilename)))
    bFrame = int(np.sum(getMatrix(question["B"].visualFilename)))
    dFrame = int(np.sum(getMatrix(question["D"].visualFilename)))
    eFrame = int(np.sum(getMatrix(question["E"].visualFilename)))
    fFrame = int(np.sum(getMatrix(question["F"].visualFilename)))
    hFrame = int(np.sum(getMatrix(question["H"].visualFilename)))
    diff = eFrame - aFrame
    abDiff = bFrame - aFrame
    adDiff = dFrame - aFrame
    efDiff = fFrame - eFrame
    ehDiff = hFrame - eFrame
    ratio = np.abs(diff)/(np.abs(abDiff)+np.abs(adDiff))
    predictedSum = eFrame + (efDiff + ehDiff)*ratio
    answerScores = [np.absolute(np.sum(getMatrix(answer[option].visualFilename)) - predictedSum) for option in answer.keys()]
    return np.argmin(answerScores) + 1

def sudokuSum(question, answer):
    aFrame = int(np.sum(getMatrix(question["A"].visualFilename)))
    bFrame = int(np.sum(getMatrix(question["B"].visualFilename)))
    cFrame = int(np.sum(getMatrix(question["C"].visualFilename)))
    dFrame = int(np.sum(getMatrix(question["D"].visualFilename)))
    eFrame = int(np.sum(getMatrix(question["E"].visualFilename)))
    fFrame = int(np.sum(getMatrix(question["F"].visualFilename)))
    gFrame = int(np.sum(getMatrix(question["G"].visualFilename)))
    hFrame = int(np.sum(getMatrix(question["H"].visualFilename)))

    rowOne = aFrame + bFrame + cFrame
    rowTwo = dFrame + eFrame + fFrame
    colOne = aFrame + dFrame + gFrame
    colTwo = bFrame + eFrame + hFrame

    if rowOne == rowTwo and rowOne == colOne and rowOne == colTwo:
        estimatedSum = rowOne - gFrame - hFrame
        guesses = [np.abs(np.sum(getMatrix(answer[option].visualFilename)) - estimatedSum) for option in answer.keys()]
        return np.argmin(guesses) + 1
    return None


def switcharoo(question, questionNumber): #work in progress
    aFrame = getMatrix(question["A"].visualFilename)
    cFrame = getMatrix(question["C"].visualFilename)

    if np.sum(aFrame) == 0:
        return None
    part1a, part2a = np.split(aFrame, 2, axis=1)
    newFrame = np.column_stack((part2a, part1a))
    h = np.mean(np.absolute(cFrame - newFrame))
    if h < 1:
        gFrame = getMatrix(question["G"].visualFilename)
        part1g, part2g = np.split(gFrame, 2, axis=1)
        return np.column_stack((part2g, part1g))
    return None

    

def solveThree(problem, questionNumber):
    question, answer = splitQuestionAnswer(problem)
    isRowIdentity = rowIdentity(question)
    isColumnIdentity = columnIdentity(question)
    isSudokuSum = sudokuSum(question, answer)
    isSwitcharoo = switcharoo(question, questionNumber)
    if np.any(isRowIdentity):
        return returnClosestAnswer(isRowIdentity, answer)
    if np.any(isColumnIdentity):
        return returnClosestAnswer(isColumnIdentity, answer)
    if isSudokuSum:
        return isSudokuSum
    


    return catchAll(question, answer)