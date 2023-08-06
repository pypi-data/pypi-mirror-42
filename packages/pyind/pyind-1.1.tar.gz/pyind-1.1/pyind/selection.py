import numpy as np

from . import util
# import util


def elitism(ftns, num):
    """
    Elitism selection

    Select best "num" individuals

    Parameters
    ----------
    ftns : ndarray
        Fitness of individuals
    num : int
        Number of the selection

    Returns
    -------
    idxs : int
        Indices of selected individuals
    """

    return np.argsort(ftns)[-num::]


def roulette(ftns, num):
    """
    Roulette wheel selection (RWS)

    Parameters
    ----------
    ftns : ndarray
        Fitness of individuals
    num : int
        Number of the selection

    Returns
    -------
    idxs : int
        Indices of selected individuals
    """

    w = ftns / ftns.sum()
    return np.random.choice(len(ftns), num, p=w)


def random(num):
    """
    Random selection

    Parameters
    ----------
    num : int
        Number of the selection

    Returns
    -------
    idxs : int
        Indices of selected individuals
    """

    return np.random.choice(len(ftns), num)


class Selection:
    def __init__(self, pop_len, conf):
        # conf["num"] = int(pop_len * conf["rate"])
        self._func = conf["func"]
        self._args = util.cre_args(self._func, conf, exclusion=("ftns",))

    def sel(self, pop, ftns):
        return pop[self._func(ftns, *self._args)]


def evl(ind):
    return ind.sum()


if __name__ == "__main__":
    conf = {
        "func": roulette,
        "num": 3
        # "rate": 0.1
    }
    pop = np.array([
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [1, 1, 1, 1],
        [0, 0, 1, 1],
    ])

    s = Selection(len(pop), conf)
    t = s.sel(pop, pop.sum(axis=1))
    print(t)
    """
    ar = np.array([0, 0, 0, 0, 0])
    for i in range(10000):
        t = _roulette_simple(pop, 0.3, evl).sum()
        # print(t)
        ar[t] += 1
    print(ar/1000)
    """
