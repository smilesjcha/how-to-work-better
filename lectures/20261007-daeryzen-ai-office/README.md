# 2026 데어리젠 AI 실무교육

2026-10-07 14:00–17:30, 사무직 대상. 교육 주제는 **데이터에서 보고서까지**입니다. 2026-10-04 기준 Google Forms 응답 17건을 분석해 148장 장표와 가상 실습 자료를 구성했습니다.

## 바로 사용할 파일

- 발표: `output/daeryzen-ai-office-20261007.pptx`
- 인쇄·검토: `output/daeryzen-ai-office-20261007.pdf`
- 수강생 배포: `dist/daeryzen-practice-kit.zip`
- 전체 묶음: `dist/daeryzen-complete-kit.zip`
- 운영: `docs/07-facilitator-runbook.md`
- 설문 분석: `docs/06-survey-analysis.md`

## 운영 구조

14:00–15:30 수업, 15:30–15:40 휴식, 15:40–17:10 수업, 17:10–17:30 휴식 겸 Q&A·개별 상담입니다. 실습은 1인 개별 수행이며 수강생 필수 경로는 웹 브라우저·복사/붙여넣기입니다. 장비가 없으면 개인 인쇄물에 계산·기입합니다. Codex 또는 Claude Code의 파일·폴더 작업은 강사 선택 시연이며 도구 비교는 진행하지 않습니다.

`materials/05-document-forms/`에는 데이터 요약표, WBS·Gantt, 임원 제안서 2pager, PRD, 대시보드 정의와 작성 프롬프트가 있습니다. 1페이지 보고서는 `materials/02-report/`를 재사용합니다. PPT에는 편집 가능한 완성 예시가 포함됩니다. 최종 보고서와 AI 작성·수정 기록을 구분하는 내용은 114–116장에 반영했습니다.

## 재생성

```bash
python3 lectures/20261007-daeryzen-ai-office/build_pptx/build.py
```

내용은 `build_pptx/slides_data.py`, 구성 선택은 `build_pptx/composition.py`, 디자인 토큰은 `build_pptx/theme.py`와 `design/ppt-design-system.md`에서 관리합니다. 공통 제작 기준은 [`docs/harness/ppt-production-playbook.md`](../../docs/harness/ppt-production-playbook.md)에 있습니다. 실습 데이터는 가상 회사 「한빛유업」의 교육용 수치입니다. 실제 개인정보·고객정보·회사 내부정보를 입력하지 마세요.

심화 실습용 `materials/01-data/weekly-ops-sample.csv`는 월별 요약과 합계가 일치하는 24행 가상 운영 원장입니다. PPT의 작업 흐름은 편집 가능한 도형으로 구성했고, 대응 Mermaid 원문은 `design/`에 있습니다.
