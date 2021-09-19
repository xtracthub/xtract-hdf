# Python program to demonstrate
# HDF5 file
 
import numpy as np
import h5py
 
# initializing a random numpy array
arr = np.random.randn(1000)
 
# creating a file
with h5py.File('test.hdf5', 'w') as f:
    dset = f.create_dataset("default", data = arr)