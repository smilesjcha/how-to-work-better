# 2026 청년 여성 밸런스 워크숍 — Codex 작업 지침 (AGENTS.md)

- 강의: 「AI 시대의 업무 경쟁력과 생산성 향상」 / 2026-07-23(목) 13:00–17:00 온라인
- 레포 공통 규칙: `../../docs/harness/common-guidelines.md` 우선 적용

## 파일 소유권 (수정 대상 매핑)

| 바꾸고 싶은 것 | 수정할 파일 |
| --- | --- |
| 강의 내용·시간표 | `docs/02-curriculum.md` |
| 슬라이드 구성·순서 | `design/slide-plan.md` → `build_pptx/slides_data.py` |
| 색상·폰트·간격 | `build_pptx/theme.py` (+ `design/ppt-design-system.md` 동기화) |
| 레이아웃 종류 | `build_pptx/layouts.py` |
| 실습 자료 | `materials/ai-work-competency-workshop/` |

## 빌드·검증

```bash
python3 build_pptx/build.py                     # PPT 생성 → output/
cd output && soffice --headless --convert-to pdf *.pptx && pdftoppm -jpeg -r 100 *.pdf slide
cd materials && zip -r ../dist/WORK-LIFE-practice-kit.zip ai-work-competency-workshop -x "*.DS_Store"
```

## 금지 사항

- PPTX 파일 직접 편집(항상 코드에서 재생성)
- 디자인 토큰 외 색상 사용, 참여자 실습 개수 확대, 실제 개인정보 포함
- `output/`·`dist/` 산출물을 빌드 없이 수동 수정
