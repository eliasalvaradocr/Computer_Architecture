# IE0521 Estructuras de Computadoras Digitales II
# Tarea 1 - Branch Predictor
## Elias Alvarado Vargas

Development of a Branch Predictor Simulator in Python, that allows obtain performance metrics using as input a trace indicating the memory address where the branch ocurrs as well the result of it, take (T) or not taken(NT).

## Table of Contents

- [Execution Instructions](#execute)


## Execution Instructions
On Windows Environment:

To run the Branch Predictors in the main file _branch_predictor.py_, use the following parameterized commands:

- Bimodal:
 
  ``` python .\branch_predictor.py --bp 0 -n X -g Y ```

  Where  ```X ``` is the number of bits for indexing,  ```Y ``` are the counters and ```0 ``` means the type, in this case Bimodal.

- G-Share:
 
  ``` python .\branch_predictor.py --bp 1 -n X -g Y ```

  Where  ```X ``` is the number of bits for indexing,  ```Y ``` is the global history and  ```1 ``` means the type, in this case G-Share.


- P-Share:
 
  ``` python .\branch_predictor.py --bp 2 -n X -g Y ```

  Where  ```X ``` is the number of bits for indexing,  ```Y ``` is the local history and  ```2 ``` means the type, in this case P-Share.
  
- Perceptron:

   ``` python .\branch_predictor.py --bp 3 -n X -g Y ```

  Where ```X ``` is the number of bits for indexing, ```Y ``` is the global history and  ```3 ``` the type, in this case Perceptron.
 
- Proposed Predictor _ie0521_bp.py_

   ``` python .\branch_predictor.py --bp 4 -n 14 -g 6 ```
 
 


