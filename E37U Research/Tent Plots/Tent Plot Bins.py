binSize = .1

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
    def clearContent(self):
        self.binContent = 0
    def getContent(self):
        return self.binContent
    def getID(self):
        return (str(self.start) + "," + str(self.end))
    def isInRange(self, rangeStart, rangeEnd):
        if self.start >= rangeStart and self.end <= rangeEnd:
            return True
        else:
            return False
    def percentageOfRange(self, rangeStart, rangeEnd):
        if self.isInRange(rangeStart, rangeEnd) == True:
            return self.binSize /(rangeEnd - rangeStart)
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
    #def getX(self, y): #cant pass only one point so not writing now for ease
    def getY(self, x):
        if x <= self.alpha:
            return self.equation0.getY(x)
        else:
            return self.equation1.getY(x)

def binIni(binSize):
    print(3*binSize)
    print(binSize)
    binList = []
    for i in range(0, int(1/binSize)):
        print(int(1/binSize))
        binList.append(bin(start=(i*binSize), end=((i*binSize)+binSize)))
        print("Start= " + str(i*binSize)+ ", End= " + str((i*binSize)+binSize))
    return binList

binsForDayz = binIni(binSize)
bigEquation = tentEquation(equation0=equation(m=2), equation1=equation(m=-2, b=2), alpha=.5)

for i in range(int(1/binSize)):
    yStart = bigEquation.getY(i/10)
    yEnd = bigEquation.getY(i/10 + binSize)
    print("I: " +str(i))
    print("yStart: " + str(bigEquation.getY(i/10)))
    print("yEnd: " + str(bigEquation.getY(i/10 + binSize)))
    contentTotal = 0
    #print(i)
    for j in range(len(binsForDayz)): #NOTE This assumes no bins will ever need multiple contents added to them in some way
        tempPercentage = binsForDayz[j].percentageOfRange(rangeStart = yStart, rangeEnd = yEnd)
        if tempPercentage == 1:
            binsForDayz[i].setContent(1)
            contentTotal = 1
        elif tempPercentage > 0:
            binsForDayz[i].setContent(tempPercentage)
            contentTotal = contentTotal + tempPercentage
        if contentTotal == 1:
            break



#print(str(bigEquation.getM()))
#print(str(bigEquation.getB()))
#print("Length of list: "+ str(len(binsForDayz)))
for i in range(len(binsForDayz)):
    print (str(binsForDayz[i].getID()) + ", Content: " + str(binsForDayz[i].getContent()))