import numpy as np


class PWApprx:

    def __init__(self, x_values, r):
        self.x_values = x_values
        self.r = r
        self.y_values = np.multiply(x_values, r) * np.subtract(1, x_values)
        self.func_list = self.__create_func_list(x_values, self.y_values, r)
        self.slope_list = self.__create_slope_list(x_values, self.y_values, r)

    def compute(self, x):
        # clamp x to between zero and one
        x = max(min(x, 1), 0)
        idx = -1
        try:
            idx = min(int(x * len(self.func_list)), len(self.func_list)-1)
            return max(min(self.func_list[idx](x), 1), 0)
        except:
            print(f"idx={idx}  x={x}   r={self.r} func")
            return 0

    def slope(self, x):
        # clamp x to between zero and one
        x = max(min(x, 1), 0)
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
                func_list.append(self.__func_factory(
                    x_values[i], x_values[i+1], y_values[i], y_values[i+1]))
        return func_list

    def __func_factory(self, x1, x2, y1, y2):
        return lambda x: ((y2-y1)/(x2-x1)) * (x - x1) + y1

    def __create_slope_list(self, x_values, y_values, r_value):
        slope_list = []
        for i in range(len(x_values)):
            if i+1 < len(x_values):
                slope_list.append(
                    (y_values[i+1]-y_values[i])/(x_values[i+1]-x_values[i]))
        return slope_list
