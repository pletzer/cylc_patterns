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


cylc install resilient_cycling
cylc tui resilient_cycling
```
Type return on the workflow_name/run1 and then select "play".





