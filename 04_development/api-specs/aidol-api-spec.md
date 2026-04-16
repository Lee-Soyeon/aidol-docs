# AIdol API Specification

- 원본: [Notion](https://www.notion.so/2f046f965504805ca766fd5d0850b3e7)
- Base URL: `http://localhost:8000` (로컬)

---

## API 분류 기준

- `Domain`: 특정 도메인의 정식 계약입니다. 단일 도메인 책임에 가깝고, 다른 클라이언트에서도 재사용 가능한 API를 의미합니다.
- `BFF`: 화면/플로우 최적화용 API입니다. 여러 도메인 데이터를 조합하거나 외부 연동을 오케스트레이션하여 프론트엔드 친화적인 응답 형태를 제공합니다.

---

## 전체 엔드포인트

| 엔드포인트                                          | 메서드 | 설명                        | 도메인       | 계층   | 인증   | Sprint |
| --------------------------------------------------- | ------ | --------------------------- | ------------ | ------ | ------ | ------ |
| `/aidols`                                           | POST   | AIdol 그룹 생성             | AIdol        | Domain | Cookie | 1      |
| `/aidols`                                           | GET    | 아이돌 그룹 전체 조회       | AIdol        | Domain | Public | 2      |
| `/me/aidols`                                        | GET    | 사용자 아이돌 그룹 조회     | AIdol        | Domain | Cookie | 2      |
| `/aidols/{id}`                                      | GET    | AIdol 그룹 조회             | AIdol        | Domain | Public | 1      |
| `/aidols/{id}`                                      | PATCH  | AIdol 그룹 수정             | AIdol        | Domain | Public | 1      |
| `/aidols/images`                                    | POST   | AIdol 이미지 생성           | AIdol        | BFF    | Public | 1      |
| `/groups/featured`                                  | GET    | 피처드 그룹 카드 조회       | AIdol Group  | BFF    | Public | -      |
| `/companions`                                       | GET    | Companion 목록 조회         | Companion    | Domain | Public | 1      |
| `/companions`                                       | POST   | Companion 멤버 생성         | Companion    | Domain | Public | 1      |
| `/companions/{id}`                                  | GET    | Companion 멤버 조회         | Companion    | Domain | Public | 2      |
| `/companions/{id}`                                  | PATCH  | Companion 멤버 수정         | Companion    | Domain | Public | 1      |
| `/companions/{id}`                                  | DELETE | Companion 멤버 삭제         | Companion    | Domain | Public | 1      |
| `/companions/images`                                | POST   | Companion 프로필 이미지 생성 | Companion    | Domain | Public | 1      |
| `/leads`                                            | POST   | email 수집                  | Lead         | Domain | Public | 1      |
| `/aidol-highlights`                                 | GET    | 아이돌 하이라이트 조회      | Highlight    | Domain | Public | 2      |
| `/aidol-highlights/{id}/messages`                   | GET    | 하이라이트 메세지 조회      | Highlight    | Domain | Public | 2      |
| `/aidol-feeds`                                      | GET    | 피드 콘텐츠 목록 조회       | Feed         | Domain | Public | 4      |
| `/companions/{id}/credits/free`                     | GET    | 무료 연습 크레딧 조회       | Credit       | Domain | Cookie | 6      |
| `/me/credits/charge`                                | GET    | 충전 크레딧 조회            | Credit       | Domain | Cookie | 6      |
| `/me/credits/recharge`                              | POST   | 충전 크레딧 지급            | Credit       | Domain | Cookie | 5      |
| `/companions/{id}/practices`                        | POST   | 연습 생성                   | Practice     | BFF    | Cookie | 6      |
| `/me/collectibles`                                  | GET    | 컬렉터블 목록 조회          | Collectible  | Domain | Cookie | 6      |
| `/me/collectibles/{id}`                             | GET    | 컬렉터블 상세 조회          | Collectible  | Domain | Cookie | 6      |
| `/me/collectibles/{id}`                             | DELETE | 컬렉터블 삭제               | Collectible  | Domain | Cookie | 6      |
| `/companions/{id}/collectibles`                     | GET    | 공개 컬렉터블 목록 조회     | Collectible  | Domain | Public | 6      |
| `/companions/{id}/collectibles/{collectibleId}`     | GET    | 공개 컬렉터블 상세 조회     | Collectible  | Domain | Public | 6      |
| `/companion-relationships`                          | GET    | 아이돌 관계 조회            | Relationship | Domain | Public | 2      |
| `/companion-relationships/{id}`                     | GET    | 아이돌 관계 조회            | Relationship | Domain | Public | 2      |
| `/companion-relationships`                          | POST   | 아이돌 관계성 생성          | Relationship | Domain | Public | 2      |
| `/companion-relationships/{id}`                     | DELETE | 아이돌 관계 삭제            | Relationship | Domain | Public | 2      |
| `/chatrooms`                                        | POST   | 채팅방 생성                 | Chatroom     | Domain | Cookie | 3      |
| `/me/chatrooms`                                     | GET    | 채팅방 목록 조회            | Chatroom     | BFF    | Cookie | 3      |
| `/chatrooms/{id}`                                   | GET    | 채팅방 조회                 | Chatroom     | Domain | Public | 3      |
| `/chatrooms/{id}/messages`                          | GET    | 메시지 목록 조회            | Message      | Domain | Public | 3      |
| `/chatrooms/{id}/messages`                          | POST   | 메시지 전송                 | Message      | Domain | Cookie | 3      |
| `/chatrooms/{id}/companions/{cid}/response`         | POST   | AI 응답 생성                | Chat AI      | BFF    | Public | 3      |
| `/chatrooms/{id}/companions/{cid}/initial-response` | POST   | 선 발화 AI 응답 생성        | Chat AI      | BFF    | Public | 3      |

---

## 세부 명세

List 조회 API의 `current`, `pageSize`, `sort`, `filters` 규칙은 문서 하단 `## 🔧 List Query Parameters`를 공통으로 따릅니다.
- `current`: 페이지 번호 (기본: 1, ≥ 1)
- `pageSize`: 페이지당 항목 수 (기본: 10, 1-100)
- `sort`: 정렬 조건 
- `filters`: 필터 조건 

### POST /aidols - AIdol 그룹 생성

새로운 아이돌 그룹을 생성합니다. 생성된 그룹은 요청자의 쿠키 ID (anonymousId)와 연결됩니다.

- URL: POST /aidols
- Domain: AIdol
- Layer: Domain
- Auth: 쿠키 필수 (anonymousId)

**Request**:

```json
{
  "name": "string (선택)",
  "email": "string (선택)",
  "greeting": "string (선택)",
  "concept": "string (선택)",
  "profileImageUrl": "string (선택)"
}
```

**Response** (201 Created):

```json

{
  "data": {
    "id": "string"
  }
}
```

---

### GET /aidols - 아이돌 그룹 전체 조회

생성된 모든 아이돌 그룹을 조회합니다. 페이지네이션과 필터링을 지원합니다.

- URL: GET /aidols
- Domain: AIdol
- Layer: Domain
- Auth: 공개

Query Parameters (공통 List 규칙)

- `current`, `pageSize`, `sort`, `filters`
- 예시: `?current=1&pageSize=10&sort=[["createdAt","desc"]]&filters=[{"field":"name","operator":"contains","value":"aidol"}]`

**Response** (200 OK):

```json
{
  "data": [
    {
	    "id": "string",
	    "name": "string",
	    "email": "string",
	    "concept": "string",
	    "greeting": "string",
	    "profileImageUrl": "string",
      "status": "DRAFT | PUBLISHED",
      "createdAt": "datetime",
      "updatedAt": "datetime"
		 },
    {
	    "id": "string",
	    "name": "string",
	    "email": "string",
	    "concept": "string",
	    "greeting": "string",
	    "profileImageUrl": "string",
      "status": "DRAFT | PUBLISHED",
      "createdAt": "datetime",
      "updatedAt": "datetime"
		 },
  ],
  "total": 2
}
```

---

### GET /me/aidols - 사용자가 만든 그룹 전체 조회

현재 사용자(쿠키 ID 기준)가 생성한 그룹만 필터링하여 조회합니다.

- URL: GET /me/aidols
- Domain: AIdol
- Layer: Domain
- Auth: 쿠키 필수 (`aioia_anonymous_id`)

Query Parameters (공통 List 규칙)

- `current`, `pageSize`, `sort`, `filters`
- 추가 조건: 현재 사용자 소유 데이터만 조회되도록 서버에서 자동 필터링

**Response** (200 OK):

```json
{
  "data": [
    {
	    "id": "string",
	    "name": "string",
	    "email": "string",
	    "concept": "string",
	    "greeting": "string",
	    "profileImageUrl": "string",
      "status": "DRAFT | PUBLISHED",
      "createdAt": "datetime",
      "updatedAt": "datetime"
		 },
    {
	    "id": "string",
	    "name": "string",
	    "email": "string",
	    "concept": "string",
	    "greeting": "string",
	    "profileImageUrl": "string",
      "status": "DRAFT | PUBLISHED",
      "createdAt": "datetime",
      "updatedAt": "datetime"
		 },
  ],
  "total": 2
}

```

---

### GET /aidols/{id} - AIdol 그룹 조회

특정 그룹의 상세 정보를 조회합니다.

- URL: GET /aidols/{id}
- Domain: AIdol
- Layer: Domain
- Auth: Public

**Response** (200 OK):

```json
{
  "data": {
    "id": "string",
    "name": "string",
    "email": "string",
    "greeting": "string",
    "concept": "string",
    "profileImageUrl": "string",
    "status": "DRAFT | PUBLISHED",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
}
```

**Errors**:

- `404` - AIdol 그룹 없음

---

### PATCH /aidols/{id} - AIdols 그룹 수정

그룹 생성 과정에서 정보를 업데이트 합니다.

- URL: PATCH /aidols/{id}
- Domain: AIdol
- Layer: Domain
- Auth: 공개 (추후 소유권 검증 로직 추가 예정)

**Request**:

```json
{
  "name": "string (선택)",
  "email": "string (선택)",
  "greeting": "string (선택)",
  "concept": "string (선택)",
  "profileImageUrl": "string (선택)",
  "status": "DRAFT | PUBLISHED (선택)"
}

```

**Response** (200 OK):

```json
{
  "data": {
    "id": "string",
    "name": "string",
    "email": "string",
    "greeting": "string",
    "concept": "string",
    "profileImageUrl": "string",
    "status": "DRAFT | PUBLISHED",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
}
```

**Errors**:

- `404` - AIdol 그룹 없음

---

### POST /aidols/images - 이미지 생성

aidols 엠블럼 이미지를 생성합니다.

- URL: POST /aidols/images
- Domain: AIdol
- Layer: BFF
- Auth: 공개

**Request**:

```json
{
  "prompt": "5인 그룹 검정색 배경 엠블럼.."
}

```

**Response** (201 Created):

```json
{
  "data": {
    "imageUrl": "string",
    "width": 1024,
    "height": 1024,
    "format": "png"
  }
}
```

**Errors**:

- `422` - prompt 길이 초과 (max 200자)
- `500` - 이미지 생성 실패

---

### GET /groups/featured - 피처드 그룹 카드 조회

홈/탐색 화면에서 사용하는 피처드 그룹 카드 목록을 커서 기반으로 조회합니다. 각 카드에는 최신 무료 하이라이트와 공개 멤버 수가 함께 포함됩니다.

- URL: GET /groups/featured
- Domain: AIdol Group
- Layer: BFF
- Auth: 공개

Query Parameters

- `cursor` (optional): 다음 페이지 조회용 opaque cursor
- `pageSize` (optional): 페이지 크기 (기본 20, 1~100)

동작 규칙:

- `PUBLISHED` 상태의 그룹만 포함됩니다.
- `memberCount`는 `PUBLISHED` 상태 멤버만 집계합니다.
- `highlight`는 그룹별 최신 무료 하이라이트 1건입니다.
- 무료 하이라이트가 없는 그룹은 응답에 포함되지 않습니다.
- 정렬은 `createdAt desc`, `id desc` 기준 커서 페이지네이션입니다.

**Response** (200 OK):

```json
{
  "data": [
    {
      "id": "aidol-1",
      "name": "FLEUR",
      "profileImageUrl": "https://example.com/fleur.png",
      "concept": "girl-crush",
      "memberCount": 4,
      "createdAt": "2026-03-10T00:04:21.716491Z",
      "highlight": {
        "id": "highlight-1",
        "title": "Member Four Cut",
        "subtitle": "FLEUR unit selfie challenge",
        "thumbnailUrl": "https://example.com/thumb.png"
      }
    }
  ],
  "nextCursor": null,
  "hasMore": false
}
```

**Errors**:

- `422 INVALID_CURSOR` - cursor 형식이 올바르지 않음
- `422 INVALID_PAGE_SIZE` - `pageSize`가 1~100 범위를 벗어남

---

### GET /companions - Companion 목록 조회

멤버 목록을 조회합니다. 보통 aidolId 필터와 함께 사용하여 특정 그룹의 멤버를 조회합니다.

- URL: GET /companions
- Domain: Companion
- Layer: Domain
- Auth: 공개

Query Parameters (공통 List 규칙)

- `current`, `pageSize`, `sort`, `filters`
- 대표 `filters` 예시:
  - `[{"field":"aidolId","operator":"eq","value":"aidol-uuid..."}]`
  - `[{"field":"status","operator":"eq","value":"PUBLISHED"}]`

**Response** (200 OK):

```json
{
  "data": [
    {
      "id": "string",
      "aidolId": "string",
      "name": "string",
      "gender": "MALE|FEMALE",
      "grade": "F|D|C|B|A",
      "biography": "string",
      "profilePictureUrl": "string",
      "position": "LEADER|MAIN_VOCAL|SUB_VOCAL|...",
      "mbti": "string",
      "status": "PUBLISHED",
      "stats": {
        "vocal": 0,
        "dance": 0,
        "rap": 0,
        "visual": 0,
        "stamina": 0,
        "charm": 0
      },
      "createdAt": "datetime",
      "updatedAt": "datetime"
    }
  ],
  "total": 0
}
```

**Errors**:

- `400` - 잘못된 쿼리 파라미터 형식

---

### POST /companions - Companion 멤버 생성

특정 그룹(aidolId)에 소속될 멤버를 생성합니다.
POST /companions는 기존 id를 받아 attach하지 않으며,
attach는 PATCH /companions/{id}로 수행됩니다.
- URL: POST /companions
- Domain: Companion
- Layer: Domain
- Auth: 공개

**Request**:

```json
 {
   "aidolId": "aidol-uuid"
 }
```

**Response** (201 Created):

- system_prompt는 보안상 응답에서 제외됩니다.
  
```json
{
  "data": {
    "id": "comp_1",
    "name": "Updated Name",
    "aidolId": "aidol_123",
    "gender": "FEMALE",
    "grade": "A",
    "mbti": "ENTP",
    "stats": { "vocal": 100, "dance": 90, "rap": 80, "visual": 100, "stamina": 80, "charm": 95 },
    "createdAt": "2024-01-28T12:00:00Z",
    "updatedAt": "2024-01-29T15:00:00Z"
  }
}
```

---

### GET /companions/{id} - Companion 멤버 조회

- URL: GET /companions/{id}
- Domain: Companion
- Layer: Domain
- Auth: 공개

Sprint 6 기준 변경사항:

- `stats` 최대값은 각 항목별 `0~200`입니다.
- `grade`는 클라이언트 입력값이 아니라 서버 계산값이며, `stats` 합계 기준 `F | D | C | B | A`를 사용합니다.
- `ethnicities` 필드가 추가되며, 저장된 값은 `POST /companions/images` 프롬프트 조립에 사용됩니다.

**Response** (200 OK): 

```json
{
  "data": {
    "id": "comp_1",
    "aidolId": "aidol_123",
    "name": "Minji",
    "gender": "FEMALE",
    "ethnicities": ["EAST_ASIAN"],
    "grade": "A",
    "biography": "...",
    "profilePictureUrl": "...",
    "position": "MAIN_VOCAL",
    "mbti": "ENTP",
    "status": "PUBLISHED",
    "stats": { "vocal": 100, "dance": 90, "rap": 80, "visual": 100, "stamina": 80, "charm": 95 },
    "createdAt": "2024-01-28T12:00:00Z",
    "updatedAt": "2024-01-28T12:00:00Z"
  }
}
```

**Errors**:

- `404 RESOURCE_NOT_FOUND` - Companion 없음

---

### PATCH /companions/{id} - Companion 멤버 수정

연습생 생성 및 캐스팅 과정에서 Companion 정보를 업데이트합니다.

- URL: PATCH /companions/{id}
- Domain: Companion
- Layer: Domain
- Auth: 공개
Sprint 6 기준 변경사항:

- `grade`는 요청으로 받지 않으며 서버가 `stats` 합계 기준으로 계산합니다.
- `stats` 각 항목의 허용 범위는 `0~200`입니다.
- `ethnicities`는 1~2개의 enum 배열로 저장합니다.
- 저장된 `gender`, `ethnicities`는 `POST /companions/images`에서 자동 반영됩니다.

**Request**:

```json
{
  "aidolId": "aidol-uuid...",
  "name": "멤버 이름",
  "gender": "FEMALE",
  "ethnicities": ["EAST_ASIAN", "EUROPEAN"],
  "biography": "어릴 때부터...",
  "profilePictureUrl": "...",
  "position": "MAIN_VOCAL",
  "status": "PUBLISHED", // 선택사항 (기본값: DRAFT)
  "mbtiEnergy": 8,
  "mbtiPerception": 3,
  "mbtiJudgment": 7,
  "mbtiLifestyle": 2,
  "stats": {
    "vocal": 120,
    "dance": 80,
    "rap": 20,
    "visual": 135,
    "stamina": 70,
    "charm": 95
  }
}
```

**Response** (200 OK):

```json
{
  "data": {
    "id": "companion-uuid...",
    "aidolId": "...",
    "name": "멤버 이름",
    "gender": "FEMALE",
    "ethnicities": ["EAST_ASIAN", "EUROPEAN"],
    "mbti": "ESTP",
    "grade": "B",
    "stats": { "vocal": 120, ... },
    "status": "PUBLISHED",
    "createdAt": "...",
    "updatedAt": "..."
  }
}
```

**Errors**:

- `400 Bad Request` - `ethnicities` 빈 배열, 3개 이상, 유효하지 않은 enum 값
- `404 RESOURCE_NOT_FOUND` - Companion 없음

---

### DELETE /companions/{id} - Companion 멤버 삭제

• **설명:** 컴패니언을 그룹에서 제거합니다 (`aidolId`를 null로 설정). 컴패니언 데이터 자체가 삭제되지는 않습니다.

- URL: DELETE /companions/{id}
- Domain: Companion
- Layer: Domain
- Auth: 공개

**Sprint**: Sprint 1

**Request:** `id`

**Response** (200 OK): 

```json
{
  "data": {
    "id": "comp_1",
    "aidolId": null,
    "name": "Minji",
    "gender": "FEMALE",
    "grade": "A",
    "mbti": "ENTP",
    "stats": { "vocal": 100, "dance": 90, "rap": 80, "visual": 100, "stamina": 80, "charm": 95 },
    "createdAt": "2024-01-28T12:00:00Z",
    "updatedAt": "2024-01-29T15:00:00Z"
  }
}
```

**Errors**:

- `404` - Companion 없음

---

### POST /companions/images - Companion 프로필 이미지 생성

Companion에 저장된 `gender`, `ethnicities`와 선택한 칩 키를 조합해 프로필 이미지를 생성합니다. 프론트엔드는 직접 프롬프트를 구성하지 않습니다.

- URL: POST /companions/images
- Domain: Companion
- Layer: Domain
- Auth: 공개

**Request**:

```json
{
  "companionId": "companion-uuid",
  "mood": "CUTE",
  "impression": "SOFT",
  "hairstyle": "BLACK_LONG"
}
```

**Response** (201 Created):

```json
{
  "data": {
    "imageUrl": "https://cdn.example.com/companions/profile-1.png",
    "gender": "FEMALE",
    "ethnicities": ["EAST_ASIAN"]
  }
}
```

응답의 `gender`, `ethnicities`는 이미지 생성 시 실제로 사용된 Companion 저장값을 반환하며, 프론트엔드 검증 및 디버깅 용도로 사용됩니다.

누락 필드 예시:

```json
{
  "status": 400,
  "detail": "Companion profile is incomplete.",
  "code": "VALIDATION_ERROR",
  "meta": {
    "missingFields": ["ethnicities"]
  }
}
```

**Errors**:

- `400 Bad Request` - `mood`, `impression`, `hairstyle` 누락 또는 유효하지 않은 칩 키
- `400 Bad Request` - Companion의 `gender` 또는 `ethnicities`가 저장되지 않음 (`meta.missingFields` 포함)
- `404 RESOURCE_NOT_FOUND` - Companion 없음
- `500 EXTERNAL_SERVICE_ERROR` - 이미지 생성 실패

---

### POST /leads - email 수집

이메일을 입력받아 저장합니다. 만약 쿠키(anonymousId)가 있고, 해당 쿠키로 생성된 아이돌 그룹(aidol_id)이 있다면, 해당 아이돌 그룹 정보에 이메일을 연동하여 업데이트합니다.

- URL: POST /leads
- Domain: Lead
- Layer: Domain
- Auth: 공개 (하지만 쿠키가 있으면 연동 로직 수행)

**Request**:

```json
{
  "aidolId": "aidol-uuid",
  "email": "user@example.com"
}
```

요청 본문에서 `email`은 필수이며, `aidolId`는 선택입니다.

동작 로직:
1. 클라이언트가 anonymousId 쿠키를 가지고 있는지 확인.
2. `aidolId`가 있으면 해당 aidolId 그룹의 소유자(anonymousId)가 쿠키 값과 일치하는지 확인.
3. `aidolId`가 있고 소유자가 일치한다면 -> aidols 테이블의 해당 그룹 레코드에 email 컬럼을 업데이트.
4. `aidolId`가 없거나, 쿠키가 없거나, 소유자가 일치하지 않으면 -> aidol_leads 테이블에 단순히 이메일 정보 저장.

**Response** (201 Created):

```json
{
  "data": {
    "email": "user@example.com"
  }
}
```

**Errors**:

- `422 VALIDATION_ERROR` - `email` 누락

---

### GET /aidol-highlights - AIdol 하이라이트 목록 조회

AIdol 하이라이트를 조회합니다.

- URL: GET /aidol-highlights
- Domain: Highlight
- Layer: Domain
- Auth: 공개

Query Parameters (공통 List 규칙)

- `current`, `pageSize`, `sort`, `filters`
- 대표 `filters` 예시: `[{"field":"aidolId","operator":"eq","value":"aidol-uuid..."}]`

**Response** (200 OK):

```json
{
  "data": [
    {
      "id": "string",
      "aidolId": "string",
      "title": "string",
      "thumbnailUrl": "string",
      "subtitle": "string",
      "isPremium": true,
      "createdAt": "datetime",
      "updatedAt": "datetime"
     },
    {
      "id": "string",
      "aidolId": "string",
      "title": "string",
      "thumbnailUrl": "string",
      "subtitle": "string",
      "isPremium": true,
      "createdAt": "datetime",
      "updatedAt": "datetime"
     }
  ],
  "total": 2
}
```

---

### GET /aidol-highlights/{id}/messages - 하이라이트 메세지 조회

하이라이트 ID로 하이라이트 메세지를 조회합니다.

- URL: GET /aidol-highlights/{id}/messages
- Domain: Highlight
- Layer: Domain
- Auth: 공개

**Response** (200 OK):

```json
[
  {
    "id": "string",
    "highlightId": "string",
    "companionId": "string",
    "sequence": 1,
    "content": "안녕하세요",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  },
  {
    "id": "string",
    "highlightId": "string",
    "companionId": "string",
    "sequence": 2,
    "content": "안녕",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
]
```

---

 ### GET /aidol-feeds - 피드 콘텐츠 목록 조회

  AIdol 피드 콘텐츠를 조회합니다. (MyGroup 피드 탭, OtherGroup 피드 탭)

  - URL: GET /aidol-feeds
  - Domain: Feed
  - Layer: Domain
  - Auth: 공개

  Query Parameters (공통 List 규칙)

  - `current`, `pageSize`, `sort`, `filters`
  - 대표 `filters` 예시: `[{"field":"aidolId","operator":"eq","value":"aidol-uuid..."}]`

  **Response** (200 OK):

  ```json
  {
    "data": [
      {
        "id": "string",
        "aidolId": "string",
        "mediaType": "IMAGE | VIDEO",
        "mediaUrl": "string",
        "thumbnailUrl": "string | null",
        "createdAt": "string (ISO 8601)",
        "updatedAt": "string (ISO 8601)"
      }
    ],
    "total": 1
  }
```

---
### GET /companion-relationships -멤버 관계 조회

멤버 관계 정보를 조회합니다.

- URL: GET /companion-relationships
- Domain: Relationship
- Layer: Domain
- Auth: 공개

Query Parameters (공통 List 규칙)

- `current`, `pageSize`, `sort`, `filters`
- 대표 `filters` 예시:
  - A가 생각하는 관계들: `[{"field":"fromCompanionId","operator":"eq","value":"member-A-uuid"}]`
  - A를 생각하는 관계들: `[{"field":"toCompanionId","operator":"eq","value":"member-A-uuid"}]`

**Response** (200 OK):

```json
{
  "data": [
    {
	    "id": "string",
	    "fromCompanionId": "string",
	    "toCompanionId": "string",
	    "intimacy": "number",
	    "nickname": "string",
      "createdAt": "datetime",
      "updatedAt": "datetime"
		 },
    {
	    "id": "string",
	    "fromCompanionId": "string",
	    "toCompanionId": "string",
	    "intimacy": "number",
	    "nickname": "string",
      "createdAt": "datetime",
      "updatedAt": "datetime"
		 },
  ],
  "total": 2
}

```

---

### GET /companion-relationships/{id} -멤버 관계 조회

멤버 관계 정보를 조회합니다.

- URL: GET /companion-relationships/{id}
- Domain: Relationship
- Layer: Domain
- Auth: 공개

**Response** (200 OK):

```json
{
  "data": {
    "id": "string",
    "fromCompanionId": "string",
    "toCompanionId": "string",
    "intimacy": "number",
    "nickname": "string",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
}
```

---

### POST /companion-relationships -멤버 관계 생성

멤버 관계를 생성 합니다.

- URL: POST /companion-relationships
- Domain: Relationship
- Layer: Domain
- Auth: 공개

**Sprint**: Sprint 2

**Request**:

```json
{
  "fromCompanionId": "string",
  "toCompanionId": "string",
  "intimacy": "int",
  "nickname": "string" //선택
}
```

**Response** (201 Created):

```json
{
  "data": {
	  "id": "string", 
    "fromCompanionId": "string",
    "toCompanionId": "string",
    "intimacy": "int",
    "nickname": "string",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
}
```

---

### DELETE /companion-relationships/{id} -멤버 관계 삭제

멤버 관계를 삭제 합니다.

- URL: DELETE /companion-relationships/{id}
- Domain: Relationship
- Layer: Domain
- Auth: 공개

**Response** (204 No Content):
---

### GET /me/chatrooms - 채팅방 목록 조회

현재 참여 중인 채팅방 목록을 조회합니다.

- URL: GET /me/chatrooms
- Domain: Chatroom
- Layer: BFF
- Auth: Cookie 필수 (`aioia_anonymous_id`)

Query Parameters

- `aidolId` (optional): 그룹 필터
- `filters` (optional, JSON string): 채팅방 조건 필터
- `aioia_anonymous_id` (required, cookie): 사용자 식별자
- `current`, `pageSize`, `sort`는 지원하지 않음

- 동작 분기
  1. 항상 chatrooms.anonymous_id = cookie로 기본 범위 제한
  2. aidolId가 있으면 companions 조인 후 companions.aidol_id = aidolId 적용
  3. filters가 있으면 chatrooms 컬럼 조건을 추가 적용
  4. aidolId가 없으면 기존 동작(조인 없음)과 동일

- 주의사항
  - aidolId는 전용 파라미터입니다. filters에서 aidolId 필드로 처리하지 않습니다.
  - filters는 JSON 문자열이어야 하며, camelCase/snake_case 필드 모두 허용됩니다(내부에서 snake_case로 변환).

**Response** (200 OK):

```json
{
  "data": [
    {
      "id": "chatroom-uuid-1",
      "companionId": "companion-uuid-1",
      "name": "나의 시크릿 챗",
      "language": "ko",
      "lastMessage": {
        "content": "안녕하세요!",
        "createdAt": "2024-02-13T12:00:00Z"
      },
      "createdAt": "2024-02-09T10:00:00Z",
      "updatedAt": "2024-02-13T12:00:00Z"
    },
    {
      "id": "chatroom-uuid-2",
      "companionId": "companion-uuid-2",
      "name": "새 채팅방",
      "language": "en",
      "lastMessage": null,
      "createdAt": "2024-02-10T09:00:00Z",
      "updatedAt": "2024-02-10T09:00:00Z"
    }
  ]
}
```

---

### POST /chatrooms - 채팅방 생성

채팅방을 생성 합니다.

- URL: POST /chatrooms
- Domain: Chatroom
- Layer: Domain
- Auth: Cookie 필수 (anonymousId)

**Request**:

```json
{
  "companionId": "companion-uuid",
  "name": "나의 시크릿 챗",
  "language": "ko"
}
```

**Response** (201 Created):

```json
{
  "data": {
    "id": "chatroom-uuid-1234",
    "companionId": "companion-uuid",
    "name": "나의 시크릿 챗",
    "language": "ko",
    "createdAt": "2024-02-09T10:00:00Z",
    "updatedAt": "2024-02-09T10:00:00Z"
  }
}
```

---

### GET /chatrooms/{id} - 채팅방 상세 조회

특정 채팅방 조회합니다.

- URL: GET /chatrooms/{id}
- Domain: Chatroom
- Layer: Domain
- Auth: 공개

**Response** (200 OK):

```json
{
  "data": {
    "id": "chatroom-uuid-1234",
    "companionId": "companion-uuid",
    "name": "나의 시크릿 챗",
    "language": "ko",
    "createdAt": "2024-02-09T10:00:00Z",
    "updatedAt": "2024-02-09T10:00:00Z"
  }
}

```
---

### GET /chatrooms/{id}/messages - 채팅방 메시지 조회

특정 채팅방의 메시지를 조회합니다.

- URL: GET /chatrooms/{id}/messages
- Domain: Message
- Layer: Domain
- Auth: 공개

Input Parameters (Query)

- limit: 한 번에 가져올 메시지 수 (기본: 100)
- offset: 건너뛸 메시지 수 (기본: 0)
- `current`, `pageSize`, `sort`, `filters`는 지원하지 않음

**Response** (200 OK):
- 시간 순서대로 정렬된 메시지 배열 반환(내림차순)
```json
[
  {
    "id": "msg-124",
    "senderType": "COMPANION",
    "content": "오늘 날씨가 좋아서 정말 상쾌해요! ",
    "createdAt": "2024-02-09T10:01:05Z"
  },
  {
    "id": "msg-123",
    "senderType": "USER",
    "content": "안녕, 오늘 기분 어때?",
    "createdAt": "2024-02-09T10:01:00Z"
  }
]

```

---

### POST /chatrooms/{id}/messages - 채팅방 메시지 전송

특정 채팅방에 메시지를 전송합니다.

- URL: POST /chatrooms/{id}/messages
- Domain: Message
- Layer: Domain
- Auth: 쿠키 기반 인증 - 메시지를 보낸 사람을 익명 ID로 기록하기 위해 필요합니다.

**Request**:

```json
{
  "content": "안녕, 오늘 기분 어때?"
}
```

**Response** (201 Created):
```json
{
  "id": "msg-125",
  "senderType": "USER",
  "content": "나 오늘 좀 우울해...",
  "createdAt": "2024-02-09T10:02:00Z"
}
```
---

### POST /chatrooms/{id}/companions/{cid}/response - AI 멤버 응답 생성

채팅방(id)에 있는 사용자 메시지에 대해 특정 멤버(cid)가 대답하도록 요청합니다. 이 API는 비동기적으로 동작하지 않고, 응답이 생성될 때까지 기다렸다가(Sync) 생성된 메시지를 반환합니다.

- URL: POST /chatrooms/{id}/companions/{cid}/response
- id: Chatroom ID (대화가 일어나는 방)
- cid: Companion ID (대답을 해야 하는 멤버)
- Domain: Chat AI
- Layer: BFF
- Auth: 공개

동작 원리:

1. 백엔드는 cid에 해당하는 멤버 정보를 DB에서 조회합니다.
2. 멤버의 system_prompt와 채팅방의 최근 대화 내역(History)을 조합하여 LLM에 보낼 프롬프트를 구성합니다.
3. 현재 시간(KST) 정보도 프롬프트에 포함하여 시간 감각을 부여합니다.
4. LLM(OpenAI)을 통해 답변을 생성합니다.
5. 생성된 답변을 companion 타입의 메시지로 DB에 저장합니다

**Request**:

```json
{
  body 없음
}
```

**Response** (201 Created):
```json
{
  "messageId": "msg-126",
  "content": "저런, 무슨 일 있으셨어요? 제가 옆에서 이야기 들어드릴게요. "
}
```
---
### POST /chatrooms/{id}/companions/{cid}/initial-response - 선 발화 AI 멤버 응답 생성

선 발화 메세지를 위한 API 입니다.

- URL: POST /chatrooms/{id}/companions/{cid}/initial-response
- id: Chatroom ID (대화가 일어나는 방)
- cid: Companion ID (대답을 해야 하는 멤버)
- Domain: Chat AI
- Layer: BFF
- Auth: 공개

**Request**:

```json
{
  body 없음
}
```

**Response** (201 Created):
```json
{
  "messageId": "msg-126",
  "content": "안녕하세요 ..."
}
```

---

### GET /companions/{id}/credits/free - 무료 연습 크레딧 조회

특정 멤버와 연습 타입 기준 무료 크레딧 잔여량을 조회합니다. 무료 크레딧은 멤버별, 연습 타입별로 독립 관리됩니다.

- URL: GET /companions/{id}/credits/free
- Domain: Credit
- Layer: Domain
- Auth: Cookie 필수 (`aioia_anonymous_id`)

Query Parameters

- `type` (required): `PHOTOCARD | SHOT`

**Response** (200 OK):

```json
{
  "data": {
    "companionId": "companion-uuid",
    "type": "PHOTOCARD",
    "freeCreditsRemaining": 2
  }
}
```

**Errors**:

- `400 INVALID_QUERY_PARAMS` - `type` 누락 또는 지원하지 않는 값
- `403 FORBIDDEN` - 본인 소유 멤버가 아님
- `404 RESOURCE_NOT_FOUND` - Companion 없음

---

### GET /me/credits/charge - 충전 크레딧 조회

사용자 단위 공유 충전 크레딧 잔여량과 다음 충전 가능 시각을 조회합니다. 어떤 연습 타입에서 충전 크레딧을 소비했는지와 무관하게 이 엔드포인트 하나로 조회합니다.

- URL: GET /me/credits/charge
- Domain: Credit
- Layer: Domain
- Auth: Cookie 필수 (`aioia_anonymous_id`)

**Response** (200 OK):

```json
{
  "data": {
    "chargeCreditsRemaining": 3,
    "nextRechargeAvailableAt": null
  }
}
```

**Errors**:

- 없음. 무료/충전 크레딧이 모두 0이어도 정상 응답합니다.

---

### POST /me/credits/recharge - 크레딧 충전

사용자 단위 공유 충전 크레딧을 지급합니다. 잔여량 조회는 `GET /me/credits/charge`, 실제 충전 실행은 이 엔드포인트를 사용합니다.

- URL: POST /me/credits/recharge
- Domain: Credit
- Layer: Domain
- Auth: Cookie 필수 (`aioia_anonymous_id`)

**Request**:

```json
{}
```

**Response** (200 OK):

```json
{
  "data": {
    "grantedCredits": 3,
    "chargeCreditsRemaining": 3,
    "nextRechargeAvailableAt": "2026-03-26T03:00:00Z"
  }
}
```

**Errors**:

- `409 CREDIT_RECHARGE_COOLDOWN` - 아직 충전 쿨다운이 끝나지 않음 (`meta.nextRechargeAvailableAt` 포함)

---

### POST /companions/{id}/practices - 연습 생성

특정 멤버의 연습을 생성합니다. Sprint 6부터 포토카드와 샷 생성은 모두 이 엔드포인트로 통합되며, 생성 성공 시 Companion 스탯이 즉시 반영되고 Practice 영속 레코드와 Collectible 산출물이 함께 생성됩니다.

- URL: POST /companions/{id}/practices
- Domain: Practice
- Layer: BFF
- Auth: Cookie 필수 (`aioia_anonymous_id`)

동작 원리:

1. 멤버의 현재 등급과 연습 가능 여부를 확인합니다.
2. 멤버별 무료 크레딧과 사용자 공유 충전 크레딧을 순서대로 확인합니다.
3. 서버는 먼저 `PENDING` 상태의 Practice를 저장하고, 유료 크레딧을 사용하는 경우 차감 내역도 동일 Practice와 연결해 영속화합니다.
4. AI 산출물 생성 및 업로드는 외부 서비스 호출이므로 단일 DB 트랜잭션에 포함되지 않습니다.
5. AI 산출물 생성이 성공하면 Companion 스탯을 반영하고, 마지막으로 Practice/Collectible 완료 상태를 확정합니다.
6. AI 호출 이후 실패하면 서버는 실패 상태 기록, 유료 크레딧 환불, 이미 반영된 Companion 스탯 원복을 순서대로 시도합니다.

**Request**:

```json
{
  "type": "PHOTOCARD",
  "variant": "DAILY",
  "mode": "FIXED"
}
```

- `type`: `PHOTOCARD | SHOT`
- `variant`:
  - `PHOTOCARD`일 때 `SCHOOL_LIFE | FINGER_HEART | DAILY | RANDOM`
  - `SHOT`일 때 `SIDE | FULL`
- `mode`: `FIXED | RANDOM`
- `type = PHOTOCARD` 이고 `variant = RANDOM`인 경우 `grade >= D` 멤버에게만 허용됩니다.

**Response** (201 Created):

```json
{
  "data": {
    "id": "collectible-uuid",
    "companionId": "companion-uuid",
    "type": "PHOTOCARD",
    "variant": "DAILY",
    "serialNumber": "AIDOL-250325-000001",
    "imageUrl": "https://cdn.example.com/collectibles/photo-1.png",
    "resultGrade": null,
    "isNearMiss": false,
    "statDelta": {
      "vocal": 0,
      "dance": 0,
      "rap": 0,
      "visual": 5,
      "stamina": 1,
      "charm": 2
    },
    "totalStatDelta": 8,
    "currentStats": {
      "vocal": 120,
      "dance": 80,
      "rap": 20,
      "visual": 135,
      "stamina": 71,
      "charm": 97
    },
    "currentTotalStat": 523,
    "currentGrade": "A",
    "createdAt": "2026-03-25T03:00:00Z"
  }
}
```

설명:

- 응답의 `id`는 Practice ID가 아니라 생성된 Collectible ID입니다.
- 응답의 `serialNumber`는 `PHOTOCARD`, `SHOT` 공통으로 발급되는 컬렉터블 시리얼입니다.
- `resultGrade`는 `mode = FIXED`일 때 `null`입니다.
- `resultGrade`는 `mode = RANDOM`일 때 `MISS | NORMAL | GREAT | JACKPOT` 중 하나입니다.
- `SHOT` 타입에서는 `statDelta.charm`이 `null`이며, `vocal`, `dance`, `rap`은 `0`으로 유지됩니다.
- `currentTotalStat`, `currentStats`, `currentGrade`는 연습 결과 화면 갱신을 위한 Companion 상태 스냅샷입니다.
- `GET /me/collectibles`에는 완료(`COMPLETED`)된 Collectible만 포함되며, 실패 처리된 Practice는 컬렉션에 노출되지 않습니다.
- 이미지 생성/업로드 실패 후 보상 처리까지 완료되면 최종 응답은 원래 실패 원인 기준으로 `500 EXTERNAL_SERVICE_ERROR`를 반환합니다.
- 멤버 스탯 반영에 실패했거나, 실패 이후 스탯 원복에 실패하면 `500 RESOURCE_UPDATE_FAILED`를 반환합니다.
- 실패 상태 기록, 환불 연결 등 보상 처리 중 예상치 못한 내부 오류가 발생하면 `500 INTERNAL_SERVER_ERROR`가 반환될 수 있습니다.

**Errors**:

- `400 Bad Request` - `type`, `variant`, `mode` 누락 또는 지원하지 않는 조합
- `403 FORBIDDEN` - 본인 소유 멤버가 아님
- `404 RESOURCE_NOT_FOUND` - Companion 없음
- `409 PRACTICE_CREDITS_EXHAUSTED` - 무료/충전 크레딧 모두 소진됨
- `409 PRACTICE_RANDOM_PHOTOCARD_GRADE_RESTRICTED` - `D` 등급 미만 멤버가 `PHOTOCARD + RANDOM` 조합을 선택함
- `500 EXTERNAL_SERVICE_ERROR` - 이미지 생성 또는 업로드 실패
- `500 RESOURCE_UPDATE_FAILED` - 멤버 스탯 반영 또는 롤백 실패
- `500 INTERNAL_SERVER_ERROR` - 실패 상태 기록 또는 환불 처리 중 예상치 못한 내부 오류

---

### GET /me/collectibles - 컬렉터블 목록 조회

현재 사용자가 보유한 컬렉터블 목록을 조회합니다. soft delete 된 산출물은 제외하며, 포토카드와 샷을 공통 필드로 통합 반환합니다.

- URL: GET /me/collectibles
- Domain: Collectible
- Layer: Domain
- Auth: Cookie 필수 (`aioia_anonymous_id`)

Query Parameters (공통 List 규칙)

- `current`, `pageSize`, `sort`, `filters`
- 서버 기본 정렬: `createdAt desc`, `id desc`
- `sort` 파라미터를 보내더라도 현재 컬렉터블 API에서는 서버 기본 정렬만 사용합니다.
- 대표 `filters` 예시:
  - `[{"field":"type","operator":"eq","value":"PHOTOCARD"}]`
  - `[{"field":"variant","operator":"eq","value":"SIDE"}]`
  - `[{"field":"companionId","operator":"eq","value":"companion-uuid"}]`
- `variant` 필터는 반드시 `type` 필터와 함께 사용해야 합니다.

**Response** (200 OK):

```json
{
  "data": [
    {
      "id": "collectible-uuid-1",
      "serialNumber": "AIDOL-250325-000142",
      "companionId": "companion-uuid-1",
      "imageUrl": "https://cdn.example.com/collectibles/photo-1.png",
      "type": "SHOT",
      "variant": "SIDE",
      "resultGrade": "NORMAL",
      "isNew": true,
      "createdAt": "2026-03-25T03:00:00Z"
    }
  ],
  "total": 1
}
```

**Errors**:

- `400 INVALID_QUERY_PARAMS` - 잘못된 쿼리 파라미터 형식
- `400 INVALID_QUERY_PARAMS` - `variant` 필터만 단독으로 사용함

---

### GET /me/collectibles/{id} - 컬렉터블 상세 조회

컬렉터블 상세 화면 진입 시 필요한 단건 데이터를 조회합니다. 페이지 새로고침 또는 URL 직접 접근 시에도 동일한 화면을 복원할 수 있도록 제공합니다.

- URL: GET /me/collectibles/{id}
- Domain: Collectible
- Layer: Domain
- Auth: Cookie 필수 (`aioia_anonymous_id`)

**Response** (200 OK):

```json
{
  "data": {
    "id": "collectible-uuid-1",
    "serialNumber": "AIDOL-250325-000142",
    "type": "PHOTOCARD",
    "variant": "SCHOOL_LIFE",
    "companionName": "test",
    "imageUrl": "https://cdn.example.com/collectibles/photo-1.png",
    "resultGrade": "NORMAL",
    "totalStatDelta": 8,
    "statDelta": {
      "vocal": 0,
      "dance": 0,
      "rap": 0,
      "visual": 5,
      "stamina": 1,
      "charm": 2
    },
    "isNew": true,
    "createdAt": "2026-03-25T03:00:00Z"
  }
}
```

**Errors**:

- `403 FORBIDDEN` - 본인 소유 컬렉터블이 아님
- `404 RESOURCE_NOT_FOUND` - 컬렉터블 없음

---

### DELETE /me/collectibles/{id} - 컬렉터블 삭제

컬렉터블을 컬렉션에서 삭제합니다. soft delete로 처리하며, 해당 Practice로 획득한 스탯은 유지됩니다.

- URL: DELETE /me/collectibles/{id}
- Domain: Collectible
- Layer: Domain
- Auth: Cookie 필수 (`aioia_anonymous_id`)

**Response** (204 No Content)

**Errors**:

- `403 FORBIDDEN` - 본인 소유 컬렉터블이 아님
- `404 RESOURCE_NOT_FOUND` - 컬렉터블 없음

---

### GET /companions/{id}/collectibles - 공개 컬렉터블 목록 조회

특정 공개 멤버의 컬렉터블 목록을 조회합니다. 공개 컬렉션 화면에서 사용하며, `PUBLISHED` 상태의 그룹에 속한 `PUBLISHED` 멤버의 완료된 산출물만 노출합니다. soft delete 된 산출물은 제외합니다.

- URL: GET /companions/{id}/collectibles
- path의 `{id}`는 Companion ID입니다.
- Domain: Collectible
- Layer: Domain
- Auth: Public

Query Parameters (공통 List 규칙)

- `current`, `pageSize`, `sort`, `filters`
- 서버 기본 정렬: `createdAt desc`, `id desc`
- `sort` 파라미터를 보내더라도 현재 공개 컬렉터블 API에서는 서버 기본 정렬만 사용합니다.
- `companionId`는 path로 조회 범위가 고정되므로 `filters`에서 허용하지 않습니다.
- 대표 `filters` 예시:
  - `[{"field":"type","operator":"eq","value":"PHOTOCARD"}]`
  - `[{"field":"variant","operator":"eq","value":"SIDE"}]`
- `variant` 필터는 반드시 `type` 필터와 함께 사용해야 합니다.
- 공개 조회 API도 `CollectibleListItem` 공통 계약을 사용합니다. 현재 저장소 구현이 photocard 중심이더라도 응답 스키마는 collectible 공통 모델을 기준으로 정의합니다.

**Response** (200 OK):

```json
{
  "data": [
    {
      "id": "collectible-uuid-1",
      "serialNumber": "AIDOL-250325-000142",
      "companionId": "companion-uuid-1",
      "imageUrl": "https://cdn.example.com/collectibles/photo-1.png",
      "type": "PHOTOCARD",
      "variant": "DAILY",
      "resultGrade": null,
      "isNew": true,
      "createdAt": "2026-03-25T03:00:00Z"
    }
  ],
  "total": 1
}
```

**Errors**:

- `400 INVALID_QUERY_PARAMS` - 잘못된 쿼리 파라미터 형식 또는 허용하지 않는 필터를 사용함
- `400 INVALID_QUERY_PARAMS` - `variant` 필터만 단독으로 사용함
- `404 RESOURCE_NOT_FOUND` - Companion 없음 또는 공개 조회 대상이 아님

---

### GET /companions/{id}/collectibles/{collectibleId} - 공개 컬렉터블 상세 조회

특정 공개 멤버의 컬렉터블 상세 정보를 조회합니다. 공개 컬렉션 상세 화면에서 사용하며, 해당 멤버 소속의 공개 가능한 산출물만 조회할 수 있습니다.

- URL: GET /companions/{id}/collectibles/{collectibleId}
- path의 `{id}`는 Companion ID, `{collectibleId}`는 컬렉터블 ID입니다.
- Domain: Collectible
- Layer: Domain
- Auth: Public

**Response** (200 OK):

```json
{
  "data": {
    "id": "collectible-uuid-1",
    "serialNumber": "AIDOL-250325-000142",
    "type": "PHOTOCARD",
    "variant": "SCHOOL_LIFE",
    "companionName": "test",
    "imageUrl": "https://cdn.example.com/collectibles/photo-1.png",
    "resultGrade": "NORMAL",
    "totalStatDelta": 8,
    "statDelta": {
      "vocal": 0,
      "dance": 0,
      "rap": 0,
      "visual": 5,
      "stamina": 1,
      "charm": 2
    },
    "isNew": true,
    "createdAt": "2026-03-25T03:00:00Z"
  }
}
```

**Errors**:

- `404 RESOURCE_NOT_FOUND` - 컬렉터블 없음, 다른 멤버 소속 컬렉터블이거나 공개 조회 대상이 아님

---

## 데이터 모델

### AIdol

```tsx
{
  id: string                        // UUID
  name: string | null               // 그룹명
  email: string | null              // 사용자 Email
  concept: string | null            // 그룹 컨셉
  greeting: string | null           // 인사 문구
  profileImageUrl: string | null    // 엠블럼 이미지 URL
  status: "DRAFT" | "PUBLISHED"     // 상태
  anonymousId: string | null         // 소유권 토큰 (응답에 미포함)
  createdAt: string                 // ISO 8601 datetime
  updatedAt: string                 // ISO 8601 datetime
}

```

### AIdolGroupHighlightSummary

```tsx
{
  id: string                        // 하이라이트 ID
  title: string                     // 하이라이트 제목
  subtitle: string | null           // 하이라이트 부제
  thumbnailUrl: string              // 하이라이트 썸네일 URL
}
```

### AIdolGroupSummary

```tsx
{
  id: string                        // 그룹 ID
  name: string                      // 그룹명
  profileImageUrl: string | null    // 그룹 프로필 이미지
  concept: string | null            // 그룹 컨셉
  memberCount: number               // 공개(PUBLISHED) 멤버 수
  createdAt: string                 // 그룹 생성 시각 (ISO 8601 datetime)
  highlight: AIdolGroupHighlightSummary // 최신 무료 하이라이트 요약
}
```

### Companion

```tsx
{
  id: string                        // UUID
  aidolId: string | null            // 소속된 AIdol 그룹 ID (없으면 null)
  name: string | null               // 이름
  gender: string | null             // 성별 (Gender Enum 참고)
  ethnicities: ("EAST_ASIAN" | "SOUTHEAST_ASIAN" | "EUROPEAN" | "SOUTH_AMERICAN")[] | null // 선택 민족 배열
  grade: "F" | "D" | "C" | "B" | "A" | null // stats 합계 기반 등급
  biography: string | null          // 자기소개/설정
  profilePictureUrl: string | null  // 프로필 이미지 URL
  position: string | null           // 포지션 (Position Enum 참고)
  status: string | null             // DRAFT | PUBLISHED
  mbti: string | null               // 계산된 MBTI (예: "ENTP")
  stats: {                          // 능력치 객체
    vocal: number     // 0~200 (보컬)
    dance: number     // 0~200 (댄스)
    rap: number       // 0~200 (랩)
    visual: number    // 0~200 (비주얼)
    stamina: number   // 0~200 (체력)
    charm: number     // 0~200 (매력)
  }
  createdAt: string                 // ISO 8601 datetime
  updatedAt: string                 // ISO 8601 datetime
}
```

- Sprint 5부터 `grade`는 `stats` 평균이 아니라 합계 기준으로 계산합니다.

### FreeCreditBalance

```tsx
{
  companionId: string               // 조회 대상 멤버 ID
  type: "PHOTOCARD" | "SHOT"        // 무료 횟수를 계산할 연습 타입
  freeCreditsRemaining: number      // 0~3, 해당 멤버/타입 기준 남은 무료 횟수
}
```

### ChargeCreditBalance

```tsx
{
  chargeCreditsRemaining: number    // 사용자 단위 공유 충전 크레딧 잔여량
  nextRechargeAvailableAt: string | null // 다음 충전 가능 시각, 쿨다운이 없으면 null
}
```

### CreditRechargeResult

```tsx
{
  grantedCredits: number            // 이번 충전으로 지급된 크레딧 수, Sprint 5는 항상 3
  chargeCreditsRemaining: number    // 충전 직후 사용자 공유 충전 크레딧 잔여량
  nextRechargeAvailableAt: string   // 다음 충전 가능 시각 (ISO 8601 datetime)
}
```

### PracticeCreateResult

```tsx
{
  id: string                        // 생성된 Collectible 식별자 (Practice ID 아님)
  companionId: string               // 연습 대상 멤버 ID
  type: "PHOTOCARD" | "SHOT"        // 연습 타입
  variant: "SCHOOL_LIFE" | "FINGER_HEART" | "DAILY" | "RANDOM" | "SIDE" | "FULL" // 타입별 세부 옵션
  serialNumber: string              // PHOTOCARD, SHOT 공통 시리얼 넘버
  imageUrl: string | null           // 생성된 이미지 URL
  resultGrade: "MISS" | "NORMAL" | "GREAT" | "JACKPOT" | null // RANDOM 모드 결과 등급, FIXED면 null
  isNearMiss: boolean               // Near-Miss 연출 발동 여부
  statDelta: {
    vocal: number                   // 이번 생성으로 증가한 보컬 수치
    dance: number                   // 이번 생성으로 증가한 댄스 수치
    rap: number                     // 이번 생성으로 증가한 랩 수치
    visual: number                  // 이번 생성으로 증가한 비주얼 수치
    stamina: number                 // 이번 생성으로 증가한 체력 수치
    charm: number | null            // 이번 생성으로 증가한 매력 수치 (SHOT은 null)
  }
  totalStatDelta: number            // 이번 생성으로 획득한 총 스탯 합계
  currentTotalStat: number          // 생성 직후 멤버의 현재 총 스탯 합계
  currentStats: {
    vocal: number                   // 생성 직후 멤버의 현재 보컬 수치
    dance: number                   // 생성 직후 멤버의 현재 댄스 수치
    rap: number                     // 생성 직후 멤버의 현재 랩 수치
    visual: number                  // 생성 직후 멤버의 현재 비주얼 수치
    stamina: number                 // 생성 직후 멤버의 현재 체력 수치
    charm: number                   // 생성 직후 멤버의 현재 매력 수치
  }
  currentGrade: "F" | "D" | "C" | "B" | "A" // 생성 직후 멤버의 현재 등급
  createdAt: string                 // 생성 시각 (ISO 8601 datetime)
}
```

### CollectibleListItem

```tsx
{
  id: string                        // 컬렉터블 식별자
  serialNumber: string              // PHOTOCARD, SHOT 공통 시리얼 넘버
  companionId: string               // 컬렉터블 대상 멤버 ID
  imageUrl: string                  // 대표 이미지 URL
  type: "PHOTOCARD" | "SHOT"        // 어떤 연습으로 생성되었는지
  variant: "SCHOOL_LIFE" | "FINGER_HEART" | "DAILY" | "RANDOM" | "SIDE" | "FULL" // 타입별 세부 옵션
  resultGrade: "MISS" | "NORMAL" | "GREAT" | "JACKPOT" | null // 생성 시 보상 등급
  isNew: boolean                    // createdAt 기준 24시간 이내 여부
  createdAt: string                 // 생성 시각 (ISO 8601 datetime)
}
```

### CollectibleDetail

```tsx
{
  id: string                        // 컬렉터블 식별자
  serialNumber: string              // PHOTOCARD, SHOT 공통 시리얼 넘버
  type: "PHOTOCARD" | "SHOT"        // 어떤 연습으로 생성되었는지
  variant: "SCHOOL_LIFE" | "FINGER_HEART" | "DAILY" | "RANDOM" | "SIDE" | "FULL" // 타입별 세부 옵션
  companionName: string | null      // 컬렉터블 대상 멤버 이름
  imageUrl: string                  // 대표 이미지 URL
  resultGrade: "MISS" | "NORMAL" | "GREAT" | "JACKPOT" | null // 생성 시 보상 등급
  totalStatDelta: number            // 이번 생성으로 획득한 총 스탯 합계
  statDelta: {
    vocal: number                   // 이번 생성으로 증가한 보컬 수치
    dance: number                   // 이번 생성으로 증가한 댄스 수치
    rap: number                     // 이번 생성으로 증가한 랩 수치
    visual: number                  // 이번 생성으로 증가한 비주얼 수치
    stamina: number                 // 이번 생성으로 증가한 체력 수치
    charm: number | null            // 이번 생성으로 증가한 매력 수치 (SHOT은 null)
  }
  isNew: boolean                    // createdAt 기준 24시간 이내 여부
  createdAt: string                 // 생성 시각 (ISO 8601 datetime)
}
```

### AIdolHighlights

```tsx
{
  id: string                       // UUID
  aidolId: string                  // 그룹 ID
  title: string                    // 제목
	thumbnailUrl: string             // 썸네일 이미지
	subtitle: string
  isPremium: boolean               // 프리미엄 여부
  createdAt: string                // ISO 8601 datetime
  updatedAt: string                // ISO 8601 datetime
}
```

### HighlightMessages

```tsx
{
  id: string                        // UUID
  highlightId: string               // 하이라이트
  companionId: string               // 멤버
  sequence: number                  // 메세지 순서
  content: string                   // 메세지 내용
  createdAt: string                 // ISO 8601 datetime
  updatedAt: string                 // ISO 8601 datetime
}

```
### AIdolFeed

  ```tsx
  {
    id: string                         // UUID
    aidolId: string                    // 그룹 ID
    mediaType: "IMAGE" | "VIDEO"       // 콘텐츠 유형
    mediaUrl: string                   // 이미지/영상 URL
    thumbnailUrl: string | null        // 영상 썸네일 URL
    createdAt: string                  // ISO 8601 datetime
    updatedAt: string                  // ISO 8601 datetime
  }
```

### CompanionRelationships

```tsx
{
  id: string                         // UUID
  fromCompanionId: string           // 멤버 1
  toCompanionId: string            // 멤버 2
  intimacy: number                   // 친밀도
  nickname: string | null            // 관계 별명
  createdAt: string                  // ISO 8601 datetime
  updatedAt: string                  // ISO 8601 datetime
}
```

### Chatroom 

```tsx
{
  id: string                        // UUID
  companionId: string               // 채팅 대상 companion ID
  name: string                      // 채팅방 이름
  language: string                  // 언어 코드 (기본: "en")
  lastMessage: {                    // 최근 메시지 요약 (GET /me/chatrooms 응답에서만 포함)
    content: string
    createdAt: string
  } | null
  createdAt: string                 // ISO 8601 datetime
  updatedAt: string
}

```

### Message

```tsx
{
  id: string                        // UUID
  senderType: "USER" | "COMPANION"  // 발신자 유형
  content: string                   // 메시지 내용
  createdAt: string                 // ISO 8601 datetime
}

```

### CompanionImageGenerationResult

```tsx
{
  imageUrl: string                  // 생성된 이미지 URL
  gender: "MALE" | "FEMALE"         // 이미지 생성 시 실제로 사용된 Companion 성별 값
  ethnicities: ("EAST_ASIAN" | "SOUTHEAST_ASIAN" | "EUROPEAN" | "SOUTH_AMERICAN")[] // 이미지 생성 시 실제로 사용된 Companion 민족 값
}

```

---

## 🔧 List Query Parameters

적용 endpoint:

- `GET /aidols`
- `GET /me/aidols`
- `GET /companions`
- `GET /aidol-highlights`
- `GET /companion-relationships`
- `GET /aidol-feeds`
- `GET /me/collectibles`
- `GET /companions/{id}/collectibles`

비적용 endpoint:

- `GET /groups/featured` (전용 파라미터: `cursor`, `pageSize`; 커서 기반 페이지네이션)
- `GET /me/chatrooms` (전용 파라미터: `aidolId`, `filters`)
- `GET /chatrooms/{id}/messages` (전용 파라미터: `limit`, `offset`)

### Pagination

- `current`: 페이지 번호 (기본: 1, ≥ 1)
- `pageSize`: 페이지당 항목 수 (기본: 10, 1-100)

### Sort

```
?sort=[["createdAt","desc"]]

```

### Filters

```
?filters=[{"field":"aidolId","operator":"eq","value":"uuid"}]

```

- `field`는 camelCase/snake_case 모두 허용되며 서버에서 내부 snake_case로 정규화됩니다.

| 연산자                   | 설명             |
| ------------------------ | ---------------- |
| `eq`, `ne`               | 같음 / 같지 않음 |
| `in`                     | 배열 포함        |
| `contains`               | 문자열 포함      |
| `gt`, `gte`, `lt`, `lte` | 비교             |
| `or`, `and`              | 조건 결합        |

---

## 에러 응답

모든 에러는 다음 형식을 따릅니다:

```json
{
  "status": 422,
  "detail": "사용자 친화적 메시지",
  "code": "ERROR_CODE"
}

```

상태 기반 에러는 추가 정보를 위해 `meta` 객체를 포함할 수 있습니다.

```json
{
  "status": 409,
  "detail": "아직 충전할 수 없습니다.",
  "code": "CREDIT_RECHARGE_COOLDOWN",
  "meta": {
    "nextRechargeAvailableAt": "2026-03-26T03:00:00Z"
  }
}
```

### Error Codes

| Code                            | HTTP Status | 설명                                                          |
| ------------------------------- | ----------- | ------------------------------------------------------------- |
| `VALIDATION_ERROR`              | 400, 422    | 요청 바디/필드 검증 실패. Sprint 6 신규 입력형 API는 400을 우선 사용 |
| `INVALID_QUERY_PARAMS`          | 400         | `sort`, `filters`, 기타 query parameter 형식/허용값 오류      |
| `FORBIDDEN`                     | 403         | 요청 리소스에 대한 접근 권한 없음                             |
| `RESOURCE_NOT_FOUND`            | 404         | 요청한 리소스 없음                                            |
| `FIRST_RESPONSE_ALREADY_EXISTS` | 409         | `initial-response` API에서 이미 메시지가 존재하는 채팅방 요청 |
| `CREDIT_RECHARGE_COOLDOWN`      | 409         | 충전 쿨다운이 끝나지 않아 재충전할 수 없음                    |
| `PRACTICE_CREDITS_EXHAUSTED`    | 409         | 무료/충전 크레딧이 모두 소진되어 연습을 생성할 수 없음       |
| `PRACTICE_RANDOM_PHOTOCARD_GRADE_RESTRICTED` | 409 | `D` 등급 미만 멤버는 `PHOTOCARD + RANDOM` 조합을 선택할 수 없음 |
| `BadRequestError`               | 400         | LLM 공급자 요청 오류                                          |
| `RateLimitError`                | 429         | LLM 공급자 호출 한도 초과                                     |
| `ServiceUnavailableError`       | 503         | LLM 공급자 서비스 일시 장애                                   |
| `EXTERNAL_SERVICE_ERROR`        | 500         | 외부 서비스 연동 오류(공통 코드)                              |
| `RESOURCE_UPDATE_FAILED`        | 500         | 리소스 갱신 또는 보상 롤백 처리에 실패함                      |
| `INTERNAL_SERVER_ERROR`         | 500         | 예상치 못한 서버 오류                                         |


---

## API 문서 링크

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Spec**: `/openapi.json`
