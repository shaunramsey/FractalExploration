binSize = .5

class bin:
    def __init__(self, **kwargs):
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.binContent = kwargs.get('content')
        if self.binContent == None:
            self.binContent = 0
        self.binSize = self.end - self.start
    def setContent(self, content):
        self.binContent = content
    def addContent(self, content):
        self.binContent = self.binContent + content
    def clearContent(self):
        self.binContent = 0
    def getContent(self):
        return self.binContent
    def getID(self):
        return (str(self.start) + "," + str(self.end))
    def percentageOfRange(self, rangeStart, rangeEnd):
        if rangeStart > rangeEnd:
            rangeStart, rangeEnd = rangeEnd, rangeStart
        #The logic for testing if two ranges intersect comes from Ned Batchelder's blog:
        #https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
        if self.end >=rangeStart and rangeEnd >= self.start:  
            #The logic for finding the intersection of the two ranges is inspired by User Oscar Smith's reply on StackExchange:
            #https://codereview.stackexchange.com/questions/178427/given-2-disjoint-sets-of-intervals-find-the-intersections/178432#178432
            return ((min(self.end, rangeEnd)-max(self.start, rangeStart))/(rangeEnd-rangeStart))
        else:
            return 0
            
            
class equation:
    def __init__(self, **kwargs):
        self.m = kwargs.get('m')
        self.b = kwargs.get('b')
        if self.m == None:
            self.m = 0
        if self.b == None:
            self.b = 0
       
    def getString(self):
        if self.b > 0:
            return str(self.m) + "x+" + str(self.b)
        elif self.b < 0:
            return str(self.m) + "x" + str(self.b)
        else:
            return str(self.m) + "x"
    def getM(self):
        return self.m
    def getB(self):
        return self.b
    def isBNegative(self):
        if self.b < 0:
            return True
        else:
            return False
    def setM(self, m):
        self.m = m
    def setB(self,b):
        self.b = b
    def setFromString(self, equationString): #Pass in equationString in the form of "mx+b", "mx-b", "-mx+b", "-mx-b", "mx" or "-mx"
        if equationString[0] == "-":
            self.setM(float(equationString[0]+equationString[1]))
            if len(equationString) == 3:
                return
            elif equationString[3] == "-":
                self.setB(float(equationString[3]+equationString[4]))
            else:
                self.setB(float(equationString[4]))
        else:
            self.setM(float(equationString[0]))
            if len(equationString) == 2:
                return
            elif equationString[2] == "-":
                self.setB(float(equationString[2]+equationString[3]))
            else:
                self.setB(float(equationString[3]))
    def getX(self, y):
        return((y-self.b)/self.m)

    def getY(self, x):
        return((x * self.m)+self.b)

class tentEquation: #TODO expand to have full functionality to modify, etc
    def __init__(self, equation0, equation1, alpha):
        self.equation0 = equation0
        self.equation1 = equation1
        self.alpha = alpha
    #def getX(self, y): #Cant pass only one point back because, well you know, so not writing now for ease
    def getY(self, x):
        if x <= self.alpha:
            return self.equation0.getY(x)
        else:
            return self.equation1.getY(x)

def binIni(binSize):
    binList = []
    for i in range(0, int(1/binSize)):
        print(int(1/binSize))
        binList.append(bin(start=(i*binSize), end=((i*binSize)+binSize)))
        print("Start= " + str(i*binSize)+ ", End= " + str((i*binSize)+binSize))
    return binList

binsForDayz = binIni(binSize)
bigEquation = tentEquation(equation0=equation(m=2), equation1=equation(m=-1.5, b=1.75), alpha=.5)

def printBIN():
    for i in range(len(binsForDayz)):
        print (str(binsForDayz[i].getID()) + ", Content: " + str(binsForDayz[i].getContent()))

for i in range(int(1/binSize)):
    
    yStart = bigEquation.getY(i * binSize)
    yEnd = bigEquation.getY((i+1) * binSize)
    print("I: " +str(i))
    print("yStart: " + str(yStart))
    print("yEnd: " + str(yEnd))
    contentTotal = 0
    #print(i)
    for j in range(len(binsForDayz)):
        tempPercentage = binsForDayz[j].percentageOfRange(rangeStart = yStart, rangeEnd = yEnd)
        binsForDayz[j].addContent(tempPercentage)
        contentTotal = contentTotal + tempPercentage
        if contentTotal >= 1:
            break
    printBIN()
print(bigEquation.equation0.getString())
print(bigEquation.equation1.getString())
#print(str(bigEquation.getM()))
#print(str(bigEquation.getB()))
#print("Length of list: "+ str(len(binsForDayz)))
#for i in range(len(binsForDayz)):
#    print (str(binsForDayz[i].getID()) + ", Content: " + str(binsForDayz[i].getContent()))