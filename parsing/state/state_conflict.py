

class StateConflict(RuntimeError):

    def __init__(self, state):
        RuntimeError.__init__(self, "State conflict for {}".format(repr(state)))
