import numpy as np
from matplotlib import pyplot as plt

rResolution = 5000 #number of r's tested
rMax = 4 #maximum r
initialLoopCount = 100 #number of iterations before starting list
initialPoint = 0.5 #initial starting point for iterations
postLoopCount = 1000 #number of loops adding to list and testing before deciding no reoccuring number will be found

def bifurcationPoint(r,initialLoopCount, initialPoint, postLoopCount):
    tempPoint = initialPoint
    for i in range(initialLoopCount):
        tempPoint = r * tempPoint * (1- tempPoint)
    
    tempList = [tempPoint]
    foundGroup = False
    for i in range(postLoopCount-1):
        tempPointPost = r * tempList[i] * (1- tempList[i])
        
        for j in range(len(tempList)):
            if tempPointPost == tempList[j]:
                foundGroup = True
                break
        if foundGroup == True:
            break
        tempList.append(tempPointPost)
    print(r, foundGroup, len(tempList))
    return tempList
    
rInterval = (rMax-1)/rResolution
for i in range(rResolution):
    tempR = (rInterval * i) + 1
    tempListPost = bifurcationPoint(tempR,initialLoopCount, initialPoint, postLoopCount)
    sizedRList = []
    for j in range(len(tempListPost)):
        sizedRList.append(tempR)
    plt.scatter(sizedRList,tempListPost, s=.01, marker='.', linewidths=0)


plt.title("Bifurcation Plot")
plt.xlabel("r")
plt.ylabel("Orbits")
plt.savefig("Bifurcation (Resolution=" + str(rResolution) + ").png", dpi=1000, format='png', bbox_inches='tight')
plt.show()