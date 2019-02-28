from typing import List, NewType


class FARule:

    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    def follow(self):
        return self.next_state

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.state} -- {self.character} --> {self.next_state}'


class DFARuleBook:

    def __init__(self, rules: List[FARule]):
        self.rules = rules

    def rule_for(self, state, character):
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule

    def next_state(self, state, character):
        return self.rule_for(state, character).follow()


class DFA:
    def __init__(self, current_state: int, accept_states: List[int], rulebook: DFARuleBook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)

    def read_string(self, string):
        for s in string:
            self.read_character(s)


class DFAFactory:
    def __init__(self, start_state: int, accept_states: List[int], rulebook: DFARuleBook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def get_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accept(self, string):
        dfa = self.get_dfa()
        dfa.read_string(string)
        return dfa.accepting()
