# Retry pattern

In this directory, type
```
cylc install .
cylc play -n retry
```

To view the output of each task
```
cylc cat-log retry//1/a
cylc cat-log retry//1/b
```