# 강사 전용 폴더 시연 — 가상 데이터만

이 폴더는 ChatGPT Desktop의 Codex와 Claude Desktop의 Claude Code에서 같은 요청 구조를 보여 주기 위한 예시입니다. 계정·플랜·앱 설치는 수강생 필수 조건이 아닙니다.

```text
04-agent-demo/
├── context/       # 목적·계산 기준·금지 행동
├── inputs/        # 이번 회차 가상 CSV
├── work/          # 계산 메모·초안 검수
├── outputs/       # 사람이 확인할 최종 초안
├── decisions/     # 사람의 승인·변경 이유
└── archive/       # 지난 회차 보관
```

시연 전 `demo-prompt.md`를 읽고 파일 변경 범위를 `work/`, `outputs/`로 제한합니다. 원본 `inputs/`는 덮어쓰지 않습니다. 실무 도입 전에 회사 보안정책·앱 권한을 확인합니다.
