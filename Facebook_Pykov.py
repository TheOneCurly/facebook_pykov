from bs4 import BeautifulSoup

import pandas
import matplotlib
import scipy
import pykov

import sys
import pickle
import re
import math

def ParseFacebookMessages():
    # Replacement map for emojii, we're just going to ignore them for now
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    # Path to messages file from facebook dump
    # in this case I extracted the entire zip to a folder called 'facebook'
    messagesPath = "facebook\html\messages.htm"
    messagesFile = open(messagesPath, encoding='utf-8',  mode='r')
    messagesText = messagesFile.read()
    messagesFile.close()

    soup = BeautifulSoup(messagesText, 'html.parser')
    print(soup.title)

    messagesByPerson = {}

    peopleTags = soup.find_all("span", class_="user")
    for span in peopleTags:
        message = span.find_next("p")
        if(message.string != None):
            #print(span.string + ": " + (message.string).translate(non_bmp_map))
            if span.string not in messagesByPerson:
                messagesByPerson[span.string] = list()
                print(span.string + " found")
                
            messagesByPerson[span.string].append((message.string).translate(non_bmp_map))

    return messagesByPerson

def GenerateChains(name, messageList):
    # Create vector for individual symbol probabilities
    dataVector = pykov.Vector()
    
    # Create matrix of all transitions in data
    dataMatrix = pykov.Matrix()
    
    for message in messageList:
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

    for message in messageList:
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
    writePath = name + " Chain.dat"
    writeDataFile = open(writePath, 'wb')
    pickle.dump(dataChain, writeDataFile)
    writeDataFile.close()

def GenerateMessage(chain, threshold):
    outputString = '['
    newSymbol = ''
    lastSymbol = '['

    while (lastSymbol != ']'):
        lastProbability = 0
        while (lastProbability < threshold):
            newSymbol = chain.move(lastSymbol)
            lastProbability = math.exp(chain.walk_probability([lastSymbol, newSymbol]))

        outputString = outputString + " " + newSymbol
        lastSymbol =  newSymbol
    return outputString

def BuildAll():
    messagesByPerson = ParseFacebookMessages()
    for name in messagesByPerson:
        GenerateChains(name, messagesByPerson[name])
