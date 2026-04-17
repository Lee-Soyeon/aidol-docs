# AIdol ERD

- 원본: [Notion](https://www.notion.so/2f046f96550480168a53f9f6a9f79d0b)
- 업데이트: Sprint 6 기능 반영 (`Practice/Collectible 분리`, `SHOT`, `ethnicities`, `무료/충전 크레딧 분리`)

---

## Entity Relationship Diagram

```mermaid
erDiagram
    aidols ||--o{ companions : "has members (casted)"
    aidols ||--o{ aidol_highlights : "owns"
    aidols ||--o{ aidol_leads : "has leads (logical reference)"
    aidols ||--o{ aidol_feeds : "owns feed contents"

    aidol_highlights ||--|{ highlight_messages : "contains"

    companions ||--o{ highlight_messages : "sends"

    companions ||--o{ chatrooms : "has chatrooms"
    companions ||--o{ practices : "has practice results"
    companions ||--o{ credits : "uses credits"

    chatrooms ||--o{ messages : "has messages"

    companions ||--o{ companion_relationships : "forms (from)"
    companions ||--o{ companion_relationships : "forms (to)"
    practices ||--o| collectibles : "creates collectible"
    practices ||--o{ practice_credits : "linked credit entries"
    credits ||--|| practice_credits : "consume/refund subtype (JTI)"
    collectibles ||--o| photocard_collectibles : "photocard subtype"
    collectibles ||--o| shot_collectibles : "shot subtype"

    aidols {
        string id PK
        string name
        string email "Optional"
        string greeting "인사 문구"
        string concept
        string profile_image_url
        string anonymous_id "쿠키: aioia_anonymous_id"
        string status "Enum: DRAFT, PUBLISHED"
        datetime created_at
        datetime updated_at
    }

    companions {
        string id PK
        string aidol_id FK "NULL: 연습생 / NOT NULL: 캐스팅됨"
        string name
        string gender "Enum: MALE, FEMALE"
        string[] ethnicities "1~2개 선택"
        string grade "Enum: F, D, C, B, A / based on stats total"
        string position "Enum: MAIN_VOCAL, etc."
        text biography
        string profile_picture_url
        text system_prompt
        int mbti_energy "1-10 (E - I)"
        int mbti_perception "1-10 (N - S)"
        int mbti_judgment "1-10 (T - F)"
        int mbti_lifestyle "1-10 (P - J)"
        int vocal "0-200"
        int dance "0-200"
        int rap "0-200"
        int visual "0-200"
        int stamina "0-200"
        int charm "0-200"
        string status "Enum: PUBLISHED, DRAFT"
        datetime created_at
        datetime updated_at
    }

    practices {
        string id PK
        string companion_id FK "NOT NULL, IX"
        string type "Enum: PHOTOCARD, SHOT / future types TBD"
        string variant "PHOTOCARD: SCHOOL_LIFE|FINGER_HEART|DAILY|RANDOM / SHOT: SIDE|FULL / others TBD"
        string mode "Enum: FIXED, RANDOM"
        string result_grade "Enum: MISS, NORMAL, GREAT, JACKPOT / NULLABLE, COMPLETED + RANDOM only"
        string status "Enum: PENDING, COMPLETED, FAILED"
        bool is_near_miss "default false"
        int vocal_delta "NULLABLE"
        int dance_delta "NULLABLE"
        int rap_delta "NULLABLE"
        int visual_delta "NULLABLE"
        int stamina_delta "NULLABLE"
        int charm_delta "NULLABLE"
        datetime created_at
        datetime updated_at
    }

    collectibles {
        string id PK
        string practice_id FK "UNIQUE, NOT NULL"
        string type "Enum: PHOTOCARD, SHOT / linked practices.type와 동일"
        datetime deleted_at "NULLABLE, soft delete"
        datetime created_at
    }

    photocard_collectibles {
        string collectible_id PK, FK
        string image_url "NOT NULL"
        string serial_number "UNIQUE"
    }

    shot_collectibles {
        string collectible_id PK, FK
        string image_url "NOT NULL"
        string serial_number "UNIQUE"
    }

    credits {
        string id PK
        string type "Enum: RECHARGE_GRANT, CONSUME, REFUND"
        int amount "signed ledger amount"
        string anonymous_id "NOT NULL, IX"
        string companion_id FK "NULLABLE, IX"
        datetime created_at
    }

    practice_credits {
        string id PK, FK
        string practice_id FK "NOT NULL, IX"
    }

    chatrooms {
        string id PK
        string companion_id FK "NOT NULL, IX"
        string name "NOT NULL"
        string anonymous_id "NULLABLE, IX"
        string language
        datetime created_at
        datetime updated_at
    }

    messages {
        string id PK
        string chatroom_id FK "NOT NULL, IX"
        string sender_type "Enum: USER, COMPANION"
        text content "NOT NULL"
        string anonymous_id "NULLABLE, IX"
        string companion_id "NULLABLE, IX (NO FK)"
        datetime created_at
        datetime updated_at
    }

    aidol_leads {
        string id PK
        string aidol_id "NOT NULL, NO FK"
        string email "NOT NULL"
        datetime created_at
        datetime updated_at
    }

    aidol_highlights {
        string id PK
        string aidol_id FK, IX
        string title
        string thumbnail_url
        string subtitle
        bool is_premium
    }

    highlight_messages {
        string id PK
        string highlight_id FK, IX
        string companion_id FK, IX
        int sequence
        text content
    }

    companion_relationships {
        string id PK
        string from_companion_id FK, IX
        string to_companion_id FK, IX
        int intimacy
        string nickname
    }

    aidol_feeds {
        string id PK
        string aidol_id FK, NOT NULL, IX
        string media_type "Enum: IMAGE, VIDEO"
        string media_url
        string thumbnail_url "NULLABLE, VIDEO 타입일 경우 필수"
        datetime created_at
        datetime updated_at
    }
```

---

## 테이블 요약

| 테이블                    | 설명                     | Sprint |
| ------------------------- | ------------------------ | ------ |
| `aidols`                  | 아이돌 그룹              | 1      |
| `companions`              | 그룹 멤버                | 1      |
| `aidol_leads`             | Viewer 정보              | 1      |
| `aidol_highlights`        | 아이돌 하이라이트        | 2      |
| `highlight_messages`      | 하이라이트 메세지        | 2      |
| `companion_relationships` | 멤버 관계 설정           | 2      |
| `chatrooms`               | 채팅방                   | 3      |
| `messages`                | 메시지                   | 3      |
| `aidol_feeds`             | 피드 콘텐츠              | 4      |
| `credits`                 | 크레딧 원장 base (JTI)   | 5      |
| `practices`               | 연습 결과 base           | 6      |
| `collectibles`            | 연습 산출물 공통 메타    | 6      |
| `photocard_collectibles`  | 포토카드 산출물 subtype  | 6      |
| `shot_collectibles`       | 샷 산출물 subtype        | 6      |
| `practice_credits`        | 연습 소비/환불 subtype   | 6      |

---

## 관계

| 관계                                  | 설명                                         |
| ------------------------------------- | -------------------------------------------- |
| aidols → companions                   | 1:N (그룹당 여러 멤버)                       |
| aidols → aidol_highlights             | 1:N (그룹당 여러 하이라이트)                 |
| aidols → aidol_leads                  | 1:N (그룹당 여러 viewer, DB FK는 없음)       |
| aidols → aidol_feeds                  | 1:N (그룹당 여러 피드)                       |
| aidol_highlights → highlight_messages | 1:N (하이라이트당 여러 하이라이트 메세지)    |
| companions → highlight_messages       | 1:N (멤버당 여러 하이라이트 메세지)          |
| companions → chatrooms                | 1:N (멤버당 여러 채팅방)                     |
| companions → practices                | 1:N (멤버당 여러 연습 결과)                  |
| companions → credits                  | 1:N (멤버에 귀속된 소비/환불 크레딧)         |
| companions → companion_relationships  | 1:N (한 멤버당 여러 관계)                    |
| chatrooms → messages                  | 1:N (채팅방당 여러 메시지)                   |
| practices → collectibles              | 1:0..1 (하나의 연습은 최대 하나의 산출물 생성) |
| practices → practice_credits          | 1:N (하나의 practice에 연결된 credit entry)  |
| credits → practice_credits            | 1:1 (consume/refund subtype only, JTI)       |
| collectibles → photocard_collectibles | 1:0..1 (포토카드 산출물 상세)                |
| collectibles → shot_collectibles      | 1:0..1 (샷 산출물 상세)                      |

---

## 필드 상세

### aidols

| 필드              | 타입    | 제약     | 설명                                          |
| ----------------- | ------- | -------- | --------------------------------------------- |
| id                | UUID    | PK       | 자동 생성                                     |
| name              | str     | -        | 그룹명                                        |
| email             | str     | -        | Creator 이메일                                |
| greeting          | str     | -        | 인사 문구                                     |
| concept           | str     | -        | 그룹 컨셉                                     |
| profile_image_url | str     | -        | 엠블럼 이미지                                 |
| anonymous_id      | str(36) | -        | 익명 사용자 식별자 (쿠키: aioia_anonymous_id) |
| status            | str     | NOT NULL | 상태(DRAFT OR PUBLISHED)                      |

인덱스
  - 복합 인덱스: `ix_aidols_status_created_at_id_desc`: (`status`, `created_at`, `id`)

### aidol_leads

| 필드     | 타입 | 제약     | 설명                                      |
| -------- | ---- | -------- | ----------------------------------------- |
| id       | UUID | PK       | 자동 생성                                 |
| aidol_id | UUID | NOT NULL | 그룹 ID (애플리케이션 레벨 참조, FK 없음) |
| email    | str  | NOT NULL | Viewer 이메일                             |

인덱스
  - 없음

### companions

| 필드                | 타입     | 제약     | 설명                                                   |
| ------------------- | -------- | -------- | ------------------------------------------------------ |
| id                  | UUID     | PK       | 자동 생성                                              |
| aidol_id            | UUID     | FK, IX   | aidols 참조                                            |
| name                | str      | -        | 멤버 이름                                              |
| gender              | str      | -        | 성별                                                   |
| ethnicities         | str[]    | 1~2개    | 선택한 민족 배열                                       |
| grade               | str      | -        | 등급 (`F` \| `D` \| `C` \| `B` \| `A`, stats 합계 기반) |
| biography           | text     | -        | 성격 설명                                              |
| profile_picture_url | str      | -        | 프로필 이미지                                          |
| system_prompt       | text     | -        | LLM 시스템 프롬프트                                    |
| mbti_energy         | int      | 1-10     | E ↔ I                                                  |
| mbti_perception     | int      | 1-10     | S ↔ N                                                  |
| mbti_judgment       | int      | 1-10     | T ↔ F                                                  |
| mbti_lifestyle      | int      | 1-10     | J ↔ P                                                  |
| vocal               | int      | 0-200    | 가창력                                                 |
| dance               | int      | 0-200    | 댄스 실력                                              |
| rap                 | int      | 0-200    | 랩 실력                                                |
| visual              | int      | 0-200    | 비주얼                                                 |
| stamina             | int      | 0-200    | 체력                                                   |
| charm               | int      | 0-200    | 매력도                                                 |
| position            | str      | -        | 포지션                                                 |
| status              | str      | NOT NULL | 상태(PUBLISHED OR DRAFT)                               |

참고
  - `companions.vocal`, `dance`, `rap`, `visual`, `stamina`, `charm`은 완료된 Practice 누적 결과를 반영한 현재 상태 값입니다.
  - `companions.grade`는 현재 스탯 합계 기반 파생 값입니다.

인덱스
  - 단일 컬럼 인덱스: `aidol_id`

### practices

| 필드          | 타입     | 제약                    | 설명                                                                  |
| ------------- | -------- | ----------------------- | --------------------------------------------------------------------- |
| id            | UUID     | PK                      | 자동 생성                                                             |
| companion_id  | UUID     | FK, IX, NOT NULL        | companions 참조                                                       |
| type          | str      | NOT NULL                | 연습 종류 (`PHOTOCARD` \| `SHOT`, 이후 타입 TBD)                      |
| variant       | str      | NOT NULL                | type별 세부 옵션 (`SCHOOL_LIFE`, `FINGER_HEART`, `DAILY`, `RANDOM`, `SIDE`, `FULL`, 기타 TBD) |
| mode          | str      | NOT NULL                | `FIXED` \| `RANDOM`                                                   |
| result_grade  | str      | NULLABLE                | 결과 판정 (`MISS` \| `NORMAL` \| `GREAT` \| `JACKPOT`, `COMPLETED` + `RANDOM`에서만 값 존재) |
| status        | str      | NOT NULL                | 상태(`PENDING` \| `COMPLETED` \| `FAILED`)                            |
| is_near_miss  | bool     | NOT NULL, default false | Near-Miss 연출 여부                                                   |
| vocal_delta   | int      | NULLABLE                | 이번 연습으로 변화한 vocal                                            |
| dance_delta   | int      | NULLABLE                | 이번 연습으로 변화한 dance                                            |
| rap_delta     | int      | NULLABLE                | 이번 연습으로 변화한 rap                                              |
| visual_delta  | int      | NULLABLE                | 이번 연습으로 변화한 visual                                           |
| stamina_delta | int      | NULLABLE                | 이번 연습으로 변화한 stamina                                          |
| charm_delta   | int      | NULLABLE                | 이번 연습으로 변화한 charm                                            |
| created_at    | datetime | NOT NULL                | 생성 시간                                                             |
| updated_at    | datetime | NOT NULL                | 수정 시간                                                             |

참고
  - `PHOTOCARD`와 `SHOT`은 동일한 연습 엔터티에서 `type + variant`로 구분합니다.
  - `result_grade`는 `COMPLETED` 상태의 `RANDOM` 모드에서만 값이 존재합니다.
  - `PENDING`, `FAILED`, `FIXED` 모드에서는 `result_grade`가 NULL 입니다.
  - 모든 `*_delta` 필드는 NULLABLE 입니다.
  - `PENDING`, `FAILED` 상태에서는 모든 `*_delta`가 NULL 입니다.
  - `COMPLETED` 상태에서도 `type`별 스탯 적립 정책에 따라 일부 `*_delta`는 NULL 일 수 있습니다.
  - 이 경우 NULL은 값 미정이 아니라, 해당 타입에 비적용인 스탯을 의미합니다.
  - 예: 현재 `SHOT`의 `charm_delta`는 `COMPLETED` 상태에서도 NULL 입니다.
  - 실패한 Practice는 기록으로 남고, Collectible은 생성되지 않습니다.
  - AI 생성 또는 완료 처리 실패 시 Practice는 삭제되지 않고 `FAILED` 상태로 유지됩니다.
  - 이후 연습 타입이 추가되면 해당 타입 전용 Collectible subtype을 추가하는 방식으로 확장할 수 있습니다.

인덱스
  - 단일 컬럼 인덱스: `companion_id`
  - 복합 인덱스: `ix_practices_companion_type_created_desc`: (`companion_id`, `type`, `created_at`)

### collectibles

| 필드          | 타입     | 제약             | 설명                                     |
| ------------- | -------- | ---------------- | ---------------------------------------- |
| id            | UUID     | PK               | 자동 생성                                |
| practice_id   | UUID     | FK, UNIQUE       | practices.id 참조                        |
| type          | str      | NOT NULL         | 산출물 종류 (`PHOTOCARD` \| `SHOT`)     |
| deleted_at    | datetime | -                | 산출물 삭제 시각 (soft delete, 스탯은 유지) |
| created_at    | datetime | NOT NULL         | 생성 시간                                |

참고
  - `collectibles`는 완료된 Practice 산출물만 저장합니다.
  - 삭제해도 해당 Practice로 획득한 스탯은 유지됩니다.
  - `collectibles.type`은 산출물 subtype 구분 및 조회 필터링을 위한 컬럼이며, linked `practices.type`과 동일해야 합니다.
  - `variant`, `mode`, `result_grade`, `stat_delta`의 정본은 `practices`를 참조합니다.
  - 실제 미디어 URL과 `serial_number`는 공통 테이블이 아니라 도메인 subtype 테이블에 저장합니다.
  - 각 `collectible`에는 `collectibles.type`에 대응하는 subtype row가 정확히 하나 존재하며, 이 제약은 mermaid ERD에 직접 표현되지 않습니다.
  - 현재는 `photocard_collectibles`, `shot_collectibles`만 정의하며, 이후 subtype은 TBD 입니다.

인덱스
  - 복합 인덱스: `ix_collectibles_type_created_desc`: (`type`, `created_at`)

### photocard_collectibles

| 필드          | 타입 | 제약   | 설명                      |
| ------------- | ---- | ------ | ------------------------- |
| collectible_id | UUID | PK, FK | collectibles.id 참조      |
| image_url     | str  | NOT NULL | 포토카드 이미지 URL     |
| serial_number | str  | UNIQUE | 포토카드 시리얼 번호     |

참고
  - `PHOTOCARD` 타입 산출물을 저장합니다.

인덱스
  - 없음

### shot_collectibles

| 필드          | 타입 | 제약   | 설명                 |
| ------------- | ---- | ------ | -------------------- |
| collectible_id | UUID | PK, FK | collectibles.id 참조 |
| image_url     | str  | NOT NULL | 샷 이미지 URL       |
| serial_number | str  | UNIQUE | 샷 시리얼 번호       |

참고
  - `SHOT` 타입 산출물을 저장합니다.

인덱스
  - 없음

### credits

| 필드         | 타입     | 제약             | 설명                                          |
| ------------ | -------- | ---------------- | --------------------------------------------- |
| id           | UUID     | PK               | 자동 생성                                     |
| type         | str      | NOT NULL         | `RECHARGE_GRANT` \| `CONSUME` \| `REFUND`     |
| amount       | int      | NOT NULL         | 원장 증감량 (충전/환불 `+`, 소비 `-`)         |
| anonymous_id | str(36)  | NOT NULL, IX     | 사용자 단위 식별자                            |
| companion_id | UUID     | FK, IX, NULLABLE | 소비/환불이 귀속된 companion, recharge는 NULL |
| created_at   | datetime | NOT NULL         | 엔트리 생성 시간                              |

참고
  - 무료 크레딧은 `credits` 엔트리로 저장하지 않고 비즈니스 규칙으로 계산합니다.
  - 무료 소진 계산 단위는 `companion_id + practices.type` 입니다.
  - 무료 사용량은 `practice_credits`가 없는 Practice 중 `COMPLETED` 상태만 카운트하며, `PENDING`, `FAILED`는 제외합니다.
  - 무료 크레딧 잔여량은 `max(3 - count(COMPLETED 무료 Practice), 0)` 이며, 무료 Practice는 동일 `companion_id + type` 범위의 `practice_credits`가 없는 Practice를 의미합니다.
  - `RECHARGE_GRANT`는 사용자 단위 공유 풀입니다.
  - `companion_id`는 `RECHARGE_GRANT`에서 NULLABLE 입니다.

인덱스
  - 단일 컬럼 인덱스: `anonymous_id`
  - 단일 컬럼 인덱스: `companion_id`
  - 복합 인덱스: `ix_credits_anonymous_type_created_desc`: (`anonymous_id`, `type`, `created_at`)
  - 복합 인덱스: `ix_credits_companion_type_created_desc`: (`companion_id`, `type`, `created_at`)

### practice_credits

| 필드       | 타입 | 제약             | 설명               |
| ---------- | ---- | ---------------- | ------------------ |
| id         | UUID | PK, FK           | credits.id 참조    |
| practice_id | UUID | FK, IX, NOT NULL | practices.id 참조  |

참고
  - `practice_credits`는 `CONSUME`, `REFUND` 엔트리에만 존재합니다.
  - 무료 크레딧 사용 Practice는 `practice_credits`가 생성되지 않습니다.
  - 유료 크레딧 사용 Practice가 실패하면, 동일 Practice에 연결된 `CONSUME` 이후 `REFUND` 엔트리가 추가될 수 있습니다.
  - 하나의 Practice에는 `CONSUME`, `REFUND`가 모두 연결될 수 있으므로 `practice_id`는 UNIQUE가 아닙니다.

인덱스
  - 단일 컬럼 인덱스: `practice_id`

### aidol_highlights

| 필드          | 타입 | 제약                    | 설명          |
| ------------- | ---- | ----------------------- | ------------- |
| id            | UUID | PK                      | 자동 생성     |
| aidol_id      | UUID | FK, IX                  | aidols 참조   |
| title         | str  | NOT NULL                | 제목          |
| thumbnail_url | str  | NOT NULL                | 썸네일 이미지 |
| subtitle      | str  | NOT NULL                | 부제목        |
| is_premium    | bool | NOT NULL, default false | 프리미엄 여부 |

인덱스
  - 단일 컬럼 인덱스: `aidol_id`
  - 복합 인덱스: `ix_aidol_highlights_aidol_id_premium_created_id_desc`: (`aidol_id`, `is_premium`, `created_at`, `id`)

### highlight_messages

| 필드         | 타입 | 제약     | 설명                  |
| ------------ | ---- | -------- | --------------------- |
| id           | UUID | PK       | 자동 생성             |
| highlight_id | UUID | FK, IX   | aidol_highlights 참조 |
| companion_id | UUID | FK, IX   | companions 참조       |
| sequence     | int  | NOT NULL | 채팅 순서             |
| content      | text | NOT NULL | 메세지 내용           |

인덱스
  - 단일 컬럼 인덱스: `highlight_id`
  - 단일 컬럼 인덱스: `companion_id`

### companion_relationships

| 필드              | 타입 | 제약   | 설명            |
| ----------------- | ---- | ------ | --------------- |
| id                | UUID | PK     | 자동 생성       |
| from_companion_id | UUID | FK, IX | companions 참조 |
| to_companion_id   | UUID | FK, IX | companions 참조 |
| intimacy          | int  | -      | 친밀도          |
| nickname          | str  | -      | 관계 별명       |

인덱스
  - 단일 컬럼 인덱스: `from_companion_id`
  - 단일 컬럼 인덱스: `to_companion_id`

### chatrooms

| 필드         | 타입    | 제약             | 설명                                          |
| ------------ | ------- | ---------------- | --------------------------------------------- |
| id           | UUID    | PK               | 자동 생성                                     |
| companion_id | UUID    | FK, IX, NOT NULL | companions 참조                               |
| name         | str     | NOT NULL         | 채팅방 이름                                   |
| anonymous_id | str(36) | IX               | 익명 사용자 식별자 (쿠키: aioia_anonymous_id) |
| language     | str     | NOT NULL         | 언어 코드                                     |

인덱스
  - 단일 컬럼 인덱스: `companion_id`
  - 단일 컬럼 인덱스: `anonymous_id`

### messages

| 필드         | 타입    | 제약             | 설명                                          |
| ------------ | ------- | ---------------- | --------------------------------------------- |
| id           | UUID    | PK               | 자동 생성                                     |
| chatroom_id  | UUID    | FK, IX, NOT NULL | chatrooms 참조                                |
| sender_type  | str     | NOT NULL         | "USER" \| "COMPANION"                         |
| content      | text    | NOT NULL         | 메시지 내용                                   |
| anonymous_id | str(36) |                  | 익명 사용자 식별자 (쿠키: aioia_anonymous_id) |
| companion_id | UUID    | IX               | 이전 대화를 불러오기 위한 companion 식별자    |

인덱스
  - 단일 컬럼 인덱스: `chatroom_id`
  - 단일 컬럼 인덱스: `companion_id`
  - 복합 인덱스: `ix_messages_chatroom_created`: (`chatroom_id`, `created_at`)
  - 복합 인덱스: `ix_messages_thread_created`: (`thread_id`, `created_at`)

### aidol_feeds

| 필드          | 타입     | 제약             | 설명                           |
| ------------- | -------- | ---------------- | ------------------------------ |
| id            | UUID     | PK               | 자동 생성                      |
| aidol_id      | UUID     | FK, IX, NOT NULL | aidols 참조                    |
| media_type    | str      | NOT NULL         | "IMAGE" \| "VIDEO"             |
| media_url     | str      | NOT NULL         | 미디어 URL                     |
| thumbnail_url | str      |                  | 썸네일 URL (VIDEO일 경우 필수) |
| created_at    | datetime | NOT NULL         | 생성 시간                      |
| updated_at    | datetime | NOT NULL         | 수정 시간                      |

인덱스
  - 단일 컬럼 인덱스: `aidol_id`
  - 복합 인덱스: `ix_aidol_feeds_aidol_created_id_desc`: (`aidol_id`, `created_at`, `id`)
