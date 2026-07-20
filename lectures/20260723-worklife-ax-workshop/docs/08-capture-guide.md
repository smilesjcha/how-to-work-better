# 08. 스크린샷 캡처 가이드 (사용자 직접 준비)

캡처 파일을 `assets/screenshots/`에 **지정 파일명 그대로** 저장한 뒤
`python3 build_pptx/build.py`를 실행하면 해당 슬라이드에 자동 삽입됩니다.
(파일이 없으면 슬라이드에 회색 자리표시가 나타납니다 — 강의 전 채워야 할 목록이 곧 이 표입니다.)

## 공통 캡처 규칙

- 브라우저 창 크기 약 **1280×800**, 배율 100% (슬라이드 비율 16:9와 잘 맞음)
- 개인정보 노출 주의: 프로필 사진·이메일 주소가 화면 우상단에 보이면 잘라내거나 가리기
- macOS: `Cmd+Shift+4` → 영역 지정 (창 단위는 `Cmd+Shift+4` 후 Space)
- 파일 형식: PNG 권장

## A. Claude 무료 계정 화면 (별도 Gmail의 Chrome 프로필에서) — 6장

> 실습 ①·② 프롬프트는 `dist/WORK-LIFE-practice-kit.zip`의 실습 폴더에 있는 것을 그대로 사용하세요.
> 그래야 캡처 결과와 수강생 결과가 일치합니다.

| # | 파일명 | 캡처 내용 | 포함할 요소 |
| --- | --- | --- | --- |
| 1 | `free_01_signup.png` | claude.ai 로그아웃 상태 첫 화면 | 'Google로 계속하기' 버튼 |
| 2 | `free_02_new_chat.png` | 로그인 직후 새 대화 화면 | 입력창, 새 대화 버튼 |
| 3 | `free_03_meeting_result.png` | 실습 ① 프롬프트 전송 후 결과 | 액션아이템 표 + '확인 필요' 표시 부분 |
| 4 | `free_04_markdown_table.png` | Markdown 표를 Notion에 붙여넣은 화면 | Notion 페이지에 렌더된 표 (Claude 창과 나란히면 최고) |
| 5 | `free_05_report_result.png` | 실습 ② 보고서 결과 | 대응안 비교표 + 이메일 버전 시작 부분 |
| 6 | `free_06_usage_limit.png` | 무료 사용량 제한 안내 메시지 | 재설정 시각 표시 (제한에 걸렸을 때만 캡처 가능 — 실습 테스트 중 만나면 바로 캡처) |

## B. 유료·시연 화면 (강사 계정) — 5장 (시연 실패 대비 백업 겸용)

| # | 파일명 | 캡처 내용 |
| --- | --- | --- |
| 7 | `paid_01_excel.png` | Claude for Excel — `excel_demo_sample.csv` 열고 요약·계산 열 추가된 화면 |
| 8 | `paid_02_ppt.png` | Claude for PowerPoint — 브리프에서 구성안 생성된 화면 |
| 9 | `paid_03_word.png` | Claude for Word — `word_demo_draft.txt` 초안 다듬는 화면 |
| 10 | `paid_04_mcp.png` | Claude 설정 → 커넥터 목록 화면 |
| 11 | `paid_05_skills.png` | Skills 목록 또는 실행 화면 |

## 캡처 후 반영 절차

```bash
# 1) 파일을 assets/screenshots/ 에 저장 (파일명 그대로)
# 2) 재빌드
python3 build_pptx/build.py
# 3) PDF 갱신 (선택)
cd output && soffice --headless --convert-to pdf worklife-ax-workshop.pptx
```

Claude Code에게 "스크린샷 넣었으니 재빌드하고 검수해줘"라고 요청해도 됩니다.

## 우선순위 (시간이 없을 때)

1. **필수**: 3, 5 (실습 결과 — 수강생이 자기 결과와 비교하는 기준)
2. **강력 권장**: 1, 2 (초심자 2명 온보딩), 7~11 (시연 실패 백업)
3. **여유 시**: 4, 6
