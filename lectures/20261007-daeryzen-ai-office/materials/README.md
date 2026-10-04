# 수강생 실습 자료 — 가상 사례만 사용

이 패키지는 데어리젠의 실제 자료가 아닙니다. 모든 회사명·제품명·수치는 교육을 위해 만든 가상 값입니다. 실제 고객정보, 개인정보, 계약·원가·레시피·품질 이슈 원문을 외부 AI에 입력하지 마세요. 회사의 AI·정보보안 정책을 먼저 확인하세요.

## 14:00–15:30 · 실습 A

1. `01-data/sales-quality-sample.csv`를 열어 월·제품·판매 수량·반품 건수를 확인합니다.
2. `01-data/july-targets.csv`의 목표와 실적을 비교합니다.
3. `01-data/metric-guide.md`로 계산식을 확인하고 `01-data/prompts.md`의 요청을 웹 AI에 붙여 넣습니다.
4. 수치가 다르면 계산기로 확인한 뒤 `01-data/expected-summary.md`와 대조합니다.
5. 같은 값을 엑셀 형식으로 보고 싶으면 `01-data/training-data.xlsx`를 엽니다. `Summary`는 계산 결과, `Inputs`는 원자료입니다.

## 15:40–17:10 · 실습 B·C

1. `02-report/source-card.md`의 확정 사실·미확인 항목만 보고서 입력으로 사용합니다.
2. `02-report/report-prompt.md`로 1페이지 보고서 초안을 만듭니다.
3. `03-repeat/review-prompt.md`로 오류표를 만들고 `03-repeat/report-review-checklist.md`를 확인합니다.
4. `02-report/expected-report.md`는 정답 하나가 아니라 검수 기준을 보여 주는 예시입니다.

## 선택형 강사 시연

`04-agent-demo/`는 ChatGPT Desktop·Codex와 Claude Desktop·Claude Code의 폴더 기반 흐름을 강사가 보여 주기 위한 가상 프로젝트입니다. 참여자에게 앱 설치·코딩·로그인을 요구하지 않습니다.

## 파일 형식

- `.csv`: 엑셀·스프레드시트에서 열 수 있는 표. 한글이 깨지면 UTF-8로 가져오거나 본 강의 PDF 표를 사용하세요.
- `.md`: 일반 텍스트. 메모장/텍스트 편집기로 열고 프롬프트 본문을 복사하면 됩니다.

첫 결과물: 데이터 요약표. 둘째: 1페이지 보고서. 셋째: 재사용 검수 체크리스트.
