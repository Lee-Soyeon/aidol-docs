# AIdol ERD

- 원본: [Notion](https://www.notion.so/2f046f96550480168a53f9f6a9f79d0b)

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
    companions ||--o{ trainings : "has training results"
    companions ||--o{ credits : "uses credits"
    
    chatrooms ||--o{ messages : "has messages"

    companions ||--o{ companion_relationships : "forms (from)"
    companions ||--o{ companion_relationships : "forms (to)"
    trainings ||--|| photocard_trainings : "photocard subtype (JTI)"
    trainings ||--o{ training_credits : "linked credit entries"
    credits ||--|| training_credits : "consume/refund subtype (JTI)"

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

    trainings {
        string id PK
        string companion_id FK "NOT NULL, IX"
        string type "Enum: photocard (Sprint 5), JTI discriminator"
        string draw_mode "Enum: FIXED, RANDOM"
        string result_grade "Enum: MISS, NORMAL, GREAT, JACKPOT / NULLABLE while PENDING"
        string status "Enum: PENDING, COMPLETED"
        bool is_near_miss "default false"
        int vocal_delta "NULLABLE while PENDING"
        int dance_delta "NULLABLE while PENDING"
        int rap_delta "NULLABLE while PENDING"
        int visual_delta "NULLABLE while PENDING"
        int stamina_delta "NULLABLE while PENDING"
        int charm_delta "NULLABLE while PENDING"
        datetime created_at
        datetime updated_at
    }

    photocard_trainings {
        string id PK, FK
        string image_url "NULLABLE while PENDING"
        string serial_number "UNIQUE, NULLABLE while PENDING"
        string concept "Enum: SCHOOL_LIFE, FINGER_HEART, DAILY, RANDOM"
        datetime deleted_at "NULLABLE, soft delete for collection card"
    }

    credits {
        string id PK
        string type "Enum: recharge_grant, consume, refund"
        int amount "signed ledger amount"
        string anonymous_id "NOT NULL, IX"
        string companion_id FK "NULLABLE, IX"
        datetime created_at
    }

    training_credits {
        string id PK, FK
        string training_id FK "NOT NULL, IX"
    }

    chatrooms {
        string id PK
        string companion_id FK "NOT NULL, IX"
        string name "NOT NULL"
        string anonymous_id "NULLABLE, IX"
        string language "default: ko"
        datetime created_at
        datetime updated_at
    }

    messages {
        string id PK
        string chatroom_id FK "NOT NULL"
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

| 테이블                    | 설명                       | Sprint |
| ------------------------- | -------------------------- | ------ |
| `aidols`                  | 아이돌 그룹                | 1      |
| `companions`              | 그룹 멤버                  | 1      |
| `aidol_leads`             | Viewer 정보                | 1      |
| `aidol_highlights`        | 아이돌 하이라이트          | 2      |
| `highlight_messages`      | 하이라이트 메세지          | 2      |
| `companion_relationships` | 멤버 관계 설정             | 2      |
| `chatrooms`               | 채팅방                     | 3      |
| `messages`                | 메시지                     | 3      |
| `aidol_feeds`             | 피드 콘텐츠                | 4      |
| `trainings`               | 트레이닝 결과 base (JTI)   | 5      |
| `photocard_trainings`     | 포토카드 트레이닝 subtype  | 5      |
| `credits`                 | 크레딧 원장 base (JTI)     | 5      |
| `training_credits`        | 트레이닝 소비/환불 subtype | 5      |

---

## 관계

| 관계                                  | 설명                                        |
| ------------------------------------- | ------------------------------------------- |
| aidols → companions                   | 1:N (그룹당 여러 멤버)                      |
| aidols → aidol_highlights             | 1:N (그룹당 여러 하이라이트)                |
| aidols → aidol_leads                  | 1:N (그룹당 여러 viewer, DB FK는 없음)      |
| aidols → aidol_feeds                  | 1:N (그룹당 여러 피드)                      |
| aidol_highlights → highlight_messages | 1:N (하이라이트당 여러 하이라이트 메세지)   |
| companions → highlight_messages       | 1:N (멤버당 여러 하이라이트 메세지)         |
| companions → chatrooms                | 1:N (멤버당 여러 채팅방)                    |
| companions → trainings                | 1:N (멤버당 여러 트레이닝 결과)             |
| companions → credits                  | 1:N (멤버에 귀속된 소비/환불 크레딧)        |
| companions → companion_relationships  | 1:N (한 멤버당 여러 관계)                   |
| chatrooms → messages                  | 1:N (채팅방당 여러 메시지)                  |
| trainings → photocard_trainings       | 1:1 (photocard subtype, JTI)                |
| trainings → training_credits          | 1:N (하나의 training에 연결된 credit entry) |
| credits → training_credits            | 1:1 (consume/refund subtype only, JTI)      |
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

### aidol_leads

| 필드     | 타입 | 제약     | 설명                                      |
| -------- | ---- | -------- | ----------------------------------------- |
| id       | UUID | PK       | 자동 생성                                 |
| aidol_id | UUID | NOT NULL | 그룹 ID (애플리케이션 레벨 참조, FK 없음) |
| email    | str  | NOT NULL | Viewer 이메일                             |

### companions

| 필드                | 타입 | 제약     | 설명                     |
| ------------------- | ---- | -------- | ------------------------ |
| id                  | UUID | PK       | 자동 생성                |
| aidol_id            | UUID | FK, IX   | aidols 참조              |
| name                | str  | -        | 멤버 이름                |
| gender              | str  | -        | 성별                     |
| grade               | str  | -        | 등급 (`F` \| `D` \| `C` \| `B` \| `A`, stats 합계 기반) |
| biography           | text | -        | 성격 설명                |
| profile_picture_url | str  | -        | 프로필 이미지            |
| system_prompt       | text | -        | LLM 시스템 프롬프트      |
| mbti_energy         | int  | 1-10     | E ↔ I                    |
| mbti_perception     | int  | 1-10     | S ↔ N                    |
| mbti_judgment       | int  | 1-10     | T ↔ F                    |
| mbti_lifestyle      | int  | 1-10     | J ↔ P                    |
| vocal               | int  | 0-200    | 가창력                   |
| dance               | int  | 0-200    | 댄스 실력                |
| rap                 | int  | 0-200    | 랩 실력                  |
| visual              | int  | 0-200    | 비주얼                   |
| stamina             | int  | 0-200    | 체력                     |
| charm               | int  | 0-200    | 매력도                   |
| position            | str  | -        | 포지션                   |
| status              | str  | NOT NULL | 상태(PUBLISHED OR DRAFT) |

### trainings

| 필드          | 타입     | 제약                    | 설명                                                   |
| ------------- | -------- | ----------------------- | ------------------------------------------------------ |
| id            | UUID     | PK                      | 자동 생성                                              |
| companion_id  | UUID     | FK, IX, NOT NULL        | companions 참조                                        |
| type          | str      | NOT NULL                | JTI discriminator (`photocard`)                        |
| draw_mode     | str      | NOT NULL                | `FIXED` \| `RANDOM`                                    |
| result_grade  | str      | -                       | 결과 판정 (`MISS` \| `NORMAL` \| `GREAT` \| `JACKPOT`) |
| status        | str      | NOT NULL                | 상태(`PENDING` \| `COMPLETED`)                         |
| is_near_miss  | bool     | NOT NULL, default false | Near-Miss 연출 여부                                    |
| vocal_delta   | int      | -                       | 이번 트레이닝으로 변화한 vocal                         |
| dance_delta   | int      | -                       | 이번 트레이닝으로 변화한 dance                         |
| rap_delta     | int      | -                       | 이번 트레이닝으로 변화한 rap                           |
| visual_delta  | int      | -                       | 이번 트레이닝으로 변화한 visual                        |
| stamina_delta | int      | -                       | 이번 트레이닝으로 변화한 stamina                       |
| charm_delta   | int      | -                       | 이번 트레이닝으로 변화한 charm                         |
| created_at    | datetime | NOT NULL                | 생성 시간                                              |
| updated_at    | datetime | NOT NULL                | 수정 시간                                              |

인덱스
  - `ix_trainings_companion_type_created_desc` (`companion_id`, `type`, `created_at` DESC)

### photocard_trainings

| 필드          | 타입     | 제약             | 설명                                                   |
| ------------- | -------- | ---------------- | ------------------------------------------------------ |
| id            | UUID     | PK, FK           | trainings.id 참조                                      |
| image_url     | str      | NULLABLE         | 생성된 포토카드 이미지 URL                             |
| serial_number | str      | UNIQUE, NULLABLE | 카드 시리얼 번호                                       |
| concept       | str      | NOT NULL         | `SCHOOL_LIFE` \| `FINGER_HEART` \| `DAILY` \| `RANDOM` |
| deleted_at    | datetime | -                | 카드 삭제 시각 (soft delete, 스탯은 유지)              |

참고
  - JTI 관계는 1:1로 유지합니다.
  - 다만 `trainings`가 `PENDING` 상태로 먼저 생성될 수 있으므로, 구현 방식에 따라 `photocard_trainings`의 결과 필드(`image_url`, `serial_number`)는 완료 전까지 일시적으로 NULL일 수 있습니다.

인덱스
  - `ux_photocard_trainings_serial_number` (`serial_number`, UNIQUE)

### credits

| 필드         | 타입     | 제약             | 설명                                          |
| ------------ | -------- | ---------------- | --------------------------------------------- |
| id           | UUID     | PK               | 자동 생성                                     |
| type         | str      | NOT NULL         | `recharge_grant` \| `consume` \| `refund`     |
| amount       | int      | NOT NULL         | 원장 증감량 (충전/환불 `+`, 소비 `-`)         |
| anonymous_id | str(36)  | NOT NULL, IX     | 사용자 단위 식별자                            |
| companion_id | UUID     | FK, IX, NULLABLE | 소비/환불이 귀속된 companion, recharge는 NULL |
| created_at   | datetime | NOT NULL         | 엔트리 생성 시간                              |

참고
  - 무료 3회는 credits 엔트리로 저장하지 않고 비즈니스 규칙 상수로 계산합니다.
  - 무료 소진 계산 단위는 `companion_id + trainings.type` 입니다.
  - `recharge_grant`는 사용자 단위 공유 풀입니다.
  - `companion_id`는 `recharge_grant`에서 NULLABLE 입니다. 충전은 특정 companion이 아니라 사용자 공용 풀에 적립되기 때문입니다.

인덱스
  - `ix_credits_anonymous_type_created_desc` (`anonymous_id`, `type`, `created_at` DESC)
  - `ix_credits_companion_type_created_desc` (`companion_id`, `type`, `created_at` DESC)

### training_credits

| 필드        | 타입 | 제약             | 설명              |
| ----------- | ---- | ---------------- | ----------------- |
| id          | UUID | PK, FK           | credits.id 참조   |
| training_id | UUID | FK, IX, NOT NULL | trainings.id 참조 |

참고
  - `training_credits`는 `consume`, `refund` 엔트리에만 존재합니다.
  - 하나의 training에는 `consume`, `refund`가 모두 연결될 수 있으므로 `training_id`는 UNIQUE가 아닙니다.

인덱스
  - `ix_training_credits_training_id` (`training_id`)

### aidol_highlights

| 필드          | 타입 | 제약                    | 설명          |
| ------------- | ---- | ----------------------- | ------------- |
| id            | UUID | PK                      | 자동 생성     |
| aidol_id      | UUID | FK, IX                  | aidols 참조   |
| title         | str  | NOT NULL                | 제목          |
| thumbnail_url | str  | NOT NULL                | 썸네일 이미지 |
| subtitle      | str  | NOT NULL                | 부제목        |
| is_premium    | bool | NOT NULL, default false | 프리미엄 여부 |

### highlight_messages

| 필드         | 타입 | 제약     | 설명                  |
| ------------ | ---- | -------- | --------------------- |
| id           | UUID | PK       | 자동 생성             |
| highlight_id | UUID | FK, IX   | aidol_highlights 참조 |
| companion_id | UUID | FK, IX   | companions 참조       |
| sequence     | int  | NOT NULL | 채팅 순서             |
| content      | text | NOT NULL | 메세지 내용           |

### companion_relationships

| 필드              | 타입 | 제약   | 설명            |
| ----------------- | ---- | ------ | --------------- |
| id                | UUID | PK     | 자동 생성       |
| from_companion_id | UUID | FK, IX | companions 참조 |
| to_companion_id   | UUID | FK, IX | companions 참조 |
| intimacy          | int  | -      | 친밀도          |
| nickname          | str  | -      | 관계 별명       |

### chatrooms
| 필드         | 타입    | 제약             | 설명                                          |
| ------------ | ------- | ---------------- | --------------------------------------------- |
| id           | UUID    | PK               | 자동 생성                                     |
| companion_id | UUID    | FK, IX, NOT NULL | companions 참조                               |
| name         | str     | NOT NULL         | 채팅방 이름                                   |
| anonymous_id | str(36) | IX               | 익명 사용자 식별자 (쿠키: aioia_anonymous_id) |
| language     | str     | NOT NULL         | 언어 (기본: "ko")                             |

### messages 

| 필드         | 타입    | 제약             | 설명                                          |
| ------------ | ------- | ---------------- | --------------------------------------------- |
| id           | UUID    | PK               | 자동 생성                                     |
| chatroom_id  | UUID    | FK, IX, NOT NULL | chatrooms 참조                                |
| sender_type  | str     | NOT NULL         | "USER" \| "COMPANION"                         |
| content      | text    | NOT NULL         | 메시지 내용                                   |
| anonymous_id | str(36) |                  | 익명 사용자 식별자 (쿠키: aioia_anonymous_id) |
| companion_id | UUID    | IX               | 이전 대화를 불러오기 위한 companion 식별자    |

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
  - `ix_aidol_feeds_aidol_created_id_desc` (`aidol_id`, `created_at` DESC, `id` DESC)
