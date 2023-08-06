def get_args(func, exclusion=()):
    args = list(
        func.__code__.co_varnames[:func.__code__.co_argcount]
    )
    for e in exclusion:
        args.remove(e)
    return tuple(args)


def cre_args(func, conf, exclusion=()):
    return tuple([
        conf[e] for e in get_args(func, exclusion)
    ])
