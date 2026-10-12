"""`slides_data.py`만 편집해 재현하는 PPTX 빌드 진입점."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pptx import Presentation
import theme as T
import layouts as L
from slides_data import SLIDES

def build():
    L.TOTAL = len(SLIDES)
    prs = Presentation(); prs.slide_width = T.SLIDE_W; prs.slide_height = T.SLIDE_H
    for no, data in enumerate(SLIDES, 1):
        data["no"] = no
        try: L.TYPE_TO_FN[data["type"]](prs, data)
        except Exception as exc: raise RuntimeError(f"slide {no}: {data.get('title')}") from exc
    output = os.path.abspath(os.path.join(HERE, "..", "output")); os.makedirs(output, exist_ok=True)
    path = os.path.join(output, "samcheok-ai-docs-workshop.pptx"); prs.save(path)
    print(f"Saved: {path} ({len(prs.slides)} slides)")
    return path
if __name__ == "__main__": build()
