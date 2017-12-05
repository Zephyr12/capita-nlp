import unittest
import pipes
from unittest.mock import Mock, call


class PipesTestSuite(unittest.TestCase):

    def test_source(self):
        output = Mock()
        output.process = Mock()
        lst = [1,"fish", ["arr", "bar"], {"one time": "no mangle"}]
        source = pipes.Source(lambda x: lst)
        source.add_out_pipe(output)
        source.run().join()
        output.process.assert_has_calls([call(l) for l in lst], any_order=True)

    def test_processor(self):
        output = Mock()
        output.process = Mock()
        processor = pipes.Processor(lambda x: [x*x])
        processor.add_out_pipe(output)
        processor.process(1)
        processor.process(2)
        processor.process(3)
        output.process.assert_has_calls([call(l*l) for l in [1,2,3]], any_order=False)
