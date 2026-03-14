#!/usr/bin/env node
/**
 * Fireflies Transcript → LLM 요약 → Meeting Note PR
 *
 * 1. Fireflies API에서 트랜스크립트 가져오기 (retry until ready)
 * 2. LLM API로 미팅록 요약 (OpenAI or Anthropic, 환경변수로 선택)
 * 3. GitHub PR 생성
 */

const https = require('https');
const { execSync } = require('child_process');
const fs = require('fs');

const MEETING_ID = process.env.MEETING_ID;
const FIREFLIES_API_KEY = process.env.FIREFLIES_API_KEY;

// ─── config ─────────────────────────────────────────────────────
const MIN_TRANSCRIPT_SENTENCES = 10;
const MIN_TRANSCRIPT_DURATION_SEC = 60;
const MAX_TRANSCRIPT_CHARS = 180_000;
const LLM_MAX_TOKENS = 8192;

// LLM provider: "openai" (default) or "anthropic"
const LLM_PROVIDER = (process.env.LLM_PROVIDER || 'openai').toLowerCase();

// OpenAI config
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-5.4';

// Anthropic config
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_MODEL = process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-20250514';
const ANTHROPIC_VERSION = '2023-06-01';

// 팀원 이름 목록 (환경변수로 오버라이드 가능)
const TEAM_NAMES = process.env.MEETING_PARTICIPANT_NAMES
  || '소연, 수지, 영욱, 제이, 미지, 채연, 은재, 재형, 지영';

// ─── helpers ────────────────────────────────────────────────────
function httpsPost(hostname, path, headers, body) {
  return new Promise((resolve, reject) => {
    const req = https.request({ hostname, path, method: 'POST', headers }, res => {
      let data = '';
      res.on('data', c => (data += c));
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse error: ${e.message}\n${data.slice(0, 500)}`)); }
      });
    });
    req.on('error', reject);
    req.write(typeof body === 'string' ? body : JSON.stringify(body));
    req.end();
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function getOpenAITokenLimitParams(model) {
  return /^gpt-5(?:[.-]|$)/i.test(model)
    ? { max_completion_tokens: LLM_MAX_TOKENS }
    : { max_tokens: LLM_MAX_TOKENS };
}

// ─── Fireflies GraphQL (with retry) ────────────────────────────
async function getTranscript(meetingId, maxRetries = 6) {
  const query = `
    query Transcript($transcriptId: String!) {
      transcript(id: $transcriptId) {
        id title date duration participants
        summary { overview action_items keywords }
        sentences { speaker_name text start_time end_time }
      }
    }`;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    console.log(`[Fireflies] attempt ${attempt}/${maxRetries} …`);
    const json = await httpsPost(
      'api.fireflies.ai', '/graphql',
      { Authorization: `Bearer ${FIREFLIES_API_KEY}`, 'Content-Type': 'application/json' },
      { query, variables: { transcriptId: meetingId } }
    );

    if (json.errors) throw new Error(json.errors[0].message);
    const t = json.data?.transcript;

    if (t && t.sentences && t.sentences.length > MIN_TRANSCRIPT_SENTENCES && t.duration > MIN_TRANSCRIPT_DURATION_SEC) {
      console.log(`[Fireflies] ✅ transcript ready — ${t.sentences.length} sentences, ${Math.round(t.duration / 60)}min`);
      return t;
    }

    if (attempt < maxRetries) {
      const waitSec = attempt * 60;
      console.log(`[Fireflies] ⏳ transcript not ready yet (sentences=${t?.sentences?.length || 0}, duration=${t?.duration || 0}). Waiting ${waitSec}s …`);
      await sleep(waitSec * 1000);
    }
  }

  throw new Error('Transcript not ready after all retries');
}

// ─── Build prompt ───────────────────────────────────────────────
function buildPrompt(transcript) {
  const lines = transcript.sentences.map(s => `${s.speaker_name}: ${s.text}`);
  const fullText = lines.join('\n');

  let transcriptText = fullText;
  if (fullText.length > MAX_TRANSCRIPT_CHARS) {
    const half = Math.floor(MAX_TRANSCRIPT_CHARS / 2);
    transcriptText = fullText.slice(0, half) + '\n\n[… 중간 생략 …]\n\n' + fullText.slice(-half);
  }

  const dateObj = new Date(transcript.date);
  const dateStr = `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')}`;
  const durationMin = Math.round(transcript.duration / 60);
  const participants = transcript.participants?.join(', ') || 'Unknown';

  const systemPrompt = '당신은 스타트업 AIdol 팀의 미팅록 작성자입니다. 회의 기록을 분석하여 정확하고 꼼꼼한 미팅록을 작성해주세요.';

  const userPrompt = `첨부한 회의 기록을 가지고 미팅록을 아주 꼼꼼히 각 참가자가 해야 할 일들이나 의사 결정한 내용들을 아래 형식으로 정리해주세요!

## 회의 정보
- 제목: ${transcript.title}
- 일시: ${dateStr} (약 ${durationMin}분)
- 참석자: ${participants}

## 출력 형식 (이 형식을 정확히 따라주세요)

> TL;DR
> - [한 줄 요약]

## 요약
- ...
- ...

## 결정 사항
- ...

## 액션 아이템
| # | 액션 아이템 | 담당 | 마감일 | 상태 |
|---|-------------|------|--------|------|
| 1 | | | | ☐ |

※ 잡담/중복/의견 나열은 모두 제거하고,
※ "누가 무엇을 언제까지 할지"를 가장 먼저, 가장 또렷하게 보여줘.
※ 담당자 이름은 성(이) 없이 이름(${TEAM_NAMES})으로 표기.

---

<회의 기록>
${transcriptText}
</회의 기록>`;

  return { systemPrompt, userPrompt, charCount: transcriptText.length };
}

// ─── OpenAI API ─────────────────────────────────────────────────
async function summarizeWithOpenAI(transcript) {
  const { systemPrompt, userPrompt, charCount } = buildPrompt(transcript);
  console.log(`[OpenAI] Sending ${charCount} chars to ${OPENAI_MODEL} …`);

  const json = await httpsPost(
    'api.openai.com', '/v1/chat/completions',
    {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    },
    {
      model: OPENAI_MODEL,
      ...getOpenAITokenLimitParams(OPENAI_MODEL),
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ]
    }
  );

  if (json.error) throw new Error(`OpenAI API error: ${json.error.message}`);

  const summary = json.choices?.[0]?.message?.content;
  if (!summary) throw new Error('OpenAI returned empty response');

  console.log(`[OpenAI] ✅ Got ${summary.length} chars summary (model: ${json.model})`);
  return { summary, model: json.model || OPENAI_MODEL };
}

// ─── Anthropic API ──────────────────────────────────────────────
async function summarizeWithAnthropic(transcript) {
  const { systemPrompt, userPrompt, charCount } = buildPrompt(transcript);
  console.log(`[Anthropic] Sending ${charCount} chars to ${ANTHROPIC_MODEL} …`);

  const json = await httpsPost(
    'api.anthropic.com', '/v1/messages',
    {
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': ANTHROPIC_VERSION,
      'content-type': 'application/json'
    },
    {
      model: ANTHROPIC_MODEL,
      max_tokens: LLM_MAX_TOKENS,
      system: systemPrompt,
      messages: [{ role: 'user', content: userPrompt }]
    }
  );

  if (json.error) throw new Error(`Anthropic API error: ${json.error.message}`);

  const summary = json.content?.[0]?.text;
  if (!summary) throw new Error('Anthropic returned empty response');

  console.log(`[Anthropic] ✅ Got ${summary.length} chars summary`);
  return { summary, model: ANTHROPIC_MODEL };
}

// ─── LLM dispatch ───────────────────────────────────────────────
async function summarize(transcript) {
  if (LLM_PROVIDER === 'anthropic') {
    if (!ANTHROPIC_API_KEY) throw new Error('Missing ANTHROPIC_API_KEY');
    return summarizeWithAnthropic(transcript);
  } else {
    if (!OPENAI_API_KEY) throw new Error('Missing OPENAI_API_KEY');
    return summarizeWithOpenAI(transcript);
  }
}

// ─── Generate Meeting Note ──────────────────────────────────────
function generateMeetingNote(transcript, summary, model) {
  const date = new Date(transcript.date);
  const dateStr = date.toISOString().slice(0, 10).replace(/-/g, '');
  const dateFormatted = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
  const dayNames = ['일', '월', '화', '수', '목', '금', '토'];
  const dayName = dayNames[date.getDay()];

  const durationMin = Math.round(transcript.duration / 60);
  const participants = transcript.participants?.join(', ') || 'Unknown';
  const keywords = transcript.summary?.keywords || [];

  const titleSlug = transcript.title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 50);

  const filename = `${dateStr.slice(2)}-${titleSlug}.md`;

  const content = `# ${transcript.title}

- 일시: ${dateFormatted} (${dayName}) 약 ${durationMin}분
- 참석자: ${participants}

---

${summary}

---

**키워드**: ${keywords.map(k => `\`${k}\``).join(', ') || '(없음)'}

*이 미팅 노트는 Fireflies.ai 트랜스크립트 + ${model} 요약으로 자동 생성되었습니다.*
`;

  return { filename, content, model };
}

// ─── Create PR ──────────────────────────────────────────────────
function createPR(filename, content, model) {
  const branchName = `meeting-notes/${filename.replace('.md', '')}`;
  const filePath = `meetings/${filename}`;

  execSync('git config user.name "github-actions[bot]"');
  execSync('git config user.email "github-actions[bot]@users.noreply.github.com"');

  execSync(`git checkout -b "${branchName}"`);

  fs.mkdirSync('meetings', { recursive: true });
  fs.writeFileSync(filePath, content);

  execSync(`git add "${filePath}"`);
  execSync(`git commit -m "docs: ${filename}"`);
  execSync(`git push -u origin "${branchName}"`);

  const prBody = `## 🎙️ Fireflies 자동 미팅 노트

이 PR은 Fireflies 녹음 완료 후 자동으로 생성되었습니다.
- **트랜스크립트**: Fireflies.ai
- **요약**: ${model}

### 체크리스트
- [ ] 내용 확인
- [ ] 액션 아이템 검토
- [ ] 필요시 수정 후 머지`;

  execSync(`gh pr create --title "docs: ${filename}" --body-file - --base main`, { input: prBody });
  console.log(`✅ PR created for ${filename}`);
}

// ─── Main ───────────────────────────────────────────────────────
async function main() {
  if (!MEETING_ID) { console.error('Missing MEETING_ID'); process.exit(1); }
  if (!FIREFLIES_API_KEY) { console.error('Missing FIREFLIES_API_KEY'); process.exit(1); }

  console.log(`\n=== Fireflies → ${LLM_PROVIDER.toUpperCase()} → Meeting Note PR ===`);
  console.log(`Meeting ID: ${MEETING_ID}`);
  console.log(`LLM: ${LLM_PROVIDER === 'anthropic' ? ANTHROPIC_MODEL : OPENAI_MODEL}\n`);

  try {
    const transcript = await getTranscript(MEETING_ID);
    const { summary, model } = await summarize(transcript);
    const { filename, content } = generateMeetingNote(transcript, summary, model);
    console.log(`Generated note: ${filename}`);
    createPR(filename, content, model);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
