def sumTuples(t1, t2):
    return tuple(sum(x) for x in zip(t1, t2))

def multTupleWithScalar(t, a):
    return tuple(x * a for x in t)

def subTuples(t1, t2):
    t2 = multTupleWithScalar(t2, -1)
    return tuple(sum(x) for x in zip(t1, t2))

def absTuple(t):
    return (abs(t[0]), abs(t[1]))
