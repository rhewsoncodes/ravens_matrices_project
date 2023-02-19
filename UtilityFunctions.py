from PIL import Image
import numpy as np
import math
import collections

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

def returnShapes(matrix):
    m = np.copy(matrix)
    m = np.mean(m, axis = 2)
    m = m/255
    m = m.astype(int)

    rows, cols = np.shape(m)
    visit = set()
    shapes = []

    def bfs(r,c):
        q = collections.deque()
        visit.add((r, c))
        q.append((r,c))
        sizeCount = 0
        while q:
            row, col = q.popleft()
            directions = [[1,0], [-1, 0], [0, 1], [0, -1]]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if (r in range(rows) and
                   c in range(cols) and
                   m[r][c] == 0 and
                   (r, c) not in visit):
                   sizeCount += 1
                   q.append((r,c))
                   visit.add((r,c))
        
        return sizeCount
                   
                

    for r in range(rows):
        for c in range(cols):
            if m[r][c] == 0 and (r,c) not in visit:
                shapes.append(bfs(r,c))

    return shapes    
    
