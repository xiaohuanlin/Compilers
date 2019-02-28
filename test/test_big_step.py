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

    def test_to_python(self):
        func = eval(Number(5).to_python())
        self.assertEqual(func({}),
                         5)
        func = eval(Boolean(True).to_python())
        self.assertEqual(func({}),
                         True)
        func = eval(Variable('x').to_python())
        self.assertEqual(func({'x': 5}),
                         5)
        func = eval(Add(Variable('x'), Number(5)).to_python())
        self.assertEqual(func({'x': 5}),
                         10)
        func = eval(Multiply(Variable('x'), Number(5)).to_python())
        self.assertEqual(func({'x': 5}),
                         25)
        func = eval(LessThan(Variable('x'), Number(3)).to_python())
        self.assertEqual(func({'x': 5}),
                         False)
        func = eval(Assign('x', Number(3)).to_python())
        self.assertEqual(func({'x': 5}),
                         {'x': 3})
        func = eval(IF(
            Variable('x'),
            Assign('y', Number(1)),
            Assign('y', Number(2))
        ).to_python())
        self.assertEqual(func({'x': 5}),
                         {'x': 5, 'y': 1})
        func = eval(Sequence(Assign('x', Add(Number(1), Variable('x'))),
                             Assign('x', Multiply(Number(2), Variable('x')))).to_python())
        self.assertEqual(func({'x': 2}),
                         {'x': 6})
        func = lambda env: \
            exec(While(
                LessThan(Variable('x'), Number(5)),
                Assign('x', Multiply(Variable('x'), Number(3)))
            ).to_python() % env)
        func({'x': 2})
        self.assertEqual(globals()['env'], {'x': 6})
