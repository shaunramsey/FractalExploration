Research Log Summer 2021 - Eric Botti

Questions:

- What You've Finished for the Day
- What you're still working on (what's next)
- What tools you used - links that you used for references that day?
- Are there any blockages/bugs/errors?

6/7/2021

I spend the first hour or so of the day getting familiar with Matplotlib in Python. Before this experience I have only used it briefly and for scatter plots and confusion matrices. Learning the basics of Matplotlib was essential before trying to do anything more advanced like the Cobweb plot I was researching. 

After reading through the Wikipedia pages on cobweb plots and logistic maps, I had a grasp of what exactly they were, which allowed me to get started on my own function that creates cobweb plots based off the logistic map equation. The first step was to graph the line y=x and the curve created by rx(1-x). This was relatively simple to do with the plot function.  
Drawing the boxes, or the cobwebs if you would, was a little more difficult. I tried doing it on my own by following the 4 steps outlined in the Wikipedia page for cobweb plots: 


1.	Find the point on the curve at x_0, 
2.	Plot horizontally across from this point to the diagonal line
3.	Plot vertically from the point on the diagonal to the function curve
4.	Repeat from step 2 as required.

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

![image]


I also took some time today to familiarize myself with GitHub and being able to get my code and research logs backed up on to there. 


Resources Today: 
- https://en.wikipedia.org/wiki/Bifurcation_diagram