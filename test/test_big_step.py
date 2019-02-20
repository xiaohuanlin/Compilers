import unittest
from io import StringIO
from unittest.mock import patch

from model.big_step import Number, Add, Multiply, Machine, LessThan, Variable, Assign, \
    IF, Boolean, Sequence, While


class ModelTestCase(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_number(self, mock_stdout):
        Machine(
            Number(23),
            {}
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "<23>\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_variable(self, mock_stdout):
        Machine(
            Variable('x'),
            {
                'x': Number(5)
            }
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "<5>\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_less_than(self, mock_stdout):
        Machine(
            LessThan(
                Add(Variable('x'), Number(2)),
                Variable('y')
            ),
            {
                'x': Number(2),
                'y': Number(5)
            }
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "<True>\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_if_else(self, mock_stdout):
        Machine(
            IF(
                Variable('x'),
                Assign('y', Number(1)),
                Assign('y', Number(2))
            ),
            {
                'x': Boolean(True)
            }
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "{'x': <True>, 'y': <1>}\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_sequence(self, mock_stdout):
        Machine(
            Sequence(
                Assign('x', Add(Number(1), Number(1))),
                Assign('y', Multiply(Number(2), Variable('x')))
            ),
            {}
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "{'x': <2>, 'y': <4>}\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_while(self, mock_stdout):
        Machine(
            While(
                LessThan(Variable('x'), Number(5)),
                Assign('x', Multiply(Variable('x'), Number(3)))
            ),
            {
                'x': Number(1)
            }
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "{'x': <9>}\n"
                         )



