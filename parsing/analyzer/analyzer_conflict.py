

class AnalyzerConflict(RuntimeError):

    def __init__(self, context):
        RuntimeError.__init__(self, "Unable to continue {}, please check your input ...".format(context))
