"""삼척새일센터 강의의 색상·서체·간격·배치 단일 원본."""
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt


def color(value):
    value = value.lstrip("#")
    return RGBColor(int(value[:2], 16), int(value[2:4], 16), int(value[4:], 16))


INK = color("#17212B")
NAVY = color("#0B1F33")
TEAL = color("#007C83")
TEAL_LIGHT = color("#DCEFF0")
APRICOT = color("#FFCD8A")
PAPER = color("#FBFCFA")
MIST = color("#F2F5F7")
LINE = color("#C9D1D6")
MUTED = color("#5C6973")
ERROR = color("#B42318")
WHITE = color("#FFFFFF")

FONT = "Apple SD Gothic Neo"
FONT_MONO = "Menlo"
PT_COVER = Pt(40)
PT_TITLE = Pt(32)
PT_LEAD = Pt(27)
PT_BODY = Pt(20)
PT_DOCUMENT = Pt(20)
PT_TABLE = Pt(20)
PT_CODE = Pt(20)
PT_SMALL = Pt(17)
PT_CAPTION = Pt(12)
PT_TINY = Pt(10)
PT_SPACER = Pt(8)

ZERO = Emu(0)
LINE_THIN = Pt(1.2)
LINE_MED = Pt(2.2)
TEXT_LINE_SPACING = 1.10
BOX_LINE_SPACING = 1.05
TABLE_LINE_SPACING = 1.00
PAD = Inches(0.16)
TABLE_PAD_X = Inches(0.10)
TABLE_PAD_Y = Inches(0.08)
BOX_RADIUS = 0.06

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MX = Inches(0.62)
MY = Inches(0.5)
CW = SLIDE_W - MX * 2
GAP = Inches(0.28)
HALF_W = (CW - GAP) / 2
BODY_Y = Inches(1.63)
BODY_H = Inches(5.15)
TITLE_Y = Inches(0.52)
RULE_Y = Inches(1.26)
FOOT_Y = Inches(7.08)

# 영역 튜플은 (x, y, 너비, 높이). 모든 레이아웃은 이 토큰만 사용한다.
TITLE_AREA = (MX, TITLE_Y, CW, Inches(0.65))
RULE_W = Inches(0.92)
FOOTER_AREA = (MX, FOOT_Y, Inches(9), Inches(0.24))
PAGE_AREA = (SLIDE_W - MX - Inches(0.8), FOOT_Y, Inches(0.8), Inches(0.24))

COVER_KICKER_AREA = (MX, Inches(0.72), CW, Inches(0.38))
COVER_TITLE_AREA = (MX, Inches(1.65), CW, Inches(1.6))
COVER_SUBTITLE_AREA = (MX, Inches(3.25), CW, Inches(0.78))
COVER_DATE_AREA = (MX, Inches(5.45), CW, Inches(0.45))
COVER_AUTHOR_AREA = (MX, Inches(6.12), CW, Inches(0.5))
SECTION_KICKER_AREA = (MX, Inches(1.75), CW, Inches(0.45))
SECTION_TITLE_AREA = (MX, Inches(2.35), CW, Inches(1.05))
SECTION_SUBTITLE_AREA = (MX, Inches(3.65), CW, Inches(1.0))
STATEMENT_LEAD_AREA = (MX, Inches(2.05), CW, Inches(1.55))
STATEMENT_CAPTION_AREA = (MX, Inches(4.15), CW, Inches(1.55))
BULLETS_LEAD_AREA = (MX, BODY_Y, CW, Inches(0.65))
BULLETS_BODY_AREA = (MX, Inches(2.5), CW, Inches(4.1))

SCHEDULE_TIME_W = Inches(1.85)
SCHEDULE_MINUTES_W = Inches(0.7)
SCHEDULE_WIDTHS = [SCHEDULE_TIME_W, SCHEDULE_MINUTES_W, CW - SCHEDULE_TIME_W - SCHEDULE_MINUTES_W]
GANTT_TASK_W = Inches(5.1)
GANTT_WIDTHS = [GANTT_TASK_W] + [(CW - GANTT_TASK_W) / 4] * 4
FLOW_Y = Inches(2.4)
FLOW_H = Inches(1.35)
FLOW_ARROW_Y = Inches(2.9)
FLOW_ARROW_H = Inches(0.35)
FLOW_CAPTION_AREA = (MX, Inches(4.45), CW, Inches(1.55))
COLUMN_TITLE_Y = BODY_Y
COLUMN_TITLE_H = Inches(0.45)
COLUMN_RULE_Y = Inches(2.15)
COLUMN_BODY_Y = Inches(2.4)
COLUMN_BODY_H = Inches(4.2)

PROMPT_INSTRUCTION_AREA = (MX, BODY_Y, CW, Inches(0.55))
PROMPT_AREA = (MX, Inches(2.32), CW, Inches(4.3))
DOCUMENT_AREA = (MX + Inches(0.18), Inches(1.86), CW - Inches(0.36), Inches(4.93))
DOCUMENT_LABEL_AREA = (MX + Inches(0.18), Inches(1.43), Inches(2.25), Inches(0.33))
LABEL_PAD_X = Inches(0.08)
LABEL_PAD_Y = Inches(0.025)
SOURCE_FILE_AREA = (MX, Inches(6.86), CW, Inches(0.2))
TABLE_AREA = (MX, BODY_Y, CW, Inches(4.92))
TABLE_CAPTION_AREA = (MX, Inches(6.65), CW, Inches(0.32))

QUIZ_QUESTION_AREA = (MX, Inches(1.95), CW, Inches(1.15))
QUIZ_OPTION_Y = Inches(3.35)
QUIZ_OPTION_H = Inches(1.4)
QUIZ_ANSWER_AREA = (MX, Inches(5.4), CW, Inches(0.95))
IMAGE_AREA = (MX, Inches(1.72), CW, Inches(3.2))
IMAGE_CAPTION_AREA = (MX, Inches(5.22), CW, Inches(1.1))
PAUSE_TITLE_AREA = (MX, Inches(1.7), CW, Inches(1.1))
PAUSE_MESSAGE_AREA = (MX, Inches(3.0), CW, Inches(2.9))

# 원본 이미지의 오른쪽 인물만 보인다. 유효 종횡비로 너비를 계산한다.
PROFILE_CROP_LEFT = 0.57
PROFILE_PHOTO_X = MX
PROFILE_PHOTO_Y = BODY_Y
PROFILE_PHOTO_H = Inches(2.7)
PROFILE_NAME_AREA = (Inches(3.4), BODY_Y, Inches(9.2), Inches(0.55))
PROFILE_ROLE_AREA = (Inches(3.4), Inches(2.4), Inches(9.2), Inches(1.2))
PROFILE_BIO_AREA = (MX, Inches(4.65), CW, Inches(1.75))

PHOTO_AREA = (MX, Inches(1.7), Inches(3.6), Inches(4.9))
PHOTO_LEAD_AREA = (Inches(4.7), Inches(1.9), Inches(7.9), Inches(1.4))
PHOTO_CAPTION_AREA = (Inches(4.7), Inches(3.65), Inches(7.9), Inches(2.7))
PREVIEW_IMAGE_AREA = (Inches(0.9), Inches(1.63), Inches(3.6), Inches(5.0))
PREVIEW_LEAD_AREA = (Inches(5.0), Inches(1.85), Inches(7.4), Inches(1.25))
PREVIEW_CAPTION_AREA = (Inches(5.0), Inches(3.25), Inches(7.4), Inches(3.3))
CLOSING_TITLE_AREA = (MX, Inches(2.05), CW, Inches(1.1))
CLOSING_MESSAGE_AREA = (MX, Inches(3.45), CW, Inches(1.2))
