from model.state_machine import DFARuleBook, FARule, DFA, DFAFactory
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


