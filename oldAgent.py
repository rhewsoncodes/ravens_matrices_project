# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy as np
import math

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def returnImageMatrix(self, myImage):
        image = Image.open(myImage)
        imageNP = np.array(image)
        dimensions = imageNP.shape
        height = 4
        width = 4
        ImageMatrix = np.zeros((height,width))
        for i in range(height):
            heightIterator = int(dimensions[0]/height * i)
            heightIteratorEnd = int(heightIterator + dimensions[0]/height)
            for x in range(width):
                widthIterator = int(dimensions[1]/width * i)
                widthIteratorEnd = int(widthIterator + dimensions[1]/width)
                ImageMatrix[i][x] = np.mean(imageNP[heightIterator:heightIteratorEnd,widthIterator:widthIteratorEnd])
        return ImageMatrix


    # In 3x3, the figures in the first row are named from left to right A, B,
        # and C. The figures in the second row are named from left to right D, E,
        # and F. The figures in the third row are named from left to right G and H.
        # Relationships are present across rows and down columns: A is to B is to
        # C as D is to E is to F as G is to H is to one of the answer choices. A is
        # to D is G as B is to E is to H as C is to F is to one of the answer
        # choices. The answer choices are named 1 through 6.
    def returnEstimatedDifferential(self, figures):
        verticalDifferential = np.zeros((4,4))
        horizontalDifferential = np.zeros((4,4))
        imageMatrices = {}
        for key in figures.keys():
                imageMatrices[key] = self.returnImageMatrix(figures[key].visualFilename)
        if "D" in figures.keys():
            ad_D = imageMatrices["A"] - imageMatrices["D"]
            dg_D = imageMatrices["D"] - imageMatrices["G"]
            be_D = imageMatrices["B"] - imageMatrices["E"]
            eh_D = imageMatrices["E"] - imageMatrices["H"]
            cf_D = imageMatrices["C"] - imageMatrices["F"]
            verticalDifferential = (ad_D + dg_D + be_D + eh_D + cf_D)/5
            ab_D = imageMatrices["A"] - imageMatrices["B"]
            bc_D = imageMatrices["B"] - imageMatrices["C"]
            de_D = imageMatrices["D"] - imageMatrices["E"]
            ef_D = imageMatrices["E"] - imageMatrices["F"]
            gh_D = imageMatrices["G"] - imageMatrices["H"]
            horizontalDifferential = (ab_D + bc_D + de_D + ef_D + gh_D)/5
            return verticalDifferential, horizontalDifferential
        else:
            horizontalDifferential = (imageMatrices["A"] - imageMatrices["B"])
            verticalDifferential = (imageMatrices["A"] - imageMatrices["C"])
            return verticalDifferential, horizontalDifferential

    def verticalOnly(self, verticalDifferential):
        pass

    def horizontalOnly(self, horizontalDifferential):
        pass
    
    def vertAndHorizontal(self, verticalDifferential, horizontalDifferential):
        pass

    def returnBestGuess(self, eVertical, eHorizontal, figures):
        if "D" in figures.keys():
            horizontalFrame = self.returnImageMatrix(figures["H"].visualFilename)
            verticalFrame = self.returnImageMatrix(figures["F"].visualFilename)
        else:
            horizontalFrame = self.returnImageMatrix(figures["C"].visualFilename)
            verticalFrame = self.returnImageMatrix(figures["B"].visualFilename)
        guessHeuristics = {}
        for figure in figures.keys():
            if figure.isdigit():
                horizontalDiff = horizontalFrame - self.returnImageMatrix(figures[figure].visualFilename)
                verticalDiff = verticalFrame - self.returnImageMatrix(figures[figure].visualFilename)
                h = np.mean(np.absolute(horizontalDiff - eHorizontal))+np.mean(np.absolute(verticalDiff - eVertical))
                guessHeuristics[figure] = h

        minvalue = 100000
        minchoice = -1
        for key in guessHeuristics.keys():
            if guessHeuristics[key] < minvalue:
                minchoice = int(key)
                minvalue = guessHeuristics[key]
        
        return minchoice

    



    def Solve(self,problem):

        figures = problem.figures

        print(figures)

        expectedVert, expectedHorizontal = self.returnEstimatedDifferential(figures)

        return self.returnBestGuess(expectedVert, expectedHorizontal, figures)