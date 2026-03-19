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
// 짧은 미팅도 처리하도록 기본값 완화 (sentences > 10, duration > 30초)
const MIN_TRANSCRIPT_SENTENCES = Number(process.env.MIN_TRANSCRIPT_SENTENCES || 10);
const MIN_TRANSCRIPT_DURATION_SEC = Number(process.env.MIN_TRANSCRIPT_DURATION_SEC || 30);
const MAX_TRANSCRIPT_CHARS = Number(process.env.MAX_TRANSCRIPT_CHARS || 180_000);
const LLM_MAX_TOKENS = Number(process.env.LLM_MAX_TOKENS || 8192);
const STABLE_POLLS_REQUIRED = Number(process.env.STABLE_POLLS_REQUIRED || 2);
const MAX_RETRIES = Number(process.env.TRANSCRIPT_MAX_RETRIES || 8);

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
// 주의: 이름 오타 주의! 미진(O) 미지(X), 현준(O) 현주(X), 제형(O) 재형(X), 은재(O) 은제(X)
const TEAM_NAMES = process.env.MEETING_PARTICIPANT_NAMES
  || '소연, 영욱, 제이, 수지, 은재, 채현, 제형, 지영, 미진, 시영, 현준, 다현';

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

function getTranscriptMetrics(transcript) {
  const sentenceCount = transcript?.sentences?.length || 0;
  const durationSec = transcript?.duration || 0;
  const overview = transcript?.summary?.overview?.trim() || '';
  const actionItems = transcript?.summary?.action_items || [];
  const keywords = transcript?.summary?.keywords || [];

  return {
    sentenceCount,
    durationSec,
    hasSummary: Boolean(overview || actionItems.length || keywords.length),
    overviewLength: overview.length,
    actionItemCount: actionItems.length,
    keywordCount: keywords.length
  };
}

function isTranscriptReady(metrics, prevMetrics, stablePolls) {
  const meetsMinimum =
    metrics.sentenceCount >= MIN_TRANSCRIPT_SENTENCES
    && metrics.durationSec >= MIN_TRANSCRIPT_DURATION_SEC
    && metrics.hasSummary;

  if (!meetsMinimum) return false;
  if (!prevMetrics) return false;

  const sentenceGrowth = metrics.sentenceCount - prevMetrics.sentenceCount;
  const durationGrowth = metrics.durationSec - prevMetrics.durationSec;
  const summaryChanged =
    metrics.overviewLength !== prevMetrics.overviewLength
    || metrics.actionItemCount !== prevMetrics.actionItemCount
    || metrics.keywordCount !== prevMetrics.keywordCount;

  const stabilized = sentenceGrowth <= 3 && durationGrowth <= 10 && !summaryChanged;
  return stabilized && stablePolls >= STABLE_POLLS_REQUIRED;
}

function truncateTranscript(fullText) {
  if (fullText.length <= MAX_TRANSCRIPT_CHARS) {
    return { transcriptText: fullText, wasTruncated: false };
  }

  const headChars = Math.floor(MAX_TRANSCRIPT_CHARS * 0.35);
  const tailChars = Math.floor(MAX_TRANSCRIPT_CHARS * 0.25);
  const middleChars = MAX_TRANSCRIPT_CHARS - headChars - tailChars;
  const middleStart = Math.max(0, Math.floor((fullText.length - middleChars) / 2));

  const transcriptText = [
    fullText.slice(0, headChars),
    '\n\n[… 중간 일부 생략 …]\n\n',
    fullText.slice(middleStart, middleStart + middleChars),
    '\n\n[… 후반 일부 생략 …]\n\n',
    fullText.slice(-tailChars)
  ].join('');

  return { transcriptText, wasTruncated: true };
}
// ─── Fireflies GraphQL (with retry) ────────────────────────────
async function getTranscript(meetingId, maxRetries = MAX_RETRIES) {
  const query = `
    query Transcript($transcriptId: String!) {
      transcript(id: $transcriptId) {
        id title date duration participants
        summary { overview action_items keywords }
        sentences { speaker_name text start_time end_time }
      }
    }`;

  let prevMetrics = null;
  let stablePolls = 0;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    console.log(`[Fireflies] attempt ${attempt}/${maxRetries} …`);
    const json = await httpsPost(
      'api.fireflies.ai', '/graphql',
      { Authorization: `Bearer ${FIREFLIES_API_KEY}`, 'Content-Type': 'application/json' },
      { query, variables: { transcriptId: meetingId } }
    );

    if (json.errors) throw new Error(json.errors[0].message);
    const t = json.data?.transcript;
    const metrics = getTranscriptMetrics(t);

    if (prevMetrics) {
      const sentenceGrowth = metrics.sentenceCount - prevMetrics.sentenceCount;
      const durationGrowth = metrics.durationSec - prevMetrics.durationSec;
      const summaryChanged =
        metrics.overviewLength !== prevMetrics.overviewLength
        || metrics.actionItemCount !== prevMetrics.actionItemCount
        || metrics.keywordCount !== prevMetrics.keywordCount;

      if (sentenceGrowth <= 3 && durationGrowth <= 10 && !summaryChanged) {
        stablePolls += 1;
      } else {
        stablePolls = 0;
      }
    }

    // Ready 조건: sentences가 충분하면 OK (duration은 보조 체크만)
    // 짧은 미팅이라도 sentences > MIN_TRANSCRIPT_SENTENCES면 바로 처리
    const hasSentences = metrics.sentenceCount > MIN_TRANSCRIPT_SENTENCES;
    const hasDuration = metrics.durationSec >= MIN_TRANSCRIPT_DURATION_SEC;
    
    if (t && hasSentences && (hasDuration || isTranscriptReady(metrics, prevMetrics, stablePolls))) {
      console.log(`[Fireflies] ✅ transcript ready — ${metrics.sentenceCount} sentences, ${Math.round(metrics.durationSec / 60)}min, stablePolls=${stablePolls}`);
      return t;
    }

    if (attempt < maxRetries) {
      const waitSec = Math.min(90, 30 + attempt * 30);
      console.log(
        `[Fireflies] ⏳ transcript not ready yet `
        + `(sentences=${metrics.sentenceCount}, duration=${metrics.durationSec}, hasSummary=${metrics.hasSummary}, stablePolls=${stablePolls}/${STABLE_POLLS_REQUIRED}). Waiting ${waitSec}s …`
      );
      prevMetrics = metrics;
      await sleep(waitSec * 1000);
    }
  }

  throw new Error('Transcript not ready after all retries');
}

// ─── Build prompt ───────────────────────────────────────────────
function buildPrompt(transcript) {
  const lines = transcript.sentences.map(s => `${s.speaker_name}: ${s.text}`);
  const fullText = lines.join('\n');
  const { transcriptText, wasTruncated } = truncateTranscript(fullText);

  const dateObj = new Date(transcript.date);
  const dateStr = `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')}`;
  const durationMin = Math.round(transcript.duration / 60);
  const participants = transcript.participants?.join(', ') || 'Unknown';

  const ffOverview = transcript.summary?.overview?.trim();
  const rawActionItems = transcript.summary?.action_items;
  const ffActionItems = Array.isArray(rawActionItems) ? rawActionItems : [];
  const rawKeywords = transcript.summary?.keywords;
  const ffKeywords = Array.isArray(rawKeywords) ? rawKeywords : [];

  const systemPrompt = [
    '당신은 스타트업 AIdol 팀의 미팅록 작성자입니다.',
    '당신의 목표는 긴 회의 원문을 다시 써주는 것이 아니라, 의사결정·할 일·쟁점을 압축해서 읽기 쉬운 미팅록으로 만드는 것입니다.',
    '발화 순서 재현, 원문 길게 인용, 잡담 나열은 금지합니다.',
    '회의 제목, 참석자, 일반적인 업무 맥락만으로 의제를 추정하지 마세요.',
    '트랜스크립트에 명시적으로 없는 사실은 쓰지 마세요.',
    '결정 사항은 명시적 합의가 있을 때만 적고, 액션 아이템은 담당/할 일 근거가 분명할 때만 적으세요.'
  ].join(' ');

  const userPrompt = `첨부한 회의 기록을 바탕으로, 원문을 재현하지 말고 핵심만 압축한 미팅록을 작성해주세요.

## 회의 정보
- 제목: ${transcript.title}
- 일시: ${dateStr} (약 ${durationMin}분)
- 참석자: ${participants}
- 원문 길이: ${lines.length}개 발화${wasTruncated ? ' (너무 길어 일부만 발췌됨)' : ''}

## Fireflies 자동 요약 힌트
- overview: ${ffOverview || '(없음)'}
- action_items: ${ffActionItems.length ? ffActionItems.join(' | ') : '(없음)'}
- keywords: ${ffKeywords.length ? ffKeywords.join(', ') : '(없음)'}

※ 위 힌트는 참고용일 뿐이며, 트랜스크립트에 없는 사실을 보강하는 근거로 사용하면 안 됩니다.

## 출력 형식 (정확히 지켜주세요)

> TL;DR
> - 한 문장으로 회의 핵심만 요약

## 요약
- 2~5개 bullet만 작성
- 각 bullet은 "실제로 중요한 논의/공유/문제 인식"만 남기세요
- 발화 순서/대화체/군더더기 금지
- 잡담, 배경설명, 사족은 제거하세요

## 결정 사항
- 명시적으로 합의되거나 확정된 내용만 bullet로 정리
- 논의만 있었고 결론이 없으면 적지 마세요
- 결정이 없으면 "- 없음"이라고 작성

## 액션 아이템
| # | 액션 아이템 | 담당 | 마감일 | 상태 |
|---|-------------|------|--------|------|
| 1 | 없음 | - | - | - |

## 반드시 지킬 규칙
- 원문 문장을 길게 베끼지 마세요.
- 화자별 대본처럼 쓰지 마세요.
- 회의 제목만 보고 의제를 추정하지 마세요.
- 잡담, 중복, 탐색적 아이디어, 배경설명은 제거하세요.
- 중요해 보여도 트랜스크립트에 근거가 없으면 쓰지 마세요.
- 논의는 있었지만 결론이 없으면 "요약"에만 짧게 적고 "결정 사항"에는 넣지 마세요.
- "누가 무엇을 언제까지 할지"가 명확할 때만 액션 아이템으로 올리세요.
- 담당자 이름은 성(이) 없이 이름(${TEAM_NAMES})으로 표기하세요.
- 근거가 불충분한 추측은 쓰지 마세요.

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
      temperature: 0.2,
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
