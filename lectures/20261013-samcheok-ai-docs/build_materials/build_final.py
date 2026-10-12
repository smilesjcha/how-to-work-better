#!/usr/bin/env python3
"""현재 강의의 자료·PPT·PDF·배포 ZIP만 재현하는 최종 빌더."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'materials/08-realistic-admin-case'
DEMO=ROOT/'materials/09-instructor-demo'
DECK='samcheok-ai-docs-workshop'

def run(*cmd):
    print('실행:', ' '.join(map(str,cmd)),flush=True)
    subprocess.run(list(map(str,cmd)),cwd=ROOT,check=True)

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.strip()+'\n',encoding='utf-8')

def documents():
    moddata=runpy.run_path(str(ROOT/'build_pptx/slides_data.py'))
    blocks,slides=moddata['BLOCKS'],moddata['SLIDES']
    rows='\n'.join(f"| {b['start']}-{b['end']} | {b['title']} |" for b in blocks)
    write(ROOT/'docs/01-lecture-runbook.md',f'''# 10월 13일 강사 운영표
2026년 10월 13일 화요일 14:00-17:00. 무료 웹 기본 실습이다. 강의 80분, 휴식 10분, 강의 70분, 휴식·선택 Q&A 20분이다. 모든 운영 구간은 10분이다.

| 시간 | 내용 |
| --- | --- |
{rows}

## 운영 기준
자료는 가상 기관의 충분한 원자료를 제공한다. 수강생은 실습 전용 ZIP을 풀고 핵심 사실, 요청문, WBS TXT, 오류문서 TXT를 복사한다. 웹 계정 하나만 있으면 기본 실습을 진행할 수 있다. 업로드는 선택 사항이다. 로그인, 설치, 코딩이 필요한 강사 시연은 16:30-16:40에만 진행한다.

## 진행과 완료 확인
14:40-14:50 보고서 생성, 14:50-15:00 수치 검수, 15:10-15:20 기획서 생성을 진행한다. 15:20에 결과를 저장하고 15:30에 다시 시작한다. 15:40-16:00 WBS와 일정 영향, 16:00-16:10 오류 검수, 16:10-16:20 최종본과 안내메일, 16:20-16:30 저장과 재사용을 확인한다.

보고서·기획서·검수표·안내메일, 확인한 숫자 3개, 남은 질문 1개를 결과로 남긴다. AI 첫 응답과 최종본은 구분한다. 특정 모델이 참고답안과 같은 문장을 출력한다고 약속하지 않는다.

## 한도와 접속 장애
현재 결과를 먼저 저장한다. 사용 가능한 다른 웹 계정은 선택적으로 쓰되, 한도를 우회하기 위해 계정을 늘리지 않는다. 접속과 사용량이 막히면 참고답안과 검수표로 직접 수정하여 동일한 결과물을 완성한다. 실습당 필수 생성 요청을 줄이고 반복 요청 대신 사람의 독립 검수를 강조한다.

## 16시 30분 관찰 시연
실습 폴더를 강사의 Claude Desktop 또는 ChatGPT Desktop/Codex에서 연다. 공통 지침과 개별 요청의 차이, 같은 원자료에서 보고서와 기획서를 만드는 방식, WBS 변경과 Gantt 연결, PPT·PDF 재생성, 버전 저장을 보여준다. 실시간 작업이 느리면 준비된 결과를 바로 연다. 학생에게 유료 계정이나 설치를 요구하지 않는다.

## 휴식과 Q&A
16:40 이후에는 새 필수 학습을 진행하지 않는다. 두 개의 10분 구간은 연속된 20분 휴식과 선택 질문 시간이다. 17:00에 종료한다.
''')
    notes='# 슬라이드별 강사 메모\n\n개별 장표의 시간은 추가 배정이 아니라 공유하는 10분 블록이다.\n\n'
    for i,s in enumerate(slides,1):
        notes+=f"## {i:02d} {s['title'].replace(chr(10),' ')}\n\n{s['note'].replace(chr(10), chr(10)+chr(10))}\n\n"
    write(ROOT/'docs/06-slide-instructor-notes.md',notes)
    write(ROOT/'docs/10-pre-class-preparation.md','''# 참여자 준비 안내
ChatGPT 또는 Claude 중 하나의 무료 웹 계정을 만들고 로그인 상태를 확인한다. 기본 실습은 웹에서 진행한다. 데스크톱 앱 설치, 유료 결제, GitHub 가입, 코딩은 필요하지 않다. 별도 문서를 준비할 필요가 없으며 강의에서 가상 실습 자료를 제공한다. 강사의 데스크톱 활용은 마지막 관찰 시연이다.
''')
    write(ROOT/'README.md',f'''# 삼척새일센터 생성형 AI 실무 문서 작성 강의
2026년 10월 13일 화요일 14:00-17:00 / 강사 차성재 / 최종 개정 2026-10-12

무료 웹에서 보고서와 실행 기획서를 만들고, WBS·Gantt·검수표·안내메일로 연결하는 강의다. 마지막 10분은 강사의 데스크톱 활용 사례 관찰이다.

## 바로 내려받기
- [실습 전용 ZIP](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/learner-practice.zip): 수강생은 이 파일 하나만 내려받는다.
- [전체 강의 패키지 ZIP](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/complete-kit.zip): PPTX, PDF, 강사 운영표, 실습, 시연 폴더와 빌드 원본.
- [PPTX](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/{DECK}.pptx)
- [PDF](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/{DECK}.pdf)
- [최종 배포 릴리스](https://github.com/smilesjcha/how-to-work-better/releases/tag/samcheok-ai-docs-20261013)

## 180분 운영
| 시간 | 내용 |
| --- | --- |
| 14:00-15:20 | 강의와 무료 웹 실습 80분 |
| 15:20-15:30 | 휴식 10분 |
| 15:30-16:40 | 강의와 실습 70분, 마지막 10분 강사 시연 |
| 16:40-17:00 | 연속 휴식과 선택 Q&A 20분 |

상세 운영표는 docs/01-lecture-runbook.md이며 모든 시간은 10분 단위다.

## 충분한 가상 원자료
등록 360행, 상담 1,440행, 설문 320행, 집행 60행, 기업 연계 36행, WBS 24행. 총 2,240행을 연결한다. 예산, 회의록, 운영 메모, 기획 초안과 오류 문서를 함께 제공한다. 모든 자료는 가상이며 실제 개인정보와 기업 내부정보는 없다.

무료 실습은 materials/08-realistic-admin-case의 핵심 TXT를 복사한다. 큰 파일 업로드와 코딩을 요구하지 않는다. 한도에 도달하면 참고답안과 검수표로 최종본을 완성한다. 워크북은 8개 시트의 원자료·집계·WBS·Gantt 수식을 연결한다.

## ZIP과 clone
처음 참여자는 실습 ZIP을 압축 해제한다. 전체 GitHub 저장소가 필요하면 저장소의 Code / Download ZIP을 쓴다. 이력과 변경 비교가 필요한 강사·운영자는 `git clone https://github.com/smilesjcha/how-to-work-better.git` 후 이 강의 폴더를 연다. clone과 GitHub 가입은 학생 필수 준비가 아니다.

## 재생성
Python은 python-pptx, reportlab, pypdf, pdfplumber가 필요하며 LibreOffice와 Poppler를 사용한다. XLSX는 Codex 번들 Node.js의 @oai/artifact-tool로 생성한다.
1. `python3 build_materials/build_case.py`
2. `node build_materials/build_admin_workbook.mjs`
3. `python3 build_materials/build_final.py --build-only`
4. 렌더 검수 후 `python3 build_materials/build_final.py --package-only`

PPT 내용은 build_pptx/slides_data.py, 디자인 값은 build_pptx/theme.py에서 관리한다. 원문 이메일, Zoom 참가 정보, 강사 행정서류와 임시 파일은 공개 패키지에서 제외한다.
''')
    write(DEMO/'README.md','''# 강사 관찰 시연 폴더
16:30-16:40에 강사의 현재 계정으로 보여주는 자료다. 학생 실습에 설치와 결제를 요구하지 않는다. inputs의 사실과 WBS, context의 지표 정의, templates의 서식, outputs의 검수된 결과를 연결한다.

Claude Desktop의 Code와 ChatGPT Desktop/Codex에서 폴더를 선택한 뒤 demo-prompt.txt를 사용한다. 기능 접근과 사용량은 현재 계정에서 확인한다. 실시간 생성이 느리면 prepared-results의 실제 결과 예시와 강의 PPT·PDF 원본을 연다. 이 자료는 두 서비스에서 실측한 응답 기록이라고 표시하지 않는다.
''')
    rules='''문서는 한국어로 쓴다. 입력은 교육용 가상자료만 사용한다. 원본과 출처를 보존한다. 등록·수료·취업·상담의 분모와 단위를 유지한다. 원인·목표·승인 상태를 임의로 만들지 않는다. 가정과 확인 필요를 구분한다. 결과는 outputs, 초안은 work, 승인·변경 이유는 decisions에 저장한다. 외부 발송이나 게시를 자동 실행하지 않는다. 최종 완료 기준은 숫자·근거·담당·일정·완료 기준·결정 요청이다.'''
    write(DEMO/'context/common-rules.md','# 공통 규칙\n\n'+rules)
    for name in ['AGENTS.md','CLAUDE.md']:
        write(DEMO/name,'# 가상 행정문서 시연 지침\n\ncontext/common-rules.md를 읽고 inputs의 원자료와 templates의 서식을 사용한다.\n\n'+rules)
    write(DEMO/'templates/document-template.md','''# 결과 문서 서식
제목 / 수신자 / 기간 / 버전

현황과 비교 / 근거 / 확인 필요 / 담당과 일정 / 완료 기준 / 승인 요청

숫자 검수 기록 / 변경 이유 / 남은 질문
''')
    write(DEMO/'demo-prompt.txt','''공통 규칙과 inputs의 가상자료를 읽어 주세요.
같은 근거로 월간 보고서와 4주 기획서를 outputs에 작성합니다.
WBS를 검토하고 T08 지연의 영향을 별도 기록으로 남깁니다.
원본을 유지하고 가정과 확인 필요를 표시합니다.
완료 기준으로 수치와 선행관계를 검수하고 변경한 파일을 보고합니다.
외부 발송과 게시 단계는 담당자가 별도로 결정합니다.
''')
    for rel in ['inputs','outputs','work','decisions','archive','prepared-results']:
        (DEMO/rel).mkdir(parents=True,exist_ok=True)
    for rel,label in [('outputs','검수한 최종 결과'),('work','중간 초안'),('decisions','승인과 변경 이유'),('archive','이전 버전')]:
        write(DEMO/rel/'README.md',f'# {label}\n\n이 폴더에 {label}를 저장한다. 교육용 가상자료만 사용한다.')
    shutil.copy2(CASE/'01-facts-to-paste.txt',DEMO/'inputs/facts.txt')
    shutil.copy2(CASE/'data/wbs.csv',DEMO/'inputs/wbs.csv')
    for name in ['report-example.md','plan-example.md']:
        shutil.copy2(CASE/'answers'/name,DEMO/'prepared-results'/name)

def pdf_module():
    spec=importlib.util.spec_from_file_location('material_pdf',ROOT/'materials/scripts/build_materials.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.MATERIALS=ROOT
    return module

def build():
    documents()
    module=pdf_module()
    sources=list(CASE.rglob('*.md'))+[ROOT/'README.md',ROOT/'docs/01-lecture-runbook.md',ROOT/'docs/10-pre-class-preparation.md']
    for p in sources: module.build(p)
    previews=ROOT/'assets/previews';previews.mkdir(parents=True,exist_ok=True)
    for filename,pdf in [('report-final',CASE/'answers/report-example.pdf'),('plan-final',CASE/'answers/plan-example.pdf')]:
        run('pdftoppm','-f','1','-singlefile','-png','-r','150',pdf,previews/filename)
    shutil.copy2(ROOT/'tmp/workbook-review/sheet-2.png',previews/'gantt-final.png')
    run(sys.executable,ROOT/'build_pptx/build.py')
    conversion=ROOT/'tmp/final-conversion';conversion.mkdir(parents=True,exist_ok=True)
    run('soffice',f'-env:UserInstallation={(conversion/"profile").as_uri()}','--headless','--convert-to','pdf','--outdir',conversion,ROOT/f'output/{DECK}.pptx')
    shutil.copy2(conversion/f'{DECK}.pdf',ROOT/f'output/{DECK}.pdf')
    rendered=ROOT/'tmp/final-render-20261012';rendered.mkdir(parents=True,exist_ok=True)
    run('pdftoppm','-png','-r','110',ROOT/f'output/{DECK}.pdf',rendered/'slide')

def public_files():
    files=[ROOT/'README.md']
    for folder in [CASE,DEMO]:
        files+=list(folder.rglob('*'))
    files += [ROOT/'assets/profile_photo.jpg']+list((ROOT/'assets/previews').glob('*-final.png'))
    for rel in ['docs/01-lecture-runbook.md','docs/01-lecture-runbook.pdf','docs/06-slide-instructor-notes.md','docs/10-pre-class-preparation.md','docs/10-pre-class-preparation.pdf','docs/13-final-delivery-plan.md','docs/14-current-product-sources.md','docs/15-final-qa-report.md','design/ppt-design-system.md','design/slide-plan.md','materials/scripts/build_materials.py']:
        files.append(ROOT/rel)
    files+=[ROOT/'build_pptx'/name for name in ['build.py','slides_data.py','theme.py','layouts.py','qa_deck.py']]
    files+=list((ROOT/'build_materials').glob('*.py'))+list((ROOT/'build_materials').glob('*.mjs'))
    files+=[ROOT/f'output/{DECK}.pptx',ROOT/f'output/{DECK}.pdf']
    return sorted(set(p for p in files if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and p.name!='case-data.json' and not p.name.endswith('.inspect.ndjson')))

def pack():
    from pptx import Presentation
    from pypdf import PdfReader
    data=runpy.run_path(str(ROOT/'build_pptx/slides_data.py'))
    assert len(Presentation(ROOT/f'output/{DECK}.pptx').slides)==len(PdfReader(ROOT/f'output/{DECK}.pdf').pages)==len(data['SLIDES'])
    assert len(data['BLOCKS'])==18 and sum(b['minutes'] for b in data['BLOCKS'])==180
    assert sum(s['minutes'] for s in data['SLIDES'])==180
    assert all(int(b['start'].split(':')[1])%10==0 and int(b['end'].split(':')[1])%10==0 for b in data['BLOCKS'])
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    core=[p for p in CASE.rglob('*') if p.is_file() and p.name!='case-data.json' and not p.name.endswith('.inspect.ndjson')]
    with ZipFile(dist/'learner-practice.zip','w',ZIP_DEFLATED) as z:
        for p in sorted(core): z.write(p,'samcheok-practice/'+str(p.relative_to(CASE)))
    files=public_files()
    with ZipFile(dist/'complete-kit.zip','w',ZIP_DEFLATED) as z:
        for p in files:z.write(p,'samcheok-complete-kit/'+str(p.relative_to(ROOT)))
        z.write(dist/'learner-practice.zip','samcheok-complete-kit/dist/learner-practice.zip')
    manifest=files+[dist/'learner-practice.zip',dist/'complete-kit.zip']
    write(ROOT/'tmp/publish-files.txt','\n'.join(str(p.relative_to(ROOT.parent.parent)) for p in manifest))
    facts=json.loads((CASE/'data/case-data.json').read_text(encoding='utf-8'))
    receipt={'slides':len(data['SLIDES']),'minutes':180,'blocks':data['BLOCKS'],'records':facts['record_counts'],'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in manifest}}
    write(ROOT/'output/release-validation.json',json.dumps(receipt,ensure_ascii=False,indent=2))
    print(json.dumps({'slides':len(data['SLIDES']),'core_files':len(core),'published_files':len(manifest),'zip_bytes':{p.name:p.stat().st_size for p in dist.glob('*.zip')}},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--build-only',action='store_true');parser.add_argument('--package-only',action='store_true');args=parser.parse_args()
    if not args.package_only:build()
    if not args.build_only:pack()
