import { useState, useEffect, useCallback } from 'react'

const QUESTIONS = [
  { sound: 'ピーポー ピーポー', correctId: 'ambulance', correctLabel: 'きゅうきゅうしゃ' },
  { sound: 'ウーーー カンカンカン', correctId: 'firetruck', correctLabel: 'しょうぼうしゃ' },
  { sound: 'ブッブー', correctId: 'car', correctLabel: 'じどうしゃ' },
  { sound: 'ガタンゴトン ガタンゴトン', correctId: 'train', correctLabel: 'でんしゃ' },
  { sound: 'ブロロロロ…', correctId: 'motorcycle', correctLabel: 'バイク' },
]

const ALL_CHOICES = [
  { id: 'ambulance', emoji: '🚑', label: 'きゅうきゅうしゃ' },
  { id: 'firetruck', emoji: '🚒', label: 'しょうぼうしゃ' },
  { id: 'car', emoji: '🚗', label: 'じどうしゃ' },
  { id: 'train', emoji: '🚃', label: 'でんしゃ' },
  { id: 'motorcycle', emoji: '🏍️', label: 'バイク' },
  { id: 'ship', emoji: '🚢', label: 'ふね' },
  { id: 'plane', emoji: '✈️', label: 'ひこうき' },
  { id: 'bicycle', emoji: '🚲', label: 'じてんしゃ' },
]

function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5)
}

function getChoices(correctId) {
  const correct = ALL_CHOICES.find(c => c.id === correctId)
  const others = shuffle(ALL_CHOICES.filter(c => c.id !== correctId)).slice(0, 3)
  return shuffle([correct, ...others])
}

function Particle({ x, y, delay }) {
  return (
    <div
      style={{
        position: 'absolute',
        left: x + '%',
        top: y + '%',
        fontSize: '24px',
        animation: `particle 1s ease-out ${delay}s forwards`,
        opacity: 0,
        pointerEvents: 'none',
      }}
    >
      ⭐
    </div>
  )
}

function Particles({ active }) {
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    x: Math.random() * 90 + 5,
    y: Math.random() * 80 + 10,
    delay: Math.random() * 0.4,
  }))

  if (!active) return null

  return (
    <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 100 }}>
      {particles.map(p => (
        <Particle key={p.id} x={p.x} y={p.y} delay={p.delay} />
      ))}
    </div>
  )
}

export default function VehicleQuiz() {
  const [questionIndex, setQuestionIndex] = useState(0)
  const [choices, setChoices] = useState(() => getChoices(QUESTIONS[0].correctId))
  const [showSound, setShowSound] = useState(false)
  const [result, setResult] = useState(null) // 'correct' | 'wrong' | null
  const [wrongId, setWrongId] = useState(null)
  const [finished, setFinished] = useState(false)
  const [particles, setParticles] = useState(false)

  const question = QUESTIONS[questionIndex]

  const playSound = useCallback(() => {
    setShowSound(true)
  }, [])

  const handleChoice = (id) => {
    if (result === 'correct') return

    if (id === question.correctId) {
      setResult('correct')
      setParticles(true)
      setTimeout(() => setParticles(false), 1200)
      setTimeout(() => {
        const next = questionIndex + 1
        if (next >= QUESTIONS.length) {
          setFinished(true)
        } else {
          setQuestionIndex(next)
          setChoices(getChoices(QUESTIONS[next].correctId))
          setShowSound(false)
          setResult(null)
          setWrongId(null)
        }
      }, 2000)
    } else {
      setWrongId(id)
      setResult('wrong')
      setTimeout(() => {
        setResult(null)
        setWrongId(null)
      }, 800)
    }
  }

  useEffect(() => {
    setChoices(getChoices(QUESTIONS[questionIndex].correctId))
    setShowSound(false)
    setResult(null)
    setWrongId(null)
  }, [questionIndex])

  if (finished) {
    return (
      <>
        <style>{styles}</style>
        <div className="app">
          <div className="finish-screen">
            <div className="finish-emoji">🎉</div>
            <div className="finish-text">すごい！</div>
            <div className="finish-sub">ぜんぶできたね！</div>
            <button
              className="play-again-btn"
              onClick={() => {
                setQuestionIndex(0)
                setFinished(false)
                setShowSound(false)
                setResult(null)
                setWrongId(null)
              }}
            >
              もういちど あそぶ
            </button>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <style>{styles}</style>
      <Particles active={particles} />
      <div className="app">
        <div className="progress">
          {questionIndex + 1} / {QUESTIONS.length}
        </div>

        <div className="sound-area">
          {showSound ? (
            <div className="sound-text wave-text">
              {question.sound.split('').map((ch, i) => (
                <span
                  key={i}
                  className="wave-char"
                  style={{ animationDelay: `${i * 0.06}s` }}
                >
                  {ch === ' ' ? ' ' : ch}
                </span>
              ))}
            </div>
          ) : (
            <div className="sound-placeholder">？</div>
          )}
        </div>

        <button className="listen-btn" onClick={playSound}>
          きいてみよう！
        </button>

        {result === 'correct' && (
          <div className="result-correct">せいかい！ 🎉</div>
        )}
        {result === 'wrong' && (
          <div className="result-wrong">もういちど きいてみよう</div>
        )}

        <div className="choices">
          {choices.map(choice => {
            const isCorrectAndDone = result === 'correct' && choice.id === question.correctId
            const isWrong = wrongId === choice.id
            return (
              <button
                key={choice.id}
                className={`choice-btn${isCorrectAndDone ? ' correct-highlight' : ''}${isWrong ? ' shake' : ''}`}
                onClick={() => handleChoice(choice.id)}
              >
                <span className="choice-emoji">{choice.emoji}</span>
                <span className="choice-label">{choice.label}</span>
              </button>
            )
          })}
        </div>
      </div>
    </>
  )
}

const styles = `
  * { box-sizing: border-box; margin: 0; padding: 0; }

  .app {
    min-height: 100vh;
    background: linear-gradient(160deg, #b3e5fc 0%, #e1f5fe 60%, #f0f9ff 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 16px 32px;
    font-family: 'Hiragino Maru Gothic ProN', 'BIZ UDPGothic', 'Noto Sans JP', sans-serif;
  }

  .progress {
    font-size: 20px;
    font-weight: bold;
    color: #0277bd;
    margin-bottom: 12px;
    letter-spacing: 2px;
  }

  .sound-area {
    width: 100%;
    max-width: 600px;
    min-height: 130px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 8px 0;
  }

  .sound-text {
    font-size: clamp(36px, 8vw, 56px);
    font-weight: 900;
    color: #01579b;
    text-align: center;
    line-height: 1.3;
    text-shadow: 2px 3px 0 #b3e5fc;
    animation: fadeIn 0.4s ease forwards;
  }

  .sound-placeholder {
    font-size: 72px;
    color: #b0bec5;
    animation: pulse 1.5s ease-in-out infinite;
  }

  .wave-text {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

  .wave-char {
    display: inline-block;
    animation: wave 0.6s ease-in-out infinite alternate;
  }

  .listen-btn {
    background: linear-gradient(135deg, #ffeb3b, #ffc107);
    border: none;
    border-radius: 50px;
    padding: 16px 40px;
    font-size: clamp(20px, 4vw, 26px);
    font-weight: 900;
    color: #4a3000;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(255, 193, 7, 0.5);
    transition: transform 0.1s, box-shadow 0.1s;
    margin: 12px 0;
    font-family: inherit;
    letter-spacing: 1px;
  }

  .listen-btn:active {
    transform: scale(0.95);
    box-shadow: 0 3px 10px rgba(255, 193, 7, 0.4);
  }

  .result-correct {
    font-size: clamp(28px, 6vw, 40px);
    font-weight: 900;
    color: #e65100;
    animation: popIn 0.3s ease forwards;
    text-shadow: 1px 2px 0 #ffe0b2;
    margin: 8px 0;
  }

  .result-wrong {
    font-size: clamp(18px, 4vw, 24px);
    font-weight: bold;
    color: #c62828;
    margin: 8px 0;
    animation: fadeIn 0.2s ease;
  }

  .choices {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
    width: 100%;
    max-width: 500px;
  }

  .choice-btn {
    background: white;
    border: 3px solid #81d4fa;
    border-radius: 24px;
    padding: 16px 8px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    transition: transform 0.1s, box-shadow 0.1s, border-color 0.2s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    min-height: 120px;
    font-family: inherit;
  }

  .choice-btn:active {
    transform: scale(0.95);
  }

  .choice-btn.correct-highlight {
    border-color: #ffd600;
    background: #fffde7;
    box-shadow: 0 0 24px 6px rgba(255, 214, 0, 0.6);
    animation: bigPop 0.4s ease forwards;
  }

  .choice-btn.shake {
    animation: shake 0.5s ease;
    border-color: #ef9a9a;
    background: #ffebee;
  }

  .choice-emoji {
    font-size: clamp(48px, 10vw, 72px);
    line-height: 1;
  }

  .choice-label {
    font-size: clamp(14px, 3.5vw, 18px);
    font-weight: bold;
    color: #01579b;
    letter-spacing: 1px;
  }

  .finish-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    gap: 16px;
    animation: fadeIn 0.5s ease;
  }

  .finish-emoji {
    font-size: 100px;
    animation: bigPop 0.6s ease;
  }

  .finish-text {
    font-size: clamp(48px, 10vw, 72px);
    font-weight: 900;
    color: #e65100;
    text-shadow: 2px 3px 0 #ffe0b2;
  }

  .finish-sub {
    font-size: clamp(24px, 5vw, 36px);
    font-weight: bold;
    color: #01579b;
  }

  .play-again-btn {
    margin-top: 16px;
    background: linear-gradient(135deg, #66bb6a, #43a047);
    border: none;
    border-radius: 50px;
    padding: 16px 40px;
    font-size: clamp(18px, 4vw, 24px);
    font-weight: 900;
    color: white;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(67, 160, 71, 0.4);
    transition: transform 0.1s;
    font-family: inherit;
  }

  .play-again-btn:active {
    transform: scale(0.95);
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
  }

  @keyframes wave {
    from { transform: translateY(0); }
    to { transform: translateY(-10px); }
  }

  @keyframes popIn {
    0% { transform: scale(0.5); opacity: 0; }
    70% { transform: scale(1.2); }
    100% { transform: scale(1); opacity: 1; }
  }

  @keyframes bigPop {
    0% { transform: scale(1); }
    50% { transform: scale(1.15); }
    100% { transform: scale(1); }
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-10px); }
    40% { transform: translateX(10px); }
    60% { transform: translateX(-8px); }
    80% { transform: translateX(8px); }
  }

  @keyframes pulse {
    from { opacity: 0.4; transform: scale(0.95); }
    to { opacity: 0.8; transform: scale(1.05); }
  }

  @keyframes particle {
    0% { opacity: 1; transform: translateY(0) scale(1); }
    100% { opacity: 0; transform: translateY(-60px) scale(1.5); }
  }
`
