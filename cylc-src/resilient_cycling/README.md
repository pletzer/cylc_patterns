# Sequential pattern

In this directory, type
```
cylc install .
cylc play -n resilient_cycling
```

To view the output of each task
```
cylc cat-log resilient_cycling//1/diagnose
cylc cat-log resilient_cycling//1/model
```
