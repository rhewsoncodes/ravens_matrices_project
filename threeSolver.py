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

def solveThree(problem):
    question, answer = splitQuestionAnswer(problem)
    isRowIdentity = rowIdentity(question)
    isColumnIdentity = columnIdentity(question)
    if np.any(isRowIdentity):
        return returnClosestAnswer(isRowIdentity, answer)
    if np.any(isColumnIdentity):
        return returnClosestAnswer(isColumnIdentity, answer)


    return catchAll(question, answer)