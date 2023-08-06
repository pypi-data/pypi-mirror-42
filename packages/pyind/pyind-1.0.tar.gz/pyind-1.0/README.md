# pyind
A genetic algorithm library in Python3

**pyind ONLY supports ndarray (numpy)**

[日本語](https://github.com/chankane/pyind/blob/dev/README.ja.md)

## Installation
Coming soon...
~~``pip install pyind``~~

## About evaluation function
An evaluation function has the following format
```python
def evaluation_function(individual):  # individual is an array of gene
    return fitness_of_this_individual

```

## About `conf`
`conf` has the following format
```python
conf_format = {
    "eval": {
        "func": evaluation_function  # Required fields and it has not default value.
    },
    "sel": {
        # See "Table Sel" below
    },
    "xovr": {
        # See "Table Xovr" below
    },
    "mut": {
        # See "Table Mut" below
    },
}
```
Value that can be set to `conf["sel"]` are as shown in the table

In parentheses is default value

Table Sel

"sel" (elitism) | "num" (10)
-- | :--:
elitism | 0&ndash;size of poplation
roulette | 0&ndash;size of poplation

Value that can be set to `conf["xovr"]` are as shown in the table

In parentheses is default value

Table Xovr

"xovr" (p2) | "pb" (0.875)
-- | :--:
p2 | 0&ndash;1
uniform | 0&ndash;1
ox | 0&ndash;1

Value that can be set to `conf["mut"]` are as shown in the table

In parentheses is default value

Table Mut

"mut" (flip_bit) | "pb" (0.0075)| "delta" (1)
-- | :--: | :--:
flip_bit | 0&ndash;1
boundary | 0&ndash;1 | 0&ndash;&infin;
swap_idx | 0&ndash;1

## Future Releases
1. Fix bug
1. Add functions of selection, crossover and mutation
1. Run more faster
## License
MIT

## Sample code
### Onemax problem
```python
# Onemax Problem
import numpy as np

from pyind import pyind as pi
from pyind import defaults as df


IND_LEN = 100
POP_LEN = 100


def evl(ind):
    return ind.sum()


if __name__ == "__main__":
    pop = np.random.randint(2, size=(POP_LEN, IND_LEN))

    conf = df.CONF
    conf["eval"]["func"] = evl

    best = pi.Pyind(pop, conf).run()

    print("best ind: ")
    print(best)

```
### Traveling salesman problem (TSP)
```python
# Traveling salesman problem

import numpy as np
import matplotlib.pyplot as plt

from pyind import pyind as pi
from pyind import crossover as xovr
from pyind import mutation as mut
from pyind import defaults as df


CITIES_LEN = 30
POP_LEN = 300
END_GEN = 500

cities = np.random.rand(CITIES_LEN * 2).reshape((-1, 2))


def evl(ind):
    total = 0
    for i in range(1, len(ind)):
        total += np.linalg.norm(cities[ind[i]] - cities[ind[i - 1]])
    return -total


def solve(pop):
    conf = df.CONF
    conf["eval"]["func"] = evl
    conf["xovr"]["func"] = xovr.ox
    conf["mut"]["func"] = mut.swap_idx
    conf["mut"]["pb"] = 0.10
    return pi.Pyind(pop, conf).run(END_GEN)


if __name__ == "__main__":
    t = cities.T

    # Create pop
    pop = np.tile(np.arange(CITIES_LEN), (POP_LEN, 1))
    for e in pop:
        np.random.shuffle(e)

    # Plot gen 0
    idx = pop[0]
    plt.plot(t[0, idx], t[1, idx], label="gen 0", marker="o")

    best = solve(pop)
    print("best ind: ")
    print(best)

    # Plot gen END_GEN
    idx = best
    plt.plot(t[0, idx], t[1, idx], label="gen " + str(END_GEN), marker="o")

    plt.legend()
    plt.show()

```
