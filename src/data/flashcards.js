/**
 * フラッシュカード（レッスン No.6）のカードDB
 *
 * リンクカード（No.5）も同じ形式で扱う。
 * カードの中身（ことわざ・百人一首・反対語・四字熟語・俳句・英語など）は
 * 既存の教材から入れるため、ここでは枚数と設定だけを定義して cards は空にしてある。
 *
 * deck.count … 入れる予定の枚数（null = 未定）
 * deck.cards … 実際のカード。deck.type ごとに持ち物が変わる:
 *   'picture' … 絵カード     { emoji, ja, en?, phrase? }
 *   'letter'  … 文字カード   { kana, word, emoji }（ひらがな → 絵の順で見せる）
 *   'pair'    … 反対語カード { a, aEmoji, b, bEmoji }
 *   'text'    … 文のカード   { text, reading?, meaning?, author? }
 *
 * deck.mode  … 'auto'（完全自動）/ 'audio'（音声のみ自動）/ 'flip'（めくりのみ自動）/ 'teacher'（先生進行）
 * deck.voice … 'peru'（ペル君）/ 'lulu'（ルルちゃん）/ 'hakase'（博士）/ 'ojiichan'（おじいちゃん）
 * deck.speed … 1枚あたりの表示ミリ秒（mode が 'teacher' のときは未使用）
 */

export const VOICES = {
  peru: 'ペル君',
  lulu: 'ルルちゃん',
  hakase: '博士',
  ojiichan: 'おじいちゃん',
}

export const DECKS = [
  /* ---------------- 絵カード（枚数未定） ---------------- */
  {
    id: 'animals-ja',
    name: 'どうぶつ',
    type: 'picture',
    count: null,
    mode: 'auto',
    voice: 'peru',
    speed: 1200,
    cards: [],
  },
  {
    id: 'vehicles-ja',
    name: 'のりもの',
    type: 'picture',
    count: null,
    mode: 'auto',
    voice: 'peru',
    speed: 1200,
    cards: [],
  },
  {
    id: 'vegetables-ja',
    name: 'やさい',
    type: 'picture',
    count: null,
    mode: 'auto',
    voice: 'lulu',
    speed: 1200,
    cards: [],
  },

  /* ---------------- 文字（ひらがな → 絵）※内容確定済み ---------------- */
  {
    id: 'hiragana-a',
    name: 'もじ（あ行）',
    type: 'letter',
    count: 5,
    mode: 'teacher',
    voice: 'peru',
    speed: 1500,
    cards: [
      { kana: 'あ', word: 'あり', emoji: '🐜' },
      { kana: 'い', word: 'いぬ', emoji: '🐶' },
      { kana: 'う', word: 'うし', emoji: '🐄' },
      { kana: 'え', word: 'えび', emoji: '🦐' },
      { kana: 'お', word: 'おに', emoji: '👹' },
    ],
  },

  /* ---------------- 枚数のみ確定（中身は既存教材から） ---------------- */
  {
    id: 'kotowaza-1',
    name: 'ことわざ',
    type: 'text',
    count: 5,
    mode: 'audio',
    voice: 'ojiichan',
    speed: 2500,
    cards: [],
  },
  {
    id: 'hyakunin-1',
    name: '百人一首',
    type: 'text',
    count: 3,
    mode: 'audio',
    voice: 'ojiichan',
    speed: 4000,
    cards: [],
  },
  {
    id: 'hantaigo-1',
    name: 'はんたいご',
    type: 'pair',
    count: 3,
    mode: 'teacher',
    voice: 'lulu',
    speed: 2000,
    cards: [],
  },
  {
    id: 'yojijukugo-1',
    name: '四字熟語',
    type: 'text',
    count: 3,
    mode: 'audio',
    voice: 'hakase',
    speed: 2500,
    cards: [],
  },
  {
    id: 'haiku-issa',
    name: '俳句（一茶）',
    type: 'text',
    count: 4,
    mode: 'audio',
    voice: 'ojiichan',
    speed: 3000,
    cards: [],
  },

  /* ---------------- 速読（詩）※内容・枚数とも未定 ---------------- */
  {
    id: 'sokudoku-1',
    name: '速読（詩）',
    type: 'text',
    count: null,
    mode: 'auto',
    voice: 'peru',
    speed: 900,
    cards: [],
  },

  /* ---------------- 英語 ---------------- */
  {
    id: 'en-animals-1',
    name: 'English / Animals 1',
    type: 'picture',
    count: null,
    mode: 'auto',
    voice: 'lulu',
    speed: 1500,
    cards: [],
  },
  {
    id: 'en-getting-dressed-1',
    name: 'English / Getting dressed in the morning',
    type: 'picture',
    count: null,
    mode: 'auto',
    voice: 'lulu',
    speed: 1800,
    cards: [],
  },
]

/** id からデッキを取り出す */
export const getDeck = (id) => DECKS.find((d) => d.id === id)

/** カードが入っていて、指定枚数どおりに揃っているデッキか */
export const isDeckReady = (deck) =>
  deck.cards.length > 0 && (deck.count === null || deck.cards.length === deck.count)
