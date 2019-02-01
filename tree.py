class node:
    ID = -1
    isDomain = True
    extension = None
    domainValue = None
    isSubDomain = True
    subDomainValue = None
    childrens = []
    spamValue = -1
    outwardLinks = []
    completeDomainName = None
    
    def getID(self):
        return self.ID
    
    def getChildrens(self):
        return self.childrens
    
    def hasChildrens(self):
        if(len(self.childrens) > 0):
            return True
        return False
        
    def setOutwardLinks(self, paramOutwardLinks):
        self.outwardLinks = paramOutwardLinks
        
    def getCompleteDomainName(self):
        return self.completeDomainName
    
    def hasOutwardLinks(self):
        if(len(self.outwardLinks) == 0):
            return False
        return True
    
    def getOutwardLinks(self):
        return self.outwardLinks