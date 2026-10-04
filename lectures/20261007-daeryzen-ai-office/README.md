# 2026 데어리젠 AI 실무교육

2026-10-07 14:00–17:30, 사무직 대상. 교육 주제는 **표에서 근거를 찾고 AI로 보고서까지 완성하는 일**입니다. 2026-10-04 기준 Google Forms 응답 17건을 분석해 140장 장표와 가상 실습 자료를 구성했습니다.

## 바로 사용할 파일

- 발표: `output/daeryzen-ai-office-20261007.pptx`
- 인쇄·검토: `output/daeryzen-ai-office-20261007.pdf`
- 수강생 배포: `dist/daeryzen-practice-kit.zip`
- 전체 묶음: `dist/daeryzen-complete-kit.zip`
- 운영: `docs/07-facilitator-runbook.md`
- 설문 분석: `docs/06-survey-analysis.md`

## 운영 구조

14:00–15:30 수업, 15:30–15:40 휴식, 15:40–17:10 수업, 17:10–17:30 휴식 겸 Q&A·개별 상담입니다. 수강생 필수 경로는 웹 브라우저·복사/붙여넣기입니다. Codex와 Claude Code의 파일·폴더 작업은 강사 선택 시연입니다.

## 재생성

```bash
python3 lectures/20261007-daeryzen-ai-office/build_pptx/build.py
```

내용은 `build_pptx/slides_data.py`, 디자인 토큰은 `build_pptx/theme.py`와 `design/ppt-design-system.md`에서 관리합니다. 실습 데이터는 가상 회사 「한빛유업」의 교육용 수치입니다. 실제 개인정보·고객정보·회사 내부정보를 입력하지 마세요.
