# meetings

모든 미팅록을 이 폴더에 보관합니다.

## 파일명 규칙

```
YYMMDD-slug.md
```

- `YYMMDD`: 미팅 날짜 (예: 260309)
- `slug`: 영문 kebab-case, 참석자 + 주제 (예: `jay-soyeon-design-marketing-ir`)
- **한글/특수문자 금지** (GitHub 브랜치명 호환)

### 예시
- `260309-jay-soyeon-design-marketing-ir.md`
- `260307-phase2-team-meeting.md`
- `260303-sunjin-sprint2-ut.md`

## 자동 생성

Fireflies.ai 녹음 완료 → GitHub Actions → Claude 요약 → PR 자동 생성
(`.github/scripts/fireflies-to-note.js` 참고)
