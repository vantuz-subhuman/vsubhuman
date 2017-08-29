def empty(s):
    return s is None or len(s) == 0


def assoc(dict, k, v):
    dict[k] = v
    return dict


def P(f, *args, **kwargs):
    def foo(*args2, **kwargs2):
        largs2 = list(args2)
        fargs=[]
        for a in args:
            fargs.append(largs2.pop(0) if a == P else a)
        for k in kwargs:
            if kwargs[k] == P:
                kwargs[k] = largs2.pop(0)
        kwargs.update(kwargs2)
        return f(*fargs, *largs2, **kwargs)
    return foo
