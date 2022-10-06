# Fortran restart pattern

This example shows how to call a Fortran, time stepping code multiple times until the last output file is written.

First compile the code
```
cd bin
cmake ..
make
cd ..
```

Then type
```
cylc install .
cylc play -n fortran_restart
```

To view the output of each task
```
cylc cat-log fortran_restart//1/model
cylc cat-log fortran_restart//1/model_restart
```

Feel free to change the number of steps (nsteps) in the namelist file "model.nml".