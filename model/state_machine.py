from typing import List, Sequence
from itertools import chain


class FARule:

    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def applies_to(self, state, character):
        # indicate if it can accept this state and character
        return self.state == state and self.character == character

    def follow(self):
        # return the next transfer state
        return self.next_state

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.state} / {self.character} --> {self.next_state}'


class DFARuleBook:

    def __init__(self, rules: List[FARule]):
        self.rules = rules

    def rule_for(self, state, character):
        # search for and return the right rule
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule

    def next_state(self, state, character):
        # transfer to next state
        return self.rule_for(state, character).follow()


class DFA:
    def __init__(self, current_state: int, accept_states: List[int], rulebook: DFARuleBook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        # determine if it can be accepted
        return self.current_state in self.accept_states

    def read_character(self, character):
        # transfer to next state by using this character
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
        # generate a new dfa
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accept(self, string):
        dfa = self.get_dfa()
        dfa.read_string(string)
        return dfa.accepting()


class NFARuleBook:
    def __init__(self, rules: List[FARule]):
        self.rules = rules

    def rule_for(self, state, character) -> Sequence:
        # collect all rules meet the state and character
        return [rule for rule in self.rules if rule.applies_to(state, character)]

    def follow_rules_for(self, state, character) -> Sequence:
        # gather all states after one state transfer to next state
        return [rule.follow() for rule in self.rule_for(state, character)]

    def next_states(self, states, character):
        # return all possible states
        return set(_state
                   for state in states
                   for _state in self.follow_rules_for(state, character))


class NFA:
    def __init__(self, current_states: set, accept_states: set, rulebook: NFARuleBook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        # determine if it can be accepted
        return self.current_states & self.accept_states

    def read_character(self, character):
        # transfer to next state by using this character
        self.current_states = self.rulebook.next_states(self.current_states, character)

    def read_string(self, string):
        for s in string:
            self.read_character(s)


class NFAFactory:
    def __init__(self, start_state: int, accept_states: List[int], rulebook: NFARuleBook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def get_dfa(self):
        # generate a new nfa
        return NFA({self.start_state}, set(self.accept_states), self.rulebook)

    def accept(self, string):
        dfa = self.get_dfa()
        dfa.read_string(string)
        return dfa.accepting()
