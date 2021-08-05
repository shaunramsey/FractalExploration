
import numpy as np
# measure time it takes
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import copy
from numba import jit
# Scipy sparse matrix solvers
import scipy
from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

class PWApprx:

    def __init__(self, x_values, r):
        self.x_values = x_values
        self.r = r
        self.y_values = np.multiply(x_values, r) * np.subtract(1, x_values)
        self.func_list = self.__create_func_list(x_values, self.y_values, r)  
        self.slope_list = self.__create_slope_list(x_values,self.y_values, r)      
    
    def compute(self, x):
        # clamp x to between zero and one
        x = max(min(x,1),0)
        idx = -1
        try:
            idx = min(int(x * len(self.func_list)), len(self.func_list)-1)
            return max(min(self.func_list[idx](x),1),0)
        except:
            print(f"idx={idx}  x={x}   r={self.r} func")
            return 0
        
    def slope(self, x):
        # clamp x to between zero and one
        x = max(min(x,1),0)
        idx = -1
        try:
            # multiply x by the length of the list conveted to an integer will give us what bin x should go to
            idx = min(int(x * len(self.slope_list)), len(self.slope_list)-1)
            return self.slope_list[idx]
        except:
            print(f"idx={idx}  x={x}   r={self.r} slope")
            return 0
    
    def get_x_values(self):
        return self.x_values
    
    def get_y_values(self):
        return self.y_values
    
    def get_func_list(self):
        return self.func_list
    
    def get_slope_list(self):
        return self.slope_list
    
    # private methods 
    
    def __create_func_list(self, x_values, y_values, r_value):
        func_list = []
        for i in range(len(x_values)):
            if i+1 < len(x_values):
                func_list.append(self.__func_factory(x_values[i],x_values[i+1],y_values[i],y_values[i+1]))  
        return func_list
    
    def __func_factory(self, x1,x2,y1,y2):
        return lambda x: ((y2-y1)/(x2-x1)) * (x - x1) + y1
    
    def __create_slope_list(self, x_values, y_values, r_value):
        slope_list = []
        for i in range(len(x_values)):
            if i+1 < len(x_values):
                slope_list.append((y_values[i+1]-y_values[i])/(x_values[i+1]-x_values[i]))
        return slope_list
    
def lyapunov_fractal(apprx_type = 'logistic', # determines which of the three kinds of approximations to use, linear, logistic, and invariant_linear
                     n_iter = 120, # number of iterations used to compute the lyapunov exponents
                     n_warmups = 1200, # number of warmup iterations
                     a_lb = 2, a_ub = 4, # lower and upper bounds of the A axis
                     b_lb = 2 , b_ub = 4, # lower and upper bounds of the B axis
                     steps = 500, # the number of values between each upper and lower bound
                     x_0 = 0.5, # starting value of x
                     n_points = 5, # number of (internal) points used to construct a linear apprx
                     savepng = False, # save a png of the fractal image
                     savefile = False # save a binary file with the lyapunov data from the fractal
                     solver_type = 'sparse' # 'automatic' if n_points > 135 uses a sparse solver else uses a tradtional solver, 'sparse', 'traditional'
                    ):
    
    @jit
    def logisitc_derivative(x, r, epsilon = 0):
        return np.add(np.abs(np.multiply(r, (np.subtract(1, (np.multiply(2, x)))))), epsilon)
    
    @jit
    def linear_derivative(x, function):
        return np.abs(function.slope(x))
    
#     @jit
    def iterative_lyapunov(n_warmups, n_iter, r_a, r_b, x_0):
        x = x_0
        lyapunov_ex = 0
        
        for i in range(n_warmups):
            if i % 2 == 0:
                x = np.multiply(x, r_a) * np.subtract(1,x) # multiplies every column a value of ra
            else :
                x = np.multiply(x, r_b) * np.subtract(1,x) # multiples every row by a value of rb
#                 x = np.multiply(x.T, rb).T * np.subtract(1,x)
    
        for i in range(n_iter):
            if i % 2 == 0:
                x = np.multiply(x, r_a) * np.subtract(1,x)
                lyapunov_ex = np.add(lyapunov_ex , np.log(logisitc_derivative(x, r_a)))
            else:
                x = np.multiply(x, r_b) * np.subtract(1,x)
#                 x = np.multiply(x.T, rb).T * np.subtract(1,x)
                lyapunov_ex = np.add(lyapunov_ex , np.log(logisitc_derivative(x, r_b)))
                
        lyapunov_ex = np.divide(lyapunov_ex, n_iter)

        return lyapunov_ex
    
    
    @jit
    def calc_equal_portion(n, total_x_interval):
        p = (1/n) * total_x_interval
        return p

    # returns the weight (the proportion) of x values of a function mapped by y values of another fuction   
    @jit
    def calc_weight(x_lb, x_ub, y_lb, y_ub):
        overlap_lb = max(x_lb,y_lb)
        overlap_ub = min(x_ub,y_ub)

        if overlap_lb > overlap_ub:
            return 0
        else:
            w = (overlap_ub - overlap_lb) /(y_ub - y_lb)
        return w  

    start = time.time()

    ra = np.linspace(a_lb, a_ub, steps)
    rb = np.linspace(b_lb, b_ub, steps)
    
    x_values = np.round(np.linspace(0, 1, n_points+2), 3) # values of x on the curve that will be used to create the approximation
    
    lyapunov_grid = []
    
    total_x_interval = np.amax(x_values) - np.amin(x_values)
    
    
    # create functions for linear approximation
    
#     @jit # Object Mode Warning
    def create_pwfunc_list(range_of_r):
    
        func_list = [0 for r in range(len(range_of_r))]

        for r_i, r in enumerate(range_of_r):
            # create the piecewise functions for that ra value
            func = PWApprx(x_values, r)
            func_list[r_i] = func

        return func_list    
        
    func_list_a  = create_pwfunc_list(ra)
    
    if not a_lb == b_lb and a_ub == b_ub:
        func_list_b = create_pwfunc_list(rb)     
    else:
        func_list_b = func_list_a

    n_equations = len(x_values)-1
    
    zeros = np.zeros((n_equations,n_equations))
    for z_i, z in enumerate(zeros):
        z[z_i] = -1
    
    p = [(calc_equal_portion(n_equations, total_x_interval)/2) for i in range(n_equations * 2)]
    ans = np.zeros(len(p))
    ans[-1] = 1
    bottoms = []
    right_csc_matrices = []
    
#     @jit # Object Mode Warning
    def lyapunov_from_matrix(matrix, slopes):
        solution = np.linalg.solve(matrix, ans)
        
        return np.sum(p * solution * np.log(np.abs(slopes)))
    
    def lyapunov_from_sparse_matrix(sparse_matrix, slopes):
        # sparse matrix is a matrix in csc or csr form
        
        solution = spsolve(sparse_matrix, ans)
    
        return np.sum(p * solution * np.log(np.abs(slopes)))
    
    # counts the number of times a singular matrix is encountered
    singularities = 0
    # counts the number of times a lyap exponent is far below the normal, possibly caused by an approach to negative infinity in the log
    negative_outliers = 0
    
    v_precent_interval = max(int(steps/20), 1)
    
    # Calc Lyapunov using CSC Matrices
    # Info about CSC form
    # https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_column_(CSC_or_CCS)
    # https://scipy-lectures.org/advanced/scipy_sparse/csc_matrix.html
    
#     def create_left_csc_matrix(y_values):
        
#         # For each column the left side of the matrix will be the same, the change in the 
#         left_data = []
#         left_indices = []
#         left_indptrs = []
#         left_indptr = 0 # index pointer
#         left_indptrs.append(left_indptr)
        
#         # Left Half of Matrix
#         for i in range(len(x_values)):
#             # Columns
#             if i != 0: 
#                 # Add the diagonal of negative 1s to the top half of the left side
#                 left_data.append(-1) # the data array holds the nonzero values
#                 left_indices.append(i - 1) # row index
#                 left_indptr = left_indptr + 1 # each time we add a new row index add on to the index pointer signifying another entry in that column

#                 # The way our data is structured after seeing the values the rest of the row except for the last column will be zero
#                 seen_non_zero = False
                
#                 for j in range(len(x_values)):
#                     # Rows
#                     if j != 0 and j != n_equations:  
#                         weight = calc_weight(x_values[j-1],x_values[j], min(y_values[i-1],y_values[i]),max(y_values[i-1],y_values[i]))
#                         # Add non zero weights to the row
#                         if weight != 0:
#                             left_data.append(weight)
#                             left_indices.append(j + n_equations - 1)
#                             left_indptr = left_indptr + 1
#                             seen_non_zero = True
#                         elif seen_non_zero:
#                             # if zero is seen after not seeing zero
#                             break
                
#                 # append the proportions to the last row
#                 left_data.append(p[i-1])
#                 left_indices.append((2 * n_equations) - 1)
#                 left_indptr = left_indptr + 1

#                 left_indptrs.append(left_indptr) # at the end of the column appened the index pointer to the list of pointers

#         return (left_data, left_indices, left_indptrs)
        
#     def create_right_csc_matrix(y_values_b):
#         # The create right matrix func is very similiar but the order of some things are switched around
#         # The negatives 1s on the diagonal must be added after the weights are
        
#         right_data = []
#         right_indices = []
#         right_indptrs = []
#         right_indptr = 0 # index pointer
#         right_indptrs.append(right_indptr)
        
#         # Right Half of Matrix
#         for i in range(len(x_values)):
#             # Columns
#             if i != 0: 
#                 # The way our data is structured after seeing the values the rest of the row except for the last column will be zero
#                 seen_non_zero = False
                
#                 for j in range(len(x_values)):
#                     # Rows
#                     if j != 0:  
#                         weight = calc_weight(x_values[j-1],x_values[j], min(y_values_b[i-1],y_values_b[i]),max(y_values_b[i-1],y_values_b[i]))
#                         if weight != 0:
#                             right_data.append(weight)
#                             right_indices.append(j - 1)
#                             right_indptr = right_indptr + 1
#                             seen_non_zero = True
#                         elif seen_non_zero:
#                             # if zero is seen after not seeing zero
#                             break

#                 if i < n_equations:
#                     right_data.append(-1)
#                     right_indices.append(i + n_equations - 1)
#                     right_indptr = right_indptr + 1

#                 right_data.append(p[i+n_equations - 1])
#                 right_indices.append((n_equations*2)-1)
#                 right_indptr = right_indptr + 1

#                 right_indptrs.append(right_indptr)
                
#         return (right_data, right_indices, right_indptrs)


#     def fuse_LR_matrices(left_csc_matrix, right_csc_matrix):
#         # concatenate data and indices lists
#         data = left_csc_matrix[0] + right_csc_matrix[0]
# #         print(len(data), (len(left_csc_matrix[0]) + len(right_csc_matrix[0])))
#         indices = left_csc_matrix[1] + right_csc_matrix[1]
#         # get the last indptr of the left array and add it to the elemnts of the right array because they come after
#         adjusted_right_indptrs = np.add(right_csc_matrix[2], left_csc_matrix[2][-1])
#         # remove the first element so it is not duplicated
# #         print(adjusted_right_indptrs)
#         adjusted_right_indptrs = np.delete(adjusted_right_indptrs, 0)
#         indptrs = np.concatenate((left_csc_matrix[2], adjusted_right_indptrs))
        
#         return (data, indices, indptrs)
    
    
#     for a_i, a in enumerate(ra):
        
#         if a_i % v_precent_interval == 0:
#             print("a = {}, {:2.2%} done {} seconds elapsed".format(a, (a_i/steps), (time.time() - start)))
        
#         lyapunov_row = []
#         y_values_a = func_list_a[a_i].get_y_values()
#         slopes_a = func_list_a[a_i].get_slope_list()
        
#         left_csc_matrix = create_left_csc_matrix(y_values_a)
        
#         for b_i, b in enumerate(rb):
            
#             y_values_b = func_list_b[b_i].get_y_values()
#             slopes_b = func_list_a[b_i].get_slope_list()
            
#             if a_i == 0:           
#                 right_csc_matrices.append(create_right_csc_matrix(y_values_b))
                
#             full_matrix_tuple = fuse_LR_matrices(left_csc_matrix, right_csc_matrices[b_i])
            
#             full_matrix = csc_matrix(full_matrix_tuple, shape=(2 * n_equations, 2 * n_equations))
            
#             slopes = slopes_a + slopes_b
            
# #             lyapunov_ex = lyapunov_from_sparse_matrix(sparse_matrix, slopes)
            
#             try:
#                 lyapunov_ex = lyapunov_from_sparse_matrix(full_matrix, slopes)
                
#                 if lyapunov_ex < -4:
# #                     print(a, b)
# #                     print(matrix)
#                     negative_outliers = negative_outliers + 1
#                     lyapunov_ex = -4
        

#             except:
# #                 print(a, b)
# #                 print(matrix)
#                 singularities = singularities + 1
                
# #                 lyapunov_ex = iterative_lyapunov(n_warmups, n_iter, a, b, x_0) # use iterative method to compute places where invariant measure fails
# #                 print(lyapunov_ex)
#                 lyapunov_ex = 0
    
#             lyapunov_row.append(lyapunov_ex)
    
#         lyapunov_grid.append(lyapunov_row)
           
    
    # Calc Lyapunoc using Regular Matrices
    
    for b_i, b in enumerate(rb):
        
        y_values_b = func_list_b[b_i].get_y_values()
        top_right_square = []
        
        for i in range(len(x_values)):
            if i != 0:      
                w_i = []
                for j in range(len(x_values)):
                    if j != 0:  
                        # Top Right Square
                        weight = calc_weight(x_values[i-1],x_values[i], min(y_values_b[j-1],y_values_b[j]),max(y_values_b[j-1],y_values_b[j]))
                        w_i.append(weight)
                            
           
                top_right_square.append(w_i)
        
        if b_i % (max(int(steps/20), 1)) == 0:
            print("b = {:1.3}, {:2.2%} done".format(b, (b_i/steps)))
        lyapunov_row = []
        
        # needed to compute lyapunov exponent
        slopes_b = func_list_b[b_i].get_slope_list()
        
        top = np.concatenate((zeros, top_right_square), axis = 1)
        
        for a_i, a in enumerate(ra):
            
            if b_i == 0:
                y_values_a = func_list_b[a_i].get_y_values()
                matrix = []

                for i in range(len(x_values)):
                    if i != 0:      
                        w_i = []
                        for j in range(len(x_values)):
                            if j != 0:  
                                # Bottom Left Square
                                weight = calc_weight(x_values[i-1],x_values[i], min(y_values_a[j-1],y_values_a[j]),max(y_values_a[j-1],y_values_a[j]))
                                w_i.append(weight) 
                        matrix.append(w_i)
                
                bottom = np.concatenate((matrix, zeros), axis = 1)
                bottoms.append(bottom)
            
            matrix = np.concatenate((top, bottoms[a_i]))
            matrix[-1] = p
            
            print(matrix)
            
            slopes_a = func_list_a[a_i].get_slope_list()
            slopes = slopes_a + slopes_b
            
            try:
                lyapunov_ex = lyapunov_from_matrix(matrix, slopes)
                
                if lyapunov_ex < -4:
#                     print(a, b)
#                     print(matrix)
                    negative_outliers = negative_outliers + 1
                    lyapunov_ex = -4
            except:
#                 print(a, b)
#                 print(matrix)
                singularities = singularities + 1
                
#                 lyapunov_ex = iterative_lyapunov(n_warmups, n_iter, a, b, x_0) # use iterative method to compute places where invariant measure fails
#                 print(lyapunov_ex)
                lyapunov_ex = 0
                
        
#             lyapunov_ex = lyapunov_from_matrix(matrix, slopes)
            
            lyapunov_row.append(lyapunov_ex)
            
        lyapunov_grid.append(lyapunov_row)
    
    
    print("Singularities: " + str(singularities))
    print("Negative Outliers: " + str(negative_outliers))
    
    if savefile:
        f = open("invariat_fractal_apprx n_points= " + str(n_points) + " steps=" + str(steps) + ".dat", "wb")
        lyapunov_grid = np.ascontiguousarray(lyapunov_grid)
        f.write(lyapunov_grid)
        f.close()
    
    # plot information
    
    fig, ax = plt.subplots(figsize=(10, 9))
    
    fig.patch.set_facecolor('white')
    
#     lya_cmap = copy.copy(mpl.cm.get_cmap('viridis'))
    lya_cmap = copy.copy(mpl.cm.get_cmap('jet'))
    lya_cmap.set_over('black')
#     lya_cmap.set_under('white')
#     lya_cmap.set_bad('black')
    
    plt.imshow(lyapunov_grid , cmap = lya_cmap, origin = 'lower', vmax = 0, vmin = -4)
    
    plt.colorbar()
    plt.suptitle("Lyapunov Logistic Fractal - Linear Apprx")
    plt.title("steps = " + str(steps) + " n_points = " + str(n_points))  
    
    xticks = np.arange(a_lb, a_ub, .2)
    yticks = np.arange(b_lb, b_ub, .2)
    
    plt.xlabel("A")  
    plt.ylabel("B") 
    
    plt.xticks([])
    plt.yticks([])
    
    if(savepng):
        plt.savefig("invariat_fractal_apprx csc n_points = "+ str(n_points) +".png")
    
    plt.show()
    
    end = time.time()

    print("This took", end - start, "seconds to execute")
