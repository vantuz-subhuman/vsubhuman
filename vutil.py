def chain(v, *functions, break_on_none=False):
    """
    Apply the chain of functions to the value 'pipe-style',
     e.i. `v | f1 | f2 | ... | fn` or `fn(...(f2(f1(v))))`
    :param v: first value of the chain
    :param functions: the chain of functions to be applied to the value
    :param break_on_none: if true - the chain is terminated
     the moment value becomes none (false by default).
    :return: the result of the last applied function
    """
    for f in functions:
        if break_on_none and v is None:
            return v
        v = f(v)
    return v


def chain2(v, *functions):
    """
    Apply the chain of functions to the value 'pipe-style'.
    The chain is terminated the moment value becomes none.
    The same as `chain` with `break_on_none=True`
    :param v: first value of the chain
    :param functions:  the chain of functions
    :return: the result of the last applied function
    """
    return chain(v, *functions, break_on_none=True)


def P(f, *args, **kwargs):
    def foo(*args2, **kwargs2):
        largs2 = list(args2)
        fargs = []
        for a in args:
            fargs.append(largs2.pop(0) if a == P._ else a)
        for k in kwargs:
            if kwargs[k] == P._:
                kwargs[k] = largs2.pop(0)
        kwargs.update(kwargs2)
        return f(*fargs, *largs2, **kwargs)

    return foo


P._ = object()


def mapv(v, f, *args, **kwargs):
    return chain2(v, P(f, *args, **kwargs))


def empty(s):
    return s is None or len(s) == 0


def lower(s):
    return mapv(s, str.lower)


def split(s, sep=None, maxsplit=-1):
    return mapv(s, str.split, P._, sep, maxsplit) or []


def destruct(dict, *keys):
    return [dict.get(k) if dict else None for k in keys]


def assoc(dict, k, v):
    dict[k] = v
    return dict
