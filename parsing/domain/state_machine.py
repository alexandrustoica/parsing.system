from parsing.domain.state import State


class StateMachine:

    def __init__(self, start: State):
        
        self.__start = start
        self.start_root = {
            "node": None,
            "neighbours": []
        }
        state_set = {start}
        self.build_state_machine(start, self.start_root, state_set)

        for x in state_set:
            print (x)
            print()

    def build_state_machine(self, current: State, edge: dict, state_set):

        neighbours = []
        for sym in (x.next for x in current.items if x.has_next):

            next = current.go_to(sym)
            if next in state_set:
                neighbours.append(next)
                continue
            state_set.add(next)
            if next.is_valid:
                neighbours.append((self.build_state_machine(next, {
                    "node": next
                }, state_set), sym))

        edge['neighbours']= neighbours

