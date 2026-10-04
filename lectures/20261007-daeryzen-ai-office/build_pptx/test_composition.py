"""장표 구성 선택의 재현성과 반복 방지 검사."""
import copy
import unittest
from composition import choose, repetition_report
from slides_data import SLIDES


class CompositionTest(unittest.TestCase):
    def test_all_slides_have_valid_composition(self):
        data = copy.deepcopy(SLIDES)
        log = choose(data)
        self.assertEqual(len(log), 140)
        self.assertGreaterEqual(len(set(row[3] for row in log)), 20)
        self.assertEqual(repetition_report(log), [])

    def test_dense_table_selects_matrix(self):
        data = [{'type': 'table', 'title': '검산표',
                 'headers': ['a', 'b', 'c', 'd', 'e'], 'rows': [['1']*5]}]
        self.assertEqual(choose(data)[0][3], 'matrix')

    def test_long_prompt_gets_full_width(self):
        data = [{'type': 'prompt', 'title': '긴 요청', 'prompt': '가'*211}]
        self.assertEqual(choose(data)[0][3], 'source')

    def test_explicit_override(self):
        data = [{'type': 'triad', 'title': '선택', 'cards': [('a', 'b')]*3,
                 'composition': 'spotlight'}]
        self.assertEqual(choose(data)[0][3], 'spotlight')


if __name__ == '__main__':
    unittest.main()
