class Nodo:
    
    def __init__ (self, state, movements, n, q, i, children, parent, max_movements):
        self.state = state
        self.movements = movements
        self.n = n
        self.q = q
        self.i = i
        self.children = children
        self.parent = parent
        self.max_movements = max_movements