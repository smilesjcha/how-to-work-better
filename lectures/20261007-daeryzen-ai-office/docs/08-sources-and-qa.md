# 출처와 제작 검수

## 사실·방법론 출처

- 설문 수치: [2026 데어리젠 AI 실무교육 사전 설문](https://docs.google.com/forms/d/1a0wwTt0MG9j-V8PYhCowVYazVkHpqMXoKKbCpmDAumA/edit#responses), 2026-10-04 확인, n=17. 문항별 표와 해석은 `06-survey-analysis.md`.
- 프롬프트 설계·예시·평가: [OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [Anthropic Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
- 생성형 AI의 자신감 있는 오답·위험 관리: [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework).
- 간접 프롬프트 인젝션·민감정보 노출: [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [OWASP LLM02](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/).
- 데스크톱 파일 작업 개요: [ChatGPT Work with files](https://learn.chatgpt.com/docs/artifacts-viewer?surface=app), [Claude Code Desktop](https://code.claude.com/docs/en/desktop). 기능·플랜은 강의 당일 계정별로 확인한다.
- 기업 공개 정보와 교육 설계 가설: `01-company-needs.md`. 내부 프로세스·수치로 단정하지 않았다.
- 강사 경력: 강사 제공 이력 자료 및 상위 강의 프로젝트의 공개용 소개 문구를 교차 확인. 에이젠글로벌·아이넥스코퍼레이션·크레버스·무신사의 산업·역할만 표기하고 내부 성과 수치와 비공개 프로젝트는 제외했다.

## 이미지

- KT 「모두의 AI」 단체 사진: 사용자가 직접 제공한 사진. 4번 강사 소개 장표에 작게 사용했다.
- NIST AI 600-1 표지 및 목차 페이지: 공식 PDF의 1·4페이지를 장표 83·95에 이미지 캡처로 사용했다. 화면에 원문 링크를 넣었다.
- 사진 속 인물의 신원이나 기업별 역할은 확인·추정하지 않는다.
- 앱 화면은 기능·UI 변경이 잦아 정적 캡처를 추가하지 않았다. 공식 문서 링크와 강의 당일 가상 프로젝트 화면 시연을 권장한다. 후보와 이유는 `09-visual-reference-options.md`에 정리했다.

## 검수 게이트

- 2026-10-05 수정본: `python3 build_pptx/build.py` 성공, 148장 생성.
- `soffice --headless --convert-to pdf` 성공. PDF 148페이지.
- `pdftoppm`으로 전 페이지 렌더하고 8개 콘택트시트(20장씩) 눈검수.
- `qa_deck.py`: 제목 중복 0건, 슬라이드 밖 도형 0건, 연속 3장 같은 구성 0건, 수강생 불필요 문구 0건. 29개 화면 구성. 소개·93장·결과 문서/작업 기록·보고서·새 문서 예시는 확대 렌더로 확인했다.
- `python3 -m unittest discover -s build_pptx -p 'test_*.py'`: 10건 통과. 93장 자동 줄바꿈과 가변 행 높이, 전 프롬프트 본문 높이, 제작 TMI/짝 실습 제거, 사실 근거/작업 기록의 구분, 원자료-예시 수치 일치, WBS 선행 관계·일정 검증 포함.
- 화면의 시간 표기는 90분 수업 2구간과 두 휴식으로 단순화했다.
- XLSX 월별 입력 6행과 주차별 가상 원장 24행. 월별 합계·반품률·제품별 달성률·월별/주차별 차이를 수식과 독립 산식으로 대조. 차이 0건, 생성 도구 오류 검색 0건. `Summary`, `Inputs`, `Weekly detail` 세 시트를 렌더 확인.
- 실습 자료는 가상 회사·가상 수치만 사용. 설문 자유서술 원문, 응답자 신원, 실제 기업 데이터는 배포 파일에 없다.
- `05-document-forms/`: 요약표·WBS/Gantt·2pager·PRD·대시보드의 재사용 예시와 요청문 추가. WBS의 역할·일정, 제안서의 인수 목표는 관측 사실과 구별했다. PRD는 필수 열 누락·0·미승인 등 예외를 정의했다.
- 보고서 본문의 수정 과정·AI 요청 이력을 제거하고, 근거표·검수 질문·수정 이력은 작업 기록으로 보존하는 기준을 배포 프롬프트와 체크리스트에도 반영했다. 필요한 사업 결정 이유와 승인 기록은 삭제 대상이 아니다.
- 기존 시간 구조 유지, 모든 실습은 개별 수행. 도구 비교는 제외하고 가능한 도구 하나로 폴더 시연.

## 제약

- 실제 회사의 외부 AI 허용·접근 권한은 본 제작 과정에서 확인되지 않았다. 강의 당일에도 가상 자료만 사용한다.
- PDF 렌더는 이 컴퓨터의 서체 환경을 기준으로 한다. 현장 PC는 PDF를 비상본으로 준비한다.
- Microsoft PowerPoint 앱에서 직접 연 최종 검수는 하지 않았다. LibreOffice PDF 렌더와 PPTX 구조 검사 기준으로 완료했다.
- 148장 전체를 동일한 속도로 설명하는 덱이 아니다. 실습 진행·정답 공개·선택 심화 장표가 포함돼 있고, 새 문서 양식은 청중과 속도에 맞춰 선택한다. 강사용 운영 메모에 생략 분기를 적었다.
