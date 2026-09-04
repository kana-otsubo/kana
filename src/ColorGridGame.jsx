import { useState, useRef, useEffect, useCallback } from 'react'

// いろの まじわる マス（ざひょうとり）
// うえの いろ（たて）と ひだりの いろ（よこ）、ふたつが であう マスを さがす あそび。
// ・まちがえても ×・ブザー・shake は なし
// ・1かいめ … たての れつを たどる ヒント
// ・2かいめ … たて・よこ 両方の おびを 光らせる（交点は 光らせない）
// ・3かいめ … まじわる マスを 見せて つぎへ

const COLORS = {
  pink: { name: 'ピンク', base: '#ff8ab5', soft: '#ffdfec', ink: '#7c1743' },
  yellow: { name: 'きいろ', base: '#ffd23f', soft: '#fff3c9', ink: '#7a5400' },
  green: { name: 'みどり', base: '#6ed36e', soft: '#dbf6db', ink: '#14561a' },
  red: { name: 'あか', base: '#ff6b6b', soft: '#ffdedb', ink: '#7d1414' },
  blue: { name: 'あお', base: '#5aa9f7', soft: '#dbecff', ink: '#0b3f75' },
  purple: { name: 'むらさき', base: '#b18cf0', soft: '#eae0ff', ink: '#3f1d75' },
  orange: { name: 'オレンジ', base: '#ffa14d', soft: '#ffe7d1', ink: '#7a3a00' },
  lightblue: { name: 'みずいろ', base: '#6fd8e6', soft: '#d7f5fa', ink: '#0a5560' },
}

const LEVELS = [
  {
    label: 'レベル1',
    size: '2 × 2',
    note: 'はじめて',
    cols: ['pink', 'yellow'],
    rows: ['red', 'blue'],
  },
  {
    label: 'レベル2',
    size: '3 × 3',
    note: 'なれてきたら',
    cols: ['pink', 'yellow', 'green'],
    rows: ['red', 'blue', 'purple'],
  },
  {
    label: 'レベル3',
    size: '4 × 4',
    note: 'にた いろも',
    cols: ['pink', 'red', 'orange', 'purple'],
    rows: ['yellow', 'green', 'blue', 'lightblue'],
  },
]

const ROUND_LENGTH = 6

function makeQuestion(level, prev) {
  for (let i = 0; i < 20; i++) {
    const colIdx = Math.floor(Math.random() * level.cols.length)
    const rowIdx = Math.floor(Math.random() * level.rows.length)
    if (!prev || prev.colIdx !== colIdx || prev.rowIdx !== rowIdx) {
      return { colIdx, rowIdx }
    }
  }
  return { colIdx: 0, rowIdx: 0 }
}

function ColorWord({ id }) {
  const c = COLORS[id]
  return (
    <span className="color-word" style={{ background: c.soft, color: c.ink, borderColor: c.base }}>
      {c.name}
    </span>
  )
}

export default function ColorGridGame({ onExit }) {
  const [screen, setScreen] = useState('title') // 'title' | 'play' | 'finish'
  const [levelIdx, setLevelIdx] = useState(1)
  const [question, setQuestion] = useState(() => makeQuestion(LEVELS[1], null))
  const [qNum, setQNum] = useState(0)
  const [phase, setPhase] = useState('ask') // 'ask' | 'hint1' | 'hint2' | 'reveal' | 'correct'
  const [stars, setStars] = useState(0)
  const [soundOn, setSoundOn] = useState(true)

  const level = LEVELS[levelIdx]
  const timers = useRef([])
  const audioRef = useRef(null)

  const later = useCallback((fn, ms) => {
    timers.current.push(setTimeout(fn, ms))
  }, [])

  const clearTimers = useCallback(() => {
    timers.current.forEach(clearTimeout)
    timers.current = []
  }, [])

  useEffect(() => clearTimers, [clearTimers])

  const playTones = useCallback((notes) => {
    if (!soundOn) return
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext
      if (!Ctx) return
      if (!audioRef.current) audioRef.current = new Ctx()
      const ac = audioRef.current
      if (ac.state === 'suspended') ac.resume()
      notes.forEach(([freq, at, dur, vol]) => {
        const osc = ac.createOscillator()
        const gain = ac.createGain()
        osc.type = 'sine'
        osc.frequency.value = freq
        const t = ac.currentTime + at
        gain.gain.setValueAtTime(0.0001, t)
        gain.gain.exponentialRampToValueAtTime(vol, t + 0.02)
        gain.gain.exponentialRampToValueAtTime(0.0001, t + dur)
        osc.connect(gain)
        gain.connect(ac.destination)
        osc.start(t)
        osc.stop(t + dur + 0.05)
      })
    } catch {
      /* 音が でなくても あそべる */
    }
  }, [soundOn])

  const playTap = useCallback(() => playTones([[520, 0, 0.09, 0.06]]), [playTones])
  const playTrace = useCallback(() => playTones([[440, 0, 0.5, 0.05]]), [playTones])
  const playCorrect = useCallback(
    () => playTones([[784, 0, 0.16, 0.13], [988, 0.14, 0.16, 0.13], [1319, 0.28, 0.4, 0.12]]),
    [playTones],
  )

  const startLevel = (idx) => {
    clearTimers()
    setLevelIdx(idx)
    setQuestion(makeQuestion(LEVELS[idx], null))
    setQNum(0)
    setPhase('ask')
    setStars(0)
    setScreen('play')
  }

  const goNext = () => {
    if (qNum + 1 >= ROUND_LENGTH) {
      setScreen('finish')
      return
    }
    setQNum((n) => n + 1)
    setQuestion((prev) => makeQuestion(level, prev))
    setPhase('ask')
  }

  const handleCell = (rowIdx, colIdx) => {
    if (phase === 'correct' || phase === 'reveal') return

    if (rowIdx === question.rowIdx && colIdx === question.colIdx) {
      setPhase('correct')
      setStars((s) => s + 1)
      playCorrect()
      later(goNext, 2400)
      return
    }

    // まちがい：×も ブザーも shake も なし。たどる ヒントを ふやすだけ。
    playTap()
    if (phase === 'ask') {
      setPhase('hint1')
      playTrace()
    } else if (phase === 'hint1') {
      setPhase('hint2')
      playTrace()
    } else {
      setPhase('reveal')
      later(goNext, 3200)
    }
  }

  const colId = level.cols[question.colIdx]
  const rowId = level.rows[question.rowIdx]
  const answerShown = phase === 'correct' || phase === 'reveal'
  const colArrow = phase !== 'ask'
  const rowArrow = phase === 'hint2' || answerShown

  if (screen === 'title') {
    return (
      <>
        <style>{styles}</style>
        <div className="stage centered">
          <div className="title-head">
            <div className="title-main">いろの まじわる マス</div>
            <div className="title-sub">たてと よこ、ふたつが であう マスを さがそう</div>
          </div>
          <div className="level-list">
            {LEVELS.map((lv, i) => (
              <button key={lv.label} className="level-card" onClick={() => startLevel(i)}>
                <div className="level-name">{lv.label}</div>
                <div className="level-size">{lv.size}</div>
                <div className="level-chips">
                  <div className="chip-row">
                    <span className="chip-label">たて</span>
                    {lv.cols.map((c) => (
                      <span key={c} className="mini-chip" style={{ background: COLORS[c].base }} />
                    ))}
                  </div>
                  <div className="chip-row">
                    <span className="chip-label">よこ</span>
                    {lv.rows.map((c) => (
                      <span key={c} className="mini-chip" style={{ background: COLORS[c].base }} />
                    ))}
                  </div>
                </div>
                <div className="level-note">{lv.note}</div>
              </button>
            ))}
          </div>
          {onExit && (
            <button className="text-btn" onClick={onExit}>
              ← あそびを えらぶ
            </button>
          )}
        </div>
      </>
    )
  }

  if (screen === 'finish') {
    return (
      <>
        <style>{styles}</style>
        <div className="stage centered">
          <div className="finish">
            <div className="finish-emoji">🎉</div>
            <div className="finish-text">すごい！</div>
            <div className="finish-sub">ふたつを たどって、ばしょが きまったね</div>
            <div className="finish-stars">⭐ {stars} / {ROUND_LENGTH}</div>
            <div className="finish-btns">
              <button className="big-btn" onClick={() => startLevel(levelIdx)}>
                もういちど
              </button>
              <button className="big-btn ghost" onClick={() => setScreen('title')}>
                レベルを かえる
              </button>
            </div>
          </div>
        </div>
      </>
    )
  }

  const board = []
  board.push(<div key="corner" className="corner" />)
  level.cols.forEach((cid, c) => {
    const color = COLORS[cid]
    const on = colArrow && c === question.colIdx
    board.push(
      <div
        key={`h${c}`}
        className={`head head-col${on ? ' head-on' : ''}`}
        style={{ background: color.base, color: color.ink }}
      >
        <span className="head-name">{color.name}</span>
        {on && <span className="head-arrow down">⬇</span>}
      </div>,
    )
  })

  level.rows.forEach((rid, r) => {
    const color = COLORS[rid]
    const on = rowArrow && r === question.rowIdx
    board.push(
      <div
        key={`v${r}`}
        className={`head head-row${on ? ' head-on' : ''}`}
        style={{ background: color.base, color: color.ink }}
      >
        <span className="head-name">{color.name}</span>
        {on && <span className="head-arrow right">➡</span>}
      </div>,
    )

    level.cols.forEach((cid, c) => {
      const isTarget = r === question.rowIdx && c === question.colIdx
      // ヒント1：たての れつ ぜんぶ。ヒント2：たて・よこ 両方（交点は 光らせない）
      const colBand =
        (phase === 'hint1' && c === question.colIdx) ||
        (phase === 'hint2' && c === question.colIdx && !isTarget)
      const rowBand = phase === 'hint2' && r === question.rowIdx && !isTarget
      const bandId = colBand ? cid : rowBand ? rid : null
      const delay = colBand ? r * 0.09 : rowBand ? c * 0.09 : 0

      board.push(
        <button
          key={`c${r}-${c}`}
          className={`cell${bandId ? ' band' : ''}${answerShown && isTarget ? ' target' : ''}`}
          style={
            bandId
              ? {
                  background: COLORS[bandId].soft,
                  boxShadow: `inset 0 0 0 4px ${COLORS[bandId].base}`,
                  animationDelay: `${delay}s`,
                }
              : undefined
          }
          onClick={() => handleCell(r, c)}
        >
          {answerShown && isTarget && <span className="sparkle">✨</span>}
        </button>,
      )
    })
  })

  return (
    <>
      <style>{styles}</style>
      <div className="stage play">
        <div className="topbar">
          <button className="icon-btn" onClick={() => { clearTimers(); setScreen('title') }}>
            🏠
          </button>
          <div className="count">{qNum + 1} / {ROUND_LENGTH}</div>
          <div className="spacer" />
          <div className="stars">⭐ {stars}</div>
          <button className="icon-btn" onClick={() => setSoundOn((s) => !s)}>
            {soundOn ? '♪' : '🔇'}
          </button>
        </div>

        <div className="prompt">
          <ColorWord id={colId} />の れつと <ColorWord id={rowId} />の れつが
          <br />
          まじわる マスは どこ？
        </div>

        <div
          className="board"
          style={{ '--n': String(level.cols.length) }}
        >
          {board}
        </div>

        <div className="message">
          {phase === 'hint1' && (
            <span className="hint">
              まず <ColorWord id={colId} />の れつを、うえから すーっと たどってみよう
            </span>
          )}
          {phase === 'hint2' && (
            <span className="hint">
              こんどは <ColorWord id={rowId} />の れつを、ひだりから すーっと。であう ところは どこ？
            </span>
          )}
          {phase === 'reveal' && <span className="answer">ここが まじわる マス！</span>}
          {phase === 'correct' && (
            <span className="answer">そう！ ふたつが そろって、ばしょが きまるね</span>
          )}
        </div>
      </div>
    </>
  )
}

const styles = `
  .stage {
    min-height: 100vh;
    background: linear-gradient(165deg, #eaf7ff 0%, #f4fbf1 55%, #fff8ec 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 14px 16px 22px;
    font-family: 'Hiragino Maru Gothic ProN', 'BIZ UDPGothic', 'Noto Sans JP', sans-serif;
    color: #37474f;
  }

  .topbar {
    width: 100%;
    max-width: 900px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .spacer { flex: 1; }

  .icon-btn {
    background: #ffffff;
    border: 3px solid #cfe6f5;
    border-radius: 18px;
    width: 52px;
    height: 52px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 3px 0 #d5e7f2;
    font-family: inherit;
  }

  .icon-btn:active { transform: translateY(2px); box-shadow: 0 1px 0 #d5e7f2; }

  .count {
    font-size: 20px;
    font-weight: 900;
    color: #6b8fa3;
    letter-spacing: 1px;
  }

  .stars {
    font-size: clamp(20px, 3.4vmin, 26px);
    font-weight: 900;
    color: #e8890c;
    background: #fff6df;
    border: 3px solid #ffd98a;
    border-radius: 999px;
    padding: 4px 16px;
  }

  .prompt {
    margin-top: auto;
    font-size: clamp(20px, 4.2vmin, 34px);
    font-weight: 900;
    line-height: 1.6;
    text-align: center;
    color: #2f4550;
  }

  .color-word {
    display: inline-block;
    border: 3px solid;
    border-radius: 12px;
    padding: 0 10px;
    margin: 0 2px;
    font-weight: 900;
  }

  .board {
    display: grid;
    grid-template-columns: var(--head) repeat(var(--n), var(--cell));
    gap: clamp(6px, 1.2vmin, 12px);
    /* マスは グリッドの おおきさに あわせて できるだけ 大きく */
    --cell: clamp(48px, min(calc(51vh / (var(--n) + 0.8)), calc(88vw / (var(--n) + 1.3))), 136px);
    --head: calc(var(--cell) * 1.12);
    --headH: calc(var(--cell) * 0.8);
    padding: clamp(8px, 1.6vmin, 16px);
    background: #ffffff;
    border-radius: 26px;
    box-shadow: 0 10px 30px rgba(70, 110, 140, 0.16);
  }

  .head {
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    position: relative;
    font-size: clamp(13px, calc(var(--cell) * 0.21), 24px);
    font-weight: 900;
    letter-spacing: 1px;
    padding: 4px;
    text-align: center;
    box-shadow: 0 4px 0 rgba(0, 0, 0, 0.12);
  }

  .head-col { flex-direction: column; height: var(--headH); }
  .head-row { flex-direction: row; min-height: var(--cell); }

  .head-on { animation: headPulse 0.9s ease-in-out infinite alternate; }

  .head-arrow {
    font-size: clamp(18px, 3.2vmin, 28px);
    line-height: 1;
    filter: drop-shadow(0 1px 0 rgba(255,255,255,0.7));
  }

  .head-arrow.down { animation: nudgeDown 0.8s ease-in-out infinite; }
  .head-arrow.right { animation: nudgeRight 0.8s ease-in-out infinite; }

  .cell {
    width: var(--cell);
    height: var(--cell);
    border-radius: 14px;
    border: 3px solid #d3e3ee;
    background: #fbfdff;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(26px, 6vmin, 48px);
    transition: transform 0.1s;
    font-family: inherit;
  }

  .cell:active { transform: scale(0.94); }

  .cell.band {
    border-color: transparent;
    animation: traceIn 0.35s ease both;
  }

  .cell.target {
    border-color: #ffd54f;
    background:
      radial-gradient(circle at 50% 50%, #fffdf2 0%, #fff2b8 55%, #ffe07a 100%);
    box-shadow: 0 0 0 6px rgba(255, 213, 79, 0.55), 0 0 34px 12px rgba(255, 209, 71, 0.7);
    animation: sunPop 0.45s ease;
  }

  .sparkle { animation: twinkle 0.9s ease-in-out infinite alternate; }

  .message {
    margin-bottom: auto;
    min-height: clamp(52px, 9vmin, 72px);
    max-width: 900px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 8px;
  }

  .hint {
    font-size: clamp(16px, 3vmin, 26px);
    font-weight: 900;
    color: #3f6b86;
    background: #eaf6ff;
    border: 3px dashed #a8d4ef;
    border-radius: 18px;
    padding: 8px 16px;
    line-height: 1.6;
    animation: fadeUp 0.3s ease;
  }

  .answer {
    font-size: clamp(20px, 3.6vmin, 32px);
    font-weight: 900;
    color: #d8630b;
    background: #fff5e0;
    border: 3px solid #ffcf80;
    border-radius: 18px;
    padding: 8px 20px;
    animation: fadeUp 0.3s ease;
  }

  .centered { justify-content: center; }

  .title-head { text-align: center; }

  .title-main {
    font-size: clamp(30px, 7vmin, 56px);
    font-weight: 900;
    color: #ef5f96;
    text-shadow: 2px 3px 0 #ffe1ec;
    letter-spacing: 2px;
  }

  .title-sub {
    margin-top: 10px;
    font-size: clamp(15px, 2.8vmin, 24px);
    font-weight: 900;
    color: #4c6b7a;
    background: #fff6df;
    border-radius: 999px;
    padding: 8px 20px;
    display: inline-block;
  }

  .level-list {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
    margin-top: 24px;
  }

  .level-card {
    background: #ffffff;
    border: 4px solid #dfeef7;
    border-radius: 24px;
    padding: 16px 20px;
    min-width: 190px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    box-shadow: 0 6px 0 #dfeef7;
    font-family: inherit;
  }

  .level-card:active { transform: translateY(3px); box-shadow: 0 3px 0 #dfeef7; }

  .level-name { font-size: 26px; font-weight: 900; color: #ef5f96; }
  .level-size { font-size: 20px; font-weight: 900; color: #4c6b7a; letter-spacing: 2px; }
  .level-note { font-size: 15px; font-weight: 900; color: #8aa4b1; }

  .level-chips { display: flex; flex-direction: column; gap: 6px; }
  .chip-row { display: flex; align-items: center; gap: 5px; }
  .chip-label { font-size: 13px; font-weight: 900; color: #8aa4b1; width: 30px; }

  .mini-chip {
    width: 22px;
    height: 22px;
    border-radius: 7px;
    box-shadow: inset 0 -2px 0 rgba(0,0,0,0.12);
  }

  .text-btn {
    margin-top: 22px;
    background: none;
    border: none;
    font-size: 18px;
    font-weight: 900;
    color: #6b8fa3;
    cursor: pointer;
    font-family: inherit;
  }

  .finish {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    animation: fadeUp 0.5s ease;
  }

  .finish-emoji { font-size: clamp(70px, 14vmin, 120px); animation: sunPop 0.6s ease; }
  .finish-text {
    font-size: clamp(40px, 9vmin, 72px);
    font-weight: 900;
    color: #ef5f96;
    text-shadow: 2px 3px 0 #ffe1ec;
  }
  .finish-sub { font-size: clamp(18px, 3.4vmin, 28px); font-weight: 900; color: #4c6b7a; }
  .finish-stars {
    font-size: clamp(26px, 5vmin, 40px);
    font-weight: 900;
    color: #e8890c;
    background: #fff6df;
    border: 4px solid #ffd98a;
    border-radius: 999px;
    padding: 6px 26px;
  }

  .finish-btns { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; }

  .big-btn {
    background: linear-gradient(135deg, #ffb3d0, #ff7fb0);
    border: none;
    border-radius: 999px;
    padding: 14px 34px;
    font-size: clamp(18px, 3.2vmin, 24px);
    font-weight: 900;
    color: #ffffff;
    cursor: pointer;
    box-shadow: 0 5px 0 #e86899;
    font-family: inherit;
  }

  .big-btn.ghost {
    background: #ffffff;
    color: #4c6b7a;
    box-shadow: 0 5px 0 #dfeef7;
    border: 3px solid #dfeef7;
  }

  .big-btn:active { transform: translateY(3px); box-shadow: 0 2px 0 #e86899; }

  @keyframes traceIn {
    from { opacity: 0.25; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
  }

  @keyframes sunPop {
    0% { transform: scale(0.7); }
    60% { transform: scale(1.12); }
    100% { transform: scale(1); }
  }

  @keyframes twinkle {
    from { opacity: 0.55; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1.15); }
  }

  @keyframes headPulse {
    from { filter: brightness(1); }
    to { filter: brightness(1.15); }
  }

  @keyframes nudgeDown {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(5px); }
  }

  @keyframes nudgeRight {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(5px); }
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
`
