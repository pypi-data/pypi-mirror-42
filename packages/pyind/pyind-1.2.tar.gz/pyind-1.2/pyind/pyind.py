import numpy as np

from . import defaults as df
from .selection import Selection as Sel
from .crossover import Crossover as Xovr
from .mutation import Mutation as Mut


class Pyind:
    @staticmethod
    def _chk_err(pop, conf):
        if type(pop) is not np.ndarray:
            raise TypeError("Pyind only supports ndarray (numpy)")
        if len(pop) <= conf['sel']['num']:
            raise TypeError("Should set poplation size > conf['sel']['num']")

    def __init__(self, pop, conf):
        Pyind._chk_err(pop, conf)
        self._pop = pop
        self._eval_func = conf["eval"]["func"]
        self._sel = Sel(len(pop), conf["sel"])
        self._xovr = Xovr(conf["xovr"])
        self._mut = Mut(conf["mut"])

    def _get_best(self):
        ftns = np.array([self._eval_func(e) for e in self._pop])
        return self._pop[np.argsort(ftns)[-1]]

    def run(self, end_gen=df.END_GEN):
        print("\rgen: {0:d}".format(0), end="")
        # print("gen: 0")
        for i in range(end_gen):
            print("\rgen: {0:d}".format(i + 1), end="")
            # print("gen: " + str(i + 1))
            ftns = np.array([self._eval_func(e) for e in self._pop])
            parents = self._sel.sel(self._pop, ftns)
            self._pop = self._xovr.xovr(parents, len(ftns))
            self._pop = self._mut.mut(self._pop)
        print()
        return self._get_best()
