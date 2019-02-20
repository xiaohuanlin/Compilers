import unittest
from unittest.mock import patch
from io import StringIO
from model.models import Number, Add, Multiply, Machine, LessThan


class ModelTestCase(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_multiply(self, mock_stdout):
        Machine(
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
        Machine(
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
