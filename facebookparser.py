from bs4 import BeautifulSoup
import sys
import pickle

# Needed for final file serialization, this thing gets big
# Increase if pickle complains
#sys.setrecursionlimit(10000)

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
        
writeName = "Random"
while(writeName != "quit"):
    writeName = input("Select which users messages to save to disk: ")
    if writeName in messagesByPerson:
        serializePath = writeName + ".dat"
        serializeFile = open(serializePath, 'wb')
        pickle.dump(messagesByPerson[writeName], serializeFile)
        serializeFile.close()
