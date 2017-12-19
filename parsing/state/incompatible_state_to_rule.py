

class IncompatibleStateToRuleException(RuntimeError):

    def __init__(self):
        RuntimeError.__init__(self, "State incompatible to any rule from grammar.")

