import pandas
import matplotlib
import scipy
import pykov

import sys
import pickle
import re


readName = input("Select which user to read from: ")
#readName = "Suzanne Reed"
readPath = readName + ".dat"
rawDataFile = open(readPath, 'rb')
rawData = pickle.load(rawDataFile)



# Create vector for individual symbol probabilities
dataVector = pykov.Vector()

for message in rawData:
    #Preprocess
    message = message.lower()
    
    # Split message into words and punctuation
    messageList = re.findall('\w+|[.!?@;()\\-]', message);

    # Add a start for each message
    if '[' in dataVector:
        dataVector['['] = dataVector['['] + 1
    else:
        dataVector['['] = 1;

    # Add all the symbols
    for symbol in messageList:
        if symbol in dataVector:
            dataVector[symbol] = dataVector[symbol] + 1
        else:
            dataVector[symbol] = 1;

    # Add an end for each message
    if ']' in dataVector:
        dataVector[']'] = dataVector[']'] + 1
    else:
        dataVector[']'] = 1;

dataVector.normalize()



# Create matrix of all transitions in data
dataMatrix = pykov.Matrix()

for message in rawData:
    #Preprocess
    message = message.lower()
    
    # Split message into words and punctuation
    messageList = re.findall('\w+|[.!?@;()\\-]', message);

    # Start with beginner symbol
    lastSymbol = '['

    # step through message and add symbol pairs
    for i in range(len(messageList)):        
        currentSymbol = messageList[i]
        if (lastSymbol, currentSymbol) in dataMatrix:
            dataMatrix[(lastSymbol, currentSymbol)] = dataMatrix[(lastSymbol, currentSymbol)] + 1
        else:
            dataMatrix[(lastSymbol, currentSymbol)] = 1

        lastSymbol = currentSymbol

    # End with end symbol
    currentSymbol = ']'
    if (lastSymbol, currentSymbol) in dataMatrix:
        dataMatrix[(lastSymbol, currentSymbol)] = dataMatrix[(lastSymbol, currentSymbol)] + 1
    else:
        dataMatrix[(lastSymbol, currentSymbol)] = 1

# Build square, normalized transition matrix
transitionMatrix = pykov.Matrix()

for symbol in dataVector:
    transitionVector = pykov.Vector()
    
    for transitionSymbol in dataVector:
        if (symbol, transitionSymbol) in dataMatrix:
            transitionVector[transitionSymbol] = dataMatrix[(symbol, transitionSymbol)]
        else:
            transitionVector[transitionSymbol] = 0

    transitionVector.normalize()

    for transitionSymbol in transitionVector:
        transitionMatrix[(symbol, transitionSymbol)] = transitionVector[transitionSymbol]

# Build chain from transition matrix
dataChain = pykov.Chain(transitionMatrix)

# Save chain due to processing time
writePath = readName + " Chain.dat"
writeDataFile = open(writePath, 'wb')
pickle.dump(dataChain, writeDataFile)
writeDataFile.close()
