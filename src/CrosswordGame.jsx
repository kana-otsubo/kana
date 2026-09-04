import { useState, useMemo } from 'react'

// たて（down）と よこ（across）が 1マスだけ かさなる ミニクロスワード。
// かさなる マスが こたえ（di = たての なんもじめ / ai = よこの なんもじめ）。
const PUZZLES = [
  // レベル1: 2文字 × 2文字
  { level: 1, down: { word: 'かさ', emoji: '☂️' }, across: { word: 'さめ', emoji: '🦈' }, di: 1, ai: 0, choices: ['さ', 'す', 'そ'] },
  { level: 1, down: { word: 'はな', emoji: '🌸' }, across: { word: 'なす', emoji: '🍆' }, di: 1, ai: 0, choices: ['な', 'ぬ', 'ね'] },
  { level: 1, down: { word: 'くま', emoji: '🐻' }, across: { word: 'まど', emoji: '🪟' }, di: 1, ai: 0, choices: ['ま', 'み', 'む'] },
  { level: 1, down: { word: 'ねこ', emoji: '🐱' }, across: { word: 'こめ', emoji: '🍚' }, di: 1, ai: 0, choices: ['こ', 'け', 'か'] },
  { level: 1, down: { word: 'とり', emoji: '🐦' }, across: { word: 'りす', emoji: '🐿️' }, di: 1, ai: 0, choices: ['り', 'ら', 'る'] },
  { level: 1, down: { word: 'うし', emoji: '🐮' }, across: { word: 'しか', emoji: '🦌' }, di: 1, ai: 0, choices: ['し', 'さ', 'す'] },

  // レベル2: 3文字 × 2文字
  { level: 2, down: { word: 'いちご', emoji: '🍓' }, across: { word: 'ちず', emoji: '🗾' }, di: 1, ai: 0, choices: ['ち', 'り', 'こ'] },
  { level: 2, down: { word: 'たいこ', emoji: '🥁' }, across: { word: 'いす', emoji: '🪑' }, di: 1, ai: 0, choices: ['い', 'う', 'え'] },
  { level: 2, down: { word: 'さかな', emoji: '🐟' }, across: { word: 'かに', emoji: '🦀' }, di: 1, ai: 0, choices: ['か', 'き', 'な'] },
  { level: 2, down: { word: 'うさぎ', emoji: '🐰' }, across: { word: 'さる', emoji: '🐒' }, di: 1, ai: 0, choices: ['さ', 'ち', 'す'] },
  { level: 2, down: { word: 'たまご', emoji: '🥚' }, across: { word: 'まめ', emoji: '🫘' }, di: 1, ai: 0, choices: ['ま', 'み', 'も'] },
  { level: 2, down: { word: 'ばなな', emoji: '🍌' }, across: { word: 'なす', emoji: '🍆' }, di: 1, ai: 0, choices: ['な', 'ぬ', 'ば'] },

  // レベル3: 3文字 × 3文字
  { level: 3, down: { word: 'とけい', emoji: '⏰' }, across: { word: 'けむし', emoji: '🐛' }, di: 1, ai: 0, choices: ['け', 'げ', 'は'] },
  { level: 3, down: { word: 'すいか', emoji: '🍉' }, across: { word: 'いるか', emoji: '🐬' }, di: 1, ai: 0, choices: ['い', 'り', 'こ'] },
  { level: 3, down: { word: 'ねずみ', emoji: '🐭' }, across: { word: 'ずぼん', emoji: '👖' }, di: 1, ai: 0, choices: ['ず', 'す', 'つ'] },
  { level: 3, down: { word: 'さくら', emoji: '🌸' }, across: { word: 'くるま', emoji: '🚗' }, di: 1, ai: 0, choices: ['く', 'へ', 'た'] },
  { level: 3, down: { word: 'たいこ', emoji: '🥁' }, across: { word: 'いちご', emoji: '🍓' }, di: 1, ai: 0, choices: ['い', 'に', 'め'] },
]

const CLEAR_COUNT = 2 // 2問せいかいで レベルアップ
const MAX_LEVEL = 3

function shuffle(arr) {
  const out = [...arr]
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[out[i], out[j]] = [out[j], out[i]]
  }
  return out
}

function puzzlesFor(level) {
  return shuffle(PUZZLES.filter(p => p.level === level))
}

function positionWord(index, length) {
  if (index === 0) return 'さいしょ'
  if (index === length - 1) return 'さいご'
  return 'まんなか'
}

function makeSparkles() {
  return Array.from({ length: 18 }, (_, i) => ({
    id: i,
    x: Math.random() * 90 + 5,
    y: Math.random() * 70 + 15,
    delay: Math.random() * 0.35,
    mark: ['⭐', '✨', '🌟'][i % 3],
  }))
}

function Sparkles({ bits }) {
  if (bits.length === 0) return null

  return (
    <div className="sparkle-layer">
      {bits.map(b => (
        <span
          key={b.id}
          className="sparkle"
          style={{ left: b.x + '%', top: b.y + '%', animationDelay: b.delay + 's' }}
        >
          {b.mark}
        </span>
      ))}
    </div>
  )
}

function Grid({ puzzle, filled, blankHot }) {
  const { down, across, di, ai } = puzzle
  const rows = down.word.length
  const cols = across.word.length

  const cells = []
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const onDown = c === ai
      const onAcross = r === di
      if (!onDown && !onAcross) {
        cells.push(<div key={`${r}-${c}`} className="cell-gap" />)
        continue
      }
      const isBlank = onDown && onAcross
      const letter = isBlank
        ? filled
        : onDown
          ? down.word[r]
          : across.word[c]

      cells.push(
        <div
          key={`${r}-${c}`}
          className={
            'cell' +
            (isBlank ? ' cell-blank' : '') +
            (isBlank && filled ? ' cell-filled' : '') +
            (isBlank && !filled && blankHot ? ' cell-hot' : '')
          }
        >
          {letter}
        </div>,
      )
    }
  }

  return (
    <div className="grid-wrap">
      <div className="grid-labels-top" style={{ gridTemplateColumns: `repeat(${cols}, var(--cell))` }}>
        {Array.from({ length: cols }, (_, c) => (
          <div key={c} className="label-slot">
            {c === ai && (
              <span className="label-down">
                たて <span className="arrow-down">↓</span>
              </span>
            )}
          </div>
        ))}
      </div>
      <div className="grid-body">
        <div className="grid-labels-left" style={{ gridTemplateRows: `repeat(${rows}, var(--cell))` }}>
          {Array.from({ length: rows }, (_, r) => (
            <div key={r} className="label-slot">
              {r === di && (
                <span className="label-across">
                  よこ <span className="arrow-across">→</span>
                </span>
              )}
            </div>
          ))}
        </div>
        <div
          className="grid"
          style={{
            gridTemplateColumns: `repeat(${cols}, var(--cell))`,
            gridTemplateRows: `repeat(${rows}, var(--cell))`,
          }}
        >
          {cells}
        </div>
      </div>
    </div>
  )
}

export default function CrosswordGame() {
  const [level, setLevel] = useState(1)
  const [queue, setQueue] = useState(() => puzzlesFor(1))
  const [index, setIndex] = useState(0)
  const [cleared, setCleared] = useState(0) // このレベルで せいかいした かず
  const [hint, setHint] = useState(0) // 0=なし 1=よんでみよう 2=ことばを みせる 3以上=ヒカリで おしえる
  const [wrongLetter, setWrongLetter] = useState(null)
  const [phase, setPhase] = useState('play') // 'play' | 'correct' | 'levelup' | 'finished'
  const [sparkles, setSparkles] = useState([])

  const puzzle = queue[index % queue.length]
  const answer = puzzle.down.word[puzzle.di]
  const choices = useMemo(() => shuffle(puzzle.choices), [puzzle])
  const solved = phase === 'correct'

  const startLevel = (nextLevel) => {
    setLevel(nextLevel)
    setQueue(puzzlesFor(nextLevel))
    setIndex(0)
    setCleared(0)
    setHint(0)
    setWrongLetter(null)
    setPhase('play')
  }

  const handleChoice = (letter) => {
    if (phase !== 'play') return

    if (letter === answer) {
      setPhase('correct')
      setSparkles(makeSparkles())
      setWrongLetter(null)
      setTimeout(() => setSparkles([]), 1400)
      const nextCleared = cleared + 1
      setCleared(nextCleared)
      setTimeout(() => {
        if (nextCleared >= CLEAR_COUNT) {
          setPhase(level >= MAX_LEVEL ? 'finished' : 'levelup')
        } else {
          setIndex(i => i + 1)
          setHint(0)
          setWrongLetter(null)
          setPhase('play')
        }
      }, 2600)
    } else {
      setWrongLetter(letter)
      setHint(h => h + 1)
      setTimeout(() => setWrongLetter(null), 700)
    }
  }

  if (phase === 'finished') {
    return (
      <>
        <style>{styles}</style>
        <div className="app">
          <div className="center-screen">
            <div className="big-emoji">🎉</div>
            <div className="big-text">すごい！</div>
            <div className="big-sub">たてにも よこにも よめたね！</div>
            <button className="again-btn" onClick={() => startLevel(1)}>
              もういちど あそぶ
            </button>
          </div>
        </div>
      </>
    )
  }

  if (phase === 'levelup') {
    return (
      <>
        <style>{styles}</style>
        <div className="app">
          <div className="center-screen">
            <div className="big-emoji">🏅</div>
            <div className="big-text">レベル{level} クリア！</div>
            <div className="big-sub">つぎは レベル{level + 1} だよ</div>
            <button className="again-btn" onClick={() => startLevel(level + 1)}>
              つぎへ すすむ
            </button>
          </div>
        </div>
      </>
    )
  }

  const downWord = puzzle.down.word
  const readAloud = downWord
    .split('')
    .map((ch, i) => (i === puzzle.di ? '□' : ch))
    .join('・')

  return (
    <>
      <style>{styles}</style>
      <Sparkles bits={sparkles} />
      <div className="app">
        <header className="bar">
          <span className={`level-chip level-${level}`}>レベル{level}</span>
          <span className="title">たてにも よこにも なる もじを さがそう</span>
          <span className="stars">
            {Array.from({ length: CLEAR_COUNT }, (_, i) => (
              <span key={i} className={i < cleared ? 'star on' : 'star'}>
                ★
              </span>
            ))}
          </span>
        </header>

        <div className="board">
          <div className="clues">
            <div className="clue">
              <span className="clue-emoji">{puzzle.down.emoji}</span>
              {(hint >= 2 || solved) && <span className="clue-word down-word">{downWord}</span>}
            </div>
            <div className="clue">
              <span className="clue-emoji">{puzzle.across.emoji}</span>
              {solved && <span className="clue-word across-word">{puzzle.across.word}</span>}
            </div>
          </div>

          <div className="stage">
            <Grid
              puzzle={puzzle}
              filled={solved ? answer : ''}
              blankHot={hint >= 2}
            />
          </div>

          <div className="panel">
            {solved ? (
              <div className="bubble bubble-yay">
                <div className="yay-letter">{answer}！</div>
                <div className="yay-text">
                  {downWord} にも {puzzle.across.word} にも なったね！
                </div>
              </div>
            ) : (
              <>
                <div className="panel-title">もじを えらぼう</div>
                <div className="choices">
                  {choices.map(letter => (
                    <button
                      key={letter}
                      className={
                        'choice' +
                        (wrongLetter === letter ? ' shake' : '') +
                        (hint >= 3 && letter === answer ? ' glow' : '')
                      }
                      onClick={() => handleChoice(letter)}
                    >
                      {letter}
                    </button>
                  ))}
                </div>
                {hint === 1 && (
                  <div className="bubble bubble-hint">
                    たてから よんでみよう。
                    <br />
                    {readAloud}。
                    <br />
                    なんて いう ことば かな？
                  </div>
                )}
                {hint >= 2 && (
                  <div className="bubble bubble-hint">
                    {downWord}の {positionWord(puzzle.di, downWord.length)}の もじだよ。
                    <br />
                    よこも あうか たしかめてね。
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

const styles = `
  .app {
    --cell: clamp(56px, 11vmin, 104px);
    min-height: 100vh;
    background: linear-gradient(160deg, #dff2ff 0%, #eef8ff 55%, #fff8f2 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 16px 24px;
    font-family: 'Hiragino Maru Gothic ProN', 'BIZ UDPGothic', 'Noto Sans JP', sans-serif;
    color: #10456b;
  }

  .bar {
    width: 100%;
    max-width: 1100px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
  }

  .level-chip {
    font-size: clamp(14px, 2.6vw, 20px);
    font-weight: 900;
    color: white;
    border-radius: 999px;
    padding: 6px 18px;
    letter-spacing: 1px;
    white-space: nowrap;
  }
  .level-1 { background: linear-gradient(135deg, #ffb74d, #fb8c00); }
  .level-2 { background: linear-gradient(135deg, #66bb6a, #388e3c); }
  .level-3 { background: linear-gradient(135deg, #ab7cdd, #7e57c2); }

  .title {
    font-size: clamp(13px, 2.4vw, 22px);
    font-weight: 900;
    letter-spacing: 1px;
    text-align: center;
  }

  .stars { white-space: nowrap; }
  .star {
    font-size: clamp(20px, 4vw, 30px);
    color: #cfd8dc;
    transition: color 0.3s, transform 0.3s;
  }
  .star.on {
    color: #ffc400;
    transform: scale(1.15);
    text-shadow: 0 2px 6px rgba(255, 196, 0, 0.6);
  }

  .board {
    width: 100%;
    max-width: 1100px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(12px, 3vw, 40px);
    flex-wrap: wrap;
  }

  .clues {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .clue {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .clue-emoji {
    font-size: clamp(44px, 9vmin, 90px);
    line-height: 1;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.12));
  }

  .clue-word {
    font-size: clamp(20px, 4vmin, 36px);
    font-weight: 900;
    letter-spacing: 2px;
    animation: popIn 0.35s ease;
  }
  .down-word { color: #e53935; }
  .across-word { color: #1e88e5; }

  .stage { display: flex; align-items: center; justify-content: center; }

  .grid-wrap { display: flex; flex-direction: column; }
  .grid-body { display: flex; }

  .grid-labels-top { display: grid; margin-left: calc(var(--cell) * 0.72); }
  .grid-labels-left { display: grid; width: calc(var(--cell) * 0.72); }

  .label-slot {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(11px, 1.8vmin, 15px);
    font-weight: 900;
  }

  .label-down { color: #ec407a; }
  .label-across { color: #1e88e5; }
  .arrow-down, .arrow-across { font-size: 1.4em; }

  .grid { display: grid; }

  .cell-gap { width: var(--cell); height: var(--cell); }

  .cell {
    width: var(--cell);
    height: var(--cell);
    border: 3px solid #37474f;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: calc(var(--cell) * 0.6);
    font-weight: 900;
    color: #263238;
    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
  }

  .cell-blank { background: #cfe8fb; }

  .cell-hot {
    background: #fff3c4;
    animation: hotPulse 1.1s ease-in-out infinite;
  }

  .cell-filled {
    background: #ffd54f;
    color: #4a3000;
    animation: bigPop 0.5s ease;
    box-shadow: 0 0 22px 6px rgba(255, 193, 7, 0.55);
  }

  .panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    max-width: 360px;
  }

  .panel-title {
    font-size: clamp(14px, 2.6vmin, 20px);
    font-weight: 900;
    color: #0d6ca8;
    background: #e3f2fd;
    border-radius: 999px;
    padding: 6px 20px;
  }

  .choices { display: flex; gap: clamp(8px, 2vw, 18px); }

  .choice {
    width: clamp(56px, 11vmin, 96px);
    height: clamp(56px, 11vmin, 96px);
    border-radius: 20px;
    border: 3px solid #90caf9;
    background: white;
    font-size: clamp(28px, 6vmin, 52px);
    font-weight: 900;
    color: #10456b;
    cursor: pointer;
    box-shadow: 0 5px 14px rgba(0,0,0,0.12);
    transition: transform 0.1s, box-shadow 0.1s;
    font-family: inherit;
  }

  .choice:active { transform: scale(0.93); }

  .choice.shake {
    animation: shake 0.5s ease;
    border-color: #ef9a9a;
    background: #ffebee;
  }

  .choice.glow {
    animation: hotPulse 1s ease-in-out infinite;
    border-color: #ffd54f;
  }

  .bubble {
    position: relative;
    border-radius: 20px;
    padding: 14px 18px;
    font-size: clamp(14px, 2.6vmin, 20px);
    font-weight: bold;
    line-height: 1.6;
    text-align: center;
    animation: popIn 0.3s ease;
  }

  .bubble-hint {
    background: white;
    border: 3px solid #bbdefb;
    color: #10456b;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }

  .bubble-yay {
    background: #fde4ef;
    border: 3px solid #f8bbd0;
    color: #ad1457;
  }

  .yay-letter {
    font-size: clamp(36px, 8vmin, 64px);
    font-weight: 900;
    color: #e91e63;
    line-height: 1.1;
  }

  .yay-text { margin-top: 4px; }

  .center-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    gap: 14px;
    animation: fadeIn 0.5s ease;
  }

  .big-emoji { font-size: clamp(72px, 18vmin, 130px); animation: bigPop 0.6s ease; }
  .big-text {
    font-size: clamp(36px, 9vmin, 72px);
    font-weight: 900;
    color: #e65100;
    text-shadow: 2px 3px 0 #ffe0b2;
  }
  .big-sub { font-size: clamp(18px, 4.5vmin, 32px); font-weight: bold; }

  .again-btn {
    margin-top: 12px;
    background: linear-gradient(135deg, #66bb6a, #43a047);
    border: none;
    border-radius: 50px;
    padding: 14px 36px;
    font-size: clamp(18px, 4vmin, 24px);
    font-weight: 900;
    color: white;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(67, 160, 71, 0.4);
    font-family: inherit;
  }

  .again-btn:active { transform: scale(0.95); }

  .sparkle-layer { position: fixed; inset: 0; pointer-events: none; z-index: 100; }
  .sparkle {
    position: absolute;
    font-size: 26px;
    opacity: 0;
    animation: sparkleUp 1.2s ease-out forwards;
  }

  @keyframes sparkleUp {
    0% { opacity: 1; transform: translateY(0) scale(0.8); }
    100% { opacity: 0; transform: translateY(-70px) scale(1.6); }
  }

  @keyframes hotPulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.55); }
    50% { box-shadow: 0 0 20px 7px rgba(255, 193, 7, 0.55); }
  }

  @keyframes popIn {
    0% { transform: scale(0.6); opacity: 0; }
    70% { transform: scale(1.1); }
    100% { transform: scale(1); opacity: 1; }
  }

  @keyframes bigPop {
    0% { transform: scale(0.7); }
    50% { transform: scale(1.18); }
    100% { transform: scale(1); }
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-9px); }
    40% { transform: translateX(9px); }
    60% { transform: translateX(-7px); }
    80% { transform: translateX(7px); }
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: scale(0.94); }
    to { opacity: 1; transform: scale(1); }
  }
`
