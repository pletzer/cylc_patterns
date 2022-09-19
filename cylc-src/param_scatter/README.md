# Parametrized scatter pattern

In this directory, type
```
cylc install .
cylc play -n param_scatter
```

To view the output of each task
```
cylc cat-log param_scatter//1/a_m0
cylc cat-log param_scatter//1/a_m9
cylc cat-log param_scatter//1/b
```