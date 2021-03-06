import sys
import os
import copy

class Text:
    """Manages dictionary for a single text."""
    #The initialization calls on all methods needed to populate the class
    def __init__(self, filePath, fileName="__undefined"):
        if fileName != "__undefined":
            self.name = fileName
        else:
            self.name = filePath
        
        file = open(filePath, 'r')
        self.contents = file.read().split()
        self.wordCount = len(self.contents)
        #Splits the contents into words - note punctuation needs to be taken 
        #care of later
        self.buildDict() 
        file.close()

    def buildDict(self):
        """Builds the dictionary"""
        self.dict = {}
        for word in self.contents:
            wx = word.strip('?.()[]-:!;,"\'').lower()
            #strips punctuation and converts to lowercase
            if wx in self.dict:
                self.dict[wx] += 1
            else:
                self.dict[wx]  = 1
                
                
class TextGroup:
    """A grouping of texts, generally texts by the same author.
    
    Takes pathName of the directory in which to find the group, and, optionally, a name for the textGroup. Builds a dictionary for all texts in the group (equivalent to concatenation of the texts). 
    
    """
    def __init__(self, pathName, groupName="__undefined"):
        if groupName == "__undefined":
            self.name = pathName
        else:
            self.name = groupName
            
        temp_filenames = os.listdir(pathName)
        self.files = []
        for file in temp_filenames:
            filePath = (pathName + "/" + file)
            if filePath.endswith(".txt"):
                self.files.append( (filePath, file) )
            elif file[0]==".":
                pass #ignore hidden files
            else:
                print("Ignoring file: " + filePath)
        
        self.documents = []
        self.documentNames = []
        
        for file in self.files:
            self.documents.append(Text(file[0],file[1]))
            self.documentNames.append(file[1])
            
        self.build_combined_dictionary()

    def build_combined_dictionary(self):
        """Builds dictionary and wordCount"""
        self.dict = {}
        self.wordCount = 0
        for document in self.documents:
            self.wordCount += document.wordCount
            if self.dict == {}:
                self.dict = copy.copy(document.dict)
            else:
                for word in document.dict:
                    if word in self.dict:
                        self.dict[word] += document.dict[word]
                    else:
                        self.dict[word]  = document.dict[word]
        

class TextGroup_Excluded:
    def __init__(self, textGroup, exclusion):
        """Builds a dictionary excluding certain Texts form the dictionary
        
        Generally used for validation and calibration, i.e. testing the model 
        on known sets of documents. Takes a list of Texts to exclude and 
        generates self.dict, self.name, self.wordCount. Operates fairly
        efficiently; avoids constructing a new dictionary from scratch
        
        """
        self.dict = copy.copy(textGroup.dict)        
        self.name = textGroup.name + "_EX"
        self.wordCount = textGroup.wordCount
        for word in exclusion.dict:
            self.dict[word] -= exclusion.dict[word]
            self.wordCount  -= exclusion.dict[word]
            if self.dict[word] == 0:
                del self.dict[word]



