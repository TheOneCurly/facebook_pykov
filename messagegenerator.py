import pandas
import matplotlib
import scipy
import pykov

import sys
import pickle
import re

import math

readName = input("Select which user to generate from: ")
#readName = "Alex Curly Wilson"
readPath = readName + " Chain.dat"
rawDataFile = open(readPath, 'rb')
chainData = pickle.load(rawDataFile)

generateAgain = True
while generateAgain:
    outputString = '['
    newSymbol = ''
    lastSymbol = '['

    while (lastSymbol != ']'):
        lastProbability = 0
        while (lastProbability < 0.02):
            newSymbol = chainData.move(lastSymbol)
            lastProbability = math.exp(chainData.walk_probability([lastSymbol, newSymbol]))

        outputString = outputString + " " + newSymbol
        lastSymbol =  newSymbol
    print(outputString)

    userGenerateAgain = input("Go again? ")
    if(userGenerateAgain == "n"):
        generateAgain = False
