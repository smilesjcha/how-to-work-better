# 삼척새일센터 생성형 AI 실무 문서 작성 강의
2026년 10월 13일 화요일 14:00-17:00 / 강사 차성재 / 최종 개정 2026-10-12

무료 웹에서 보고서와 실행 기획서를 만들고, WBS·Gantt·검수표·안내메일로 연결하는 강의다. 마지막 10분은 강사의 데스크톱 활용 사례 관찰이다.

## 바로 내려받기
- [실습 전용 ZIP](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/learner-practice.zip): 수강생은 이 파일 하나만 내려받는다.
- [전체 강의 패키지 ZIP](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/complete-kit.zip): PPTX, PDF, 강사 운영표, 실습, 시연 폴더와 빌드 원본.
- [PPTX](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/samcheok-ai-docs-workshop.pptx)
- [PDF](https://github.com/smilesjcha/how-to-work-better/releases/download/samcheok-ai-docs-20261013/samcheok-ai-docs-workshop.pdf)
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
