from model.state_machine import DFARuleBook, FARule, DFA, DFAFactory, NFARuleBook, NFA, NFAFactory
from unittest import TestCase


class TestStateMachine(TestCase):

    def test_dfa(self):
        rulebook = DFARuleBook(
            [
                FARule(1, 'a', 2),
                FARule(1, 'b', 1),

                FARule(2, 'a', 2),
                FARule(2, 'b', 3),

                FARule(3, 'a', 3),
                FARule(3, 'b', 3),
            ]
        )
        self.assertEqual(rulebook.next_state(1, 'a'), 2)
        self.assertEqual(rulebook.next_state(1, 'b'), 1)
        self.assertEqual(rulebook.next_state(2, 'b'), 3)

        # test read_character
        dfa = DFA(1, [3], rulebook)
        self.assertFalse(dfa.accepting())

        dfa.read_character('b')
        self.assertFalse(dfa.accepting())

        for _ in range(3):
            dfa.read_character('a')
        self.assertFalse(dfa.accepting())

        dfa.read_character('b')
        self.assertTrue(dfa.accepting())

        # test read_string
        dfa = DFA(1, [3], rulebook)
        self.assertFalse(dfa.accepting())

        dfa.read_string('baaab')
        self.assertTrue(dfa.accepting())

        # test DFAFactory
        dfa_factory = DFAFactory(1, [3], rulebook)
        self.assertFalse(dfa_factory.accept('a'))
        self.assertFalse(dfa_factory.accept('baa'))
        self.assertTrue(dfa_factory.accept('baba'))

    def test_nfa(self):
        rulebook = NFARuleBook(
            [
                FARule(1, 'a', 1),
                FARule(1, 'b', 1),
                FARule(1, 'b', 2),

                FARule(2, 'a', 3),
                FARule(2, 'b', 3),

                FARule(3, 'a', 4),
                FARule(3, 'b', 4),
            ]
        )
        self.assertEqual(rulebook.next_states([1], 'b'), {1, 2})
        self.assertEqual(rulebook.next_states([1, 2], 'a'), {1, 3})
        self.assertEqual(rulebook.next_states([1, 3], 'b'), {1, 2, 4})

        # test read_character
        nfa = NFA({1}, {4}, rulebook)
        self.assertFalse(nfa.accepting())

        nfa.read_character('b')
        self.assertFalse(nfa.accepting())

        nfa.read_character('a')
        self.assertFalse(nfa.accepting())

        nfa.read_character('b')
        self.assertTrue(nfa.accepting())

        nfa = NFA({1}, {4}, rulebook)
        self.assertFalse(nfa.accepting())

        # test read_string
        nfa.read_string('bbbbb')
        self.assertTrue(nfa.accepting())

        # test NFAFactory
        nfa_factory = NFAFactory(1, [4], rulebook)
        self.assertTrue(nfa_factory.accept('bab'))
        self.assertTrue(nfa_factory.accept('bbbbb'))
        self.assertFalse(nfa_factory.accept('bbabb'))
