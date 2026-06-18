import { useState, useRef } from 'react'

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

const SWIPE_THRESHOLD = 80

export default function FlashCard() {
  const [mode, setMode] = useState(null)
  const [index, setIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [animKey, setAnimKey] = useState(0)
  const [done, setDone] = useState(false)

  // drag state
  const [dragX, setDragX] = useState(0)
  const [dragging, setDragging] = useState(false)
  const dragStart = useRef(null)

  const card = CARDS[index]

  function startMode(m) {
    setMode(m)
    setIndex(0)
    setFlipped(false)
    setDone(false)
    setAnimKey(k => k + 1)
    setDragX(0)
  }

  function next() {
    if (index + 1 >= CARDS.length) {
      setDone(true)
    } else {
      setIndex(i => i + 1)
      setFlipped(false)
      setAnimKey(k => k + 1)
    }
    setDragX(0)
  }

  // --- pointer drag handlers ---
  function onPointerDown(e) {
    if (e.button !== undefined && e.button !== 0) return
    dragStart.current = e.clientX ?? e.touches?.[0]?.clientX
    setDragging(true)
  }

  function onPointerMove(e) {
    if (!dragging || dragStart.current === null) return
    const x = e.clientX ?? e.touches?.[0]?.clientX
    const dx = x - dragStart.current
    setDragX(dx > 0 ? dx : 0) // only allow dragging right
  }

  function onPointerUp() {
    if (!dragging) return
    setDragging(false)
    if (dragX >= SWIPE_THRESHOLD) {
      next()
    } else {
      setDragX(0)
    }
    dragStart.current = null
  }

  const swipeProgress = Math.min(dragX / SWIPE_THRESHOLD, 1)
  const cardStyle = dragging || dragX > 0
    ? {
        transform: `translateX(${dragX}px) rotate(${dragX * 0.05}deg)`,
        transition: dragging ? 'none' : 'transform 0.3s ease',
        opacity: 1 - swipeProgress * 0.4,
      }
    : {}

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
          {!mode && (
            <div className="fc-hint">← モードを選んでスタート</div>
          )}

          {mode && !done && (
            <>
              {swipeProgress > 0.3 && (
                <div className="fc-swipe-indicator" style={{ opacity: swipeProgress }}>
                  つぎへ →
                </div>
              )}
              <div
                key={animKey}
                className={`fc-card ${animClass}${flipped ? ' flipped' : ''}`}
                style={cardStyle}
                onMouseDown={onPointerDown}
                onMouseMove={onPointerMove}
                onMouseUp={onPointerUp}
                onMouseLeave={onPointerUp}
                onTouchStart={e => onPointerDown(e.touches[0])}
                onTouchMove={e => onPointerMove(e.touches[0])}
                onTouchEnd={onPointerUp}
                onClick={() => { if (dragX < 5) setFlipped(f => !f) }}
              >
                <div className="fc-card-inner">
                  <div className="fc-card-front">{card.front}</div>
                  <div className="fc-card-back">{card.back}</div>
                </div>
                <div className="fc-progress">
                  {index + 1} / {CARDS.length}
                </div>
                <div className="fc-drag-hint">→ 右にドラッグで次へ</div>
              </div>
            </>
          )}

          {mode && done && (
            <div className="fc-done">
              <div className="fc-done-emoji">🎉</div>
              <div className="fc-done-text">おしまい！</div>
              <button className="fc-restart-btn" onClick={() => startMode(mode)}>
                もういちど
              </button>
            </div>
          )}
        </div>

        <div className="fc-footer" />
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
  .fc-designer { margin-left: 8px; color: #777; }

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

  .fc-mode-btn.active { border-color: #888; background: #f0ede6; }
  .fc-mode-btn:hover  { border-color: #aaa; }

  .fc-stage {
    width: 100%;
    max-width: 760px;
    min-height: 420px;
    background: #eeebe3;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }

  .fc-hint {
    color: #aaa;
    font-size: 16px;
  }

  /* Card */
  .fc-card {
    width: 240px;
    user-select: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    perspective: 1000px;
    cursor: grab;
    touch-action: none;
  }

  .fc-card:active { cursor: grabbing; }

  .fc-card-inner {
    width: 200px;
    height: 260px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.5s ease;
    border-radius: 16px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.12);
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
  }

  .fc-card-front { background: white; color: #222; }
  .fc-card-back  { background: #fff8e1; color: #e65100; transform: rotateY(180deg); }

  .fc-progress {
    font-size: 14px;
    color: #666;
    letter-spacing: 1px;
  }

  .fc-drag-hint {
    font-size: 13px;
    color: #aaa;
    letter-spacing: 0.5px;
  }

  /* Swipe indicator */
  .fc-swipe-indicator {
    position: absolute;
    right: 32px;
    font-size: 22px;
    font-weight: bold;
    color: #4caf50;
    pointer-events: none;
    transition: opacity 0.1s;
  }

  /* Done screen */
  .fc-done {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    animation: popIn 0.4s ease;
  }

  .fc-done-emoji { font-size: 72px; }

  .fc-done-text {
    font-size: 32px;
    font-weight: 900;
    color: #555;
  }

  .fc-restart-btn {
    background: #555;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 12px 32px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.2s;
  }

  .fc-restart-btn:hover { background: #333; }

  /* Entry animations */
  .fc-card.card--from-top {
    animation: slideFromTop 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  @keyframes slideFromTop {
    from { opacity: 0; transform: translateY(-80px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .fc-card.card--from-side {
    animation: slideFromSide 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  @keyframes slideFromSide {
    from { opacity: 0; transform: translateX(-100px); }
    to   { opacity: 1; transform: translateX(0); }
  }

  .fc-card.card--pop {
    animation: popIn 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  }

  @keyframes popIn {
    from { opacity: 0; transform: scale(0.4); }
    to   { opacity: 1; transform: scale(1); }
  }
`
