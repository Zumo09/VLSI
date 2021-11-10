# VLSI solved with SMT

## To run a single instance

```
usage: run.py [-h] [-r] [-t TIMEOUT] [-v] instance     

positional arguments:
  instance              number of the instance to run  

optional arguments:
  -h, --help            show this help message and exit
  -r, --allow_rotation  allow rotation of chips        
  -t TIMEOUT, --timeout TIMEOUT
                        timeout to solve the instance  
  -v, --visualize       visualize the result
```

## To visualize the result of an instance

```
usage: visualize.py [-h] [-r] instance

positional arguments:
  instance        number of the instance to visualize

optional arguments:
  -h, --help      show this help message and exit
  -r, --rotation  solutions with rotation
```