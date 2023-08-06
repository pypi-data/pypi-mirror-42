import numpy as np
import matplotlib.pyplot as plt

from . import util
# import util


def flip_bit(pop, pb):
    """
    Flip the individual's bits

    Flip bits of randomly selected genes

    Parameters
    ----------
    pop : ndarray
        Population
    pb : float
        Probability of mutation

    Returns
    -------
    new_pop : ndarray
        mutated population
    """

    mask = _cre_mask(pop, pb)
    return np.logical_xor(pop, mask)


def boundary(pop, pb, delta):
    """
    Add random value from -delta to delta to randomly selected genes

    Parameters
    ----------
    pop : ndarray
        Population
    pb : float
        Probability of mutation

    Returns
    -------
    new_pop : ndarray
        mutated population
    """

    mask = _cre_mask(pop, pb)
    r = np.random.ranf(pop.shape) * 2 - 1
    return pop + r * delta * mask


def swap_idx(pop, pb):
    """
    Swap 2 genes selected randomly and repeat it multiple times

    Parameters
    ----------
    pop : ndarray
        Population
    pb : float
        Probability of mutation

    Returns
    -------
    new_pop : ndarray
        mutated population
    """

    mut_cnt = np.random.binomial(len(pop) * pop.shape[1], pb)
    y = np.random.randint(len(pop), size=mut_cnt)
    x1 = np.random.randint(pop.shape[1], size=mut_cnt)
    x2 = x1 - np.random.randint(1, pop.shape[1], size=mut_cnt)
    for ey, ex1, ex2 in zip(y, x1, x2):
        pop[ey, ex1], pop[ey, ex2] = pop[ey, ex2], pop[ey, ex1]
    return pop


def _cre_mask(pop, pb):
    return np.random.ranf(pop.shape) < pb


class Mutation:
    def __init__(self, conf):
        self._func = conf["func"]
        self._args = util.cre_args(self._func, conf, exclusion=("pop",))

    def mut(self, pop):
        return self._func(pop, *self._args)


if __name__ == "__main__":
    pop = np.arange(1, 13).reshape((2, -1))
    conf = {
        "func": boundary,
        "pb": 0.1,
        "delta": 1
    }
    m = Mutation(conf)
    print(m.mut(pop))
