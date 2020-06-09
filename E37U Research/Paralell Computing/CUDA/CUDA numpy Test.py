import numpy as np
import cupy
import time


mempool = cupy.get_default_memory_pool()

with cupy.cuda.Device(0):
    #mempool.set_limit(size=8589934592)  # 1 GiB
    mempool.set_limit(fraction=1)  # 1 GiB

### Numpy and CPU
s = time.time()
x_cpu = np.ones((500,500,1000))
e = time.time()
print(e - s)
### CuPy and GPU
s = time.time()
x_gpu = cupy.ones((400,1000,1000))

cupy.cuda.Stream.null.synchronize()
e = time.time()
print(e - s)
print(cupy.get_default_memory_pool().get_limit())