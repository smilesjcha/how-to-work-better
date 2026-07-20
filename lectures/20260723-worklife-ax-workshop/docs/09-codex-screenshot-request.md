# 09. Codex 요청 프롬프트 (복사해서 사용)

아래 프롬프트를 Codex에 그대로 붙여넣으면 됩니다.
(전제: business.sjcha@gmail.com 무료 Claude 계정이 로그인된 Chrome과 연동된 Codex)

---

```
레포: https://github.com/smilesjcha/how-to-work-better
작업 폴더: lectures/20260723-worklife-ax-workshop/

이 강의 PPT에 스크린샷을 캡처해서 삽입해줘. 작업 규칙은 해당 폴더의 AGENTS.md
"스크린샷 캡처·삽입 워크플로우" 섹션과 docs/08-capture-guide.md를 따라.

순서:

1. 브라우저에서 claude.ai에 접속해 (현재 로그인된 무료 계정 사용)
   아래 화면을 캡처해서 assets/screenshots/에 지정 파일명으로 저장해줘.

   - free_02_new_chat.png — 새 대화 시작 화면 (입력창 보이게)
   - free_03_meeting_result.png — 실습 ① 결과:
     materials/ai-work-competency-workshop/01_free_practice_meeting_summary/의
     prompt_meeting_summary.md 프롬프트 + sample_meeting_note.txt 내용을
     그대로 전송한 뒤, 액션아이템 표와 '확인 필요' 표시가 보이는 결과 화면
   - free_05_report_result.png — 실습 ② 결과:
     02_free_practice_report_email/의 prompt_report_email.md +
     sample_work_situation.txt를 그대로 전송한 뒤,
     대응안 비교와 이메일 버전이 보이는 결과 화면
   - free_01_signup.png — (가능하면) 로그아웃 상태 또는 시크릿 창의
     claude.ai 로그인 화면 ('Google로 계속하기' 버튼 보이게)
   - free_04_markdown_table.png — (가능하면) 실습 ① 결과의 Markdown 표를
     Notion에 붙여넣은 화면

2. 캡처 공통 규칙: 창 크기 약 1280×800, 우상단 이메일·프로필 노출 금지(잘라내기), PNG.

3. 저장 후 python3 build_pptx/build.py 실행 → 이미지가 자동 삽입돼.
   slides_data.py는 수정하지 마.

4. output/에서 PDF 재생성 후 shot 슬라이드들(design/slide-plan.md의 shot 행 번호 참조)을
   렌더링해서 잘림·저해상도·개인정보 노출이 없는지 확인하고 결과를 보고해줘.

5. assets/screenshots/NEEDED.md 체크박스 갱신 후 커밋해줘.
   (push는 smilesjcha 계정 확인 후 — docs/harness/common-guidelines.md 참조)
```

---

## 참고

- 유료 시연 캡처 5장(paid_01~05)은 유료 계정 환경이 필요하므로 이 요청과 별도로 진행.
- free_06_usage_limit.png(사용량 제한 화면)은 제한에 걸렸을 때만 캡처 가능 —
  실습 테스트 중 만나면 그때 캡처해서 같은 방식으로 저장하면 된다.
- Codex 작업 후 Claude Code에서 "스크린샷 삽입 상태 검수해줘"라고 하면
  교차 검수를 수행한다.
