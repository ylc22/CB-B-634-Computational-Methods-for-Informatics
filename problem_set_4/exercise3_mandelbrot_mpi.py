#!/usr/bin/env python
# coding: utf-8

# In[3]:


from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt

# Define the original Mandelbrot function and related settings
xlo = -2.5
ylo = -1.5
yhi = 1.5
xhi = 0.75
nx = 2048
ny = 1536
dx = (xhi - xlo) / nx
dy = (yhi - ylo) / ny
iter_limit = 200
set_threshold = 2


def mandelbrot_test(x, y):
    """Test if a point is in the Mandelbrot set."""
    z = 0
    c = x + y * 1j
    for i in range(iter_limit):
        z = z ** 2 + c
        if abs(z) > set_threshold:
            return i
    return i


def calculate_mandelbrot(start_row, end_row):
    """Calculate a slice of the Mandelbrot set."""
    result = np.zeros([end_row - start_row, nx])
    for i in range(start_row, end_row):
        y = i * dy + ylo
        for j in range(nx):
            x = j * dx + xlo
            result[i - start_row, j] = mandelbrot_test(x, y)
    return result


# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Divide the work among the ranks
rows_per_process = ny // size
start_row = rank * rows_per_process
end_row = ny if rank == size - 1 else (rank + 1) * rows_per_process

# Calculate the subset of the Mandelbrot set for this rank
local_result = calculate_mandelbrot(start_row, end_row)

# Gather all subsets of the Mandelbrot set at the root rank
if rank == 0:
    final_result = np.zeros([ny, nx])
else:
    final_result = None

comm.Gather(local_result, final_result, root=0)

# Save or display the final result at the root rank
if rank == 0:
    plt.imshow(final_result, extent=(xlo, xhi, ylo, yhi))
    plt.title("Mandelbrot Set (Parallelized)")
    plt.colorbar()
    plt.savefig("mandelbrot_parallelized.png")
    plt.show()


# In[ ]:




