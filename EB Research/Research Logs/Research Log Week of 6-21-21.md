Research Log Summer 2021 - Eric Botti
Week of 6/7 - 6/11

6/23/2021

I haven’t made research log for a while because I have spent much of the last week working on my presentation for the toll fellows' luncheon at Hynson. I did that today and it went very well. I had to make many graphs for it to explain to everyone. I also had to work on understanding the linear approximation system used last summer and making graphs about it. Finally, I have been gaining more knowledge about the Lyapunov Fractal and how to compute it.
Today after the presentation I worked in toll with Dr Ramsey to start really prepping for computing the fractal. Because the fractal computes each pixel based on 2 r values, we thought it would be interesting to make a cobweb plot which alternates between an a and a b r value. With some slight modifications to the cobweb plot code, I made a function which takes an array of r values and alternates between them through each iteration. The results are incredibly interesting, with regions that used to be super stable being less and less. Below is the graph of r_a = 2 and r_b = 3.

INSERT 2 R Cobweb

Next, I moved on to create a bifurcation plot that uses 2 r values. The r_a value changes and is plotted across the bottom like in a normal bifurcation plot, but in this case the user provides a second r_b value which will be compared to every single r value. This in affect mimics a single row (or column) of the Lyapunov fractal.

INSERT 2 R Bifurcation plot

Of course, this not an exact replication of the row of the fractal as the fractal draws its values from the Lyapunov exponent. However, this value could be calculated and plotted in a similar way to the 2 r bifurcation plot, with a fixed r value and then row of r values at the bottom where the Lyapunov exponent is graphed. I found a way to implement the calculation of the Lyapunov exponent by using the equation ln(|r \* (1 – 2x)| + epsilon) where r is an array of all r values and x is an array of all x values. Espsilon is a very small number used to prevent the log of zero from being taken as that would be – infinity and impossible to plot.

INSERT Lyapunov plot

Tomorrow I am going to start trying to make a fractal out of the Lyapunov values.

6/24/2021

The first problem I needed to address today is finding a way to convert the Lyapunov plot I made into a heatmap. I found a Python library called Seaborn which lets you create heatmaps very easily. I just needed to pass in a 2d array of all the Lyapunov values. I worked on converting the code I used for the plot to the fractal. The plot only calculated row or column of the fractal so I needed to change x from being an array of values to be an array of arrays containing all the values on the grid.
I store 2 lists of r instead of one now: r_a and r_b. These represented the ranges of the columns and rows respectively. I use the np.multiply function to multiply the columns of x by r_a and I multiple the transpose of x by r_b then transpose again to multiply the rows of x by r_b. This iterates the function in the columns by r_a and in the rows by r_b.

After making the heatmap some things with it are quiet wrong. For one the y axis was reversed, and both axis used bad scaling labels (they were using the index of r rather than the value of r at those places).

For tomorrow I am not going to use seaborn to do my plot as I found there is a plot native to matlplotlib called imshow that we used last year. I am going to look at the previous fractal construction methods
