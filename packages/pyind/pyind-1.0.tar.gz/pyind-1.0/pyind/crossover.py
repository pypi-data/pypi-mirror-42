import numpy as np


def p2(ind0, ind1):
    """
    Two-point crossover

    Parameters
    ----------
    ind0 : ndarray
        Father
    ind1 : ndarray
        Mother

    Returns
    -------
    chil : ndarray
        Child
    """

    sta, end = _cre_sta_end(len(ind0))
    return (
        np.concatenate((ind0[:sta], ind1[sta:end], ind0[end:])),
        np.concatenate((ind1[:sta], ind0[sta:end], ind1[end:])),
    )


def uniform(ind0, ind1):
    """
    Uniform crossover

    Parameters
    ----------
    ind0 : ndarray
        Father
    ind1 : ndarray
        Mother

    Returns
    -------
    chil : ndarray
        Child
    """

    mask = np.random.randint(2, size=len(ind0))
    return (
        ind0 * mask + ind1 * np.logical_not(mask),
        ind1 * mask + ind0 * np.logical_not(mask),
    )


def ox(ind0, ind1):
    """
    Order-based crossover (OX)

    Parameters
    ----------
    ind0 : ndarray
        Father
    ind1 : ndarray
        Mother

    Returns
    -------
    chil : ndarray
        Child
    """

    sta, end = _cre_sta_end(len(ind0))
    keep0 = ind0[sta:end]
    keep1 = ind1[sta:end]
    rec0 = np.setdiff1d(ind1, keep0, True)
    rec1 = np.setdiff1d(ind0, keep1, True)
    return (
        np.concatenate((rec0[:sta], keep0, rec0[sta:])),
        np.concatenate((rec1[:sta], keep1, rec1[sta:])),
    )


def _cre_sta_end(_len):
    end = np.random.randint(_len) + 1
    sta = np.random.randint(end)
    return sta, end


class Crossover:
    def __init__(self, conf):
        self._func = conf["func"]
        self._pb = conf["pb"]

    def xovr(self, par, pop_len):
        chil_len = np.random.binomial(pop_len, self._pb)
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
        div, mod = divmod(size, 2)
        chil = np.array([
            self._func(par[r[i, 0]], par[r[i, 1]])
            for i in range(div)
        ]).reshape((-1,) + par.shape[1:])
        if mod == 1:
            return np.concatenate((
                chil,
                self._func(par[r[-1, 0]], par[r[-1, 1]])
            ))[:-1]
        return chil


if __name__ == "__main__":
    ind0 = np.zeros(20, dtype=int)
    ind1 = np.ones(20, dtype=int)
    par = np.array([ind0, ind1])
    conf = {
        "func": ox,
        "pb": 0.95
    }
    c = Crossover(conf)
    print(par)
    print(c.xovr(par, 10))
