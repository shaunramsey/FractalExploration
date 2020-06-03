binSize = .1

class bin:
    def __init__(self, **kwargs):
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.binContent = kwargs.get('content')
    def setContent(self, content):
        self.binContent = content
    def clearContent(self):
        self.binContent = 0
    def getContent(self):
        return self.binContent
    def getID(self):
        return str(self.start) + "," + str(self.end)

#smallbin = bin(start = .5, end = 1.0, content = .25)
smallbin = bin()
#smallbin = bin(start = .5, end = 1.0)
print(smallbin.getContent())
print(smallbin.getID())
smallbin.setContent(.2)
print(smallbin.getContent())