"""평면·편집형 PPT 레이아웃. 모든 시각 값은 theme.py에서 가져온다."""
import os
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.parts.image import Image
from pptx.oxml.xmlchemy import OxmlElement
import theme as T

TOTAL = 0
ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))

def font(run, size=T.BODY, color=T.INK, bold=False, mono=False):
    run.font.name = T.MONO if mono else T.FONT
    run.font.size = size
    run.font.bold = bold
    run.font.color.rgb = color

def textbox(slide, x, y, w, h, value, size=T.BODY, color=T.INK, bold=False,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, mono=False):
    shape = slide.shapes.add_textbox(int(x), int(y), int(w), int(h))
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for idx, line in enumerate(str(value).split('\n')):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = T.BODY_LINES
        p.space_before = p.space_after = 0
        r = p.add_run()
        r.text = line
        font(r, size, color, bold, mono)
    return shape

def clean_effects(shape):
    for effect in shape._element.xpath('.//a:effectRef'):
        effect.set('idx', '0')
    sp = shape._element.spPr
    for child in list(sp):
        if child.tag.endswith('}effectLst') or child.tag.endswith('}effectDag'):
            sp.remove(child)
    sp.append(OxmlElement('a:effectLst'))

def rect(slide, x, y, w, h, fill=T.WHITE, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(x), int(y), int(w), int(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = T.STROKE
    clean_effects(s)
    return s

def line(slide, x, y, w, color=T.LINE, weight=T.STROKE):
    s = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, int(x), int(y), int(x+w), int(y))
    s.line.color.rgb = color
    s.line.width = weight
    clean_effects(s)

def panel(slide, x, y, w, h, heading, body, highlight=False):
    rect(slide, x, y, w, h, T.PALE if highlight else T.WHITE, T.BLUE if highlight else T.LINE)
    textbox(slide, x+T.PAD, y+T.PAD, w-2*T.PAD, T.PANEL_TITLE_H, heading, T.BODY, T.BLUE if highlight else T.INK, True)
    line(slide, x+T.PAD, y+T.PANEL_TITLE_H+T.PAD, w-2*T.PAD)
    textbox(slide, x+T.PAD, y+T.PANEL_TITLE_H+2*T.PAD, w-2*T.PAD, h-T.PANEL_TITLE_H-3*T.PAD,
            body, T.BODY_SM, anchor=MSO_ANCHOR.MIDDLE)

def slide_base(prs, d, dark=False):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = T.NAVY if dark else T.WHITE
    if not dark:
        textbox(s, T.MX, T.HEADER_Y, T.CW, T.HEADER_H, d['title'], T.TITLE, T.INK, True)
        line(s, T.MX, T.RULE_Y, T.RULE_W, T.BLUE, T.RULE_THICK)
    footer_color = T.PALE if dark else T.MUTED
    textbox(s, T.MX, T.FOOTER_Y, T.CW, T.FOOTER_H,
            d.get('phase', '데어리젠 AI 실무교육'), T.CAPTION, footer_color)
    textbox(s, T.W-T.MX-T.RULE_W, T.FOOTER_Y, T.RULE_W, T.FOOTER_H,
            f"{d['no']:03d} / {TOTAL:03d}", T.PAGE, footer_color, align=PP_ALIGN.RIGHT)
    note = s.notes_slide.notes_text_frame
    note.text = d.get('note', '')
    return s

def put_lead(s, d):
    textbox(s, T.MX, T.LEAD_Y, T.CW, T.LEAD_H, d.get('lead', ''), T.LEAD, T.BLUE, True)

def put_bottom(s, d):
    if d.get('bottom'):
        textbox(s, T.MX, T.BOTTOM_Y, T.CW, T.FOOTER_H, d['bottom'], T.CAPTION, T.MUTED)

def cover(prs, d):
    s = slide_base(prs, d, True)
    textbox(s, T.MX, T.COVER_KICKER_Y, T.CW, T.PANEL_TITLE_H, '데어리젠 AI 실무교육 · 2026.10.07', T.BODY, T.WARM, True)
    textbox(s, T.MX, T.COVER_TITLE_Y, T.CW, T.SECTION_TITLE_Y, d['title'], T.COVER, T.WHITE, True)
    textbox(s, T.MX, T.COVER_SUB_Y, T.CW, T.LEAD_H*2, d['lead'], T.LEAD, T.PALE)
    line(s, T.MX, T.COVER_META_Y-T.GAP, T.CW, T.WARM, T.RULE_THICK)
    textbox(s, T.MX, T.COVER_META_Y, T.CW, T.LEAD_H, d['bottom'], T.BODY_SM, T.WHITE)
    return s

def section(prs, d):
    s = slide_base(prs, d, True)
    textbox(s, T.MX, T.SECTION_NO_Y, T.CW, T.PANEL_TITLE_H, d.get('eyebrow', ''), T.BODY, T.WARM, True)
    textbox(s, T.MX, T.SECTION_TITLE_Y, T.CW, T.LEAD_H*2, d['title'], T.COVER, T.WHITE, True)
    textbox(s, T.MX, T.SECTION_SUB_Y+T.LEAD_H, T.CW, T.LEAD_H*2, d['lead'], T.BODY, T.PALE)
    return s

def triad(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    for i, (heading, body) in enumerate(d['cards']):
        x = T.MX+i*(T.THIRD_W+T.GAP)
        panel(s, x, T.BLOCK_Y, T.THIRD_W, T.BLOCK_H, heading, body, i==d.get('focus', -1))
    put_bottom(s, d)
    return s

def compare(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    panel(s, T.MX, T.BLOCK_Y, T.COL_W, T.BLOCK_H, d['left'][0], d['left'][1], False)
    panel(s, T.MX+T.COL_W+T.GAP, T.BLOCK_Y, T.COL_W, T.BLOCK_H, d['right'][0], d['right'][1], True)
    put_bottom(s, d)
    return s

def chart(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    rows = d['rows']
    peak = max((n for _, n in rows), default=1)
    for i, (label, number) in enumerate(rows):
        y = T.CHART_START_Y+i*(T.CHART_ROW_H+T.CHART_ROW_GAP)
        textbox(s, T.MX, y, T.CHART_LABEL_W, T.CHART_ROW_H, label, T.BODY_SM)
        rect(s, T.MX+T.CHART_LABEL_W, y+T.GAP/2, T.CHART_BAR_W, T.CHART_BAR_H, T.SURFACE)
        if number:
            rect(s, T.MX+T.CHART_LABEL_W, y+T.GAP/2, T.CHART_BAR_W*number/peak, T.CHART_BAR_H, T.BLUE)
        textbox(s, T.MX+T.CHART_LABEL_W+T.CHART_BAR_W+T.GAP, y, T.CHART_NUM_W, T.CHART_ROW_H,
                f"{number}{d.get('unit', '')}", T.BODY, T.INK, True)
    put_bottom(s, d)
    return s

def table(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    rows = [d['headers']] + d['rows']
    cols = len(d['headers'])
    grid = s.shapes.add_table(len(rows), cols, int(T.MX), int(T.TABLE_Y), int(T.CW), int(T.TABLE_H)).table
    if d.get('widths'):
        for col, fraction in zip(grid.columns, d['widths']):
            col.width = int(T.CW*fraction)
    for ri, row in enumerate(rows):
        for ci, value in enumerate(row):
            cell = grid.cell(ri, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = T.NAVY if ri==0 else (T.SURFACE if ri%2 else T.WHITE)
            tf = cell.text_frame
            tf.clear()
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = tf.margin_right = T.TABLE_PAD
            tf.margin_top = tf.margin_bottom = T.TABLE_PAD
            for j, part in enumerate(str(value).split('\n')):
                p = tf.paragraphs[0] if j==0 else tf.add_paragraph()
                p.space_before = p.space_after = 0
                r = p.add_run(); r.text = part
                font(r, T.TABLE, T.WHITE if ri==0 else T.INK, ri==0)
    put_bottom(s, d)
    return s

def process(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    cards = d['cards']
    width = (T.CW-(len(cards)-1)*T.GAP)/len(cards)
    for i, (head, body) in enumerate(cards):
        x = T.MX+i*(width+T.GAP)
        panel(s, x, T.BLOCK_Y, width, T.BLOCK_H, f'{i+1:02d}  {head}', body, i==d.get('focus', -1))
        if i < len(cards)-1:
            arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                       int(x+width), int(T.BLOCK_Y+T.BLOCK_H/2-T.ARROW_H/2),
                                       int(T.GAP), int(T.ARROW_H))
            arrow.fill.solid(); arrow.fill.fore_color.rgb = T.BLUE
            arrow.line.fill.background(); clean_effects(arrow)
    put_bottom(s, d)
    return s

def prompt(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    rect(s, T.MX, T.PROMPT_Y, T.CW, T.PROMPT_H, T.SURFACE, T.LINE)
    textbox(s, T.MX+T.PAD, T.PROMPT_Y+T.PAD, T.CW-2*T.PAD, T.PROMPT_H-2*T.PAD,
            d['prompt'], T.BODY_SM, T.INK, mono=False)
    textbox(s, T.MX, T.PROMPT_FOOT_Y, T.CW, T.PANEL_TITLE_H, d.get('bottom', ''), T.CAPTION, T.MUTED)
    return s

def exercise(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    for i, (head, body) in enumerate(d['steps']):
        row, col = divmod(i, 2)
        x = T.MX+col*(T.COL_W+T.GAP)
        y = T.EXERCISE_TOP_Y+row*(T.EXERCISE_ROW_H+T.EXERCISE_ROW_GAP)
        panel(s, x, y, T.COL_W, T.EXERCISE_ROW_H, head, body, i==d.get('focus', -1))
    put_bottom(s, d)
    return s

def picture_fit(s, path, x, y, w, h):
    iw, ih = Image.from_file(path).size
    scale = min(w/iw, h/ih)
    aw, ah = iw*scale, ih*scale
    s.shapes.add_picture(path, int(x+(w-aw)/2), int(y+(h-ah)/2), width=int(aw), height=int(ah))

def image(prs, d):
    s = slide_base(prs, d)
    path = os.path.join(ASSETS, d['path'])
    if os.path.exists(path):
        picture_fit(s, path, T.IMAGE_X, T.IMAGE_Y, T.IMAGE_W, T.IMAGE_H)
    textbox(s, T.IMAGE_TEXT_X, T.IMAGE_Y, T.IMAGE_TEXT_W, T.LEAD_H*2, d['lead'], T.LEAD, T.BLUE, True)
    textbox(s, T.IMAGE_TEXT_X, T.IMAGE_Y+T.LEAD_H*2+T.GAP, T.IMAGE_TEXT_W,
            T.IMAGE_TEXT_H-T.LEAD_H*2-T.GAP, d['body'], T.BODY)
    put_bottom(s, d)
    return s

def profile(prs, d):
    s = slide_base(prs, d)
    put_lead(s, d)
    textbox(s, T.MX, T.BLOCK_Y, T.CW-T.SMALL_PHOTO_W-T.GAP, T.BLOCK_H,
            d['body'], T.BODY)
    path = os.path.join(ASSETS, d['path'])
    if os.path.exists(path):
        picture_fit(s, path, T.SMALL_PHOTO_X, T.SMALL_PHOTO_Y, T.SMALL_PHOTO_W, T.SMALL_PHOTO_H)
    put_bottom(s, d)
    return s

def pause(prs, d):
    s = slide_base(prs, d, True)
    textbox(s, T.MX, T.SECTION_TITLE_Y, T.CW, T.LEAD_H*2, d['title'], T.COVER, T.WHITE, True, PP_ALIGN.CENTER)
    textbox(s, T.MX, T.SECTION_SUB_Y+T.LEAD_H, T.CW, T.LEAD_H*2, d['lead'], T.BODY, T.PALE, align=PP_ALIGN.CENTER)
    return s

TYPES = {name: globals()[name] for name in 'cover section triad compare chart table process prompt exercise image profile pause'.split()}
