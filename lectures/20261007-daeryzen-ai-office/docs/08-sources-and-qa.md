# 출처와 제작 검수

## 사실·방법론 출처

- 설문 수치: [2026 데어리젠 AI 실무교육 사전 설문](https://docs.google.com/forms/d/1a0wwTt0MG9j-V8PYhCowVYazVkHpqMXoKKbCpmDAumA/edit#responses), 2026-10-04 확인, n=17. 문항별 표와 해석은 `06-survey-analysis.md`.
- 프롬프트 설계·예시·평가: [OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [Anthropic Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
- 생성형 AI의 자신감 있는 오답·위험 관리: [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework).
- 간접 프롬프트 인젝션·민감정보 노출: [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [OWASP LLM02](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/).
- 데스크톱 파일 작업 개요: [ChatGPT Work with files](https://learn.chatgpt.com/docs/artifacts-viewer?surface=app), [Claude Code Desktop](https://code.claude.com/docs/en/desktop). 기능·플랜은 강의 당일 계정별로 확인한다.
- 기업 공개 정보와 교육 설계 가설: `01-company-needs.md`. 내부 프로세스·수치로 단정하지 않았다.

## 이미지

- KT 「모두의 AI」 단체 사진: 사용자가 직접 제공한 사진. 4번 강사 소개 장표에 작게 사용했다.
- NIST AI 600-1 표지 및 목차 페이지: 공식 PDF의 1·4페이지를 장표 83·95에 이미지 캡처로 사용했다. 화면에 원문 링크를 넣었다.
- 사진 속 인물의 신원이나 기업별 역할은 확인·추정하지 않는다.

## 검수 게이트

- `python3 build_pptx/build.py` 성공, 140장 생성.
- `soffice --headless --convert-to pdf` 성공. PDF 140페이지.
- `pdftoppm`으로 전 페이지 렌더하고 7개 콘택트시트(20장씩) 눈검수.
- `qa_deck.py`: 제목 중복 0건, 슬라이드 밖 도형 0건. 구간별 시간표는 `02-curriculum.md`와 `slide-plan.md`가 일치.
- XLSX 입력 6행, 월별 합계·반품률·제품별 달성률을 수식과 독립 산식으로 대조. 생성 도구 오류 검색 0건. `Summary`, `Inputs` 두 시트를 렌더 확인.
- 실습 자료는 가상 회사·가상 수치만 사용. 설문 자유서술 원문, 응답자 신원, 실제 기업 데이터는 배포 파일에 없다.

## 제약

- 실제 회사의 외부 AI 허용·접근 권한은 본 제작 과정에서 확인되지 않았다. 강의 당일에도 가상 자료만 사용한다.
- PDF 렌더는 이 컴퓨터의 서체 환경을 기준으로 한다. 현장 PC는 PDF를 비상본으로 준비한다.
- 140장 전체를 동일한 속도로 설명하는 덱이 아니다. 실습 진행·정답 공개·선택 심화 장표가 포함돼 있고, 강사용 운영 메모에 생략 분기를 적었다.
