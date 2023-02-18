import numpy as np
from UtilityFunctions import getMatrix, returnClosestAnswer, splitQuestionAnswer
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
    aFrame = getMatrix(question["A"].visualFilename)
    eFrame = getMatrix(question["E"].visualFilename)
    diff = np.sum(eFrame) - np.sum(aFrame)
    predictedSum = np.sum(eFrame) + diff
    answerScores = [np.absolute(np.sum(getMatrix(answer[option].visualFilename)) - predictedSum) for option in answer.keys()]
    return np.argmin(answerScores) + 1

def solveThree(problem):
    question, answer = splitQuestionAnswer(problem)
    isRowIdentity = rowIdentity(question)
    isColumnIdentity = columnIdentity(question)
    if np.any(isRowIdentity):
        return returnClosestAnswer(isRowIdentity, answer)
    if np.any(isColumnIdentity):
        return returnClosestAnswer(isColumnIdentity, answer)


    return catchAll(question, answer)