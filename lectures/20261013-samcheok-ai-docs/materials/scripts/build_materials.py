#!/usr/bin/env python3
"""학습용 Markdown을 같은 위치의 읽기용 PDF로 만든다."""

from __future__ import annotations

import os
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    PageBreak,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

MATERIALS = Path(__file__).resolve().parents[1]
FONT = Path(os.environ.get("KOREAN_FONT", "/Users/sungjae-cha/Library/Fonts/NanumGothic.ttf"))
if not FONT.exists():
    FONT = Path("/System/Library/Fonts/Supplemental/NotoSansGothic-Regular.ttf")

pdfmetrics.registerFont(TTFont("Korean", str(FONT)))


def esc(text: str) -> str:
    """ReportLab Paragraph에서 안전하게 보이도록 최소한의 HTML을 처리한다."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r'<link href="\2" color="#246B72">\1</link>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # 프롬프트의 인라인 코드에는 한국어가 많으므로 영문 고정폭 글꼴로 바꾸지 않는다.
    text = re.sub(r"`(.+?)`", r"<font name='Korean'>\1</font>", text)
    return text


def styles(compact: bool):
    base = getSampleStyleSheet()
    body_size = 8.0 if compact else 9.5
    leading = 10.7 if compact else 14.0
    return {
        "title": ParagraphStyle(
            "KTitle", parent=base["Title"], fontName="Korean", fontSize=16 if compact else 19,
            leading=20 if compact else 23, spaceAfter=7 if compact else 8,
            textColor=colors.HexColor("#163A5F"), alignment=TA_LEFT,
        ),
        "h2": ParagraphStyle(
            "KH2", parent=base["Heading2"], fontName="Korean", fontSize=10.5 if compact else 12.5,
            leading=13 if compact else 15, spaceBefore=6 if compact else 8, spaceAfter=3 if compact else 4,
            textColor=colors.HexColor("#163A5F"), keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "KH3", parent=base["Heading3"], fontName="Korean", fontSize=9 if compact else 10.5,
            leading=11.5 if compact else 13, spaceBefore=4 if compact else 5, spaceAfter=2,
            textColor=colors.HexColor("#246B72"), keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "KBody", parent=base["BodyText"], fontName="Korean", fontSize=body_size,
            leading=leading, spaceAfter=3.5 if compact else 5, allowWidows=0, allowOrphans=0,
        ),
        "header": ParagraphStyle(
            "KHeader", parent=base["BodyText"], fontName="Korean", fontSize=body_size,
            leading=leading, textColor=colors.white,
        ),
        "code": ParagraphStyle(
            "KCode", parent=base["Code"], fontName="Korean", fontSize=7.3 if compact else 8,
            leading=10.2 if compact else 11.5, leftIndent=6, rightIndent=6,
            backColor=colors.HexColor("#F2F5F7"), borderColor=colors.HexColor("#D8E0E5"),
            borderWidth=0.5, borderPadding=5, spaceBefore=8, spaceAfter=8,
        ),
        "footer": ParagraphStyle(
            "KFooter", parent=base["BodyText"], fontName="Korean", fontSize=7.2,
            leading=9, textColor=colors.HexColor("#607080"),
        ),
    }


def table_flow(lines: list[str], sty: dict, compact: bool):
    cells = []
    for line in lines:
        parts = [x.strip() for x in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", part) for part in parts):
            continue
        cell_style = sty["header"] if not cells else sty["body"]
        cells.append([Paragraph(esc(part), cell_style) for part in parts])
    if not cells:
        return Spacer(1, 1)
    ncols = max(len(row) for row in cells)
    for row in cells:
        row.extend([Paragraph("", sty["body"])] * (ncols - len(row)))
    usable = A4[0] - 32 * mm
    widths = [usable / ncols] * ncols
    table = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Korean"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.6 if compact else 8.4),
        ("LEADING", (0, 0), (-1, -1), 10.5 if compact else 12),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163A5F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5DD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def markdown_to_story(path: Path):
    compact = "one-page" in path.stem or "revised-under-600" in path.stem or path.name == "plan-prompt.md"
    sty = styles(compact)
    story = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    in_code = False
    code_lines: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            if in_code:
                story.append(Paragraph("<br/>".join(esc(x) for x in code_lines) or " ", sty["code"]))
                code_lines = []
            in_code = not in_code
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if line.startswith("|"):
            group = []
            while i < len(lines) and lines[i].startswith("|"):
                group.append(lines[i])
                i += 1
            story.append(table_flow(group, sty, compact))
            continue
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(esc(line[2:]), sty["title"]))
        elif line.startswith("## "):
            story.append(Paragraph(esc(line[3:]), sty["h2"]))
        elif line.startswith("### "):
            story.append(Paragraph(esc(line[4:]), sty["h3"]))
        elif re.match(r"^[-*] ", line):
            bullet = Paragraph(esc(line[2:]), sty["body"])
            story.append(ListFlowable([ListItem(bullet)], bulletType="bullet", leftIndent=14, bulletFontName="Korean"))
        elif re.match(r"^\d+\. ", line):
            text = re.sub(r"^\d+\. ", "", line)
            story.append(Paragraph(esc(text), sty["body"], bulletText="•"))
        else:
            story.append(Paragraph(esc(line), sty["body"]))
        i += 1
    return story


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Korean", 7)
    canvas.setFillColor(colors.HexColor("#607080"))
    canvas.drawRightString(A4[0] - 16 * mm, 12 * mm, f"생성형 AI 실무 문서 실습 · {doc.page}")
    canvas.restoreState()


def build(path: Path):
    out = path.with_suffix(".pdf")
    compact = "one-page" in path.stem or "revised-under-600" in path.stem or path.name == "plan-prompt.md"
    margins = (13 if compact else 16) * mm
    doc = SimpleDocTemplate(
        str(out), pagesize=A4, leftMargin=margins, rightMargin=margins,
        # 긴 제목은 글꼴의 상단이 잘리지 않도록 일반 문서에 여유를 둔다.
        topMargin=(12 if compact else 22) * mm, bottomMargin=18 * mm,
        title=path.stem, author="교육용 가상 실습 자료",
    )
    doc.build(markdown_to_story(path), onFirstPage=page_number, onLaterPages=page_number)
    print(out.relative_to(MATERIALS))


if __name__ == "__main__":
    for source in sorted(MATERIALS.rglob("*.md")):
        build(source)
