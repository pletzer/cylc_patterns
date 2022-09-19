# Scatter pattern

In this directory, type
```
cylc install .
cylc play -n scatter
```

To view the output of each task
```
cylc cat-log scatter//1/a
cylc cat-log scatter//1/b
cylc cat-log scatter//1/c
```