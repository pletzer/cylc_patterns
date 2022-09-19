# Parametrized scatter pattern

In this directory, type
```
cylc install .
cylc play -n param_gather
```

To view the output of each task
```
cylc cat-log param_gather//1/a_m0
cylc cat-log param_gather//1/a_m9
cylc cat-log param_gather//1/b
```
