import unittest
from src import pipes
import unittest
import os
from scrapy.http import Response, Request, TextResponse
from src.scrapy.the_student_room.spiders import the_student_room_spider
from unittest.mock import Mock, call


class PipesTestSuite(unittest.TestCase):

    def test_source(self):
        output = Mock()
        output.process = Mock()
        lst = [1, "fish", ["arr", "bar"], {"one time": "no mangle"}]
        source = pipes.Source(lambda x: lst)
        source.add_out_pipe(output)
        source.run().join()
        output.process.assert_has_calls([call(l) for l in lst], any_order=True)

    def test_processor(self):
        output = Mock()
        output.process = Mock()
        processor = pipes.Processor(lambda x: [x * x])
        processor.add_out_pipe(output)
        processor.process(1)
        processor.process(2)
        processor.process(3)
        output.process.assert_has_calls([call(l * l) for l in [1, 2, 3]], any_order=False)


def fake_response_from_file(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'https://www.thestudentroom.co.uk/forumdisplay.php?f=14'

    request = Request(url=url)
    # if not file_name[0] == '/':
    #    responses_dir = os.path.dirname(os.path.realpath(__file__))
    #    file_path = os.path.join(responses_dir, file_name)
    # else:
    file_path = file_name

    file_content = open(file_path, 'r').read()

    response = TextResponse(url=url,
                            request=request,
                            body=file_content,
                            encoding='utf-8')
    print(response)
    # response.encoding = 'utf-8'
    return response


class StudentRoomSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = the_student_room_spider.TheStudentRoom()

    def _test_item_results(self, results, expected_length):
        count = 0
        permalinks = set()
        for item in results:
            self.assertIsNotNone(item['content'])
            self.assertIsNotNone(item['title'])
        self.assertEqual(count, expected_length)

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('scrapy_test_samples/University-of-Oxford.html'))
        for x in results:
            print("---------------")
            print("---------------")
            print(x)
            self._test_item_results(x, 10)
