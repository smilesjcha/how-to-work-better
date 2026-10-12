"""배포용 PDF 전 페이지 렌더 및 ZIP·민감정보 범위 검수."""
from pathlib import Path
import argparse
import json
import re
import subprocess
from zipfile import ZipFile
from pypdf import PdfReader
import pdfplumber

ROOT=Path(__file__).resolve().parents[1]

def documents():
    paths=sorted((ROOT/'materials/08-realistic-admin-case').rglob('*.pdf'))
    paths+=[ROOT/'docs/01-lecture-runbook.pdf',ROOT/'docs/10-pre-class-preparation.pdf',ROOT/'README.pdf']
    rendered=ROOT/'tmp/support-pdf-review';rendered.mkdir(parents=True,exist_ok=True)
    items=[];outside=[]
    for i,p in enumerate(paths,1):
        prefix=rendered/f'doc-{i:02d}'
        subprocess.run(['pdftoppm','-png','-r','100',str(p),str(prefix)],check=True)
        pages=len(PdfReader(p).pages)
        items.append({'number':i,'path':str(p.relative_to(ROOT)),'pages':pages,'images':[str(rendered/(prefix.name+f'-{n:0{len(str(pages))}d}.png')) for n in range(1,pages+1)]})
        with pdfplumber.open(p) as doc:
            for n,page in enumerate(doc.pages,1):
                for c in page.chars:
                    if c['x0']<15 or c['x1']>page.width-15 or c['top']<15 or c['bottom']>page.height-15:
                        outside.append({'file':str(p.relative_to(ROOT)),'page':n,'text':c['text']})
    result={'documents':items,'outside':outside}
    (rendered/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert not outside

def packages():
    for name in ['learner-practice.zip','complete-kit.zip']:
        with ZipFile(ROOT/'dist'/name) as z:
            assert z.testzip() is None
            names=z.namelist()
            assert not any('email-draft' in n or '/tmp/' in n or '/node_modules/' in n or '/case-data.json' in n for n in names)
            for n in names:
                if n.endswith(('.md','.txt','.csv','.py','.mjs')):
                    data=z.read(n).decode('utf-8')
                    assert not re.search(r'zoom\.us/j/\d{7,}',data)
                    assert not re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',data)
            print(name, '무결성 및 공개 범위 통과',len(names),'개 파일')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--packages',action='store_true');args=parser.parse_args()
    if args.packages:packages()
    else:documents()
