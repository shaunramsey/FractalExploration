We have recreated the original Markus-Lyapunov fractal ([https://en.wikipedia.org/wiki/Lyapunov_fractal](https://en.wikipedia.org/wiki/Lyapunov_fractal)) in python with matplotlib to explore its properties.

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





