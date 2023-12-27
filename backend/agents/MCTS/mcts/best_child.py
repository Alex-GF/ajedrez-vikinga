from math import sqrt, log

def best_child(v, c):

    best_child = None
    best_child_id = None

    for i in range(len(v.children)):

        child = v.children[i]

        if best_child == None or child_index(child, c)>child_index(best_child, c):
            best_child = child
            best_child_id = i

    return best_child_id

def child_index(v, c):

    result = (v.q/v.n) + (c*sqrt((2*log(v.n))/v.n))
    return result