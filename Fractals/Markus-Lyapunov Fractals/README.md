We have recreated the original Markus-Lyapunov fractal ([https://en.wikipedia.org/wiki/Lyapunov_fractal](https://en.wikipedia.org/wiki/Lyapunov_fractal)) in python with matplotlib to explore its properties.

## Stochasticity and Probability

### Stochastic AB Lyapunov fractal — in sequence "AB" there is a 50% chance at any time that the value will switch to the other (i.e., that A will switch to B and vice versa)
![Stochastic Fractal Image](lyapunov_fractal_stochastic.png)

### Probabilistic AB Lyapunov fractal -- in "AB" the probability that the value will switch varies is listed above the graph
![Lyapunov_Fractal_Image_Prob_0](lyapunov_fractal_probabilistic_AB_0.png)
![Lyapunov_Fractal_Image_Prob_25](lyapunov_fractal_probabilistic_AB_25.png)
![Lyapunov_Fractal_Image_Prob_75](lyapunov_fractal_probabilistic_AB_75.png)
![Lyapunov_Fractal_Image_Prob_90](lyapunov_fractal_probabilistic_AB_90.png)
![Lyapunov_Fractal_Image_Prob_100](lyapunov_fractal_probabilistic_AB_100.png)

### Animation (created using ImageMagick and ArtistAnimation) of the fractal changing with the probability
![Animated Lyapunov Fractal Image](Prob_Lyap_Fractal_Avg.gif)

## 2D Traversal of 3D Lyapunov space -- each frame is the a-b fractal generated for that fixed value of c
![Animated Lyapunov Fractal Image](Lyap_3D_slice.gif)

## 3D projection of Lyapunov space -- x-axis = a, y-axis = b, z-axis = c
If you look at the first image, you will see the first frame of the above animation represented in the front face of the cube. The white pixels--representing the border of chaos--have been replaced by translucent blue voxels for easier view of the inside structure. Chaotic voxels are completely transparent.

### Front face
![3D_Lyap_Fractal](3D_Lyapunov_Fractal.png)
### Turned 90 degrees
![3D_Lyap_Fractal_2](3D_Lyapunov_Fractal_2.png)
### Back face
![3D_Lyap_Fractal_3](3D_Lyapunov_Fractal_3.png)

## Using Fprime to Determine the Bifurcation Pattern of the Lyapunov Fractal
![Fprime Lyapunov Fractal Number of Bifurcations](Num_Bifurcations_Lyapunov_Fractal.png)

## Finding the Relative Difference between Lyapunov Exponents in a Single Fractal
![Original_Fractal](Lyapunov_Logistic_Fractal.png)
![Original Relative Difference](Relative_Difference_Fractal.png)
![Relative Difference with changes where RD > Epsilon](Relative_Difference_Fractal_Changes_Above_Epsilon.png)
![Number of Changes](Relative_Diff_Fractal_Num_Changes.png)
