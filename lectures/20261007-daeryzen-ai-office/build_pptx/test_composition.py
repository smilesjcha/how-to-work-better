"""장표 구성 선택의 재현성과 반복 방지 검사."""
import copy
import unittest
import csv
from pathlib import Path
from datetime import date
from composition import choose, repetition_report
from slides_data import SLIDES
import theme as T
from layouts import prompt_rows, wrap_text


class CompositionTest(unittest.TestCase):
    def test_all_slides_have_valid_composition(self):
        data = copy.deepcopy(SLIDES)
        log = choose(data)
        self.assertEqual(len(log), 148)
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

    def test_page93_wrapped_row_has_extra_height(self):
        rows = prompt_rows(SLIDES[92]['prompt'].split('\n'), T.PROMPT_BODY_W)
        self.assertIn('\n', rows[1][0])
        self.assertGreater(rows[1][1], rows[0][1])
        self.assertLessEqual(sum(height for _, height in rows), T.STAGE_H)

    def test_every_prompt_fits_full_width(self):
        for slide in SLIDES:
            if slide['type'] == 'prompt':
                with self.subTest(title=slide['title']):
                    prompt_rows(slide['prompt'].split('\n'), T.PROMPT_BODY_W)

    def test_audience_text_excludes_production_tmi_and_pairs(self):
        for slide in SLIDES:
            fields = [v for key, v in slide.items() if key not in ('note', 'body') or key == 'body' and slide['type'] != 'profile']
            text = str(fields)
            for prohibited in ('2인 1조', '짝과', '짝 실습', '강사 제공', '공식 입장이 아닌', 'Claude Code 비교'):
                self.assertNotIn(prohibited, text, slide['title'])

    def test_real_evidence_and_work_logs_stay_distinct(self):
        slide = SLIDES[113]
        self.assertIn('사실 출처', slide['right'][1])
        self.assertIn('업무상 필요한 결정 이유', slide['right'][1])
        self.assertIn('회의록', slide['bottom'])

    def test_example_metrics_match_source_csv(self):
        material = Path(__file__).resolve().parent.parent/'materials'
        with (material/'01-data/sales-quality-sample.csv').open() as f:
            sales = [row for row in csv.DictReader(f) if row['month'] == '2026-07']
        with (material/'01-data/july-targets.csv').open() as f:
            targets = {row['product']: int(row['target_units']) for row in csv.DictReader(f)}
        for source, displayed, bar in zip(sales, SLIDES[132]['rows'], SLIDES[138]['bars']):
            sold = int(source['sold_units']); returns = int(source['return_cases'])
            target = targets[source['product']]
            self.assertEqual(displayed[1], f'{sold:,}')
            self.assertEqual(displayed[2], f'{target:,}')
            self.assertEqual(displayed[4], f'{sold/target*100:.1f}%')
            self.assertEqual(displayed[5], str(returns))
            self.assertEqual(displayed[6], f'{returns/sold*100:.2f}%')
            self.assertAlmostEqual(bar[1], sold/target)
        total_sold = sum(int(row['sold_units']) for row in sales)
        total_returns = sum(int(row['return_cases']) for row in sales)
        self.assertEqual(SLIDES[132]['rows'][-1][1], f'{total_sold:,}')
        self.assertEqual(SLIDES[132]['rows'][-1][-1], f'{total_returns/total_sold*100:.2f}%')

    def test_wbs_dependency_dates(self):
        path = Path(__file__).resolve().parent.parent/'materials/05-document-forms/wbs-gantt.csv'
        with path.open() as f:
            rows = {row['id']: row for row in csv.DictReader(f)}
        self.assertEqual(len(rows), 6)
        for row in rows.values():
            self.assertLessEqual(date.fromisoformat(row['start_date']), date.fromisoformat(row['end_date']))
            if row['predecessor_id']:
                predecessor = rows[row['predecessor_id']]
                self.assertLess(date.fromisoformat(predecessor['end_date']), date.fromisoformat(row['start_date']))


if __name__ == '__main__':
    unittest.main()
