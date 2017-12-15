

class Action:

    def __init__(self, source_state, action_type, destination_states):
        self._source_state = source_state
        self._action_type = action_type
        self._destination_states = destination_states
