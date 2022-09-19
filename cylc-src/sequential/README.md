# Sequential pattern

In this directory, type
```
cylc install .
cylc play -n sequential
```

To view the output of each task
```
cylc cat-log sequential//1/a
cylc cat-log sequential//1/b
```