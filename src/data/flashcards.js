/**
 * フラッシュカード（レッスン No.6）のカードDB
 *
 * リンクカード（No.5）も同じ形式で扱えるようにしている。
 *
 * deck.type によってカードの持ち物が変わる:
 *   'picture' … 絵カード          card: { emoji, ja, en?, phrase? }
 *   'letter'  … 文字カード        card: { kana, word, emoji }（ひらがな → 絵の順で見せる）
 *   'pair'    … 反対語カード      card: { a, aEmoji, b, bEmoji }
 *   'text'    … 文のカード        card: { text, reading?, meaning?, author? }
 *
 * deck.mode … 'auto'（完全自動）/ 'audio'（音声のみ自動）/ 'flip'（めくりのみ自動）/ 'teacher'（先生進行）
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
  /* ---------------- 絵カード ---------------- */
  {
    id: 'animals-ja',
    name: 'どうぶつ',
    type: 'picture',
    mode: 'auto',
    voice: 'peru',
    speed: 1200,
    cards: [
      { emoji: '🐶', ja: 'いぬ' },
      { emoji: '🐱', ja: 'ねこ' },
      { emoji: '🐰', ja: 'うさぎ' },
      { emoji: '🐘', ja: 'ぞう' },
      { emoji: '🦁', ja: 'らいおん' },
      { emoji: '🐵', ja: 'さる' },
      { emoji: '🐻', ja: 'くま' },
      { emoji: '🐼', ja: 'ぱんだ' },
      { emoji: '🦒', ja: 'きりん' },
      { emoji: '🐧', ja: 'ぺんぎん' },
    ],
  },
  {
    id: 'vehicles-ja',
    name: 'のりもの',
    type: 'picture',
    mode: 'auto',
    voice: 'peru',
    speed: 1200,
    cards: [
      { emoji: '🚗', ja: 'じどうしゃ' },
      { emoji: '🚑', ja: 'きゅうきゅうしゃ' },
      { emoji: '🚒', ja: 'しょうぼうしゃ' },
      { emoji: '🚃', ja: 'でんしゃ' },
      { emoji: '🚌', ja: 'ばす' },
      { emoji: '✈️', ja: 'ひこうき' },
      { emoji: '🚢', ja: 'ふね' },
      { emoji: '🚲', ja: 'じてんしゃ' },
    ],
  },
  {
    id: 'vegetables-ja',
    name: 'やさい',
    type: 'picture',
    mode: 'auto',
    voice: 'lulu',
    speed: 1200,
    cards: [
      { emoji: '🍅', ja: 'とまと' },
      { emoji: '🥕', ja: 'にんじん' },
      { emoji: '🥒', ja: 'きゅうり' },
      { emoji: '🍆', ja: 'なす' },
      { emoji: '🌽', ja: 'とうもろこし' },
      { emoji: '🥔', ja: 'じゃがいも' },
      { emoji: '🎃', ja: 'かぼちゃ' },
      { emoji: '🧅', ja: 'たまねぎ' },
    ],
  },

  /* ---------------- 文字（ひらがな → 絵） ---------------- */
  {
    id: 'hiragana-a',
    name: 'もじ（あ行）',
    type: 'letter',
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

  /* ---------------- ことわざ 5枚 ---------------- */
  {
    id: 'kotowaza-1',
    name: 'ことわざ',
    type: 'text',
    mode: 'audio',
    voice: 'ojiichan',
    speed: 2500,
    cards: [
      { text: '石の上にも三年', reading: 'いしのうえにもさんねん', meaning: 'がまんしてつづければ、きっとうまくいく。' },
      { text: '犬も歩けば棒に当たる', reading: 'いぬもあるけばぼうにあたる', meaning: 'うごいてみると、おもいがけないことに出会う。' },
      { text: '花より団子', reading: 'はなよりだんご', meaning: 'みた目より、なかみのほうが大事。' },
      { text: '猿も木から落ちる', reading: 'さるもきからおちる', meaning: 'じょうずな人でも、しっぱいすることがある。' },
      { text: '塵も積もれば山となる', reading: 'ちりもつもればやまとなる', meaning: 'すこしずつでも、つづければ大きくなる。' },
    ],
  },

  /* ---------------- 百人一首 3枚 ---------------- */
  {
    id: 'hyakunin-1',
    name: '百人一首',
    type: 'text',
    mode: 'audio',
    voice: 'ojiichan',
    speed: 4000,
    cards: [
      {
        text: '秋の田の かりほの庵の 苫をあらみ わが衣手は 露にぬれつつ',
        reading: 'あきのたの かりほのいおの とまをあらみ わがころもでは つゆにぬれつつ',
        author: '天智天皇（一番）',
      },
      {
        text: '春過ぎて 夏来にけらし 白妙の 衣ほすてふ 天の香具山',
        reading: 'はるすぎて なつきにけらし しろたえの ころもほすちょう あまのかぐやま',
        author: '持統天皇（二番）',
      },
      {
        text: 'あしびきの 山鳥の尾の しだり尾の ながながし夜を ひとりかも寝む',
        reading: 'あしびきの やまどりのおの しだりおの ながながしよを ひとりかもねむ',
        author: '柿本人麻呂（三番）',
      },
    ],
  },

  /* ---------------- 反対語 3枚 ---------------- */
  {
    id: 'hantaigo-1',
    name: 'はんたいご',
    type: 'pair',
    mode: 'teacher',
    voice: 'lulu',
    speed: 2000,
    cards: [
      { a: 'おおきい', aEmoji: '🐘', b: 'ちいさい', bEmoji: '🐜' },
      { a: 'たかい', aEmoji: '🦒', b: 'ひくい', bEmoji: '🐢' },
      { a: 'ながい', aEmoji: '🐍', b: 'みじかい', bEmoji: '🐛' },
    ],
  },

  /* ---------------- 四字熟語 3枚 ---------------- */
  {
    id: 'yojijukugo-1',
    name: '四字熟語',
    type: 'text',
    mode: 'audio',
    voice: 'hakase',
    speed: 2500,
    cards: [
      { text: '一石二鳥', reading: 'いっせきにちょう', meaning: '一つのことで、二ついいことがある。' },
      { text: '十人十色', reading: 'じゅうにんといろ', meaning: '人はそれぞれ、みんなちがう。' },
      { text: '七転八起', reading: 'しちてんはっき', meaning: 'なんども ころんでも、また立ち上がる。' },
    ],
  },

  /* ---------------- 一茶の俳句 4枚 ---------------- */
  {
    id: 'haiku-issa',
    name: '俳句（一茶）',
    type: 'text',
    mode: 'audio',
    voice: 'ojiichan',
    speed: 3000,
    cards: [
      { text: 'やせ蛙 まけるな一茶 これにあり', reading: 'やせがえる まけるないっさ これにあり', author: '小林一茶' },
      { text: '雀の子 そこのけそこのけ お馬が通る', reading: 'すずめのこ そこのけそこのけ おうまがとおる', author: '小林一茶' },
      { text: 'われと来て 遊べや親の ない雀', reading: 'われときて あそべやおやの ないすずめ', author: '小林一茶' },
      { text: '名月を とってくれろと 泣く子かな', reading: 'めいげつを とってくれろと なくこかな', author: '小林一茶' },
    ],
  },

  /* ---------------- 速読（詩） ---------------- */
  {
    id: 'sokudoku-1',
    name: '速読（詩）',
    type: 'text',
    mode: 'auto',
    voice: 'peru',
    speed: 900,
    cards: [
      { text: 'あめんぼ あかいな あいうえお', author: '北原白秋「五十音」' },
      { text: 'うきもに こえびも およいでる', author: '北原白秋「五十音」' },
      { text: 'かきのき くりのき かきくけこ', author: '北原白秋「五十音」' },
      { text: 'きつつき こつこつ かれけやき', author: '北原白秋「五十音」' },
      { text: 'ささげに すをかけ さしすせそ', author: '北原白秋「五十音」' },
    ],
  },

  /* ---------------- 英語 ---------------- */
  {
    id: 'en-animals-1',
    name: 'English / Animals 1',
    type: 'picture',
    mode: 'auto',
    voice: 'lulu',
    speed: 1500,
    cards: [
      { emoji: '🐶', en: 'dog', ja: 'いぬ' },
      { emoji: '🐱', en: 'cat', ja: 'ねこ' },
      { emoji: '🐰', en: 'rabbit', ja: 'うさぎ' },
      { emoji: '🐻', en: 'bear', ja: 'くま' },
      { emoji: '🦁', en: 'lion', ja: 'ライオン' },
      { emoji: '🐘', en: 'elephant', ja: 'ぞう' },
      { emoji: '🐵', en: 'monkey', ja: 'さる' },
      { emoji: '🐼', en: 'panda', ja: 'パンダ' },
      { emoji: '🦒', en: 'giraffe', ja: 'きりん' },
      { emoji: '🐧', en: 'penguin', ja: 'ペンギン' },
    ],
  },
  {
    id: 'en-getting-dressed-1',
    name: 'English / Getting dressed in the morning',
    type: 'picture',
    mode: 'auto',
    voice: 'lulu',
    speed: 1800,
    cards: [
      { emoji: '👕', en: 'shirt', ja: 'シャツ', phrase: 'Put on your shirt.' },
      { emoji: '👖', en: 'pants', ja: 'ズボン', phrase: 'Put on your pants.' },
      { emoji: '🧦', en: 'socks', ja: 'くつした', phrase: 'Put on your socks.' },
      { emoji: '👟', en: 'shoes', ja: 'くつ', phrase: 'Put on your shoes.' },
      { emoji: '🧥', en: 'jacket', ja: 'うわぎ', phrase: 'Put on your jacket.' },
      { emoji: '🧢', en: 'hat', ja: 'ぼうし', phrase: 'Put on your hat.' },
      { emoji: '🪥', en: 'toothbrush', ja: 'はブラシ', phrase: 'Brush your teeth.' },
      { emoji: '🎒', en: 'backpack', ja: 'かばん', phrase: "Let's go!" },
    ],
  },
]

/** id からデッキを取り出す */
export const getDeck = (id) => DECKS.find((d) => d.id === id)
