# Python-package-to-model-tidal-stream

For this project, I was interested in Building a python package using object oriented programming
in order to solve primitive equation of the ocean in the vertical one-dimensional approximation.

## Prerequisites

This package requires **Python 3.x** and the following Python libraries installed:

-   [NumPy](http://www.numpy.org/)
-   [NetCDF4](http://unidata.github.io/netcdf4-python/)

## Installing

The source code is currently hosted on GitHub at: [github](https://github.com/Jaouadeddadsi/Paython-package-to-model-tidal-stream)

You can install the package using pip :

`pip install ocean_model`

## How to use it
Import the model:

`from ocean_model import Model `

Create the model :

`model =  Model(n, t)`
- n (int) : size of the horizontal grid
- t (float) : Time to end the simulation in day

Get the simulation results:

`model.solve_equations(i, j)`

(i,j) : the point coordinate in the horizontal grid.

The `solve_equations` method return a ** netcdf ** file that contains the simulation results.

## License

This project is licensed under the MIT License - see the [license.txt](license.txt) file for details
