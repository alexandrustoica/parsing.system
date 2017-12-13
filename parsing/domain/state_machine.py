from parsing.domain.state import State


class StateMachine:

    def __init__(self, start: State):
        
        self.__start = start
        self.edges = []
        state_set = {start}
        self.build_state_machine(start, self.edges, state_set)

        print (self.edges)
    def build_state_machine(self, current: State, edges: dict, state_set):

        neighbours = []
        for sym in (x.next for x in current.items if x.has_next):

            next = current.go_to(sym)
            if next in state_set:
                edges.append((current, next, sym))
                continue
            state_set.add(next)
            if next.is_valid:
                edges.append((current, next, sym))
                self.build_state_machine(next, edges, state_set)

