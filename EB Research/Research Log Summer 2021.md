Research Log Summer 2021 - Eric Botti
Week of 6/7 - 6/11

Questions:

- What You've Finished for the Day
- What you're still working on (what's next)
- What tools you used - links that you used for references that day?
- Are there any blockages/bugs/errors?

6/7/2021

I spend the first hour or so of the day getting familiar with Matplotlib in Python. Before this experience I have only used it briefly and for scatter plots and confusion matrices. Learning the basics of Matplotlib was essential before trying to do anything more advanced like the Cobweb plot I was researching.

After reading through the Wikipedia pages on cobweb plots and logistic maps, I had a grasp of what exactly they were, which allowed me to get started on my own function that creates cobweb plots based off the logistic map equation. The first step was to graph the line y=x and the curve created by rx(1-x). This was relatively simple to do with the plot function.  
Drawing the boxes, or the cobwebs if you would, was a little more difficult. I tried doing it on my own by following the 4 steps outlined in the Wikipedia page for cobweb plots:

1. Find the point on the curve at x_0,
2. Plot horizontally across from this point to the diagonal line
3. Plot vertically from the point on the diagonal to the function curve
4. Repeat from step 2 as required.

I quickly realized that while this made sense to a human it was impractical to code in Matplotlib. Firstly, these steps are missing a step zero where it the vertical line starts at (x_0, 0) and goes to the point on the curve at x_0. Second Matplotlib plots with 2 arrays, one of x coordinates and one of y coordinates, not one line pair at a time.
So instead I made a program that went started at the point (x_0, 0) and repeated the process of drawing a vertical line to the curve and a horizontal line to the diagonal line.

Tomorrow I will be working on using Git to sync my work in the cloud and making bifurcation plots.

Resources Today:

- https://en.wikipedia.org/wiki/Cobweb_plot
- https://en.wikipedia.org/wiki/Logistic_map
- Intro to Matplotlib Plots: https://www.youtube.com/watch?v=ziRNzO1T-Mo&t=647s
- CobWeb Plot Code Example: https://scipython.com/blog/cobweb-plots/

6/8/2021

Today I started working on making bifurcation diagrams. I read up on them on the Wikipedia page and it was relatively easy to understand as I have gone over them a few times now with Dr. Ramsey.  
My first intuition on how to make this diagram was to simply take the last point generated from the cobweb plot at each R value. So, I made a for loop that went form r of 0 to 4 and plotted the last x value of each array. This ended up being like half a bifurcation diagram where I everything when it converged on one point but could only see one of the current lines when it was bouncing between points regularly or just being chaotic.

The question became how I get the rest of the points in. I really struggled with this part for a bit and was trying some very complicated ideas such as using if statements to plot more than one point for r values if it was greater than a certain value. This makes sense as we know the behavior of logistic maps and where they become chaotic, but on principle isn't good coding as we want something flexible and more reusable.

In this time, I figured you could shorten going through the cobwebbing process I had copied over from the cobweb plot function and just iterate through the function but was not able to get very far in the. I ended up trying to plot more and. I looked at the code for a bifurcation plot used on the GitHub and saw they used a scatter plot.

I decided to come back to my idea of using the plot function. I found that by running the plot command many times with a series of x values coming from iterating the function over and over. After talking to Dr Ramsey about it I realized this relies on the assumption that these R values have sequential connection. When dealing with chaotic systems this can connection that seems like it is there can unfortunately break down. Right around r= 3.5 is an example of this where my plot generates a bar in between the points where it should not be, whilst the scatter plot does not. Dr Ramsey talked a little bit about how this problem can be overcome with hashing, and I will be working on that tomorrow.

![Scatter Bifurcation_diagram](https://github.com/shaunramsey/FractalExploration/blob/70e75f21b2591a4f77fec27e8dfd706d2d05be38/EB%20Research/bifurcation_diagram.png)
![EB Bifurcation_diagram](https://github.com/shaunramsey/FractalExploration/blob/70e75f21b2591a4f77fec27e8dfd706d2d05be38/EB%20Research/bifurcation_diagram_eb.png)

I also took some time today to familiarize myself with GitHub and being able to get my code and research logs backed up on to there.

Resources Today:

- https://en.wikipedia.org/wiki/Bifurcation_diagram

6/9/21
I started today by researching into k-d trees. K-d trees are trees which are representative of a point cloud in of dimension k. Our points are on 2d space so k=2. A k-d tree is very useful for searching as each node only has two children, and it cuts the plane of points in half by an axis. For example, if a node is x aligned then the left child, and all its children are nodes with lower x values, and right child and all its children have greater or equal x values. This nodes child will then divide the plane by the y axis. This goes on alternating until the last nodes in the tree. Therefore, searching becomes as easy as determining if the x and y values are greater or equal to the current point then following down the tree based on axis alignment.
After playing around for a bit and I found a k-d tree implantation in the scipy package. Simultaneously I had also been looking up other people's implementations of their own k-d tree classes and seeing how it worked. I try a bit to create my own simple version of the class just to gain a better understanding. I was able to conceptually understand that a tree of nodes each with a left and right child was necessary but didn't end up
It turns out however that we did not need a k-d tree at all to make this work. The original idea was to use the nearest neighbor capabilities of a k-d tree but instead we can just use some simple distance computing equations to determine where the closest next point to draw a line will be.
Today's References
• https://www.geeksforgeeks.org/k-dimensional-tree/
6/10/21
Today I set out to replace our nearest neighbor idea, with instead finding the closest x value from the previous line. Because the value

I also started looking into what
Today's References:
• https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
• https://matplotlib.org/stable/tutorials/colors/colormaps.html
• https://matplotlib.org/stable/tutorials/colors/colormap-manipulation.html
6/11/21
This morning I decided to start work on redefining what we measure as to remove duplicate points from. The simple solution we discussed earlier in the week was to redefine a = b as true when a - ε < b and b < a + ε where ε is our margin of acceptable error, something we must take in to account. The problem is a little more complicated because we must deal with whole arrays of values instead of just one. Python has a problem sometimes determining the with and statements and truth values and it was returning errors about being unable to get the truth value from an array of multiple entries. The solution I initially came up with seemed like it was working but turned out to only be accepting new values that were greater than or less than existing ones. After talking with Dr Ramsey, I changed it to instead check if the absolute value of the difference between a and b was ever less than
I went back to working on the plotting feature of the diagram. I was having a lot of trouble determining how exactly find which points were closest to each other. I realized I needed to flip the for loops I had to move through the r values first rather than through n iterations first. This means that when you have moved on to the second r value all the first r value's lines will be plotted. This allows us to look back at the previous r value to see if lines stay the same, converge, or diverge. I managed to write an equation that finds the closest x value
When talking to Dr Ramsey we changed a few important things. First now our program looks to the next r value bucket to see if the behavior of the map value. Second there is no longer a fixed number of lines created at the beginning, instead every time a new line is needed a new list is appended to the list of lines. We also have an index value which keeps track of the index of r_i that the line was created. For Monday I am going to work on implementing a stable matching problem approach to
Finally, today we talked a little bit about what to do for the presentation coming up in 2 weeks. It is hard to believe it has been a full week of working already, but it has. We developed a general idea of what should go into the presentation and know for sure we want to compare our linear approximation's plots versus the default maps. Next week we will work on finding the code for these approximations and the charts made and running them.
Today's References:
• https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
• https://www.w3schools.com/python/ref_func_all.asp
• https://www.kite.com/python/answers/how-to-count-the-number-of-unique-values-in-a-list-in-python#:~:text=Use%20set()%20and%20len,the%20number%20of%20unique%20values.
