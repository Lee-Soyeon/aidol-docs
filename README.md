# AIdol Docs

AIdol 프로젝트 문서 저장소입니다.

## 📁 폴더 구조

```
aidol-docs/
├── 01_research/          # 사용자 리서치, 시장 분석, UT 가이드
├── 02_planning/          # PRD, 기능 명세서
├── 03_design/            # 브랜딩, UI 컴포넌트
├── 04_development/       # API 스펙, ERD, 아키텍처
├── 05_ai-llm/            # 프롬프트, 실험 결과
├── 06_ir-master/         # IR 자료 (투자 관련)
├── 07_tools/             # 개발 도구, 에이전트
└── meetings/             # 미팅록 (Fireflies 자동 + 수동)
```

## 파일명 규칙

```
kebab-case-topic.md
```

- 문서 주제를 kebab-case로 작성
- 날짜, 버전, 작성자 등의 메타데이터는 파일명에 포함하지 않음
- 이력 관리는 Git 히스토리를 활용
- **미팅록**: `YYMMDD-slug.md` (예: `260309-jay-soyeon-design-ir.md`)
- **사용자 인터뷰 원본**: `sprint<N>-<user-id>-raw.md` (예: `sprint1-u3-jangsophie-raw.md`)
- **한글/특수문자는 파일명과 브랜치명에서 금지** (GitHub 호환)

### 예시

- `user-interview-kpop-fans.md`
- `aidol-api-spec.md`
- `brand-guidelines.md`
- `260309-jay-soyeon-design-ir.md` (미팅록)

## 관련 저장소

- [algorima/aidol](https://github.com/algorima/aidol) - 메인 코드
- [algorima/docs](https://github.com/algorima/docs) - Company Handbook (비공개)
