# VLSI solved with CP

## To run a single instance

usage: run.py [-h] -i INSTANCE [-t TIMEOUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INSTANCE, --instance INSTANCE
                        number of the instance to run
  -t TIMEOUT, --timeout TIMEOUT
                        maximum time allowed to run the istance
  -v, --visualize       visualize the result

## To visualize the result of an istance

usage: visualize.py [-h] -i INSTANCE

optional arguments:
  -h, --help            show this help message and exit
  -i INSTANCE, --instance INSTANCE
                        number of the instance to visualize

## To run or visualize all the instances

usage: all_instances.py [-h] [-r] [-t TIMEOUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -r, --run_all         run all the instances
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for each instance
  -v, --visualize_all   visualize all the instances
