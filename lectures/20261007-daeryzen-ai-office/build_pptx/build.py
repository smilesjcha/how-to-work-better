"""slides_data.py에서 데어리젠 교육 PPT를 재현한다."""
import os
import sys
from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import theme as T
import layouts as L
from slides_data import SLIDES

def build():
    assert 130 <= len(SLIDES) <= 150, f'장표 수 검증 실패: {len(SLIDES)}'
    prs = Presentation()
    prs.slide_width, prs.slide_height = T.W, T.H
    L.TOTAL = len(SLIDES)
    for index, data in enumerate(SLIDES, 1):
        data['no'] = index
        try:
            L.TYPES[data['type']](prs, data)
        except Exception as exc:
            raise RuntimeError(f'{index}번 장표 ({data.get("title")}) 생성 실패') from exc
    output_dir = os.path.abspath(os.path.join(HERE, '..', 'output'))
    os.makedirs(output_dir, exist_ok=True)
    output = os.path.join(output_dir, 'daeryzen-ai-office-20261007.pptx')
    prs.save(output)
    print(f'{output}: {len(prs.slides)} slides')
    return output

if __name__ == '__main__':
    build()
