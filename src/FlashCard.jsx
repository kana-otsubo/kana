import { useState } from 'react'

const CARDS = [
  { id: 1, front: 'あ', back: 'ア' },
  { id: 2, front: 'い', back: 'イ' },
  { id: 3, front: 'う', back: 'ウ' },
  { id: 4, front: 'え', back: 'エ' },
  { id: 5, front: 'お', back: 'オ' },
]

const MODES = [
  { id: 'from-top',  label: '① 上から出てくる' },
  { id: 'from-side', label: '② 横から出てくる' },
  { id: 'pop',       label: '③ 特別カード（ポップ）' },
]

export default function FlashCard() {
  const [mode, setMode] = useState(null)
  const [index, setIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [animKey, setAnimKey] = useState(0)
  const [done, setDone] = useState(false)

  const card = CARDS[index]

  function startMode(m) {
    setMode(m)
    setIndex(0)
    setFlipped(false)
    setDone(false)
    setAnimKey(k => k + 1)
  }

  function next() {
    if (index + 1 >= CARDS.length) {
      setDone(true)
    } else {
      setIndex(i => i + 1)
      setFlipped(false)
      setAnimKey(k => k + 1)
    }
  }

  const animClass = mode ? `card--${mode}` : ''

  return (
    <>
      <style>{styles}</style>
      <div className="fc-app">
        <header className="fc-header">
          <span className="fc-title">ハイブリッドレッスン サンプル</span>
          <span className="fc-sep">──</span>
          <span className="fc-subtitle">フラッシュカード</span>
          <span className="fc-designer">設計：大坪可奈</span>
        </header>

        <nav className="fc-modes">
          {MODES.map(m => (
            <button
              key={m.id}
              className={`fc-mode-btn${mode === m.id ? ' active' : ''}`}
              onClick={() => startMode(m.id)}
            >
              {m.label}
            </button>
          ))}
        </nav>

        <div className="fc-stage">
          {!mode && <div className="fc-empty" />}

          {mode && !done && (
            <div
              key={animKey}
              className={`fc-card ${animClass}${flipped ? ' flipped' : ''}`}
              onClick={() => setFlipped(f => !f)}
            >
              <div className="fc-card-inner">
                <div className="fc-card-front">{card.front}</div>
                <div className="fc-card-back">{card.back}</div>
              </div>
              <div className="fc-progress">
                {index + 1} / {CARDS.length}
              </div>
              <button
                className="fc-next-btn"
                onClick={e => { e.stopPropagation(); next() }}
              >
                {index + 1 >= CARDS.length ? 'おわり' : 'つぎへ →'}
              </button>
            </div>
          )}
        </div>

        <div className="fc-footer">おしまい！</div>
      </div>
    </>
  )
}

const styles = `
  * { box-sizing: border-box; margin: 0; padding: 0; }

  .fc-app {
    min-height: 100vh;
    background: #f9f7f2;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 16px 40px;
    font-family: 'Hiragino Maru Gothic ProN', 'BIZ UDPGothic', 'Noto Sans JP', sans-serif;
    color: #333;
  }

  .fc-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    color: #555;
    margin-bottom: 20px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .fc-sep { color: #999; }

  .fc-designer {
    margin-left: 8px;
    color: #777;
  }

  .fc-modes {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .fc-mode-btn {
    border: 1.5px solid #ccc;
    border-radius: 12px;
    padding: 10px 20px;
    background: white;
    font-size: 14px;
    cursor: pointer;
    color: #444;
    transition: border-color 0.2s, background 0.2s;
    font-family: inherit;
  }

  .fc-mode-btn.active {
    border-color: #888;
    background: #f0ede6;
  }

  .fc-mode-btn:hover {
    border-color: #aaa;
  }

  .fc-stage {
    width: 100%;
    max-width: 760px;
    min-height: 400px;
    background: #eeebe3;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }

  .fc-empty {
    width: 100%;
    height: 400px;
  }

  /* Card base */
  .fc-card {
    width: 240px;
    cursor: pointer;
    user-select: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    perspective: 1000px;
  }

  .fc-card-inner {
    width: 200px;
    height: 260px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.5s ease;
  }

  .fc-card.flipped .fc-card-inner {
    transform: rotateY(180deg);
  }

  .fc-card-front,
  .fc-card-back {
    position: absolute;
    inset: 0;
    backface-visibility: hidden;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 96px;
    font-weight: 900;
    box-shadow: 0 6px 24px rgba(0,0,0,0.12);
  }

  .fc-card-front {
    background: white;
    color: #222;
  }

  .fc-card-back {
    background: #fff8e1;
    color: #e65100;
    transform: rotateY(180deg);
  }

  .fc-progress {
    font-size: 14px;
    color: #666;
    letter-spacing: 1px;
  }

  .fc-next-btn {
    background: #555;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 10px 28px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.2s;
  }

  .fc-next-btn:hover { background: #333; }

  .fc-footer {
    margin-top: 24px;
    font-size: 20px;
    color: #555;
    letter-spacing: 2px;
  }

  /* Animation: from top */
  .fc-card.card--from-top {
    animation: slideFromTop 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  @keyframes slideFromTop {
    from { opacity: 0; transform: translateY(-80px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* Animation: from side */
  .fc-card.card--from-side {
    animation: slideFromSide 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  @keyframes slideFromSide {
    from { opacity: 0; transform: translateX(-100px); }
    to   { opacity: 1; transform: translateX(0); }
  }

  /* Animation: pop */
  .fc-card.card--pop {
    animation: popIn 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  }

  @keyframes popIn {
    from { opacity: 0; transform: scale(0.4); }
    to   { opacity: 1; transform: scale(1); }
  }
`
