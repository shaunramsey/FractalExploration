import matplotlib.pyplot as plt
import numpy as np

#r = 3.74 # 5 cylce
#r = 3.9 # 3 cycle
#r = 3.3 # 2 cycle
#r = 2  #everything goes to 1/2

#does the actual cobwebplot
#savetofig = True if you want to save every step of the cobwebplot to a diff file
def cobwebplot_xo_r(r,x,color,n, savetofig=False):
    nx = r * np.multiply(x,  (-1*x + 1))
    plt.plot([x , x],[0,  nx], c=color)
    if savetofig:
        plt.savefig("x0.png")
    plt.plot([nx, x],[nx, nx], c=color)
    if savetofig:
        plt.savefig("x1.png")
    for i in range(n):
        x = nx
        nx = r * np.multiply(x,  (-1*x + 1))      
        plt.plot([x, x], [x,  nx], c=color) 
        if savetofig:
            plt.savefig("x" + str(i*2+2) +".png")
        plt.plot([nx,x], [nx, nx], c=color)
        if savetofig:
            plt.savefig("x" + str(i*2+3) +".png")
        x = nx
        #print(i, x)
    print(x)

#makes the figure with the logistic equation and sets up all the figure options
def makefig(r):        
    fig = plt.figure(figsize=(10.5, 8))
    ax = fig.gca()
    
    plt.suptitle("Logistic Equation")
    plt.title("r = " + str(r))
    plt.xlabel("x_n")
    plt.ylabel("x_(n+1)")
    
    
    x = np.linspace(-0.01, 1.01, 1000)
    po = 0.05
    y = po / (po + (1-po)*np.exp(-r*x))
    y = r * np.multiply(x, 1-x)
    
    maxy = r*0.25
    maxy = 1.0
   
    
    #plt.imshow(fractal_grid, vmax = 0.01, cmap = lyap_cmap, origin = "lower", extent = (lowerbound, upperbound, lowerbound, upperbound))
   
    line = [[-0.01, maxy+0.1], [-0.01, maxy+0.1]] #line for y = x on the plt
    xaxes = [0, 0,             -0.06, 1.01] #line for the x axis
    yaxes = [-0.06, maxy+0.01, 0, 0] #line for the y axis
    #plt.grid(True)
    xs = np.arange(-0.1, 1.1, 0.05) #  list of xticks 
    ys = np.arange(0,maxy+0.1, 0.05) # list of yticks
    xticks = [] #this is for the labels on the xticks
    
    # setting up the list of strings for the xtick labels
    for i in range(len(xs)):
        if i%2 == 1:
            xticks.append("")
        else:
            xticks.append(str(xs[i]))
            
    
    ax.set_xticks(xs) # set the x ticks (on the axis)
    ax.set_yticks(ys) # set the y ticks (on the axis)
    ax.set_xticklabels(xticks) #set the labels on the xticks
    plt.grid(True)  #draw the grid
    
    plt.plot(line[0], line[1], linestyle=":") # y=x
    plt.plot(xaxes[0:2], yaxes[0:2], c="k")   # x axis in black
    plt.plot(xaxes[2:4], yaxes[2:4], c="k")   # y axis in black
    plt.plot(x,y)



#x = 0.26
x = 0.7
#x = 0.2549
#r = 3.9 # use this for "chaos"
r = 3.3 # use this for 2 cycle
#r = 2  # use this for single stable fixed point

n = 100


makefig(r)
#cobwebplot_xo_r(r, 0.075, "b", n)
#cobwebplot_xo_r(r, 0.05, "c", n)
#cobwebplot_xo_r(r, 0.3, "m", n)
cobwebplot_xo_r(r, 0.1, "m", n)
cobwebplot_xo_r(r, 0.5, "r", n)
#cobwebplot_xo_r(r, 0.0, "k", n)
#cobwebplot_xo_r(r, 0.02,"orange", 10)
#cobwebplot_xo_r(r,x+0.00125, "m", n)
#cobwebplot_xo_r(r,x+0.0025,"b",n)


'''
#uncomment this block to gives some room on the right for our presentation
plt.subplots_adjust(top=0.88, bottom=0.11, left=0.11,right=0.80, hspace=0.2, wspace=0.2)

if r == 3.9:
    plt.figtext(0.82,0.4,"Try x_0 values:\n(Do only 4 iter'ns)\n------------------\nx_0 = 0.1\n\nx_0 = 0.05\n\nx_0 = 0.075\n\n--------\n\nx_0 = 0.70\n\nx_0 = 0.75\n\nx_0 = 0.8", None, size=14)
elif r == 3.3:
    plt.figtext(0.82,0.5,"Try x_0 values:\n------------------\nx_0 = 0.8\n\nx_0 = 0.75\n\nx_0 = 0.5\n\n-----------------\n\nx_0 = 0.1\n\nx_0 = 0.2", None, size=14)
else:
    plt.figtext(0.82,0.4,"   Try the\n following\nx_0 values:\n------------------\nx_0 = 0.3\n\nx_0 = 0.8\n\nx_0 = 0.1\n\nx_0 = 0.5\n\nx_0 = 0.0\n\nx_0 = 0.01\n\nx_0 = 1.0",None,size=14)
'''

#you can use png or .pdf for save fig to save to other file types. You can also
# comment out this line if you don't want to save the figure to anything
plt.savefig("webr=" + str(r) + ".png") # pass the option "True" if you want to save every step of the cobwebplot
plt.show()





    