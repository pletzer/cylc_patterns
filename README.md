# cylc_patterns

A collection of commonly used [Cylc](https://www.cylc.org) workflow patterns 

## Overview

This project contains a number of commonly used workflow patterns, which range from sequential to concurrent and more elaborate patterns. These patterns 
are the building blocks with which complex workflows can be assembled.

## Preliminaries

Assuming you're running on Linux or Mac OSX, you will need to have [Cylc 8](https://cylc.github.io/cylc-doc/stable/html/) installed,
```
conda create -n cylc python=3.9
conda activate cylc
conda install -c conda-forge cylc-flow
conda install -c conda-forge cylc-uiserver
```

Mac users beware, you may need to apply the fix [here](#mac-users).

## Example of a workflow pattern

Go into any of the subdirectories, e.g.
```
cd cylc-src/resilient_cycling
cylc validate .
cylc graph .
```
This shows the first three cycles of the resilient cycling pattern. The workflow graph is encoded in the `flow.cylc` file.
```
    [[graph]]
        P1 = """
            fix[-P1] => model?
            model:succeed? => finish
            model:fail? => diagnose => fix
        """
```
In this case we have a model ("model"), which may fail or succeed. Up to 3 attempts of running "model" will be submitted. If the model succeeds after one such attempt then task "finish" is invoked. If not, then the "diagnose" and "fix" tasks are called. The latter will attempt to fix the input and run "model" gain, thereby starting a new cycle.

![alt resilient cycling pattern](https://github.com/pletzer/cylc_patterns/blob/main/figures/resilient_cycling.png?raw=true)

Install the workflow with
```
cylc install resilient_cycling
```

Run the workflow with
```
cylc tui resilient_cycling
```
Type return on the workflow_name/run1 and then select "play". The figure below shows the `model` task (blue square) of the 48th cycle being run with the 49th cycle `check` waiting for the `model` task to complete. The green square indicates that 48th `check` task was successful.

![alt terminal user interface (tui) showing a cycle of the resilient cycling pattern](https://github.com/pletzer/cylc_patterns/blob/main/figures/resilient_cycling_tui.png?raw=true)


# Troubleshooting

## Mac users

If you get error
```
...
nodename nor servname provided, or not known: '1.0.0.127.in-addr.arpa'
```
or similar, then you'll have to update the `hostuserutil.py` file. Around line 113, replace
```
                target = socket.getfqdn()
```
with 
```
                target = socket.gethostname()
```




