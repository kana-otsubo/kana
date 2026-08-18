/**
 * レッスン構成（1コマ15場面）の定義
 *
 * これまで表で決めてきた内容を、そのままプログラムから読める形にしたもの。
 * 画面はこの配列の順番どおりに進む。
 *
 * kind      … 画面の種類
 *   'song'      歌・映像を流すだけ
 *   'call'      お名前呼び（出席・気分の記録）
 *   'breath'    深呼吸・イメージトレーニング
 *   'flash'     カードを順に見せる（フラッシュカード / リンクカード / 直観像）
 *   'work'      取り組み（レッスンタイム）
 *   'print'     プリント教材を使う
 *   'material'  実物教材を使う（数・図形・そろばん）
 *   'activity'  エンジョイタイム
 *   'closing'   終わりの歌・保護者レポート
 *
 * source    … 素材の出どころ（'コペルン' / 'ハイブリッドレッスン' / '新規作成' / null）
 * teacher   … 先生の携帯に出す操作ボタン
 * tablet    … 子どもタブレットの状態 'lock'（ロック）/ 'touch'（操作あり）/ 'share'（画面共有）
 * record    … 自動で記録する項目
 * decks     … flashcards.js のデッキ id（kind が 'flash' のとき）
 * print     … 印刷物のパス
 * status    … 'ready'（用意できている）/ 'todo'（作成が必要）/ 'undecided'（内容が未定）
 */

import { DECKS } from './flashcards'

export const SCENES = [
  {
    no: 1,
    id: 'opening-song',
    name: 'はじまりのうた',
    kind: 'song',
    source: 'コペルン',
    content: 'コペルンデータの「はじまりのうた」',
    teacher: ['開始', '一時停止', '再開', '子ども画面共有ON/OFF'],
    tablet: 'lock',
    record: [],
    status: 'ready',
    note: '誤タッチしてもエラーにしない。',
  },
  {
    no: 2,
    id: 'name-call',
    name: 'お名前呼び',
    kind: 'call',
    source: '新規作成',
    content: '名前カード（例：大坪可奈 → おおつぼ かな）＋気分アイコン。今日頑張ったこと・好きなものを聞く。',
    teacher: ['次の子へ', 'もう一回呼ぶ', '先生が代理入力', 'スキップ', '質問を選ぶ'],
    tablet: 'touch',
    record: ['出席', '気分', '頑張ったこと', '好きなもの', '補助の有無'],
    status: 'todo',
    note: '既存素材がないので新規に作る。声で答えた内容は先生が記録する。',
  },
  {
    no: 3,
    id: 'breathing',
    name: '深呼吸・イメージトレーニング',
    kind: 'breath',
    source: 'E08動画',
    content: '風船がふくらむ／しぼむ、または丸が大きく・小さくを繰り返すアニメで「すう／はく」を見せる。最後に短いイメージ指示。',
    teacher: ['開始', '次へ', '音声ON/OFF'],
    tablet: 'lock',
    record: [],
    status: 'todo',
    note: '呼吸の音声・BGM・画面アニメを同期。年齢別に短くできること。',
  },
  {
    no: 4,
    id: 'eidetic',
    name: '直観像',
    kind: 'flash',
    source: 'ハイブリッドレッスン',
    content: '見せる → 消す → 見せる → 消す → 回答 → 正解表示。',
    teacher: ['表示', '消す', 'もう一回見せる', '回答へ', '正解表示', '次へ', '様子をタップ'],
    tablet: 'touch',
    record: ['解答時間', '答え', '正誤'],
    decks: [],
    status: 'todo',
    note: '子どもはタブレットでドラッグして置く。正解の位置は光る。時間が経つとヒントが光る。置きなおせば正解になる。',
  },
  {
    no: 5,
    id: 'link-cards',
    name: 'リンクカード',
    kind: 'flash',
    source: null,
    content: '',
    teacher: ['次へ', '戻る', '最初から', '音声自動ON/OFF', '先生カンペ表示'],
    tablet: 'lock',
    record: [],
    decks: [],
    status: 'undecided',
    note: 'フラッシュカードと同じカードDBで扱う。10〜30枚の可変枚数。',
  },
  {
    no: 6,
    id: 'flash-cards',
    name: 'フラッシュカード',
    kind: 'flash',
    source: null,
    content: '各デッキの内容と枚数は flashcards.js を参照。',
    teacher: ['開始', '停止', '再開', 'スキップ', '速度変更', '声の種類変更'],
    tablet: 'lock',
    record: [],
    decks: DECKS.map((d) => d.id),
    status: 'todo',
    note: 'カードごとに 音声自動・カードめくり自動・完全自動・先生進行 を設定。声：ペル君／ルルちゃん／博士／おじいちゃん。',
  },
  {
    no: 7,
    id: 'monthly-song',
    name: '今月の歌',
    kind: 'song',
    source: 'E08動画',
    content: '',
    teacher: ['開始', '一時停止', '再開', '次へ'],
    tablet: 'lock',
    record: [],
    status: 'undecided',
    note: '歌詞と音声を同期。曲は未定。',
  },
  {
    no: 8,
    id: 'lesson-time',
    name: 'レッスンタイム',
    kind: 'work',
    source: 'ハイブリッドレッスン',
    content: '',
    teacher: ['取り組み1 開始/終了', '取り組み2 開始/終了', '取り組み3 開始/終了', '次へ'],
    tablet: 'touch',
    record: ['取り組みごとの実施', '補助の有無'],
    works: [null, null, null],
    status: 'undecided',
    note: '取り組み3つを順番に提示。内容はBOX・週で差し替え。先生用の進行メモを出す。',
  },
  {
    no: 9,
    id: 'moji',
    name: 'もじ',
    kind: 'print',
    source: '新規作成',
    content: 'ひらがな書きプリント（あ行）。白抜き文字をなぞる。',
    teacher: ['開始', '次へ', '記録'],
    tablet: 'touch',
    record: ['実施', '補助の有無'],
    print: '/prints/hiragana-aiueo.pdf',
    printSource: '/prints/hiragana-aiueo.html',
    status: 'ready',
    note: '文字教材は週ごとに差し替え。',
  },
  {
    no: 10,
    id: 'number-song',
    name: 'かずのうた',
    kind: 'song',
    source: 'コペルン',
    content: 'すうじのうた',
    teacher: ['開始', '一時停止', '次へ'],
    tablet: 'lock',
    record: [],
    status: 'ready',
    note: '歌と数字表示を同期。必要に応じて数字をタッチできる。',
  },
  {
    no: 11,
    id: 'number-program',
    name: '数プログラム',
    kind: 'material',
    source: null,
    content: '卵（実物教材）を使う。',
    teacher: ['開始', '問題表示', '正解表示', '次へ', '記録'],
    tablet: 'touch',
    record: ['教材名', '正誤', '補助の有無', '反応'],
    material: '卵',
    status: 'todo',
    note: '実物教材を使う前提で、見本・指示・答えを表示する。',
  },
  {
    no: 12,
    id: 'shapes',
    name: '図形',
    kind: 'material',
    source: 'ハイブリッドレッスン',
    content: '積み木（実物教材）を使う。お手本図形を表示。',
    teacher: ['開始', '問題表示', '正解表示', '次へ', '記録'],
    tablet: 'touch',
    record: ['教材名', '正誤', '補助の有無'],
    material: '積み木',
    status: 'todo',
    note: '図形教材は週ごとに差し替え。立体・平面で表示方法を分けられること。',
  },
  {
    no: 13,
    id: 'soroban',
    name: 'そろばん',
    kind: 'material',
    source: null,
    content: '0〜20',
    teacher: ['開始', '停止', '次へ'],
    tablet: 'lock',
    record: [],
    material: 'そろばん',
    status: 'todo',
    note: '元案の「そろばんの歌」を歌として残すか、0〜20の操作課題にするかは要確認。',
  },
  {
    no: 14,
    id: 'enjoy-time',
    name: 'エンジョイタイム',
    kind: 'activity',
    source: 'E08動画',
    content: 'リトミック／実験',
    teacher: ['活動を選ぶ（リトミック／粗大／実験／バスゲーム）'],
    tablet: 'lock',
    record: ['活動種別', '参加状況'],
    activities: ['リトミック', '実験'],
    status: 'todo',
    note: '名称は「エンジョイタイム」に統一。活動により個別参加・タッチ可。',
  },
  {
    no: 15,
    id: 'closing-song',
    name: '終わりの歌',
    kind: 'closing',
    source: 'コペルン',
    content: '終わりの歌＋ペル君のほめ演出。',
    teacher: ['開始', '保護者レポート送信', '終了'],
    tablet: 'lock',
    record: ['がんばり記録', '今日の参加状況', '保護者レポート'],
    status: 'todo',
    note: '1日のまとめを保護者レポートとして送る。',
  },
]

/** no または id から場面を取り出す */
export const getScene = (key) =>
  SCENES.find((s) => s.id === key || s.no === key)

/** 準備状況ごとに場面をまとめる */
export const sceneStatus = () => ({
  ready: SCENES.filter((s) => s.status === 'ready'),
  todo: SCENES.filter((s) => s.status === 'todo'),
  undecided: SCENES.filter((s) => s.status === 'undecided'),
})
