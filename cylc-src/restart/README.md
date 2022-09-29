# Restart pattern

In this directory, type
```
cylc install .
cylc play -n restart
```

To view the output of each task
```
cylc cat-log restart//1/diagnose
cylc cat-log restart//1/model
```
