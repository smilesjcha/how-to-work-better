"""데어리젠 장표 디자인 토큰.

색·서체·크기·간격은 이 파일에서만 바꾼다. layouts.py는 조합만 담당한다.
"""
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

def rgb(value):
    return RGBColor.from_string(value.lstrip('#'))

NAVY = rgb('17283B')
INK = rgb('111315')
BLUE = rgb('28435A')
PALE = rgb('E7EBE9')
SURFACE = rgb('F3F4F1')
WHITE = rgb('FFFFFF')
LINE = rgb('CED4D1')
MUTED = rgb('59615F')
GOOD = rgb('0B684F')
WARM = rgb('95D0AC')
PAPER = rgb('FBFBF8')
SOFT_GREEN = rgb('E7F1EA')
GRAY_DARK = rgb('303638')

FONT = 'NanumGothic'
FONT_HEAVY = 'NanumGothic ExtraBold'
MONO = 'Menlo'
COVER = Pt(44)
TITLE = Pt(30)
LEAD = Pt(19)
BODY = Pt(20)
BODY_SM = Pt(18.5)
TABLE = Pt(17.5)
TABLE_COMPACT = Pt(16)
TABLE_HEAD = Pt(16)
CAPTION = Pt(11)
PAGE = Pt(10)
KICKER = Pt(12)
BIG_NUM = Pt(62)
MID_NUM = Pt(38)
SMALL_NUM = Pt(28)
PROMPT_TEXT = Pt(18)
CORNER = .10

W = Inches(13.333)
H = Inches(7.5)
MX = Inches(.72)
CW = W - 2*MX
GAP = Inches(.28)
HEADER_Y = Inches(.48)
HEADER_H = Inches(.68)
RULE_Y = Inches(1.28)
FOOTER_Y = Inches(7.11)
FOOTER_H = Inches(.20)
RULE_W = Inches(.82)
RULE_THICK = Pt(2.2)
STROKE = Pt(.8)
PAD = Inches(.17)
TABLE_PAD = Inches(.08)
BODY_LINES = 1.10

# 편집형 구성: 동일 타입 안에서도 화면 리듬을 바꾸는 공통 그리드
LEAD_Y = Inches(1.52)
LEAD_H = Inches(.63)
STAGE_Y = Inches(2.38)
STAGE_H = Inches(4.24)
STAGE_BOTTOM = STAGE_Y + STAGE_H
WIDE_LEFT = Inches(4.48)
TABLE_TOP = Inches(2.44)
TABLE_HEIGHT = Inches(4.12)
RULE_SPACING = Inches(.04)
ROW_NUM_W = Inches(1.04)
EDITORIAL_INSET = Inches(.29)
CHART_TOP = Inches(2.43)
CHART_ROW = Inches(.60)
CHART_GAP = Inches(.10)
CHART_LABEL = Inches(3.58)
CHART_BAR = Inches(6.55)
CHART_BAR_H = Inches(.26)
PROMPT_LABEL_W = Inches(1.62)
PROMPT_BODY_X = MX + PROMPT_LABEL_W
PROMPT_BODY_W = CW - PROMPT_LABEL_W
PROMPT_LINE_H = Inches(.58)
PHOTO_W = Inches(5.00)
PHOTO_H = Inches(3.15)

# 레이아웃 전용 기하값
COVER_KICKER_Y = Inches(.88)
COVER_TITLE_Y = Inches(1.55)
COVER_SUB_Y = Inches(3.55)
COVER_META_Y = Inches(5.57)
SECTION_NO_Y = Inches(1.45)
SECTION_TITLE_Y = Inches(2.25)
SECTION_SUB_Y = Inches(3.65)
PANEL_TITLE_H = Inches(.48)
IMAGE_W = Inches(5.7)

# 자동 줄바꿈: 실제 설치 서체로 폭을 측정하고 행 높이를 산정한다.
FONT_PATH = '/Users/sungjae-cha/Library/Fonts/NanumGothic.ttf'
MEASURE_SCALE = 4
WRAP_SAFE = .94
PROMPT_PAD_Y = Inches(.13)
PROMPT_MIN_H = Inches(.56)
TEXT_LEADING = 1.20
PROFILE_NAME = Pt(28)
PROFILE_NAME_H = Inches(.50)
PROFILE_GROUP_GAP = Inches(.15)
PROFILE_LABEL_H = Inches(.24)
PROFILE_ROW_H = Inches(.34)

# 문서형 장표: 서식의 목적에 따라 서로 다른 정보 구조를 사용한다.
DOC_BODY = Pt(17)
DOC_SMALL = Pt(15)
DOC_LABEL = Pt(12)
DOC_VALUE = Pt(27)
DOC_ROW_H = Inches(.48)
DOC_HEAD_H = Inches(.40)
DOC_KPI_H = Inches(1.12)
DOC_GAP = Inches(.22)
DOC_INSET = Inches(.16)
DOC_CONCLUSION_H = Inches(.96)
DOC_LEFT_RATIO = .60
DOC_RIGHT_RATIO = .40
DOC_BAND_H = Inches(.72)
DOC_BLOCK_TITLE_H = Inches(.36)
DOC_BLOCK_BODY_H = Inches(1.20)
DOC_BLOCK_GAP = Inches(.22)
DOC_BOTTOM_H = Inches(.60)
DOC_FLOW_H = Inches(.74)
DOC_FLOW_ARROW_W = Inches(.28)
DOC_SPEC_FOOT_GAP = Inches(.16)
GANTT_META_RATIO = .59
GANTT_HEAD_H = Inches(.52)
GANTT_ROW_H = Inches(.47)
GANTT_BAR_H = Inches(.21)
GANTT_COLS = (.04, .19, .12, .05, .19)
DASH_KPI_H = Inches(1.12)
DASH_DETAIL_H = Inches(2.40)
DASH_PLOT_RATIO = .57
DASH_BAR_H = Inches(.17)
DASH_ROW_H = Inches(.56)
DASH_LABEL_W = Inches(1.10)
DASH_VALUE_W = Inches(.90)
DASH_PLOT_MAX = 1.10
