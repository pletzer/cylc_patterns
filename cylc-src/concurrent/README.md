# Concurrent pattern

In this directory, type
```
cylc install .
cylc play -n concurrent
```

To view the output of each task
```
cylc cat-log concurrent//1/a
cylc cat-log concurrent//1/b
```