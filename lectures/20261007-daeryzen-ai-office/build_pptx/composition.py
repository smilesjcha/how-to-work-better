"""수업 의도에 따라 장표 구성을 고르는 결정 트리.

type은 자료의 종류이고, composition은 그 자료를 보여 주는 방식이다.
명시적 composition이 있으면 그것을 우선한다. 그렇지 않으면 내용의 밀도와
앞선 장표의 화면 리듬을 함께 고려한다. 결과는 재현 가능하다.
"""

VARIANTS = {
    'triad': ('index', 'columns', 'spotlight'),
    'compare': ('contrast', 'verdict', 'parallel'),
    'table': ('ledger', 'bands', 'matrix'),
    'exercise': ('worksheet', 'path', 'checklist'),
    'prompt': ('source', 'annotated'),
    'process': ('rail', 'stair'),
    'chart': ('bars', 'rank'),
}


def teaching_job(slide):
    """레이아웃 선택에 쓰는 교육 기능. 화면에 표시되지 않는다."""
    kind = slide['type']
    if kind in ('exercise', 'prompt'):
        return 'practice'
    if kind in ('table', 'chart'):
        return 'evidence'
    if kind in ('compare', 'triad', 'process'):
        return 'explain'
    return 'transition'


def choose(slides):
    """각 장표에 _composition을 배정하고 선택 로그를 반환한다."""
    seen = {kind: 0 for kind in VARIANTS}
    log = []
    previous = None
    for index, slide in enumerate(slides, 1):
        kind = slide['type']
        choices = VARIANTS.get(kind)
        if not choices:
            variant = kind
        elif slide.get('composition'):
            variant = slide['composition']
            if variant not in choices:
                raise ValueError(f'{index}번 장표: 지원하지 않는 composition {variant}')
        else:
            ordinal = seen[kind]
            # 고밀도 표는 전체 너비를 쓰는 행렬이 더 명료하다.
            if kind == 'table' and (len(slide['headers']) >= 5 or len(slide['rows']) >= 6):
                variant = 'matrix'
            # 긴 프롬프트는 주석 여백보다 본문 폭을 확보한다.
            elif kind == 'prompt' and len(slide['prompt']) > 210:
                variant = 'source'
            else:
                variant = choices[ordinal % len(choices)]
                if previous == variant and len(choices) > 1:
                    variant = choices[(ordinal + 1) % len(choices)]
            seen[kind] += 1
        slide['_composition'] = variant
        log.append((index, teaching_job(slide), kind, variant))
        previous = variant
    return log


def repetition_report(log):
    """연속 3장 이상 동일한 화면 유형이 나오는지 확인한다."""
    runs = []
    current = None
    start = 0
    length = 0
    for index, _, _, variant in log:
        if variant == current:
            length += 1
        else:
            if length >= 3:
                runs.append((start, index - 1, current))
            current, start, length = variant, index, 1
    if length >= 3:
        runs.append((start, log[-1][0], current))
    return runs
