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


def assoc(d, k, v):
    r = dict(d)
    r[k] = v
    return r


def raise_(ex):
    raise ex


def raiseb(msg):
    raise_(BaseException(msg))


def raisef(ex_supplier):
    return lambda: raise_(ex_supplier())


def raisefb(msg_supplier):
    return raisef(lambda: BaseException(msg_supplier()))


def switch(val, dict):
    f = dict.get(val) or dict.get(switch.ELSE)
    return f() if f else None


switch.ELSE = object()


def switch_type(val, dict):
    return switch(type(val) if val else None, dict)


def merge_dicts(d1, d2):
    r = dict(d1)
    r.update(d2)
    return r


def conj(col, el):
    return switch_type(col, {
        None: lambda: [el],
        list: lambda: list(col) + [el],
        set: lambda: set(col).union({el}),
        tuple: lambda: col + (el,),
        dict: lambda: merge_dicts(col, dict([el])),
        switch.ELSE: lambda: raiseb('Can conj only one of: list, set, tuple, or dict! Got: %s' % col)
    })


def conj_all(col1, col2):
    if col2 is None:
        return col1 or []
    return switch_type(col1, {
        None: lambda: list(col2),
        list: lambda: col1 + list(col2),
        set: lambda: col1.union(set(col2)),
        tuple: lambda: col1 + tuple(col2),
        dict: lambda: merge_dicts(col1, col2),
        switch.ELSE: lambda: raiseb('Can conj only one of: list, set, tuple, or dict! Got: %s' % col1)
    })
