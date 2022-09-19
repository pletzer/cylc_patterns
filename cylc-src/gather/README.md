# Gather pattern

In this directory, type
```
cylc install .
cylc play -n gather
```

To view the output of each task
```
cylc cat-log gather//1/a
cylc cat-log gather//1/b
cylc cat-log gather//1/c
```