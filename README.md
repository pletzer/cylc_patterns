# cylc_patterns

A collection of commonly used Cylc workflow patterns 

## Overview

This project contains a number of commonly used workflow patterns, which range from sequential to concurrent and more elaborate patterns. These patterns 
are the building blocks with which complex workflows can be assembled.

## Preliminaries

Assuming yopu're running on Linux or Mac OSX, you will need to have [Cylc 8](https://cylc.github.io/cylc-doc/stable/html/) installed,
```
conda create -n cylc python=3.9
conda activate cylc
conda install -c conda-forge cylc-flow
conda install -c conda-forge cylc-uiserver
```

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



## Example of a workflow pattern

Go into any of the subdirectories, e.g.
```
cd resilient_cycling
cylc validate .
cylc graph .
```
This shows the first three cylcles of the resilient cylcing pattern. The worflow graph is encoded in the `flow.cylc` file.
```
    [[graph]]
        R1 = """
            prep => check?
        """
        P1 = """
            model[-P1] => check:succeed? => model
            check:fail? => diagnose
        """
```
The first task, `prep` creates a file, `output_file.txt`. If file `output_file.txt` is present then task `check` succeeds and task `model` is then run. Occasionally, task `model` will fail -- we allow for up to 20 attempts. When task `check` succeeds, the next cycle starts. If task `check` fails then task `diagnose` will be run. This workflow supports an inifite number of cycles.

![alt resilient cycling oattern](https://github.com/pletzer/cylc_patterns/blob/main/figures/resilient_cycling.png.png?raw=true)

Install the worflow with
```
cylc install resilient_cycling
```

Run the workflow with
```
cylc tui resilient_cycling
```
Type return on the workflow_name/run1 and then select "play".





