from __future__ import division
import os
import re
import sys
from collections import Counter
import math
import threading
import time
from consoleColors import bcolors
from customExceptions import NoDataAvailableException
from customExceptions import invalidRowException
from customExceptions import invalidDataException


class fileLoad:
    
    fileName = None
    def __init__(self, paramFileName):
        # initializer for class
        # currently nothing
        self.fileName = paramFileName
    
    def fnLoadHostNames(self):
        print('Reading total Hosts available')
        
        # here we will get the host names
        # open the file
        # assuming it has passed the validation
        fileObj = open(self.fileName, 'r')
        
        # read the contents
        objContents = fileObj.read()
        
        # now seperate the file content by next line ('\n')
        listObjContents = objContents.split('\n')
        
        # get the total host list
        listTotalHosts = []
        
        # now for each row, extract the values
        totalRowsRead = 0
        for rows in listObjContents:
            sys.stdout.write('\r' + 'Reading host ID : ' + str(totalRowsRead) + '               ')
            sys.stdout.flush()
            listTotalHosts.append(rows.split(' ')[1])
            totalRowsRead += 1
           
        print(bcolors.OKGREEN + '\nAll host read' + bcolors.ENDC)
        return listTotalHosts
        
    def fnLoadHostGraph(self, paramListHosts):
        print('Loading host graph')
        
        # this one is important
        # we will import the node file
        from tree import node
        
        # set the core graph
        listCoreGraph = []
        
        intTotalRowIteration = 0
        # now iterate through all the host values and create the graph
        
        intTotalHosts = len(paramListHosts) - 1
        listTempHostValues = []
        for hostValues in paramListHosts:
            
            sys.stdout.write('\r' + 'Creating Raw HostGraph (without crosslinks) ' + ' ( ' + str(round(intTotalRowIteration * 100/intTotalHosts, 2)) + '% )              ')
            sys.stdout.flush()
            
            # check if it's the domain or subdomain
            listHost = hostValues.split('.')
            
            if(intTotalRowIteration == 323):
                pass
            
            totalValuesInList = -1
            if hostValues.find('www') == -1:
                totalValuesInList = 3
            else:
                totalValuesInList = 4
                
            if(len(listHost) <= totalValuesInList):
                # it's a main domain and not a sub domain
                # assuming that we have distinct domain name
                # first check whether we already have the domain name or not ?
                boolAlreadyHaveDomainName = False
                
                strCompleteDomainName = ''
                if(hostValues.find('www') == -1):
                    strCompleteDomainName = listHost[-3] + '.' + listHost[-2] + '.' + listHost[-1]
                else:
                    strCompleteDomainName = 'www.' + listHost[-3] + '.' + listHost[-2] + '.' + listHost[-1]
                    
                if(strCompleteDomainName in listTempHostValues):
                    for nodes in listCoreGraph:
                        if nodes.completeDomainName == strCompleteDomainName:
                            # we need to just update the id only
                            nodes.ID = intTotalRowIteration
                            boolAlreadyHaveDomainName = True
                            break
                
                if(boolAlreadyHaveDomainName == False):
                    nodeObj = node()
                    nodeObj.ID = intTotalRowIteration
                    nodeObj.isDomain = True
                    nodeObj.extension = listHost[-2] + '.' + listHost[-1]
                    nodeObj.domainValue = listHost[-3]
                    nodeObj.isSubDomain = False
                    nodeObj.subDomainValue = None
                    nodeObj.childrens = []
                    nodeObj.spamValue = 0
                    nodeObj.completeDomainName = hostValues
                    listCoreGraph.append(nodeObj)
                
                
            else:
                # check if the domain already exists or we have to create
                # a new domain node
                # get the domain name
                strDomain = listHost[-3]
                
                # iterate through listCoreGraph
                boolFoundDomain = False
                
                for nodes in listCoreGraph:
                    if nodes.domainValue == strDomain:
                        boolFoundDomain = True
                        # extract sub domain value
                        strSubDomain = ''
                        intTotalURLLength = len(listHost)
                        
                        for totalIteration in range(1, intTotalURLLength - 3):
                            strSubDomain += listHost[totalIteration] + '.'
                        
                        strSubDomain = strSubDomain[:-1]
                        
                        nodeObjChild = node()
                        nodeObjChild.ID = intTotalRowIteration
                        nodeObjChild.isDomain = False
                        nodeObjChild.extension = listHost[-2] + '.' + listHost[-1]
                        nodeObjChild.domainValue = listHost[-3]
                        nodeObjChild.isSubDomain = True
                        nodeObjChild.subDomainValue = strSubDomain
                        nodeObjChild.childrens = []
                        nodeObjChild.spamValue = 0
                        nodeObjChild.completeDomainName = hostValues
                        nodes.childrens.append(nodeObjChild)
                        
                if(boolFoundDomain == False):
                    # we don't have the domain value
                    # we have to add the domain first
                    # then add the child
                    
                    # add the domain
                    nodeObjParent = node()
                    nodeObjParent.ID = -1
                    nodeObjParent.isDomain = True
                    nodeObjParent.extension = listHost[-2] + '.' + listHost[-1]
                    nodeObjParent.domainValue = listHost[-3]
                    nodeObjParent.isSubDomain = False
                    nodeObjParent.subDomainValue = None
                    nodeObjParent.childrens = []
                    nodeObjParent.spamValue = 0
                    
                    strCompleteDomainName = ''
                    if(hostValues.find('www') == -1):
                        strCompleteDomainName = listHost[-3] + '.' + listHost[-2] + '.' + listHost[-1]
                    else:
                        strCompleteDomainName = 'www.' + listHost[-3] + '.' + listHost[-2] + '.' + listHost[-1]
                    
                    listTempHostValues.append(strCompleteDomainName)
                    nodeObjParent.completeDomainName = strCompleteDomainName
                    
                    strSubDomain = ''
                    intTotalURLLength = len(listHost)
                    
                    for totalIteration in range(0, intTotalURLLength - 3):
                        strSubDomain += listHost[totalIteration] + '.'
                    
                    strSubDomain = strSubDomain[:-1]
                    
                    nodeObjChild = node()
                    nodeObjChild.ID = intTotalRowIteration
                    nodeObjChild.isDomain = False
                    nodeObjChild.extension = listHost[-2] + '.' + listHost[-1]
                    nodeObjChild.domainValue = listHost[-3]
                    nodeObjChild.isSubDomain = True
                    nodeObjChild.subDomainValue = strSubDomain
                    nodeObjChild.childrens = []
                    nodeObjChild.spamValue = 0
                    nodeObjChild.completeDomainName = hostValues
                    nodeObjParent.childrens.append(nodeObjChild)
                    listCoreGraph.append(nodeObjParent)
                    
            intTotalRowIteration += 1
        
        print(bcolors.OKGREEN + '\nRaw Host graph created successfully' + bcolors.ENDC)
        print('Cross linking hosts in graph')
        print(bcolors.WARNING + 'This might take some time (depending on the processor/server)' + bcolors.ENDC)
        # opening the hostGraphWeighted file
        # open the file
        # assuming it has passed the validation
        fileObj = open(self.fileName, 'r')
        
        # read the contents
        objContents = fileObj.read()
        
        # now seperate the file content by next line ('\n')
        listObjContents = objContents.split('\n')
        
        # now the links are in the form
        # LINKID -> {TOTAL_links}
        intTotalRowIteration = 0
        
        for links in listObjContents:
            sys.stdout.write('\r' + 'Cross links Hosts for Host ID : ' + str(intTotalRowIteration) + ' ( '+str(round((intTotalRowIteration) * 100/intTotalHosts, 2))+'% )               ')
            sys.stdout.flush()
            intTotalRowIteration += 1
            
            # get the total linking hosts
            if(len(links.split('->')[1].strip().split(' ')[0]) > 0):
                strValueHostName = paramListHosts[int(links.split('->')[0])]
                listTotalOutwardLinks = links.split('->')[1].strip().split(' ')
                
                listOutwardLinkID = []
                # now get the domain name
                for outwardLinks in listTotalOutwardLinks:
                    listOutwardLinkID.append(int(outwardLinks.split(':')[0]))
                intHostValueID = int(links.split('->')[0])     
                
                if(intHostValueID == 8):
                    pass
                                
                # now with the host id add the values 
                # iterate through the complete tree list values
                boolFoundValue = False
                for hostGraphValue in listCoreGraph:
                    
                    if(str(hostGraphValue.getID()) == str(intHostValueID)):
                        hostGraphValue.setOutwardLinks(listOutwardLinkID)
                        boolFoundValue = True
                        break
                    elif hostGraphValue.getID() == -1:
                        # since it's only 2 level depth 
                        # so no recursion
                        if(hostGraphValue.hasChildrens()):
                            for hostGraphChildrens in hostGraphValue.getChildrens():
                                if(str(hostGraphChildrens.getID()) == str(intHostValueID)):
                                    hostGraphValue.setOutwardLinks(listOutwardLinkID)
                                    boolFoundValue = True
                                    break
                    else:
                        # since it's only 2 level depth 
                        # so no recursion
                        if(hostGraphValue.hasChildrens()):
                            for hostGraphChildrens in hostGraphValue.getChildrens():
                                if(str(hostGraphChildrens.getID()) == str(intHostValueID)):
                                    hostGraphValue.setOutwardLinks(listOutwardLinkID)
                                    boolFoundValue = True
                                    break
                    
        print(bcolors.OKGREEN + '\nHost Graph Created Successfully' + bcolors.ENDC)
        return listCoreGraph
    
    def fnInjectTrainLabelsToHostGraph(self, paramHostGraph, paramHostNames):
        
        # we hvae the hsot graph
        # we need to inject the training data
        print('Injecting the training data labels to the host graph')
        
        fileObj = open(self.fileName, 'r')
        
        # read the contents
        objContents = fileObj.read()
        
        # now seperate the file content by next line ('\n')
        listObjContents = objContents.split('\n')
        
        listSpammyID = []
        listNonSpammyID = []
        
        for values in listObjContents:
            
            strDomainName = values.split(' ')[0]
            strSpamType = values.split(' ')[1]
            # get the id
            idx = paramHostNames.index(strDomainName)
            
            # now check whether they are spammy or not ?
            if(strSpamType == 'normal'):
                listNonSpammyID.append(idx)
            else:
                listSpammyID.append(idx)
        
        # now we have the values for the spam and non spam
        print('Updating host spam values based on the training data')
        
        intTotalIteration = 0
        intTotalHosts = len(list(paramHostGraph)) - 1
        
        for nodeValues in paramHostGraph:
            sys.stdout.write('\r' + 'Training the model with the input label data ' + ' ( ' + str(round(intTotalIteration * 100/intTotalHosts, 2)) + '% )              ')
            sys.stdout.flush()
            
            if(nodeValues.hasOutwardLinks()):
                for outwardNodes in nodeValues.getOutwardLinks():
                    if(outwardNodes in listNonSpammyID):
                        if(nodeValues.spamValue == -1):
                            nodeValues.spamValue = 1
                        else:
                            nodeValues.spamValue = nodeValues.spamValue / 2
                    elif (outwardNodes in listSpammyID):
                        if(nodeValues.spamValue == -1):
                            nodeValues.spamValue = 1
                        else:
                            nodeValues.spamValue = (nodeValues.spamValue + 1) / 2
            
            if(nodeValues.hasChildrens()):
                for children in nodeValues.getChildrens():
                    if(children.hasOutwardLinks()):
                        for outwardNodes in children.getOutwardLinks():
                            if(outwardNodes in listNonSpammyID):
                                if(children.spamValue == -1):
                                    children.spamValue = 0
                                else:
                                    children.spamValue = (children.spamValue) / 2
                            elif(outwardNodes in listSpammyID):
                                if(children.spamValue == -1):
                                    children.spamValue = 1
                                else:
                                    children.spamValue = (children.spamValue + 1) / 2
                                    
            intTotalIteration += 1
        print(bcolors.OKGREEN + '\nModel Trained' + bcolors.ENDC)
        print('Optimizing the model')
        
        intTotalIteration = 0
        intTotalHosts = len(list(paramHostGraph)) - 1
        
        for nodeValues in paramHostGraph:
            sys.stdout.write('\r' + 'Optimizing the model with the input label data ' + ' ( ' + str(round((intTotalIteration) * 100/intTotalHosts, 2)) + '% )              ')
            sys.stdout.flush()
            intTotalIteration += 1
            floatCurrSpamValue = -1
            if(nodeValues.spamValue == -1):
                nodeValues.spamValue = 1
            
            if nodeValues.hasChildrens():
                listGetChildrenValues = []
                for child in nodeValues.getChildrens():
                    if(child.spamValue != -1):
                        listGetChildrenValues.append(child.spamValue)
                
                # now get the average of the list value
                floatAvgValue = sum(listGetChildrenValues) / len(listGetChildrenValues)
                
                # now for each child update the spam values
                # if the value is greater than givenSpamValue
                for child in nodeValues.getChildrens():
                    if(child.spamValue == -1):
                        child.spamValue = floatAvgValue
                    else:
                        child.spamValue = (child.spamValue + floatAvgValue)/2
                
                # now update the root node with updated spam value
                listGetChildrenValues = []
                for child in nodeValues.getChildrens():
                    listGetChildrenValues.append(child.spamValue)
                
                floatAvgValue = sum(listGetChildrenValues) / len(listGetChildrenValues)
                
                # now update the root node value
                nodeValues.spamValue = (nodeValues.spamValue + floatAvgValue) / 2
            
        print(bcolors.OKGREEN + '\nSuccessfully trained the host graph' + bcolors.ENDC)
        return paramHostGraph
    
    def fnPredictTestLabels(self, paramTestURL, paramHostNames):
        print('Predicting labels from the test file')
        fileObj = open(paramTestURL, 'r')
        hostGraph = self.fileName
        
        # read the contents
        objContents = fileObj.read()
        
        # now seperate the file content by next line ('\n')
        listObjContents = objContents.split('\n')
        
        listPredictedLabels = []
        listGivenTestLabels = []
        listGivenSpamValue = []
        
        intTotalHosts = len(listObjContents) - 1
        intTotalIteration = 0
        
        for values in listObjContents:
            sys.stdout.write('\r' + 'Predicting the host [host ID : '+str(intTotalIteration)+'] ' + ' ( ' + str(round((intTotalIteration) * 100/intTotalHosts, 2)) + '% )              ')
            sys.stdout.flush()
            intTotalIteration += 1
            
            strHostName = values.split(' ')[0]
            listGivenTestLabels.append(values.split(' ')[1])
            
            # filter the host name
            if(strHostName.find('http://') != -1):
                strHostName = strHostName.split('http://')[1]
            
            intID = paramHostNames.index(strHostName)
            # we have the id, 
            # we need the output label
            outputLabel = 'undecided'
            floatSpamValue = 1
            
            for nodeValues in hostGraph:
                boolValueFound = False
                
                if(str(nodeValues.getID()) == str(intID)):
                    boolValueFound = True
                    floatSpamValue = nodeValues.spamValue
                    
                    if(floatSpamValue == -1):
                        break
                    elif(floatSpamValue >= 0.5):
                        outputLabel = 'spam'
                        break
                    elif(floatSpamValue >= 0 and floatSpamValue < 0.5):
                        outputLabel = 'normal'
                        break
                
                if(boolValueFound == False):
                    if(nodeValues.hasChildrens()):
                        for children in nodeValues.getChildrens():
                            if(str(children.getID()) == str(intID)):
                                floatSpamValue = children.spamValue
                                if(floatSpamValue == -1):
                                    break
                                elif(floatSpamValue >= 0.5):
                                    outputLabel = 'spam'
                                    break
                                elif(floatSpamValue >= 0 and floatSpamValue < 0.5):
                                    outputLabel = 'normal'
                                    break
            listGivenSpamValue.append(floatSpamValue)
            listPredictedLabels.append(outputLabel)
        
        # print the values
        totalCorrect  = 0
        totalValues = len(listPredictedLabels)
        strDetails = 'Spam prediction using host graph \n Name : Deep Prakash Singh \n B00 Number : B00792279 \n ----------------------------- \n'
        strOutput = ''
        
        # calculate a,b,c,d as given in the paper
        a = 0
        b = 0
        c = 0
        d = 0
        recall = 0
        false_positive_rate = 0
        f_measure = 0
        precision = 0
        accuracy = 0
        for values in range(0, len(listPredictedLabels)):
            if listGivenTestLabels[values] == 'normal' and listPredictedLabels[values] == 'normal':
                a += 1
            if listGivenTestLabels[values] == 'normal' and listPredictedLabels[values] == 'spam':
                b += 1
            if listGivenTestLabels[values] == 'spam' and listPredictedLabels[values] == 'normal':
                c += 1
            if listGivenTestLabels[values] == 'spam' and listPredictedLabels[values] == 'spam':
                d += 1
            
            if(listPredictedLabels[values] == listGivenTestLabels[values]):
                totalCorrect += 1
                strOutput += paramHostNames[values] + ' ' + listPredictedLabels[values] + ' ' + listGivenTestLabels[values] + ' ' + str(listGivenSpamValue[values]) + ' ' + ' Correct ' + '\n'
            else:
                strOutput += paramHostNames[values] + ' ' + listPredictedLabels[values] + ' ' + listGivenTestLabels[values] + ' ' + str(listGivenSpamValue[values]) + ' ' + ' Incorrect ' + '\n'
        
        recall = round(d/(c+d),2)
        false_positive_rate = round((b/(b+a)),2)
        precision = round((d/(b+d)),2)
        f_measure = round(((2 * precision * recall)/(precision + recall)),2)
        accuracy = round((totalCorrect)/totalValues,2)
        
        strResult = '\n -------------------- \nRecall : ' + str(recall) + '\nFalse positive rate : '+str(false_positive_rate)+' \nPrecision : ' + str(precision) + ' \nF-Measure : ' + str(f_measure) + ' \nAccuracy : ' + str(accuracy) + ' \n'
        
        fObj = open('output.txt','w')
        fObj.write(strDetails + strOutput + strResult)
        fObj.close()
        print(bcolors.OKGREEN + '\nResults successfully written to output.txt file' + bcolors.ENDC)
        return listPredictedLabels
        
        
def screenPrint(isComment, boolEnablePrint, terminalColor, content):
    
    if(boolEnablePrint & isComment):
        print(terminalColor + '' + content + '' + bcolors.ENDC)
        
    if(isComment == False):
        print(terminalColor + '' + content + bcolors.ENDC)