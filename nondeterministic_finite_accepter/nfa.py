from collections.abc import Sequence


class NFA:
    def __init__(self, nfa):
        self.initial_state: str = nfa["initial_state"]
        self.final_states: set[str] = set(nfa["final_states"])
        self.transition: dict[str, dict[str, str | list[str] | None]] = nfa[
            "transition"
        ]

    def lambda_closure(self, state: str | Sequence[str]) -> set[str]:
        res: set[str] = set()
        set_to_add: set[str] = {state} if isinstance(state, str) else set(state)
        while set_to_add:
            res.update(set_to_add)
            set_to_add = self.move(set_to_add, "") - res
        return res

    def move(self, state: str | Sequence[str], symbol: str) -> str | set[str]:
        if isinstance(state, str):
            try:
                res: str | list[str] | None = self.transition[state][symbol]
                return (
                    set(res) if isinstance(res, list) else set() if res is None else res
                )
            except KeyError:
                return set()
        else:
            result: set[str] = set()
            for q in state:
                r = self.move(q, symbol)
                result.update(r) if isinstance(r, set) else result.add(r)
            return result

    def delta_star(self, state: str | Sequence[str], string: str) -> set[str]:
        res = self.lambda_closure(state)
        for symbol in string:
            res = self.lambda_closure(self.move(res, symbol))
        return res

    def accepts(self, string: str) -> bool:
        states = self.delta_star(self.initial_state, string)
        return any(state in self.final_states for state in states)
