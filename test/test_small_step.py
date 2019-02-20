import unittest
from io import StringIO
from unittest.mock import patch

from model.small_step import Number, Add, Multiply, ExpressionMachine, StatementMachine, LessThan, Variable, Assign, \
    IF, Boolean, Sequence, While


class ModelTestCase(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_multiply(self, mock_stdout):
        ExpressionMachine(
            Add(
                Multiply(Number(1), Number(2)),
                Multiply(Number(3), Number(4))
            )
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         '<<<1> * <2>> + <<3> * <4>>>\n'
                         '<<2> + <<3> * <4>>>\n'
                         '<<2> + <12>>\n'
                         '<14>\n'
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_less_than(self, mock_stdout):
        ExpressionMachine(
            LessThan(
                Number(5),
                Add(Number(2), Number(2))
            )
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         '<<5> < <<2> + <2>>>\n'
                         '<<5> < <4>>\n'
                         '<False>\n'
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_variable(self, mock_stdout):
        ExpressionMachine(
            Add(Variable('x'), Variable('y')),
            {
                'x': Number(3),
                'y': Number(4)
            }
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         '<<x> + <y>>\n'
                         '<<3> + <y>>\n'
                         '<<3> + <4>>\n'
                         '<7>\n'
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_statement_machine(self, mock_stdout):
        StatementMachine(
            Assign('x', Add(Variable('x'), Number(1))),
            {
                'x': Number(2),
            }
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "<x = <<x> + <1>>>\n"
                         "{'x': <2>}\n"
                         "<x = <<2> + <1>>>\n"
                         "{'x': <2>}\n"
                         "<x = <3>>\n"
                         "{'x': <2>}\n"
                         "<do-nothing>\n"
                         "{'x': <3>}\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_if_else(self, mock_stdout):
        StatementMachine(
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
                         "<if <x>: <y = <1>> else: <y = <2>>\n"
                         "{'x': <True>}\n"
                         "<if <True>: <y = <1>> else: <y = <2>>\n"
                         "{'x': <True>}\n"
                         "<y = <2>>\n"
                         "{'x': <True>}\n"
                         "<do-nothing>\n"
                         "{'x': <True>, 'y': <2>}\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_sequence(self, mock_stdout):
        StatementMachine(
            Sequence(
                Assign('x', Add(Number(1), Number(2))),
                Assign('y', Add(Variable('x'), Number(3)))
            ),
            {}
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "<<x = <<1> + <2>>>; <y = <<x> + <3>>>>\n"
                         "{}\n"
                         "<<x = <3>>; <y = <<x> + <3>>>>\n"
                         "{}\n"
                         "<<do-nothing>; <y = <<x> + <3>>>>\n"
                         "{'x': <3>}\n"
                         "<y = <<x> + <3>>>\n"
                         "{'x': <3>}\n"
                         "<y = <<3> + <3>>>\n"
                         "{'x': <3>}\n"
                         "<y = <6>>\n"
                         "{'x': <3>}\n"
                         "<do-nothing>\n"
                         "{'x': <3>, 'y': <6>}\n"
                         )

    @patch('sys.stdout', new_callable=StringIO)
    def test_while(self, mock_stdout):
        StatementMachine(
            While(
                LessThan(Variable('x'), Number(3)),
                Assign('x', Multiply(Variable('x'), Number(3)))
            ),
            {'x': Number(1)}
        ).run()
        self.assertEqual(mock_stdout.getvalue(),
                         "<while <<x> < <3>>: <x = <<x> * <3>>>>\n"
                         "{'x': <1>}\n"
                         "<if <<x> < <3>>: <<x = <<x> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>> else: <do-nothing>\n"
                         "{'x': <1>}\n"
                         "<if <<1> < <3>>: <<x = <<x> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>> else: <do-nothing>\n"
                         "{'x': <1>}\n"
                         "<if <True>: <<x = <<x> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>> else: <do-nothing>\n"
                         "{'x': <1>}\n"
                         "<<x = <<x> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>>\n"
                         "{'x': <1>}\n"
                         "<<x = <<1> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>>\n"
                         "{'x': <1>}\n"
                         "<<x = <3>>; <while <<x> < <3>>: <x = <<x> * <3>>>>>\n"
                         "{'x': <1>}\n"
                         "<<do-nothing>; <while <<x> < <3>>: <x = <<x> * <3>>>>>\n"
                         "{'x': <3>}\n"
                         "<while <<x> < <3>>: <x = <<x> * <3>>>>\n"
                         "{'x': <3>}\n"
                         "<if <<x> < <3>>: <<x = <<x> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>> else: <do-nothing>\n"
                         "{'x': <3>}\n"
                         "<if <<3> < <3>>: <<x = <<x> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>> else: <do-nothing>\n"
                         "{'x': <3>}\n"
                         "<if <False>: <<x = <<x> * <3>>>; <while <<x> < <3>>: <x = <<x> * <3>>>>> else: <do-nothing>\n"
                         "{'x': <3>}\n"
                         "<do-nothing>\n"
                         "{'x': <3>}\n"
                         )
