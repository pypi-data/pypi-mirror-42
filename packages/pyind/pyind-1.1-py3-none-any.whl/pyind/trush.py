def roulette(pop, sel_rate, eval_func):
    ftns = _calc_ftns(pop, eval_func)
    sel_num = _calc_sel_num(pop, sel_rate)
    r = np.random.rand(sel_num) * ftns.sum()
    return pop[(ftns.cumsum()[:, np.newaxis] < r).sum(axis=0)]


def swap_idx(pop, mut_pb):
    #r = np.random.ranf(pop.shape)
    r = np.array([
        [3, 1, 6, 2, 4, 5],
        [4, 1, 2, 3, 5, 6],
    ]) * 0.1 - 0.01
    a = np.argsort(r, axis=1)
    #print(a)
    for j, row in enumerate(a):
        for i, col in enumerate(row):
            #print(r[j, col])
            if r[j, col] >= mut_pb:
                break
            #print("x")
            #print(col)
            #print("y")
            #print(a[j, -i-1])
            o = a[j, -i-1]
            pop[j, col], pop[j, o] = pop[j, o], pop[j, col]
    print(pop)

    @staticmethod
    def _get_args(conf):
        fnc = conf["func"]
        if fnc == elite or func == roulette:
            return int(pop_len * conf["rate"])

import numpy as np
import matplotlib.pyplot as plt


PB = 0.5
POP, IND = 100, 100
SIZE = POP * IND
mu = SIZE // 2
sigma = 50
LEN = 100000


def gaus(x):
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))


def min_max(x):
    _min = x.min(keepdims=True)
    _max = x.max(keepdims=True)
    return (x - _min)/(_max - _min)


def l():
    r = np.random.rand(POP, IND)
    return (r < PB).sum()


res = np.zeros(SIZE)
res2 = np.zeros(SIZE)

for i in range(LEN):
    res2[l()] += 1
    res[np.random.binomial(SIZE, PB)] += 1

sub = POP * IND * 0.5 * 0.95
plt.xlim(sub, SIZE - sub)

res = min_max(res)
res2 = min_max(res2)
#yy, _ = np.histogram(res, bins=SIZE)
#print(yy)
# plt.hist(res, bins=60)
#plt.plot(yy)

#x = np.arange(SIZE)
#y = gaus(x)
#y = min_max(y)
#plt.plot(y)
plt.plot(res)
plt.plot(res2)

"""
hensa = res - 5000
hensa2 = hensa**2
bunsan = hensa2.sum() / SIZE
sig = np.sqrt(bunsan)
print(sig)
"""

plt.show()

import numpy as np

from pyind import defaults as df
from pyind import pyind as pi


POP, IND = 100, 100
GOAL = np.ones(IND)


def evl(ind):
    return ind.sum()


pop = np.random.randint(2, size=(POP, IND))

CONF = {
    "eval": {
        "func": evl,
    },
    "sel": {
        "func": df.SEL_FUNC,
        # "rate": df.SEL_RATE
        "num": int(pop.shape[0] * df.SEL_RATE * 10)
    },
    "xovr": {
        "func": df.XOVR_FUNC,
        "pb": df.XOVR_PB
    },
    "mut": {
        "func": df.MUT_FUNC,
        "pb": df.MUT_PB
    },
    "goal_ind": GOAL
}

pi.Pyind(pop, CONF).start(1000)


#a = np.arange(10) + np.zeros(5)[:, np.newaxis]


import numpy as np
from benchmarker import Benchmarker


A = np.array([
    [4, 0, 0],
    [1, 2, 3],
    [0, 0, 5]
])

r = np.array([2, 0, -1])


def roll3():
    rows, column_indices = np.ogrid[:A.shape[0], :A.shape[1]]
    r[r < 0] += A.shape[1]
    column_indices = column_indices - r[:, np.newaxis]

    return A[rows, column_indices]


def roll4():
    r, c = np.ogrid[:A.shape[0], :A.shape[1]]
    r[r < 0] += A.shape[1]
    c = c - r[:, np.newaxis]
    return A[r, c]


def bm():
    with Benchmarker(10000, cycle=10, extra=1) as bench:
        @bench('roll3')
        def insertion(bm):
            for i in bm:
                roll3()

        @bench('roll4')
        def insertion(bm):
            for i in bm:
                roll4()

        @bench('roll3')
        def insertion(bm):
            for i in bm:
                roll3()

        @bench('roll4')
        def insertion(bm):
            for i in bm:
                roll4()

bm()

"""
[[0 0 4]
 [1 2 3]
 [0 5 0]]
"""

#rad = 2 * np.pi / CITY_CNT
#cities = np.array([
#    [np.cos(i * rad), np.sin(i * rad)] for i in range(CITY_CNT)
    # [np.cos(i * rad), np.sin(i * rad)] for i in [6, 3, 9, 1, 7, 2, 10, 4, 11, 0, 8, 5]
#])

    def xovr(self, par, pop_len):
        chil_len = np.random.binomial(pop_len, self._pb)
        if chil_len % 2 == 1:
            chil_len += 2 * np.random.randint(2) - 1
        chil = self._cre_chil(par, chil_len)
        cln = par[np.random.choice(len(par), pop_len - chil_len)]
        if len(chil) == 0:
            return cln
        elif len(cln) == 0:
            return chil
        return np.concatenate((cln, chil))

    def _cre_chil(self, par, size):
        par_len = len(par)
        r = np.random.randint(par_len, size=(size, 2))
        return np.array([
            self._func(par[r[i, 0]], par[r[i, 1]])
            for i in range(size // 2)
        ]).reshape((-1,) + par.shape[1:])


    def run(self, end_gen=df.END_GEN):
        # ここの表示もちょっとあやしい
        #print("\rgen: {0:d}".format(0), end="")
        print("gen: 0")
        if self._contains_goal_ind():
            print("\ngoal")
            return self._goal_ind
        for i in range(end_gen):
            #print("\rgen: {0:d}".format(i + 1), end="")
            print("gen: " + str(i + 1))
            if self._contains_goal_ind():
                print("\ngoal")
                return self._goal_ind
            print("hi")
            ftns = np.array([self._eval_func(e) for e in self._pop])
            parents = self._sel.sel(self._pop, ftns)
            self._pop = self._xovr.xovr(parents, len(ftns))
            self._pop = self._mut.mut(self._pop)
        print()
        return self._get_best()
