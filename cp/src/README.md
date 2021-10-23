# VLSI solved with CP

## To run a single instance

```
usage: run.py [-h] [-r] [-c] [-t TIMEOUT] [-v] instance

positional arguments:
  instance              number of the instance to run

optional arguments:
  -h, --help            show this help message and exit
  -r, --allow_rotation  allow rotation of chips
  -c, --use_chuffed     use chuffed solver
  -t TIMEOUT, --timeout TIMEOUT
                        timeout to solve the instance
  -v, --visualize       visualize the result
```

## To visualize the result of an instance

```
usage: visualize.py [-h] instance

positional arguments:
  instance    number of the instance to visualize

optional arguments:
  -h, --help  show this help message and exit
```