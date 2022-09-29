# Resilient cycling pattern

This example combines running multiple attempts of a model with cycling until the model succeeds.

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
