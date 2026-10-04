"""편집형 강의 장표 렌더러. 색·서체·간격은 theme.py에서만 관리한다."""
import os
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.parts.image import Image
from pptx.oxml.xmlchemy import OxmlElement
import theme as T

TOTAL = 0
ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))


def textbox(slide, x, y, w, h, value, size=T.BODY, color=T.INK, bold=False,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, mono=False):
    shape = slide.shapes.add_textbox(int(x), int(y), int(w), int(h))
    tf = shape.text_frame
    tf.clear(); tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for index, part in enumerate(str(value).split('\n')):
        p = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = T.BODY_LINES
        p.space_before = p.space_after = 0
        run = p.add_run(); run.text = part
        run.font.name = T.MONO if mono else (T.FONT_HEAVY if bold else T.FONT)
        run.font.size = size; run.font.bold = bold; run.font.color.rgb = color
    return shape


def _clean(shape):
    for effect in shape._element.xpath('.//a:effectRef'):
        effect.set('idx', '0')
    sp = shape._element.spPr
    for child in list(sp):
        if child.tag.endswith('}effectLst') or child.tag.endswith('}effectDag'):
            sp.remove(child)
    sp.append(OxmlElement('a:effectLst'))


def rect(slide, x, y, w, h, fill=T.SURFACE, rounded=False):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, int(x), int(y), int(w), int(h))
    if rounded: shape.adjustments[0] = T.CORNER
    shape.fill.solid(); shape.fill.fore_color.rgb = fill
    shape.line.fill.background(); _clean(shape)
    return shape


def line(slide, x, y, w, color=T.LINE, thick=T.STROKE):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                       int(x), int(y), int(x+w), int(y))
    shape.line.color.rgb = color; shape.line.width = thick; _clean(shape)


def vertical(slide, x, y, h, color=T.LINE, thick=T.STROKE):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                       int(x), int(y), int(x), int(y+h))
    shape.line.color.rgb = color; shape.line.width = thick; _clean(shape)


def base(prs, d, dark=False, title=True):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = T.INK if dark else T.PAPER
    if title:
        size = T.TITLE if len(d['title']) < 36 else T.SMALL_NUM
        textbox(s, T.MX, T.HEADER_Y, T.CW, T.HEADER_H, d['title'], size,
                T.WHITE if dark else T.INK, True)
        line(s, T.MX, T.RULE_Y, T.CW, T.GRAY_DARK if dark else T.LINE)
        rect(s, T.MX, T.RULE_Y-T.RULE_THICK/2, T.RULE_W, T.RULE_THICK,
             T.WARM if dark else T.GOOD)
    foot = T.PALE if dark else T.MUTED
    textbox(s, T.MX, T.FOOTER_Y, T.CW, T.FOOTER_H,
            d.get('phase', 'DAERYZEN · AI OFFICE'), T.CAPTION, foot)
    textbox(s, T.W-T.MX-T.RULE_W, T.FOOTER_Y, T.RULE_W, T.FOOTER_H,
            f"{d['no']:03d} / {TOTAL:03d}", T.PAGE, foot, align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = d.get('note', '')
    return s


def lead(s, d):
    if d.get('lead'):
        textbox(s, T.MX, T.LEAD_Y, T.CW, T.LEAD_H, d['lead'], T.LEAD, T.MUTED)


def bottom(s, d):
    if d.get('bottom'):
        line(s, T.MX, T.STAGE_BOTTOM+T.RULE_SPACING, T.CW)
        textbox(s, T.MX, T.STAGE_BOTTOM+T.EDITORIAL_INSET/2,
                T.CW, T.FOOTER_H*2, d['bottom'], T.CAPTION, T.MUTED)


def cover(prs, d):
    s = base(prs, d, dark=True, title=False)
    vertical(s, T.MX, T.COVER_KICKER_Y, T.COVER_META_Y-T.COVER_KICKER_Y,
             T.WARM, T.RULE_THICK)
    x = T.MX+T.EDITORIAL_INSET
    textbox(s, x, T.COVER_KICKER_Y, T.CW, T.PANEL_TITLE_H,
            'DAERYZEN  /  OFFICE WORKSHOP', T.KICKER, T.WARM, True)
    textbox(s, x, T.COVER_TITLE_Y, T.CW-T.EDITORIAL_INSET,
            T.SECTION_TITLE_Y, d['title'], T.COVER, T.WHITE, True)
    textbox(s, x, T.COVER_SUB_Y, T.CW-T.EDITORIAL_INSET,
            T.LEAD_H*2, d['lead'], T.LEAD, T.PALE)
    line(s, x, T.COVER_META_Y-T.GAP, T.CW-T.EDITORIAL_INSET, T.GRAY_DARK)
    textbox(s, x, T.COVER_META_Y, T.CW-T.EDITORIAL_INSET,
            T.LEAD_H, d.get('bottom', ''), T.BODY_SM, T.WHITE)
    return s


def section(prs, d):
    s = base(prs, d, dark=True, title=False)
    textbox(s, T.MX, T.SECTION_NO_Y, T.CW, T.PANEL_TITLE_H,
            d.get('eyebrow', ''), T.KICKER, T.WARM, True)
    line(s, T.MX, T.SECTION_TITLE_Y-T.GAP, T.CW, T.GRAY_DARK)
    textbox(s, T.MX, T.SECTION_TITLE_Y, T.CW, T.LEAD_H*3,
            d['title'], T.COVER, T.WHITE, True)
    textbox(s, T.MX, T.SECTION_SUB_Y+T.LEAD_H, T.CW, T.LEAD_H*2,
            d.get('lead', ''), T.BODY, T.PALE)
    return s


def triad(prs, d):
    s = base(prs, d); lead(s, d)
    mode = d['_composition']; items = d['cards']
    if mode == 'index':
        height = T.STAGE_H/3
        for i, (head, body) in enumerate(items):
            y = T.STAGE_Y+i*height
            line(s, T.MX, y, T.CW)
            textbox(s, T.MX, y+T.PAD, T.ROW_NUM_W, height-T.PAD,
                    f'{i+1:02d}', T.SMALL_NUM, T.GOOD, True)
            textbox(s, T.MX+T.ROW_NUM_W, y+T.PAD,
                    T.WIDE_LEFT-T.ROW_NUM_W, height-T.PAD,
                    head, T.BODY, T.INK, True, anchor=MSO_ANCHOR.MIDDLE)
            textbox(s, T.MX+T.WIDE_LEFT+T.GAP, y+T.PAD,
                    T.CW-T.WIDE_LEFT-T.GAP, height-T.PAD,
                    body, T.BODY_SM, T.MUTED, anchor=MSO_ANCHOR.MIDDLE)
    elif mode == 'columns':
        width = (T.CW-2*T.GAP)/3
        for i, (head, body) in enumerate(items):
            x = T.MX+i*(width+T.GAP)
            line(s, x, T.STAGE_Y, width,
                 T.GOOD if i == d.get('focus', -1) else T.LINE,
                 T.RULE_THICK if i == d.get('focus', -1) else T.STROKE)
            textbox(s, x, T.STAGE_Y+T.EDITORIAL_INSET,
                    width, T.LEAD_H, f'0{i+1}', T.MID_NUM, T.GOOD, True)
            textbox(s, x, T.STAGE_Y+T.LEAD_H*1.5,
                    width, T.LEAD_H*1.4, head, T.BODY, T.INK, True)
            textbox(s, x, T.STAGE_Y+T.LEAD_H*3,
                    width, T.STAGE_H-T.LEAD_H*3,
                    body, T.BODY_SM, T.MUTED)
    else:
        head, body = items[0]
        rect(s, T.MX, T.STAGE_Y, T.WIDE_LEFT, T.STAGE_H, T.NAVY)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.EDITORIAL_INSET,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET, T.LEAD_H,
                '01', T.MID_NUM, T.WARM, True)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.LEAD_H*1.6,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET, T.LEAD_H*1.5,
                head, T.BODY, T.WHITE, True)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.LEAD_H*3,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET, T.STAGE_H-T.LEAD_H*3,
                body, T.BODY_SM, T.PALE)
        x = T.MX+T.WIDE_LEFT+T.GAP; width = T.CW-T.WIDE_LEFT-T.GAP
        for i, (head, body) in enumerate(items[1:]):
            y = T.STAGE_Y+i*T.STAGE_H/2
            line(s, x, y, width)
            textbox(s, x, y+T.PAD, T.ROW_NUM_W, T.LEAD_H,
                    f'0{i+2}', T.SMALL_NUM, T.GOOD, True)
            textbox(s, x+T.ROW_NUM_W, y+T.PAD,
                    width-T.ROW_NUM_W, T.LEAD_H, head, T.BODY, T.INK, True)
            textbox(s, x+T.ROW_NUM_W, y+T.LEAD_H+T.PAD,
                    width-T.ROW_NUM_W, T.STAGE_H/2-T.LEAD_H-T.PAD,
                    body, T.BODY_SM, T.MUTED)
    bottom(s, d); return s


def compare(prs, d):
    s = base(prs, d); lead(s, d)
    mode = d['_composition']; width = (T.CW-T.GAP)/2
    if mode == 'contrast':
        rect(s, T.MX, T.STAGE_Y, width, T.STAGE_H, T.SURFACE)
        rect(s, T.MX+width+T.GAP, T.STAGE_Y, width, T.STAGE_H, T.NAVY)
    elif mode == 'parallel':
        vertical(s, T.MX+width+T.GAP/2, T.STAGE_Y, T.STAGE_H)
    for i, entry in enumerate((d['left'], d['right'])):
        x = T.MX+i*(width+T.GAP)
        if mode == 'contrast':
            x += T.EDITORIAL_INSET; w = width-2*T.EDITORIAL_INSET
            label_color = T.MUTED if i == 0 else T.WARM
            text_color = T.INK if i == 0 else T.WHITE
            textbox(s, x, T.STAGE_Y+T.EDITORIAL_INSET, w, T.LEAD_H,
                    entry[0], T.BODY, label_color, True)
            line(s, x, T.STAGE_Y+T.LEAD_H+T.EDITORIAL_INSET,
                 w, T.LINE if i == 0 else T.GRAY_DARK)
            textbox(s, x, T.STAGE_Y+T.LEAD_H*1.5+T.EDITORIAL_INSET,
                    w, T.STAGE_H-T.LEAD_H*1.5-T.EDITORIAL_INSET,
                    entry[1], T.BODY_SM, text_color)
        else:
            w = width
            if mode == 'verdict':
                line(s, x, T.STAGE_Y, w,
                     T.MUTED if i == 0 else T.GOOD, T.RULE_THICK)
                textbox(s, x, T.STAGE_Y+T.EDITORIAL_INSET, w, T.LEAD_H,
                        '비교 / 01' if i == 0 else '선택 / 02',
                        T.KICKER, T.MUTED if i == 0 else T.GOOD, True)
                y = T.STAGE_Y+T.LEAD_H*1.2
            else: y = T.STAGE_Y
            textbox(s, x, y, w, T.LEAD_H*1.6,
                    entry[0], T.SMALL_NUM,
                    T.MUTED if i == 0 else T.GOOD, True)
            line(s, x, y+T.LEAD_H*1.7, w)
            textbox(s, x, y+T.LEAD_H*2, w,
                    T.STAGE_BOTTOM-y-T.LEAD_H*2,
                    entry[1], T.BODY_SM, T.INK)
    bottom(s, d); return s


def _widths(d):
    fractions = d.get('widths') or [1/len(d['headers'])]*len(d['headers'])
    total = sum(fractions)
    return [T.CW*f/total for f in fractions]


def table(prs, d):
    s = base(prs, d); lead(s, d)
    mode = d['_composition']; widths = _widths(d)
    rows = [d['headers']]+d['rows']; row_h = T.TABLE_HEIGHT/len(rows)
    if mode == 'matrix':
        for ri, row in enumerate(rows):
            y = T.TABLE_TOP+ri*row_h
            if ri == 0:
                rect(s, T.MX, y, T.CW, row_h, T.SOFT_GREEN)
                line(s, T.MX, y, T.CW, T.GOOD, T.RULE_THICK)
            else:
                rect(s, T.MX, y, widths[0], row_h, T.SURFACE)
                line(s, T.MX, y, T.CW)
            x = T.MX
            for ci, value in enumerate(row):
                textbox(s, x+T.TABLE_PAD, y+T.TABLE_PAD,
                        widths[ci]-2*T.TABLE_PAD, row_h-2*T.TABLE_PAD,
                        value, T.TABLE_COMPACT if len(widths) >= 5 else T.TABLE,
                        T.GOOD if ri == 0 else T.INK,
                        ri == 0 or ci == 0, anchor=MSO_ANCHOR.MIDDLE)
                x += widths[ci]
        line(s, T.MX, T.TABLE_TOP+T.TABLE_HEIGHT, T.CW, T.INK)
    else:
        for ri, row in enumerate(rows):
            y = T.TABLE_TOP+ri*row_h
            if mode == 'bands' and ri > 0 and ri % 2:
                rect(s, T.MX, y, T.CW, row_h, T.SURFACE)
            if ri == 0: line(s, T.MX, y, T.CW, T.INK, T.RULE_THICK)
            elif mode == 'ledger': line(s, T.MX, y, T.CW)
            x = T.MX
            for ci, value in enumerate(row):
                size = T.TABLE_COMPACT if len(str(value)) > 46 else T.TABLE
                textbox(s, x+T.TABLE_PAD, y+T.TABLE_PAD,
                        widths[ci]-2*T.TABLE_PAD, row_h-2*T.TABLE_PAD,
                        value, T.TABLE_HEAD if ri == 0 else size,
                        T.MUTED if ri == 0 else T.INK,
                        ri == 0 or (mode == 'bands' and ci == 0),
                        anchor=MSO_ANCHOR.MIDDLE)
                x += widths[ci]
        line(s, T.MX, T.TABLE_TOP+T.TABLE_HEIGHT, T.CW,
             T.INK if mode == 'bands' else T.LINE)
    bottom(s, d); return s


def chart(prs, d):
    s = base(prs, d); lead(s, d)
    rows = d['rows']
    if d['_composition'] == 'rank':
        sorted_rows = sorted(rows, key=lambda item: item[1], reverse=True)
        first, rest = sorted_rows[0], sorted_rows[1:]
        rect(s, T.MX, T.STAGE_Y, T.WIDE_LEFT, T.STAGE_H, T.NAVY)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.EDITORIAL_INSET,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET, T.LEAD_H,
                'TOP RESPONSE', T.KICKER, T.WARM, True)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.LEAD_H,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET, T.LEAD_H*2,
                f"{first[1]}{d.get('unit', '')}", T.BIG_NUM, T.WHITE, True)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.LEAD_H*3,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET, T.STAGE_H-T.LEAD_H*3,
                first[0], T.BODY, T.PALE, True)
        x = T.MX+T.WIDE_LEFT+T.GAP; w = T.CW-T.WIDE_LEFT-T.GAP
        row_h = T.STAGE_H/max(1, len(rest))
        for i, (label, number) in enumerate(rest):
            y = T.STAGE_Y+i*row_h; line(s, x, y, w)
            textbox(s, x, y+T.PAD, w-T.ROW_NUM_W, row_h-T.PAD,
                    label, T.BODY_SM, T.INK, anchor=MSO_ANCHOR.MIDDLE)
            textbox(s, x+w-T.ROW_NUM_W, y+T.PAD, T.ROW_NUM_W,
                    row_h-T.PAD, str(number), T.BODY, T.GOOD, True,
                    align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    else:
        peak = max((number for _, number in rows), default=1) or 1
        row_h = min(T.CHART_ROW, T.STAGE_H/len(rows))
        gap = min(T.CHART_GAP, (T.STAGE_H-len(rows)*row_h)/max(1, len(rows)-1))
        for i, (label, number) in enumerate(rows):
            y = T.CHART_TOP+i*(row_h+gap)
            textbox(s, T.MX, y, T.CHART_LABEL, row_h,
                    label, T.BODY_SM, anchor=MSO_ANCHOR.MIDDLE)
            bar_x = T.MX+T.CHART_LABEL+T.GAP
            rect(s, bar_x, y+(row_h-T.CHART_BAR_H)/2,
                 T.CHART_BAR, T.CHART_BAR_H, T.PALE)
            if number:
                rect(s, bar_x, y+(row_h-T.CHART_BAR_H)/2,
                     T.CHART_BAR*number/peak, T.CHART_BAR_H,
                     T.GOOD if i == 0 else T.BLUE)
            textbox(s, bar_x+T.CHART_BAR+T.GAP, y,
                    T.CW-T.CHART_LABEL-T.CHART_BAR-2*T.GAP, row_h,
                    f"{number}{d.get('unit', '')}", T.BODY, T.INK, True,
                    anchor=MSO_ANCHOR.MIDDLE)
    bottom(s, d); return s


def process(prs, d):
    s = base(prs, d); lead(s, d)
    items = d['cards']; width = (T.CW-(len(items)-1)*T.GAP)/len(items)
    mode = d['_composition']
    if mode == 'rail':
        rail_y = T.STAGE_Y+T.LEAD_H*1.4
        line(s, T.MX, rail_y, T.CW, T.LINE, T.RULE_THICK)
    for i, (head, body) in enumerate(items):
        x = T.MX+i*(width+T.GAP)
        if mode == 'stair':
            offset = i*T.EDITORIAL_INSET/2
            line(s, x, T.STAGE_Y+offset, width, T.GOOD, T.RULE_THICK)
            textbox(s, x, T.STAGE_Y+offset+T.PAD, width, T.LEAD_H,
                    f'{i+1:02d}', T.MID_NUM, T.GOOD, True)
            y = T.STAGE_Y+offset+T.LEAD_H*1.5
        else:
            rect(s, x, rail_y-T.RULE_THICK*2,
                 T.RULE_THICK*4, T.RULE_THICK*4, T.GOOD)
            textbox(s, x, T.STAGE_Y, width, T.LEAD_H,
                    f'{i+1:02d}', T.SMALL_NUM, T.GOOD, True)
            y = rail_y+T.EDITORIAL_INSET
        textbox(s, x, y, width, T.LEAD_H*1.3, head, T.BODY, T.INK, True)
        textbox(s, x, y+T.LEAD_H*1.5, width,
                T.STAGE_BOTTOM-y-T.LEAD_H*1.5, body, T.BODY_SM, T.MUTED)
    bottom(s, d); return s


def prompt(prs, d):
    s = base(prs, d); lead(s, d)
    items = d['prompt'].split('\n')
    mode = d['_composition']
    if mode == 'source':
        row_h = min(T.PROMPT_LINE_H, T.STAGE_H/max(1, len(items)))
        for i, item in enumerate(items):
            y = T.STAGE_Y+i*row_h; line(s, T.MX, y, T.CW)
            textbox(s, T.MX, y+T.TABLE_PAD,
                    T.PROMPT_LABEL_W-T.TABLE_PAD, row_h-T.TABLE_PAD,
                    f'{i+1:02d}', T.KICKER, T.GOOD, True,
                    anchor=MSO_ANCHOR.MIDDLE)
            textbox(s, T.PROMPT_BODY_X, y+T.TABLE_PAD,
                    T.PROMPT_BODY_W, row_h-T.TABLE_PAD,
                    item, T.PROMPT_TEXT, anchor=MSO_ANCHOR.MIDDLE)
        line(s, T.MX, T.STAGE_Y+len(items)*row_h, T.CW)
    else:
        left_w = T.CW-T.WIDE_LEFT/2-T.GAP
        rect(s, T.MX, T.STAGE_Y, left_w, T.STAGE_H, T.SURFACE)
        row_h = (T.STAGE_H-2*T.EDITORIAL_INSET)/max(1, len(items))
        for i, item in enumerate(items):
            y = T.STAGE_Y+T.EDITORIAL_INSET+i*row_h
            textbox(s, T.MX+T.EDITORIAL_INSET, y,
                    left_w-2*T.EDITORIAL_INSET, row_h,
                    item, T.PROMPT_TEXT, anchor=MSO_ANCHOR.MIDDLE)
            if i < len(items)-1:
                line(s, T.MX+T.EDITORIAL_INSET, y+row_h,
                     left_w-2*T.EDITORIAL_INSET)
        x = T.MX+left_w+T.GAP; w = T.CW-left_w-T.GAP
        textbox(s, x, T.STAGE_Y, w, T.LEAD_H,
                '요청 구조', T.KICKER, T.GOOD, True)
        line(s, x, T.STAGE_Y+T.LEAD_H, w, T.GOOD, T.RULE_THICK)
        picks = items[1:4] if len(items) >= 4 else items[:3]
        for i, item in enumerate(picks):
            stripped = item.strip()
            if stripped.startswith('[') and ']' in stripped:
                label = stripped[1:stripped.index(']')]
            elif ':' in stripped and stripped.index(':') <= 12:
                label = stripped.split(':', 1)[0]
            else:
                label = stripped[:12].rstrip(' .')
            textbox(s, x, T.STAGE_Y+T.LEAD_H*1.4+i*T.LEAD_H*1.2,
                    w, T.LEAD_H, label, T.BODY, T.INK, True)
    bottom(s, d); return s


def exercise(prs, d):
    s = base(prs, d); lead(s, d)
    items = d['steps']; mode = d['_composition']
    if mode == 'worksheet':
        row_h = T.STAGE_H/4
        for i, (head, body) in enumerate(items):
            y = T.STAGE_Y+i*row_h; line(s, T.MX, y, T.CW)
            textbox(s, T.MX, y+T.PAD, T.ROW_NUM_W, row_h-T.PAD,
                    f'0{i+1}', T.SMALL_NUM, T.GOOD, True)
            textbox(s, T.MX+T.ROW_NUM_W, y+T.PAD,
                    T.WIDE_LEFT-T.ROW_NUM_W, row_h-T.PAD,
                    head, T.BODY, T.INK, True, anchor=MSO_ANCHOR.MIDDLE)
            textbox(s, T.MX+T.WIDE_LEFT+T.GAP, y+T.PAD,
                    T.CW-T.WIDE_LEFT-T.GAP, row_h-T.PAD,
                    body, T.BODY_SM, T.MUTED, anchor=MSO_ANCHOR.MIDDLE)
    elif mode == 'path':
        width = (T.CW-3*T.GAP)/4
        line(s, T.MX, T.STAGE_Y+T.LEAD_H*1.3,
             T.CW, T.LINE, T.RULE_THICK)
        for i, (head, body) in enumerate(items):
            x = T.MX+i*(width+T.GAP)
            textbox(s, x, T.STAGE_Y, width, T.LEAD_H,
                    f'{i+1:02d}', T.MID_NUM, T.GOOD, True)
            textbox(s, x, T.STAGE_Y+T.LEAD_H*1.8,
                    width, T.LEAD_H*1.2, head, T.BODY, T.INK, True)
            textbox(s, x, T.STAGE_Y+T.LEAD_H*3.1,
                    width, T.STAGE_H-T.LEAD_H*3.1,
                    body, T.BODY_SM, T.MUTED)
    else:
        width = T.CW-T.WIDE_LEFT-T.GAP
        rect(s, T.MX, T.STAGE_Y, T.WIDE_LEFT, T.STAGE_H, T.SOFT_GREEN)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.EDITORIAL_INSET,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET,
                T.LEAD_H, 'WORKSHEET', T.KICKER, T.GOOD, True)
        textbox(s, T.MX+T.EDITORIAL_INSET, T.STAGE_Y+T.LEAD_H*1.6,
                T.WIDE_LEFT-2*T.EDITORIAL_INSET,
                T.STAGE_H-T.LEAD_H*1.6,
                items[0][0]+'\n\n'+items[0][1], T.BODY, T.INK, True)
        x = T.MX+T.WIDE_LEFT+T.GAP; row_h = T.STAGE_H/3
        for i, (head, body) in enumerate(items[1:]):
            y = T.STAGE_Y+i*row_h; line(s, x, y, width)
            textbox(s, x, y+T.PAD, T.ROW_NUM_W, row_h-T.PAD,
                    f'0{i+2}', T.SMALL_NUM, T.GOOD, True)
            textbox(s, x+T.ROW_NUM_W, y+T.PAD,
                    width-T.ROW_NUM_W, T.LEAD_H, head, T.BODY, T.INK, True)
            textbox(s, x+T.ROW_NUM_W, y+T.LEAD_H+T.PAD,
                    width-T.ROW_NUM_W, row_h-T.LEAD_H-T.PAD,
                    body, T.BODY_SM, T.MUTED)
    bottom(s, d); return s


def picture_fit(s, path, x, y, w, h):
    iw, ih = Image.from_file(path).size
    scale = min(w/iw, h/ih); aw, ah = iw*scale, ih*scale
    s.shapes.add_picture(path, int(x+(w-aw)/2), int(y+(h-ah)/2),
                         width=int(aw), height=int(ah))


def image(prs, d):
    s = base(prs, d)
    path = os.path.join(ASSETS, d['path'])
    rect(s, T.MX, T.STAGE_Y, T.IMAGE_W, T.STAGE_H, T.SURFACE)
    if os.path.exists(path):
        picture_fit(s, path, T.MX+T.EDITORIAL_INSET,
                    T.STAGE_Y+T.EDITORIAL_INSET,
                    T.IMAGE_W-2*T.EDITORIAL_INSET,
                    T.STAGE_H-2*T.EDITORIAL_INSET)
    x = T.MX+T.IMAGE_W+T.GAP; w = T.CW-T.IMAGE_W-T.GAP
    line(s, x, T.STAGE_Y, w, T.GOOD, T.RULE_THICK)
    textbox(s, x, T.STAGE_Y+T.EDITORIAL_INSET, w,
            T.LEAD_H*2, d['lead'], T.LEAD, T.BLUE, True)
    textbox(s, x, T.STAGE_Y+T.LEAD_H*2.3, w,
            T.STAGE_H-T.LEAD_H*2.3, d['body'], T.BODY_SM)
    bottom(s, d); return s


def profile(prs, d):
    s = base(prs, d); lead(s, d)
    left_w = T.CW-T.PHOTO_W-T.GAP
    line(s, T.MX, T.STAGE_Y, left_w, T.GOOD, T.RULE_THICK)
    textbox(s, T.MX, T.STAGE_Y+T.EDITORIAL_INSET,
            left_w, T.STAGE_H-T.EDITORIAL_INSET, d['body'], T.BODY_SM)
    x = T.MX+left_w+T.GAP
    rect(s, x, T.STAGE_Y, T.PHOTO_W, T.PHOTO_H, T.SURFACE)
    path = os.path.join(ASSETS, d['path'])
    if os.path.exists(path): picture_fit(s, path, x, T.STAGE_Y, T.PHOTO_W, T.PHOTO_H)
    textbox(s, x, T.STAGE_Y+T.PHOTO_H+T.PAD,
            T.PHOTO_W, T.LEAD_H, 'KT 「모두의 AI」 사업 출범식', T.CAPTION, T.MUTED)
    bottom(s, d); return s


def pause(prs, d):
    s = base(prs, d, dark=True, title=False)
    line(s, T.MX, T.SECTION_TITLE_Y-T.GAP, T.CW, T.GRAY_DARK)
    textbox(s, T.MX, T.SECTION_TITLE_Y, T.CW, T.LEAD_H*2,
            d['title'], T.COVER, T.WHITE, True)
    textbox(s, T.MX, T.SECTION_SUB_Y+T.LEAD_H, T.CW, T.LEAD_H*2,
            d.get('lead', ''), T.BODY, T.PALE)
    return s


TYPES = {name: globals()[name] for name in
         'cover section triad compare chart table process prompt exercise image profile pause'.split()}
