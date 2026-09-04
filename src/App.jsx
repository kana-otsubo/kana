import { useState } from 'react'
import VehicleQuiz from './VehicleQuiz'
import ColorGridGame from './ColorGridGame'

const GAMES = [
  { id: 'grid', emoji: '🟦', title: 'いろの まじわる マス', sub: 'たてと よこが であう マス' },
  { id: 'vehicle', emoji: '🚑', title: 'のりもの クイズ', sub: 'おとを きいて あてよう' },
]

export default function App() {
  const [game, setGame] = useState(null)

  if (game === 'grid') return <ColorGridGame onExit={() => setGame(null)} />

  if (game === 'vehicle') {
    return (
      <>
        <VehicleQuiz />
        <button className="home-float" onClick={() => setGame(null)}>
          🏠
        </button>
        <style>{menuStyles}</style>
      </>
    )
  }

  return (
    <>
      <style>{menuStyles}</style>
      <div className="menu">
        <div className="menu-title">あそびを えらぼう</div>
        <div className="menu-list">
          {GAMES.map((g) => (
            <button key={g.id} className="menu-card" onClick={() => setGame(g.id)}>
              <span className="menu-emoji">{g.emoji}</span>
              <span className="menu-name">{g.title}</span>
              <span className="menu-sub">{g.sub}</span>
            </button>
          ))}
        </div>
      </div>
    </>
  )
}

const menuStyles = `
  .menu {
    min-height: 100vh;
    background: linear-gradient(165deg, #eaf7ff 0%, #f4fbf1 55%, #fff8ec 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 28px;
    padding: 24px;
    font-family: 'Hiragino Maru Gothic ProN', 'BIZ UDPGothic', 'Noto Sans JP', sans-serif;
  }

  .menu-title {
    font-size: clamp(28px, 6vmin, 48px);
    font-weight: 900;
    color: #ef5f96;
    text-shadow: 2px 3px 0 #ffe1ec;
    letter-spacing: 2px;
  }

  .menu-list { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }

  .menu-card {
    background: #ffffff;
    border: 4px solid #dfeef7;
    border-radius: 28px;
    padding: 22px 26px;
    min-width: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    box-shadow: 0 6px 0 #dfeef7;
    font-family: inherit;
  }

  .menu-card:active { transform: translateY(3px); box-shadow: 0 3px 0 #dfeef7; }

  .menu-emoji { font-size: clamp(48px, 10vmin, 76px); line-height: 1; }
  .menu-name { font-size: clamp(18px, 3.4vmin, 26px); font-weight: 900; color: #2f4550; }
  .menu-sub { font-size: clamp(13px, 2.4vmin, 17px); font-weight: 900; color: #8aa4b1; }

  .home-float {
    position: fixed;
    top: 14px;
    left: 14px;
    z-index: 200;
    background: #ffffff;
    border: 3px solid #cfe6f5;
    border-radius: 18px;
    width: 52px;
    height: 52px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 3px 0 #d5e7f2;
  }
`
