
import numpy as np

def find_overlap(i1, i2): #find the interval overlap of i2 onto i1
    #print("find_overlap:" , i1, i2) 
    overlap = [None,None]
    if i2[1] <= i1[0] or i2[0] >= i1[1]: # no overlap
        return [0,0] #should be read as no overlap
    if i2[0] <= i1[0] and i2[1] >= i1[0]:
        overlap[0] = i1[0]
    else:
        overlap[0] = i2[0]
    if i2[1] >= i1[1] and i2[0] <= i1[1]:
        overlap[1] = i1[1]
    else:
        overlap[1] = i2[1] 
    return overlap

#points = [(0,0.5), (0.5,1), (1,0)]
#points = [ (0,0.75), (.6,1.2), (.9,.4), (1.6,.2)]  # this is in the bins
points = [ (0,0), (.5,1), (1,0), (2,3), (5, 0) ]  # points from default tent plot gui
matrix = []

line_segment_x_intervals = []
line_segment_y_intervals = []
line_segment_x_proportions = []
line_segment_slopes = []
eqn_n = ""
matrix_n = []
n = len(points) #number of points
total_x_interval = points[n-1][0] - points[0][0]  # total x _interval

last_point = (0,0)
for i,p in enumerate(points):
    if i == 0:
        last_point = p
        continue #skip the first point, line segments start at the second
    line_segment_x_intervals.append([last_point[0], p[0]])
    if p[1] > last_point[1]:
        line_segment_y_intervals.append([last_point[1], p[1]])
    else:
        line_segment_y_intervals.append([p[1], last_point[1]])
    line_segment_x_proportions.append( (p[0] - last_point[0]) / total_x_interval)
    line_segment_slopes.append( (p[1] - last_point[1]) / (p[0] - last_point[0]) )
    eqn_n = eqn_n + str(line_segment_x_proportions[i-1]) + "*w_" + str(i) + " + "
    matrix_n.append(line_segment_x_proportions[i-1])
    last_point = p
matrix.append(matrix_n)



eqn_n = eqn_n[:-2] + " = 1.0"
print("     slopes:", line_segment_slopes)
print("x intervals:", line_segment_x_intervals)
print("x proportion:", line_segment_x_proportions)
print("y intervals:", line_segment_y_intervals)


print("--------------------------------")


this_eqn = ""
this_arr = []
for i, line_x in enumerate(line_segment_x_intervals):
    if i != 0:
        matrix.append(this_arr)
        print(this_eqn)
    this_eqn = "w" + str(i+1) + " = "
    this_arr = []
    for j, line_y in enumerate(line_segment_y_intervals):
        overlap = find_overlap(line_x, line_y)
        weighted = (overlap[1] - overlap[0]) / (line_y[1] - line_y[0])
        this_eqn = this_eqn + str(weighted) + " * w" + str(j+1) + " + "
        if i == j:
            this_arr.append(weighted-1)
        else:
            this_arr.append(weighted)
    this_eqn = this_eqn[:-3]
#there is a third hidden equation
print(" --- unneeded/redundant: ", this_eqn[:-3])
print("eqn n: ", eqn_n)
print("---")
ans_array = [1]
for i in range(n-2): # we need one less than the linesegments which is one less than the num points
    ans_array.append(0)
ans = np.array(ans_array)
print("  matrix: ", matrix)
print("     ans: ", ans)
solution = np.linalg.solve(matrix,ans)
print("solution:",solution)

lyap = 0
for i, prop in enumerate(line_segment_x_proportions):
    lyap = lyap + prop * solution[i] * np.log(abs(line_segment_slopes[i]))

print(lyap)