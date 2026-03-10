# AIdol Sprint 4 - API 요구사항

## 1. 피드 콘텐츠 목록 조회 API (신규)

> `GET /aidol-feeds` — **신규 API**

| 항목        | 필드명         | 타입                 | 설명                            |
| ----------- | -------------- | -------------------- | ------------------------------- |
| 피드 ID     | `id`           | `string`             | 피드 고유 식별자                |
| 그룹 ID     | `aidolId`      | `string`             | 소속 AIdol 그룹 ID              |
| 미디어 타입 | `mediaType`    | `"IMAGE" \| "VIDEO"` | 콘텐츠 유형                     |
| 미디어 URL  | `mediaUrl`     | `string`             | 이미지 또는 영상 URL            |
| 썸네일 URL  | `thumbnailUrl` | `string \| null`     | 썸네일 이미지 URL (영상의 경우) |
| 생성일시    | `createdAt`    | `string (ISO 8601)`  | 업로드 일시                     |

- **사용처**: MyGroup 피드 탭, OtherGroup 피드 탭
- **필터 파라미터**: 공통 `filters` 쿼리 파라미터로 aidolId 필터링
