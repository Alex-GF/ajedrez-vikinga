def backup(v, delta):

    while v != None:
        v.n = v.n + 1
        v.q = v.q + delta
        v = v.parent