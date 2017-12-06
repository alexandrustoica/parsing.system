from parsing.domain.state import State


class StateMachine:



    def __init__(self, start: State):
        
        self.__start = start
        self.start_root = {
            "node": None,
            "neighbours": []
        }
        self.build_state_machine(start, self.start_root, set())

    def build_state_machine(self, current: State, edge: dict, state_set):

        neighbours = []
        for sym in (x.next for x in current.items if x.has_next):

            print(current)
            print()
            #print("Ma duc cu symbolul: " + str(sym))
            next = current.go_to(sym)
            if next in state_set:
                neighbours.append(next)
                continue
            state_set.add(next)
            if next.is_valid:
                neighbours.append(self.build_state_machine(next, {
                    "node": next
                }, state_set))

        edge['neighbours']= neighbours

