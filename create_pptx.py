#!/usr/bin/env python3
"""
篠浦塾 S-BRAIN分析発表資料 作成スクリプト
被験者: 広報担当 A様（40代女性）
観察者: 大坪可奈（発表者）
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
# Register and use Noto Sans CJK for Japanese support
_jp_font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(_jp_font_path)
_jp_font = fm.FontProperties(fname=_jp_font_path)
_jp_font_name = _jp_font.get_name()
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = [_jp_font_name, 'DejaVu Sans']
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
import copy
import io
import os

# ─── データ定義 ──────────────────────────────────────────────

# 被験者 (FU09 = 本人)
subject = {
    'name': 'Ａ様',
    'brain_type': '右脳３次元優位スタイル',
    'left_pct': 46, 'right_pct': 54,
    'left3_pt': 24, 'right3_pt': 33,
    'left2_pt': 22, 'right2_pt': 21,
    'left3_pts': 51, 'right3_pts': 70,
    'left2_pts': 47, 'right2_pts': 46,
    'brain_use': 75,
    'judo_pt': 83,   # 受動脳
    'nodo_pt': 52,   # 能動脳
    'animal_ctrl': 84,   # 動物脳コントロール力
    'animal_act': 61,    # 動物脳活性度
    'stress': 26,
    'stress_tol': 64,
    'diag_date': '2026-05-29',
    'account': 'USR46027',
    'answers': [
        3,0,2,4,0,4,3,4,0,3,3,3,3,3,0,4,4,3,2,3,  # Q001-020
        4,4,1,4,1,4,3,4,1,4,3,1,1,1,3,4,2,2,0,0,  # Q021-040
        4,3,4,4,4,4,1,4,4,4,3,3,4,4,2,2,4,4,4,4,  # Q041-060
        1,1,4,1,4,4,0,4,3,4,3,2,0,3,3,1,2,3,0,3,  # Q061-080
        3,4,4,4,3,3,3,4,4,1,4,0,3,0,4,4,4,4,1,2,  # Q081-100
        0,4,4,4,2,2,2,4,2,3,0,1,0,3,3,4,4,2,1,4,  # Q101-120
        4,2,2,4,4,3,3,3,4,3,1,4,4,3,4,4,4,4,4,3,  # Q121-140
        2,4,4,4,4,4,4,3,4,2,2,3,1,3,2,4,3,4,1,2,  # Q141-160
        0,4,2,2,3,0,0,1,0,1,3,0,3,0,3,1,0,0,0,0,  # Q161-180
        3,1,2,4,4,4,3,4,1,0,2,3,4,4,3,0,3,2,0,4,  # Q181-200
    ]
}

# 観察者 (FU10 = 観察者)
observer = {
    'name': '観察者',
    'brain_type': '左脳・右脳３次元優位スタイル',
    'left_pct': 51, 'right_pct': 49,
    'left3_pt': 29, 'right3_pt': 33,
    'left2_pt': 23, 'right2_pt': 16,
    'left3_pts': 60, 'right3_pts': 68,
    'left2_pts': 47, 'right2_pts': 33,
    'brain_use': 65,
    'judo_pt': 73,
    'nodo_pt': 52,
    'animal_ctrl': 79,
    'animal_act': 55,
    'stress': 28,
    'stress_tol': 75,
    'diag_date': '2026-06-03',
    'account': 'USR46028',
    'answers': [
        4,4,3,2,1,3,3,4,2,4,3,4,3,3,2,4,4,3,1,3,  # Q001-020
        3,4,2,4,2,4,2,4,1,4,3,0,2,2,1,0,3,4,0,2,  # Q021-040
        4,4,4,4,2,4,4,4,4,4,3,3,4,3,3,2,3,3,3,3,  # Q041-060
        0,1,1,1,4,2,0,2,2,4,2,0,1,2,1,0,3,2,2,3,  # Q061-080
        3,4,4,4,2,2,4,2,4,0,4,1,2,1,4,4,2,2,2,4,  # Q081-100
        2,2,3,3,2,0,3,2,3,4,1,0,2,2,3,3,3,2,1,3,  # Q101-120
        3,3,1,3,4,4,3,2,4,4,3,4,4,3,4,3,1,3,3,4,  # Q121-140
        2,3,2,3,4,3,3,3,3,0,2,1,1,4,2,3,4,4,2,2,  # Q141-160
        3,3,3,3,3,0,1,1,0,0,3,2,3,1,3,3,0,0,2,0,  # Q161-180
        4,4,4,4,3,4,3,3,2,2,3,3,3,3,3,0,3,4,2,3,  # Q181-200
    ]
}

# 質問テキスト (Q001-Q200)
q_texts = {
    1:'冷静に、理路整然と話をするほうだ',2:'個人的な感情を仕事に持ち込まない',3:'チームの責任者に向いていると思う',
    4:'前置きの長い話や、意図の見えない話にイライラする',5:'いわゆる「根回し」のような活動は苦手だ',
    6:'レベルの高い人と付き合っていたい',7:'自分は大器晩成型だと思う',8:'量をこなすよりも、本質を突いた仕事をしたい',
    9:'即断即決を求められるとストレスを感じる',10:'理屈のあわない行動をする人は苦手だ',
    11:'自分が無駄だと思うことは絶対したくない',12:'組織化、効率化をはかることで仕事の質を上げたい',
    13:'目標達成までのステップを着実にこなすのが好きだ',14:'自分の実績を数値化することが自信につながる',
    15:'自分の感情は表にだしたくない',16:'自分の独創的なことを話したり書いたりしたい',
    17:'一人で本を読んだり考えたりするのが好きだ',18:'結局お金がないと何もできないと思う',
    19:'宴会で自分の席から動くことはふつうはしない',20:'仕事で戦っている時に一番生きがいを感じる',
    21:'強く信じている主義や信念がある',22:'ある分野のスペシャリストになりたい',
    23:'規則には忠実に行動したい',24:'待ち合わせの時間や締め切り・計画を守れない人は許せない',
    25:'「君の言う事は正論だが」とよく言われる',26:'細部にわたり、こだわった仕事ができる',
    27:'「怒り」の感情が原動力になることがある',28:'分からないことは納得するまで何度も聞く',
    29:'ルールや原理原則を守っていると安心感がある',30:'資格の勉強に向いている',
    31:'小さなことでも気にかかることが多い',32:'リラックスして冗談をいうのが苦手である',
    33:'自分の考えを他人にあてはめて責めてしまうことがある',34:'正しいことを行うことが自分にとって一番大事',
    35:'ふだんは物静かだが追いこまれると激情にかられることがある',36:'物事を説明するのにくどくどと長くなることが多い',
    37:'自分が予測できない事態になるとひどく不安になる',38:'自分の慣れていることであれば長時間働いても苦にならない',
    39:'しゃべりかたに抑揚がなく声が小さい',40:'自分は組織に順応してうまく立ち回ることが苦手である',
    41:'常にテンションが高く、声が大きい方だ',42:'集団の中では中心で仕切りたい方だ',
    43:'エネルギッシュだと言われる',44:'独創的・革新的な仕事をしたい',
    45:'人を説得するのは得意である',46:'決断が速く、せっかちだと言われる',
    47:'交友関係は広いほうだ',48:'新しいことを始める時は、「とりあえず」やってみる',
    49:'なにか挑戦するものがあるとエネルギーがでる',50:'集団の中で誰が一番実権をもっているかがすぐにわかる',
    51:'成功して有名になり周囲の注目をあびたい',52:'状況におおじて意見をどんどん変えることは気にならない',
    53:'行動力は人一倍ある',54:'政治的に動くのは得意だ',
    55:'過去の失敗例はたいてい忘れ成功例しか思い出せない',56:'人にはじめて会う時は自分を大きくみせたくなる',
    57:'人と違うことをやりたいといつも思っている',58:'感情の起伏が激しいとよくいわれる',
    59:'楽しいことが人一倍好きだ',60:'楽観的だとよくいわれる',
    61:'世話好きで困った人を放っておけない',62:'「正しさ」よりも「相手が欲する」ほうが大事',
    63:'大きな団体よりも小グループのほうが落ち着く',64:'損得抜きで働くことがある',
    65:'人に感謝される仕事をしたい',66:'友達の数は多くないが、深い付き合いができる',
    67:'白黒をはっきりつけるのが苦手だ',68:'人に頼られるとエネルギーが湧いてくるタイプだ',
    69:'仁義や筋を通すことが重要だと思っている',70:'師匠と弟子のような人間関係が好きだ',
    71:'人に会うとまず喜ばせたいと思う',72:'親しい人と常に一緒にいたい',
    73:'自分のことは後回しになることが多い',74:'やったことで人に感謝されないと落ち込んでしまう',
    75:'自分の関わった人や教え子・部下が育つことほど嬉しいことはない',76:'周囲の人に常に気をつかってしまう',
    77:'人間関係が重荷に感じることがある',78:'目の前の人が喜んでいないのに成功や達成はないと思う',
    79:'過去を思い出すと哀しいことがたくさんあったと感じる',80:'美しく生きることが自分にとって一番大事',
    81:'問題があった場合まず現実を観察してから考える',82:'正確な情報をできるだけ集めてから仕事をする',
    83:'上司の指示がないと動きたくない★',84:'他人の意見に振り回されることが多い★',
    85:'自然を破壊するのは反対だ',86:'自分と異なる意見でも正しいと思ったら取り入れる',
    87:'ネットの情報で物事を決めることが多い★',88:'どういう人か見抜いてからその人のいうことを信じるか決める',
    89:'何かを信じていないと不安でしょうがない★',90:'自分が話すより人の話を聞いていることの方が多い',
    91:'自分が動かないと物事はかわらないとよく感じる',92:'すぐに決断するほうだ★',
    93:'自分がまず経験しないと信じないタイプである',94:'人の言葉をさえぎって自分の意見をいいたいほうだ★',
    95:'物事に対してやる気があるほうだ',96:'新しいことをやるときは不安感よりわくわく感の方が強い',
    97:'やらないよりはやって失敗したほうがいいと思っている',98:'自分の思いをとげるために人を利用することがよくある★',
    99:'自分の信じていることであれば何回失敗してもやり方を変えない★',100:'失敗すれば反省してすぐに違うやり方でトライする',
    101:'賭け事が好きなほうである',102:'魔性的な魅力を持つ異性に惹かれる',
    103:'食欲や物欲などは強いほうである',104:'目的を達成するためには手段を選ばないほうだ',
    105:'何かをやるかどうか決める一番強い理由は楽しいかどうかだ',106:'べたべたした人間関係が好きである',
    107:'何かと戦っている時が一番充実感がある',108:'遠出するときには多めの服や食べ物を持っていく',
    109:'自分が不利だと思うと、その場から離れたくなる',110:'自分のことになると不安になりやすい面がある',
    111:'親しい人にいわれると間違いだと感じても従うことがある',112:'あらゆることにおいて心配性なところがある',
    113:'他の人をうらやましいと思うことが多いほうだ',114:'自分を支え世話をしてくれる人が周りにいないと不安になる',
    115:'お祭りが大好きだ',116:'プレッシャーがあると逆に活力がでる',
    117:'負けたくやしさはずっと覚えている',118:'ストレスがあると甘いものやお酒に手がのびやすい',
    119:'自分を一番ふるいたたせるのは怒りか恨みであることが多い',120:'自分が好きなことばかりやると周囲によくいわれる',
    121:'志や目標を強くもっている',122:'言いにくいことでも相手のためなら伝えることができる',
    123:'目先の利益で動くのは嫌いだ',124:'怒りをコントロールしてエネルギーを社会のためにプラスにできる',
    125:'自分の未来にお金を投資することができる',126:'トラブルがあるとまずできるだけ情報を集める',
    127:'次の世代に必要なことを最優先に取り組みたい',128:'ストレスがあるとむしろ成長したように感じる',
    129:'つらい事があってもそれをやると気持ちが落ち着く趣味をもっている',
    130:'失敗すると人のせいにしがちだ★',131:'問題があってもそれに巻き込まれずに一歩離れて考えられる',
    132:'困難な状況に直面したとき右往左往することが多い★',133:'他の人からどう思われるかを気にして物事が決められない★',
    134:'悪いことがおこっても、その出来事の良い面を見つけられる',135:'トラブルがあると解決をさき延ばしにする★',
    136:'困った時に助けてくれる親友がいる',137:'選択に迷ったときは楽な方より困難な状況を選ぶ',
    138:'自分の行動指針となる本や師匠がいる',139:'若いころつらいことがあり人に助けられた経験がある',
    140:'行動する前から「うまくいかない」と否定的な事を考える★',
    141:'人が困っていると何を置いても助けたくなる',142:'志が同じ仲間と仕事をしている',
    143:'人から受けた恩は決して忘れないタイプだ',144:'仕事は社会をよくするためにやっている',
    145:'仕事においても自分の型がありそれをやるとうまくいく自信がある',
    146:'過去に何回も痛い目にあったがそれを乗り越えたことで今の自分がある',
    147:'次の世代につながる魂のはいった仕事を私はしているつもりである',
    148:'毎日あきることなく仕事のやりかたを改善している',149:'自分が生まれてきた役割は何であるかわかっている',
    150:'出世しないとほんとうにやりたいことはできないと思う★',
    151:'欧米風の成果をきっちり評価し給料に反映するシステムが好きだ★',
    152:'食事は主に和食にしてできるだけ体調に気を付けている',153:'すこし汗をかくような運動をほぼ毎日している',
    154:'他人に対してはできるだけ誠実でありたい',155:'他人に優しく自分に厳しくしている',
    156:'１年前とは全く別人のように進歩している実感がある',157:'自然や歴史から多くのことを学んでいる',
    158:'仕事を離れてもお互い刺激し向上しあう仲間がいる',
    159:'人に役立つレベルになるには力や技術をまず向上させることが先決だと思う★',
    160:'学んで自分が向上することが人生一番の楽しみだ',
    161:'最近は大声で笑ったことがない',162:'自分の家でため息をつくことはない★',
    163:'寝つきが良くなく、眠れないことが多い',164:'夜中に目が覚めてしまうことが多い',
    165:'下痢や便秘を繰り返している',166:'なぜか憂鬱な気分になりやすいところがある',
    167:'現在、生きがいを感じている★',168:'生活に不安を感じることがある',169:'とても元気である★',
    170:'物事に集中できないことがある',171:'気を張りつめた状態が続いている',
    172:'最近、何をするにも面倒に感じる',173:'すぐにイライラしてしまうことがある',
    174:'仕事がつらいと感じることがよくある',175:'他の人を責めてしまうことがよくある',
    176:'仕事がふえるとパニックになる',177:'月曜日の朝は暗い気持ちになりやすい',
    178:'めまいやふらつきがときどきある',179:'生活習慣病(高血圧、糖尿病等）がある',
    180:'今の仕事はやりがいがある★',
    181:'厳しい状況でも物事のいい面を見つけて落ち込みにくい',182:'あらゆることにおいて心配性なところがある★',
    183:'緊急時が起こっても冷静にまず物事を観察する方だ',184:'状況が悪くなっても楽天的に考えることが多い',
    185:'日常生活において自分の感情を抑えることが多い★',186:'人に頼まれると自分がつらくても断ることができない★',
    187:'他の人をうらやましいと思うことがよくある★',188:'周囲の人に自分は人がいいと思われたい傾向がある★',
    189:'周囲の期待には必ず応えなければいけないと感じる★',190:'短気で怒りっぽいところがある★',
    191:'過去の偉人のような人生を歩みたい',192:'突発的なことがあると慌てることが多い★',
    193:'若いころに厳しい経験をしたので大抵のことは平気だ',194:'ストレスを全く感じたことがない★',
    195:'終わったことでもクヨクヨ悩んでしまうことがある★',196:'嫌いな人はほとんどいない',
    197:'自分が不利になるほど知恵がわいてくる',198:'気が付いたらお酒や異性におぼれることがときどきある★',
    199:'過去に死にかかったことがあり今はおまけの人生だと思う',
    200:'たとえ自分が死んでも自分の志を引き継ぐ人が誰かいると思う',
}

# ★逆転質問番号
star_qs = {83,84,87,89,92,94,98,99,130,132,133,135,140,150,151,159,162,167,169,
           182,185,186,187,188,189,190,192,194,195,198}

# カテゴリ別の質問範囲
categories = {
    '左脳３次元': list(range(1,21)),
    '左脳２次元': list(range(21,41)),
    '右脳３次元': list(range(41,61)),
    '右脳２次元': list(range(61,81)),
    '受動脳': list(range(81,101)),
    '動物脳活性度': list(range(101,121)),
    '動物脳コントロール力': list(range(121,141)),
    '脳活用度': list(range(141,161)),
    'ストレス度': list(range(161,181)),
    'ストレス耐性・日本精神': list(range(181,201)),
}

# 評価ランク判定
def get_rank_brain_use(v):
    if v<=5: return '全くない'
    if v<=24: return 'かなり低い'
    if v<=39: return '低い'
    if v<=53: return 'やや低い'
    if v<=62: return '平均'
    if v<=75: return 'やや高い'
    if v<=90: return '高い'
    return 'かなり高い'

def get_rank_judo(v):  # 受動脳 平均69
    if v<=5: return '全くない'
    if v<=26: return 'かなり低い'
    if v<=41: return '低い'
    if v<=65: return 'やや低い'
    if v<=72: return '平均'
    if v<=80: return 'やや高い'
    if v<=90: return '高い'
    return 'かなり高い'

def get_rank_nodo(v):  # 能動脳 平均51
    if v<=5: return '全くない'
    if v<=24: return 'かなり低い'
    if v<=34: return '低い'
    if v<=46: return 'やや低い'
    if v<=55: return '平均'
    if v<=70: return 'やや高い'
    if v<=80: return '高い'
    return 'かなり高い'

def get_rank_animal_ctrl(v):  # 動物脳コントロール力 平均62
    if v<=5: return '全くない'
    if v<=34: return 'かなり低い'
    if v<=44: return '低い'
    if v<=58: return 'やや低い'
    if v<=65: return '平均'
    if v<=74: return 'やや高い'
    if v<=85: return '高い'
    return 'かなり高い'

def get_rank_animal_act(v):  # 動物脳活性度 最適値42
    if v<=5: return '全くない'
    if v<=18: return 'かなり低い'
    if v<=29: return '低い'
    if v<=39: return 'やや低い'
    if v<=44: return '最適'
    if v<=55: return 'やや高い'
    if v<=80: return '高い'
    return 'かなり高い'

def get_rank_stress(v):  # ストレス度 平均36
    if v<=5: return '全くない'
    if v<=15: return 'かなり低い'
    if v<=25: return '低い'
    if v<=30: return 'やや低い'
    if v<=39: return '平均'
    if v<=50: return 'やや高い'
    if v<=60: return '高い'
    return 'かなり高い'

def get_rank_stress_tol(v):  # ストレス耐性 平均49
    if v<=5: return '全くない'
    if v<=24: return 'かなり低い'
    if v<=34: return '低い'
    if v<=45: return 'やや低い'
    if v<=52: return '平均'
    if v<=60: return 'やや高い'
    if v<=70: return '高い'
    return 'かなり高い'

# ─── 色定義 ──────────────────────────────────────────────────
C_BLUE = '#0070C0'
C_PINK = '#FF69B4'
C_LIGHTBLUE = '#E6F0FF'
C_LIGHTYELLOW = '#FFFFD0'
C_LIGHTORANGE = '#FFE0B0'
C_LIGHTGREEN = '#E6FFE6'
C_RED = '#FF0000'
C_DARK = '#1F3864'
C_GRAY = '#808080'

def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    return buf

# ─── Slide 3: S-BRAIN改善分析（棒グラフ）──────────────────────
def make_bar_chart():
    fig = plt.figure(figsize=(18, 5), facecolor='white')
    fig.suptitle('Ａ様 S-BRAIN改善分析', fontsize=14, fontweight='bold', y=1.0,
                 fontproperties=None)

    colors_subject = ['#2E75B6', '#5B9BD5']
    colors_observer = ['#FF7F7F', '#FFB3B3']

    # ── Chart 1: 左脳・右脳バランス ──
    ax1 = fig.add_subplot(1, 3, 1)
    labels = ['左脳\n(時間・論理)', '右脳\n(空間・感性)']
    s_vals = [subject['left_pct'], subject['right_pct']]
    o_vals = [observer['left_pct'], observer['right_pct']]
    x = np.arange(len(labels))
    w = 0.35
    b1 = ax1.bar(x - w/2, s_vals, w, label='本人', color='#2E75B6')
    b2 = ax1.bar(x + w/2, o_vals, w, label='観察者', color='#FF6B6B')
    ax1.set_title('左脳・右脳バランス改善状況', fontsize=10, fontweight='bold')
    ax1.set_ylim(0, 70)
    ax1.set_xticks(x); ax1.set_xticklabels(labels, fontsize=9)
    ax1.set_ylabel('%', fontsize=9)
    ax1.legend(fontsize=8)
    ax1.yaxis.grid(True, alpha=0.3)
    for bar in list(b1)+list(b2):
        h = bar.get_height()
        ax1.annotate(f'{h}%', xy=(bar.get_x()+bar.get_width()/2, h),
                    xytext=(0,3), textcoords='offset points', ha='center', fontsize=9, fontweight='bold')

    # ── Chart 2: 脳の4タイプ ──
    ax2 = fig.add_subplot(1, 3, 2)
    labels4 = ['左脳\n３次元', '左脳\n２次元', '右脳\n３次元', '右脳\n２次元']
    s_vals4 = [subject['left3_pt'], subject['left2_pt'], subject['right3_pt'], subject['right2_pt']]
    o_vals4 = [observer['left3_pt'], observer['left2_pt'], observer['right3_pt'], observer['right2_pt']]
    x4 = np.arange(len(labels4))
    b3 = ax2.bar(x4 - w/2, s_vals4, w, label='本人', color='#2E75B6')
    b4 = ax2.bar(x4 + w/2, o_vals4, w, label='観察者', color='#FF6B6B')
    ax2.set_title('脳の４タイプ改善状況', fontsize=10, fontweight='bold')
    ax2.set_ylim(0, 45)
    ax2.set_xticks(x4); ax2.set_xticklabels(labels4, fontsize=9)
    ax2.set_ylabel('%', fontsize=9)
    ax2.legend(fontsize=8)
    ax2.yaxis.grid(True, alpha=0.3)
    for bar in list(b3)+list(b4):
        h = bar.get_height()
        ax2.annotate(f'{h}%', xy=(bar.get_x()+bar.get_width()/2, h),
                    xytext=(0,3), textcoords='offset points', ha='center', fontsize=9, fontweight='bold')

    # ── Chart 3: ３次元・２次元 ──
    ax3 = fig.add_subplot(1, 3, 3)
    s_3d = subject['left3_pt'] + subject['right3_pt']
    s_2d = subject['left2_pt'] + subject['right2_pt']
    o_3d = observer['left3_pt'] + observer['right3_pt']
    o_2d = observer['left2_pt'] + observer['right2_pt']
    labels32 = ['３次元\n(大局)', '２次元\n(細部)']
    s_vals32 = [s_3d, s_2d]
    o_vals32 = [o_3d, o_2d]
    x32 = np.arange(len(labels32))
    b5 = ax3.bar(x32 - w/2, s_vals32, w, label='本人', color='#2E75B6')
    b6 = ax3.bar(x32 + w/2, o_vals32, w, label='観察者', color='#FF6B6B')
    ax3.set_title('３次元・２次元改善状況', fontsize=10, fontweight='bold')
    ax3.set_ylim(0, 75)
    ax3.set_xticks(x32); ax3.set_xticklabels(labels32, fontsize=9)
    ax3.set_ylabel('%', fontsize=9)
    ax3.legend(fontsize=8)
    ax3.yaxis.grid(True, alpha=0.3)
    for bar in list(b5)+list(b6):
        h = bar.get_height()
        ax3.annotate(f'{h}%', xy=(bar.get_x()+bar.get_width()/2, h),
                    xytext=(0,3), textcoords='offset points', ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    return fig_to_bytes(fig)

# ─── Slide 4: 分析データ（スケール表）──────────────────────────
def draw_scale_row(ax, y, label, value, ranges_labels, ranges_ends, highlight_color='#FFE0E0'):
    """Draw a single scale row"""
    total_cols = len(ranges_labels)
    col_w = 1.0 / total_cols
    # find which bucket the value falls in
    bucket = len(ranges_ends)
    for i, end in enumerate(ranges_ends):
        if value <= end:
            bucket = i
            break

    for i, lbl in enumerate(ranges_labels):
        x = i * col_w
        color = highlight_color if i == bucket else '#F0F0F0'
        if i == bucket:
            ax.add_patch(plt.Rectangle((x, y-0.4), col_w, 0.8, color=color, transform=ax.transData))
        ax.add_patch(plt.Rectangle((x, y-0.4), col_w, 0.8, fill=False, edgecolor='gray', lw=0.5, transform=ax.transData))
        ax.text(x + col_w/2, y, lbl, ha='center', va='center', fontsize=7)
        if i == bucket:
            ax.text(x + col_w/2, y - 0.35, '●', ha='center', va='bottom', fontsize=8, color='black')

def make_scale_table():
    fig, ax = plt.subplots(figsize=(18, 9), facecolor='white')
    ax.set_xlim(-0.25, 1.0)
    ax.set_ylim(0, 24)
    ax.axis('off')

    scale_data = [
        # (label, value, ranges_labels, ranges_ends)
        ('脳活用度\n(本人)', subject['brain_use'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,24,39,53,62,75,90,999]),
        ('脳活用度\n(観察者)', observer['brain_use'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,24,39,53,62,75,90,999]),
        ('受動脳\n(本人)', subject['judo_pt'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,26,41,65,72,80,90,999]),
        ('受動脳\n(観察者)', observer['judo_pt'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,26,41,65,72,80,90,999]),
        ('能動脳\n(本人)', subject['nodo_pt'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,24,34,46,55,70,80,999]),
        ('能動脳\n(観察者)', observer['nodo_pt'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,24,34,46,55,70,80,999]),
    ]
    scale_data2 = [
        ('動物脳\nコントロール力\n(本人)', subject['animal_ctrl'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,34,44,58,65,74,85,999]),
        ('動物脳\nコントロール力\n(観察者)', observer['animal_ctrl'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,34,44,58,65,74,85,999]),
        ('動物脳\n活性度\n(本人)', subject['animal_act'],
         ['全くない','かなり低い','低い','やや低い','最適','やや高い','高い','かなり高い'],
         [5,18,29,39,44,55,80,999]),
        ('動物脳\n活性度\n(観察者)', observer['animal_act'],
         ['全くない','かなり低い','低い','やや低い','最適','やや高い','高い','かなり高い'],
         [5,18,29,39,44,55,80,999]),
        ('ストレス度\n(本人)', subject['stress'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,15,25,30,39,50,60,999]),
        ('ストレス度\n(観察者)', observer['stress'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,15,25,30,39,50,60,999]),
        ('ストレス\n耐性\n(本人)', subject['stress_tol'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,24,34,45,52,60,70,999]),
        ('ストレス\n耐性\n(観察者)', observer['stress_tol'],
         ['全くない','かなり低い','低い','やや低い','平均','やや高い','高い','かなり高い'],
         [5,24,34,45,52,60,70,999]),
    ]

    ax.text(0.375, 23.5, '分析データ（スケール表）', ha='center', va='center',
            fontsize=14, fontweight='bold', color=C_DARK)

    y_positions_left = [22, 21, 20, 19, 18, 17]
    for i, (lbl, val, rlbls, rends) in enumerate(scale_data):
        y = y_positions_left[i] - 0.5
        ax.text(-0.22, y+0.5, lbl, ha='left', va='center', fontsize=8, fontweight='bold',
                color='#FF0000' if '本人' in lbl else '#0070C0')
        val_color = '#FF0000' if '本人' in lbl else '#0070C0'
        ax.text(-0.02, y+0.5, str(val), ha='center', va='center', fontsize=10, fontweight='bold', color=val_color)
        draw_scale_row(ax, y+0.5, lbl, val, rlbls, rends,
                       '#FFCCCC' if '本人' in lbl else '#CCE5FF')

    y_positions_right = [22, 21, 20, 19, 18, 17, 16, 15]
    ax2 = ax.twinx()
    ax2.set_xlim(0.5, 1.75)
    ax2.set_ylim(0, 24)
    ax2.axis('off')
    for i, (lbl, val, rlbls, rends) in enumerate(scale_data2):
        pass  # will handle differently

    plt.tight_layout()
    plt.close(fig)

    # Simpler version - create a proper table figure
    fig2, axes = plt.subplots(14, 1, figsize=(16, 18), facecolor='white')
    fig2.suptitle('分析データ（スケール表）', fontsize=13, fontweight='bold', y=0.99)

    all_data = scale_data + scale_data2
    rank_fns = [
        get_rank_brain_use, get_rank_brain_use,
        get_rank_judo, get_rank_judo,
        get_rank_nodo, get_rank_nodo,
        get_rank_animal_ctrl, get_rank_animal_ctrl,
        get_rank_animal_act, get_rank_animal_act,
        get_rank_stress, get_rank_stress,
        get_rank_stress_tol, get_rank_stress_tol,
    ]

    for idx, (ax_row, (lbl, val, rlbls, rends), rfn) in enumerate(zip(axes, all_data, rank_fns)):
        ax_row.set_xlim(0, len(rlbls))
        ax_row.set_ylim(0, 1)
        ax_row.axis('off')
        is_subject = '本人' in lbl
        row_color = '#FFCCCC' if is_subject else '#CCE5FF'
        label_color = '#C00000' if is_subject else '#0070C0'

        rank = rfn(val)
        bucket = 0
        for bi, end in enumerate(rends):
            if val <= end:
                bucket = bi
                break

        for ci, col_lbl in enumerate(rlbls):
            bg = row_color if ci == bucket else '#F5F5F5'
            ax_row.add_patch(plt.Rectangle((ci, 0.1), 1, 0.8, color=bg, ec='gray', lw=0.5))
            ax_row.text(ci+0.5, 0.55, col_lbl, ha='center', va='center', fontsize=7)
            if ci == bucket:
                ax_row.text(ci+0.5, 0.2, '●', ha='center', va='center', fontsize=10, color='black')

        short_lbl = lbl.replace('\n', ' ')
        ax_row.text(-0.5, 0.5, f'{short_lbl} {val}', ha='right', va='center',
                   fontsize=8, fontweight='bold', color=label_color)

    plt.tight_layout(rect=[0.12, 0, 1, 0.98])
    return fig_to_bytes(fig2)

# ─── Slide 5: 本人観察者 S-BRAIN脳活診断結果（新シート）─────────
def make_analysis_sheet():
    fig = plt.figure(figsize=(20, 12), facecolor='white')
    fig.text(0.5, 0.98, 'Ａ様　本人観察者 S-BRAIN脳活診断結果',
             ha='center', va='top', fontsize=14, fontweight='bold', color=C_DARK)

    # --- 左パネル ---
    def draw_box(ax, x, y, w, h, text, bg='#E6F0FF', fontsize=9, bold=True, align='center'):
        ax.add_patch(plt.Rectangle((x,y), w, h, color=bg, ec='black', lw=0.7))
        ax.text(x+w/2, y+h/2, text, ha=align if align=='center' else 'left',
                va='center', fontsize=fontsize, fontweight='bold' if bold else 'normal',
                wrap=True)

    ax = fig.add_axes([0.02, 0.02, 0.96, 0.94])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Section headers
    ax.add_patch(plt.Rectangle((0,11), 20, 0.7, color='#1F3864', ec='black', lw=1))
    ax.text(10, 11.35, 'Ａ様　本人観察者 S-BRAIN脳活診断結果', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    # ── 1. 脳タイプ ──
    ax.add_patch(plt.Rectangle((0,9.5), 9.5, 1.4, color='#BDD7EE', ec='black', lw=0.8))
    ax.text(0.1, 10.85, '１ あなたの脳タイプは', fontsize=9, fontweight='bold', color=C_DARK)
    ax.text(0.3, 10.35, '・脳タイプは15タイプある', fontsize=8, color='black')
    ax.add_patch(plt.Rectangle((0.1, 9.6), 4.2, 0.7, color='#FF6B6B', ec='none'))
    ax.text(2.2, 9.95, f'本人: {subject["brain_type"]}', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')
    ax.add_patch(plt.Rectangle((4.5, 9.6), 4.9, 0.7, color='#5B9BD5', ec='none'))
    ax.text(6.9, 9.95, f'観察者: {observer["brain_type"]}', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')

    # ── 2. 脳タイプ詳細 ──
    ax.add_patch(plt.Rectangle((0,7.2), 9.5, 2.2, color='#DEEAF1', ec='black', lw=0.8))
    ax.text(0.1, 9.3, '２ 脳タイプ詳細', fontsize=9, fontweight='bold', color=C_DARK)
    # Left/Right balance
    ax.text(0.1, 8.9, '・左右脳のバランス', fontsize=8, fontweight='bold')
    ax.add_patch(plt.Rectangle((0.1,8.4), 4.2, 0.4, color='#FFCCCC', ec='gray', lw=0.3))
    ax.text(2.2, 8.6, f'本人  左脳{subject["left_pct"]}% ／ 右脳{subject["right_pct"]}%（右脳優位）',
            ha='center', va='center', fontsize=8, color='#C00000', fontweight='bold')
    ax.add_patch(plt.Rectangle((0.1,7.9), 4.2, 0.4, color='#CCE5FF', ec='gray', lw=0.3))
    ax.text(2.2, 8.1, f'観察者 左脳{observer["left_pct"]}% ／ 右脳{observer["right_pct"]}%（左脳優位）',
            ha='center', va='center', fontsize=8, color='#0070C0', fontweight='bold')
    # 3D/2D
    ax.text(4.7, 8.9, '・三次元と二次元', fontsize=8, fontweight='bold')
    ax.add_patch(plt.Rectangle((4.7,8.4), 4.7, 0.4, color='#FFCCCC', ec='gray', lw=0.3))
    s_3d = subject['left3_pt']+subject['right3_pt']
    s_2d = subject['left2_pt']+subject['right2_pt']
    o_3d = observer['left3_pt']+observer['right3_pt']
    o_2d = observer['left2_pt']+observer['right2_pt']
    ax.text(7.05, 8.6, f'本人  ３次元{s_3d} ／ ２次元{s_2d}（３次元優位）',
            ha='center', va='center', fontsize=8, color='#C00000', fontweight='bold')
    ax.add_patch(plt.Rectangle((4.7,7.9), 4.7, 0.4, color='#CCE5FF', ec='gray', lw=0.3))
    ax.text(7.05, 8.1, f'観察者 ３次元{o_3d} ／ ２次元{o_2d}（３次元優位）',
            ha='center', va='center', fontsize=8, color='#0070C0', fontweight='bold')
    # 4タイプ
    ax.text(0.1, 7.7, '・脳の４タイプ', fontsize=8, fontweight='bold')
    ax.add_patch(plt.Rectangle((0.1,7.25), 9.2, 0.4, color='#FFCCCC', ec='gray', lw=0.3))
    ax.text(4.7, 7.45,
            f'本人  右3({subject["right3_pt"]}) ＞ 左3({subject["left3_pt"]}) ＞ 左2({subject["left2_pt"]}) ＞ 右2({subject["right2_pt"]})',
            ha='center', va='center', fontsize=8, color='#C00000', fontweight='bold')

    # ── 3. 現在の脳活用度 ──
    ax.add_patch(plt.Rectangle((0,5.8), 9.5, 1.3, color='#BDD7EE', ec='black', lw=0.8))
    ax.text(0.1, 7.0, '３ 現在の脳活用度', fontsize=9, fontweight='bold', color=C_DARK)
    ax.text(0.1, 6.55, f'脳活用度は平均58に対して', fontsize=8)
    ax.add_patch(plt.Rectangle((0.1,5.9), 4.2, 0.55, color='#FFCCCC', ec='gray', lw=0.3))
    ax.text(2.2, 6.17, f'本人: {subject["brain_use"]}  　　 → {get_rank_brain_use(subject["brain_use"])}',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#C00000')
    ax.add_patch(plt.Rectangle((4.5,5.9), 4.9, 0.55, color='#CCE5FF', ec='gray', lw=0.3))
    ax.text(6.9, 6.17, f'観察者: {observer["brain_use"]}  　 → {get_rank_brain_use(observer["brain_use"])}',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#0070C0')

    # ── 4. 受動脳と能動脳 ──
    ax.add_patch(plt.Rectangle((0,4.0), 9.5, 1.7, color='#DEEAF1', ec='black', lw=0.8))
    ax.text(0.1, 5.6, '４ 受動脳と能動脳', fontsize=9, fontweight='bold', color=C_DARK)
    ax.text(0.1, 5.2, f'受動脳は平均69に対して', fontsize=8)
    ax.add_patch(plt.Rectangle((0.1,4.75), 9.2, 0.35, color='#FFCCCC', ec='gray', lw=0.3))
    ax.text(4.7, 4.92, f'本人: {subject["judo_pt"]}  → {get_rank_judo(subject["judo_pt"])}　　／　　観察者: {observer["judo_pt"]}  → {get_rank_judo(observer["judo_pt"])}',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#C00000')
    ax.text(0.1, 4.65, f'能動脳は平均51に対して', fontsize=8)
    ax.add_patch(plt.Rectangle((0.1,4.1), 9.2, 0.35, color='#CCE5FF', ec='gray', lw=0.3))
    ax.text(4.7, 4.27, f'本人: {subject["nodo_pt"]}  → {get_rank_nodo(subject["nodo_pt"])}　　　／　　観察者: {observer["nodo_pt"]}  → {get_rank_nodo(observer["nodo_pt"])}',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0070C0')

    # ── 5. 動物脳コントロール力と動物脳活性度 ──
    ax.add_patch(plt.Rectangle((10,9.5), 9.8, 1.4, color='#BDD7EE', ec='black', lw=0.8))
    ax.text(10.1, 10.85, '５ 動物脳コントロール力と動物脳活性度', fontsize=9, fontweight='bold', color=C_DARK)
    ax.text(10.1, 10.4, f'動物脳コントロール力は平均62に対して', fontsize=8)
    ax.add_patch(plt.Rectangle((10.1,9.6), 9.5, 0.65, color='#FFCCCC', ec='gray', lw=0.3))
    ax.text(14.8, 9.92, f'本人: {subject["animal_ctrl"]}  → {get_rank_animal_ctrl(subject["animal_ctrl"])}',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#C00000')

    ax.add_patch(plt.Rectangle((10,7.4), 9.8, 2.0, color='#DEEAF1', ec='black', lw=0.8))
    ax.text(10.1, 9.3, f'　　　　→ 観察者: {observer["animal_ctrl"]}  → {get_rank_animal_ctrl(observer["animal_ctrl"])}', fontsize=8.5, fontweight='bold', color='#0070C0')
    ax.text(10.1, 8.9, f'動物脳活性度は最適値42に対して', fontsize=8)
    ax.add_patch(plt.Rectangle((10.1,8.4), 9.5, 0.38, color='#FFCCCC', ec='gray', lw=0.3))
    ax.text(14.8, 8.59, f'本人: {subject["animal_act"]}  → {get_rank_animal_act(subject["animal_act"])}',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#C00000')
    ax.add_patch(plt.Rectangle((10.1,7.9), 9.5, 0.38, color='#CCE5FF', ec='gray', lw=0.3))
    ax.text(14.8, 8.09, f'観察者: {observer["animal_act"]}  → {get_rank_animal_act(observer["animal_act"])}',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#0070C0')
    ax.add_patch(plt.Rectangle((10.1,7.45), 9.5, 0.38, color='#FFFFD0', ec='gray', lw=0.3))
    ax.text(14.8, 7.64, '※動物脳活性度が高い → 本能的行動傾向・瞬発力が高い状態',
            ha='center', va='center', fontsize=7.5, color='#7B7B00')

    # ── 6. ストレス度とストレス耐性 ──
    ax.add_patch(plt.Rectangle((10,5.5), 9.8, 1.8, color='#BDD7EE', ec='black', lw=0.8))
    ax.text(10.1, 7.2, '６ ストレス度とストレス耐性', fontsize=9, fontweight='bold', color=C_DARK)
    ax.text(10.1, 6.8, f'ストレス度は平均36に対して', fontsize=8)
    ax.add_patch(plt.Rectangle((10.1,6.35), 9.5, 0.38, color='#FFCCCC', ec='gray', lw=0.3))
    ax.text(14.8, 6.54, f'本人: {subject["stress"]}  → {get_rank_stress(subject["stress"])}',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#C00000')
    ax.add_patch(plt.Rectangle((10.1,5.9), 9.5, 0.38, color='#CCE5FF', ec='gray', lw=0.3))
    ax.text(14.8, 6.09, f'観察者: {observer["stress"]}  → {get_rank_stress(observer["stress"])}',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#0070C0')
    ax.text(10.1, 5.78, f'ストレス耐性は平均49に対して', fontsize=8)
    ax.add_patch(plt.Rectangle((10.1,5.55), 9.5, 0.22, color='#FFFFD0', ec='gray', lw=0.3))
    ax.text(14.8, 5.66, f'本人: {subject["stress_tol"]} → {get_rank_stress_tol(subject["stress_tol"])}  ／  観察者: {observer["stress_tol"]} → {get_rank_stress_tol(observer["stress_tol"])}',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#7B3F00')

    # ── 7. カウンセラーからのアドバイス ──
    ax.add_patch(plt.Rectangle((0,0.1), 19.8, 3.8, color='#FFF2CC', ec='black', lw=1.2))
    ax.text(0.2, 3.7, '７ カウンセラーからのアドバイス', fontsize=10, fontweight='bold', color='#7B3F00')

    advice_text = (
        "【脳タイプ】右脳３次元優位スタイル。右脳（空間・感性）と３次元（大局）が最も強く、"
        "アイデアや直感で大局をつかむ行動派。左右脳ほぼ均等で両面をバランスよく使える強みがある。\n\n"
        "【脳活用度・受動脳・能動脳】脳活用度は75でやや高い。受動脳83は高く、周囲の情報を幅広く収集する力が非常に高い。\n"
        "一方、能動脳52は平均的で、受動脳に比べて判断・決断する力はやや劣る可能性がある。\n"
        "観察者との比較では、脳活用度・受動脳・能動脳はともに本人の方がやや高い。\n\n"
        "【動物脳】動物脳コントロール力84は「高い」、動物脳活性度61は「高い」（最適値42を超え）。\n"
        "感情のエネルギーは大きく、コントロール力も高いが、最適値を超えているため本能的行動が出やすい。\n"
        "強いこだわりやターゲットに固執する傾向は、高い動物脳活性度が一因となっている可能性がある。\n\n"
        "【ストレス】ストレス度26はやや低く、ストレス耐性64は高い。観察者のストレス耐性75（かなり高い）と比べてやや低い。\n"
        "主観的なストレス感覚は低いが、周囲への影響（攻撃性・巻き込み型の問題解決スタイル）が懸念される。\n\n"
        "【アドバイス】IQ132の高い知性と感性を活かしつつ、「動物脳の最適化」（受動脳と能動脳のバランス調整）が課題。\n"
        "気になることへの固執を手放すマインドフルネスや、趣味・瞑想で心を落ち着かせる習慣づくりを勧める。"
    )
    ax.text(0.3, 3.4, advice_text, fontsize=7.8, va='top', wrap=True,
            multialignment='left', color='#1A1A1A',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFDE7', edgecolor='none'))

    return fig_to_bytes(fig)

# ─── Slides 6-8: 200問回答データ ─────────────────────────────────
def make_200q_page(cat_pairs, title_suffix=''):
    """cat_pairs: list of (category_name, q_range) tuples, max 2 pairs per page"""
    n = len(cat_pairs)
    fig, axes = plt.subplots(1, n, figsize=(18 if n==2 else 10, 20), facecolor='white')
    if n == 1:
        axes = [axes]

    fig.suptitle(f'200問回答データ分析 {title_suffix}', fontsize=13, fontweight='bold', y=1.0)

    for ax_idx, (cat_name, q_range) in enumerate(cat_pairs):
        ax = axes[ax_idx]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, len(q_range)+2.5)
        ax.axis('off')

        # Header
        ax.add_patch(plt.Rectangle((0, len(q_range)+1.8), 10, 0.65, color=C_DARK, ec='none'))
        ax.text(5, len(q_range)+2.12, cat_name, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

        # Column headers
        col_x = [0.3, 5.5, 7.0, 8.4, 9.5]
        col_w = [5.2, 1.4, 1.3, 1.1, 0.5]
        headers_row = ['質問内容', '本人', '観察者', '差', '']
        col_colors = ['#E2EFDA', '#FFDDD0', '#D0E8FF', '#FFFFD0', 'white']
        for ci, (cx, cw, ch, cc) in enumerate(zip(col_x, col_w, headers_row, col_colors)):
            ax.add_patch(plt.Rectangle((cx, len(q_range)+1.2), cw, 0.55, color=cc, ec='gray', lw=0.5))
            ax.text(cx+cw/2, len(q_range)+1.47, ch, ha='center', va='center', fontsize=8, fontweight='bold')

        # Sub-headers
        ax.add_patch(plt.Rectangle((5.5, len(q_range)+0.8), 1.4, 0.35, color='#FFDDD0', ec='gray', lw=0.3))
        ax.text(6.2, len(q_range)+0.97, f'{subject["name"]}', ha='center', va='center', fontsize=7, color='#C00000', fontweight='bold')
        ax.add_patch(plt.Rectangle((7.0, len(q_range)+0.8), 1.3, 0.35, color='#D0E8FF', ec='gray', lw=0.3))
        ax.text(7.65, len(q_range)+0.97, '観察者', ha='center', va='center', fontsize=7, color='#0070C0', fontweight='bold')
        ax.add_patch(plt.Rectangle((8.4, len(q_range)+0.8), 1.1, 0.35, color='#FFFFD0', ec='gray', lw=0.3))
        ax.text(8.95, len(q_range)+0.97, '差', ha='center', va='center', fontsize=7, fontweight='bold')

        # Data rows
        for row_i, qno in enumerate(q_range):
            s_ans = subject['answers'][qno-1]
            o_ans = observer['answers'][qno-1]
            diff = s_ans - o_ans
            is_star = qno in star_qs
            y_pos = len(q_range) - row_i - 0.15

            # Row background
            row_bg = '#FFF8F0' if row_i % 2 == 0 else 'white'
            ax.add_patch(plt.Rectangle((0.3, y_pos), 9.2, 0.7, color=row_bg, ec='none'))

            # Highlight big differences
            if abs(diff) >= 3:
                ax.add_patch(plt.Rectangle((0.3, y_pos), 9.2, 0.7, color='#FFE0E0', ec='none', alpha=0.7))
            elif abs(diff) >= 2:
                ax.add_patch(plt.Rectangle((0.3, y_pos), 9.2, 0.7, color='#FFF0C0', ec='none', alpha=0.5))

            # Q number
            qno_text = f'Q{qno:03d}'
            star_marker = '★' if is_star else ''
            ax.text(0.1, y_pos+0.35, qno_text, ha='center', va='center', fontsize=6.5)

            # Question text (truncated)
            q_text = q_texts.get(qno, '')
            if is_star:
                q_text_disp = q_text[:22] + ('…' if len(q_text)>22 else '') + '★'
                ax.text(0.35, y_pos+0.35, q_text_disp, va='center', fontsize=6.5, color='#CC0000')
            else:
                q_text_disp = q_text[:24] + ('…' if len(q_text)>24 else '')
                ax.text(0.35, y_pos+0.35, q_text_disp, va='center', fontsize=6.5)

            # Scores
            s_color = '#C00000'
            o_color = '#0070C0'
            ax.add_patch(plt.Rectangle((5.5, y_pos+0.05), 1.35, 0.6,
                         color='#FFDDD0', ec='gray', lw=0.3))
            ax.text(6.2, y_pos+0.35, str(s_ans), ha='center', va='center',
                    fontsize=9, fontweight='bold', color=s_color)
            ax.add_patch(plt.Rectangle((7.0, y_pos+0.05), 1.25, 0.6,
                         color='#D0E8FF', ec='gray', lw=0.3))
            ax.text(7.62, y_pos+0.35, str(o_ans), ha='center', va='center',
                    fontsize=9, fontweight='bold', color=o_color)

            # Difference
            diff_color = '#C00000' if diff > 0 else ('#0070C0' if diff < 0 else 'gray')
            diff_bg = '#FFD0D0' if abs(diff) >= 3 else ('#FFFFD0' if abs(diff) >= 2 else '#F5F5F5')
            ax.add_patch(plt.Rectangle((8.4, y_pos+0.05), 1.05, 0.6,
                         color=diff_bg, ec='gray', lw=0.3))
            ax.text(8.92, y_pos+0.35, f'{diff:+d}' if diff != 0 else '0',
                    ha='center', va='center', fontsize=8, fontweight='bold', color=diff_color)

            # Grid line
            ax.axhline(y=y_pos, color='#CCCCCC', lw=0.3)

        # Bottom border
        ax.axhline(y=0.85, color='gray', lw=0.8)

        # Legend
        ax.text(0.3, 0.5, '■差が±3以上 → 本人・観察者で大きく認識が異なる設問', fontsize=6.5, color='#C00000')
        ax.text(0.3, 0.15, '■差が±2 → 認識に差あり。★=逆転質問（高得点が低い傾向を意味する）', fontsize=6.5, color='#7B7B00')

    plt.tight_layout()
    return fig_to_bytes(fig)

# ─── Slide 9: その他の特徴（発達特性関連） ────────────────────────
def make_special_features():
    fig, ax = plt.subplots(figsize=(18, 10), facecolor='white')
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.add_patch(plt.Rectangle((0, 9.3), 18, 0.7, color=C_DARK, ec='none'))
    ax.text(9, 9.65, 'その他の特徴（発達特性・メンタル傾向の観点から）', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    # ASD/発達傾向関連設問の観察
    noted_qs = [
        (33, '自分の考えを他人にあてはめて責めてしまうことがある'),
        (4, '前置きの長い話や意図の見えない話にイライラする'),
        (24, '待ち合わせや締め切りを守れない人は許せない'),
        (10, '理屈のあわない行動をする人は苦手だ'),
        (46, '決断が速く、せっかちだと言われる'),
        (116, 'プレッシャーがあると逆に活力がでる'),
        (107, '何かと戦っている時が一番充実感がある'),
        (99, '自分の信じていることであれば何回失敗してもやり方を変えない★'),
        (117, '負けたくやしさはずっと覚えている'),
        (175, '他の人を責めてしまうことがよくある'),
        (120, '自分が好きなことばかりやると周囲によくいわれる'),
        (130, '失敗すると人のせいにしがちだ★'),
    ]

    ax.add_patch(plt.Rectangle((0.2, 8.8), 17.6, 0.45, color='#FFE0B0', ec='black', lw=0.5))
    ax.text(9, 9.02, '注目設問：認識の乖離が大きい、または特性に関連する設問', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#7B3F00')

    headers_x = [0.3, 1.0, 6.5, 9.0, 11.0, 13.0]
    ax.text(0.65, 8.55, 'NO', ha='center', fontsize=8, fontweight='bold')
    ax.text(4.0, 8.55, '設問内容', ha='center', fontsize=8, fontweight='bold')
    ax.text(9.0, 8.55, f'{subject["name"]}', ha='center', fontsize=8, fontweight='bold', color='#C00000')
    ax.text(11.0, 8.55, '観察者', ha='center', fontsize=8, fontweight='bold', color='#0070C0')
    ax.text(13.0, 8.55, '差', ha='center', fontsize=8, fontweight='bold')
    ax.text(15.5, 8.55, '観察者コメント', ha='center', fontsize=8, fontweight='bold')
    ax.axhline(8.35, color='gray', lw=0.8, xmin=0.01, xmax=0.99)

    comments = {
        33: '実際に職場でも指摘あり',
        4: '会議・報告で顕著に観察',
        24: '完璧主義の現れ',
        10: '論理矛盾に強く反応する',
        46: '会議でも素早い判断傾向',
        116: 'プレッシャー下でむしろ攻撃的に',
        107: '競争場面での集中力は高い',
        99: '一度決めたら変えない強さと課題',
        117: 'ネガティブ感情の保持が長い',
        175: '部下への厳しさとして現れる',
        120: '過集中の傾向か',
        130: '責任転嫁への観察者の認識と本人のズレ',
    }

    for ri, (qno, qtext) in enumerate(noted_qs):
        s_ans = subject['answers'][qno-1]
        o_ans = observer['answers'][qno-1]
        diff = s_ans - o_ans
        y = 8.1 - ri * 0.62
        bg = '#FFF0F0' if ri % 2 == 0 else 'white'
        if abs(diff) >= 2:
            bg = '#FFE8CC'
        ax.add_patch(plt.Rectangle((0.2, y-0.28), 17.6, 0.55, color=bg, ec='#DDDDDD', lw=0.3))
        ax.text(0.65, y, f'Q{qno:03d}', ha='center', va='center', fontsize=7.5)
        is_star = qno in star_qs
        disp_text = qtext[:30] + ('…' if len(qtext)>30 else '') + ('★' if is_star else '')
        ax.text(1.1, y, disp_text, va='center', fontsize=7.5, color='#C00000' if is_star else 'black')
        ax.text(9.0, y, str(s_ans), ha='center', va='center', fontsize=9, fontweight='bold', color='#C00000')
        ax.text(11.0, y, str(o_ans), ha='center', va='center', fontsize=9, fontweight='bold', color='#0070C0')
        diff_color = '#C00000' if diff > 0 else '#0070C0'
        ax.text(13.0, y, f'{diff:+d}' if diff != 0 else '0', ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=diff_color)
        comment = comments.get(qno, '')
        ax.text(14.0, y, comment, va='center', fontsize=7, color='#555555')

    # Summary box
    ax.add_patch(plt.Rectangle((0.2, 0.1), 17.6, 1.1, color='#FFF9C4', ec='#CCAA00', lw=1.2))
    ax.text(0.5, 1.0, '■ 特性に関するまとめ観察:', fontsize=8.5, fontweight='bold', color='#7B3F00', va='top')
    summary_txt = (
        '・ IQ132（メンサ会員）かつ発達障害診断。高い論理性と感性（右脳3次元優位）が共存している。\n'
        '・ 「気になると頭から離れない」「自分のやり方を通す」傾向は高い動物脳活性度（61）と一致する。\n'
        '・ 受動脳83（高い）は情報収集能力の高さを示す一方、能動脳52（平均）とのギャップが決断・調整の困難さに繋がる可能性。\n'
        '・ ストレス耐性64は高めだが、周囲への影響（攻撃性・巻き込み型）は本人自覚より観察者側で強く感じられている。'
    )
    ax.text(0.5, 0.85, summary_txt, va='top', fontsize=7.8, color='#1A1A1A',
            multialignment='left')

    return fig_to_bytes(fig)

# ─── スライド作成 ──────────────────────────────────────────────
print('Loading template...')
prs = Presentation('/tmp/template.pptx')
slide_width = prs.slide_width
slide_height = prs.slide_height

def add_footer(slide, text='（C）2026.（一社）篠浦塾'):
    from pptx.util import Inches, Pt
    txBox = slide.shapes.add_textbox(Inches(4.4), Inches(7.1), Inches(4.5), Inches(0.4))
    tf = txBox.text_frame
    tf.text = text
    tf.paragraphs[0].font.size = Pt(8)
    tf.paragraphs[0].font.color.rgb = RGBColor(0x60,0x60,0x60)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

def set_text_box(shape, text, font_size=None, bold=False, color=None, align=PP_ALIGN.CENTER):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    if font_size:
        p.font.size = Pt(font_size)
    if bold:
        p.font.bold = True
    if color:
        p.font.color.rgb = color

def insert_image_to_slide(slide, img_bytes, left, top, width, height):
    img_bytes.seek(0)
    slide.shapes.add_picture(img_bytes, left, top, width, height)

# ── Slide 1: タイトル (use template slide 1) ──
slide1 = prs.slides[0]
for shape in slide1.shapes:
    if shape.has_text_frame and '○○' in shape.text:
        set_text_box(shape, 'Ａ様（40代女性・広報担当）\nS-BRAIN脳活診断 分析発表', font_size=20, bold=True,
                    color=RGBColor(0x1F,0x38,0x64))

# ── Slide 2: ライフヒストリー (new slide) ──
from pptx.util import Inches, Pt
slide_layout = prs.slide_layouts[6]  # blank layout

def add_blank_slide():
    return prs.slides.add_slide(prs.slide_layouts[6])

slide_life = add_blank_slide()

# Title bar
from pptx.oxml.ns import qn
def add_colored_rect(slide, left, top, width, height, color_rgb):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color_rgb
    shape.line.color.rgb = color_rgb
    return shape

title_bar = add_colored_rect(slide_life, Inches(0), Inches(0), Inches(13.33), Inches(0.75),
                              RGBColor(0x1F,0x38,0x64))
txb = slide_life.shapes.add_textbox(Inches(0.2), Inches(0.1), Inches(12), Inches(0.6))
txb.text_frame.text = 'Ａ様　ライフヒストリー'
txb.text_frame.paragraphs[0].font.size = Pt(20)
txb.text_frame.paragraphs[0].font.bold = True
txb.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF,0xFF,0xFF)

# Profile box
profile_box = add_colored_rect(slide_life, Inches(0.3), Inches(0.85), Inches(4.0), Inches(1.2),
                                RGBColor(0xBD,0xD7,0xEE))
txb2 = slide_life.shapes.add_textbox(Inches(0.4), Inches(0.9), Inches(3.8), Inches(1.1))
tf2 = txb2.text_frame
tf2.word_wrap = True
p0 = tf2.paragraphs[0]
p0.text = '基本プロフィール'
p0.font.size = Pt(11); p0.font.bold = True; p0.font.color.rgb = RGBColor(0x1F,0x38,0x64)
for line in ['・年齢: 40代　・性別: 女性', '・職業: 広報担当（PRtimes・広報業務）', '・IQ: 132　（メンサ会員）', '・発達障害診断あり']:
    p_new = tf2.add_paragraph()
    p_new.text = line; p_new.font.size = Pt(10)

# Main history text
txb3 = slide_life.shapes.add_textbox(Inches(0.3), Inches(2.15), Inches(12.8), Inches(5.1))
tf3 = txb3.text_frame
tf3.word_wrap = True

history_lines = [
    ('●生育歴・家庭背景', True),
    ('・発達障害の父親のもとで育つ。父親との関係が対人スタイルや物事の見方に影響。', False),
    ('・子供2名を育てながら多様な仕事をこなしてきた。強い責任感と実行力を持つ。', False),
    ('', False),
    ('●職業・強み', True),
    ('・文章を書くことが得意。PRtimes執筆・広報業務で活躍している。', False),
    ('・理路整然とした論理展開が得意で、企画・発信力が高い。', False),
    ('・非常に優秀で仕事の質が高く、高い成果を出してきた。', False),
    ('', False),
    ('●対人関係・観察者が感じた特徴', True),
    ('・仕事のやりにくさを感じると徹底的に改善しようとし、周囲を巻き込む傾向がある。', False),
    ('・「気になるとずっと頭から離れない」→ ターゲットが時期によって変わる。', False),
    ('・部下・同僚からは「怖い」「一方的」「無茶ぶりがすごい」という声も聞かれる。', False),
    ('・仕事上でやりにくかった複数の人物の悪口を、繰り返し話す傾向がある。', False),
    ('', False),
    ('●最近の出来事', True),
    ('・IQ132と判明し、メンサ（世界的高IQ団体）の会員登録を完了。', False),
    ('・発達障害（ASD/ADHD傾向）の診断が最近下された。', False),
    ('・自己理解を深め、強みを活かしながら弱みに向き合う時期にある。', False),
]

first = True
for (text, is_bold) in history_lines:
    if first:
        p_hist = tf3.paragraphs[0]; first = False
    else:
        p_hist = tf3.add_paragraph()
    p_hist.text = text
    p_hist.font.size = Pt(10.5)
    if is_bold:
        p_hist.font.bold = True
        p_hist.font.color.rgb = RGBColor(0x1F,0x38,0x64)
    else:
        p_hist.font.color.rgb = RGBColor(0x1A,0x1A,0x1A)

add_footer(slide_life)

# ── Slide 3: S-BRAIN結果（本人・観察者）──
slide3 = prs.slides[1]  # template slide 2
# Remove the placeholder ovals and add images
shapes_to_remove = []
for shape in slide3.shapes:
    if shape.shape_type == 1 and 'テスト結果' in shape.text:  # AutoShape oval with placeholder text
        shapes_to_remove.append(shape)
for shape in shapes_to_remove:
    sp = shape._element
    sp.getparent().remove(sp)

# Add the S-BRAIN result images
with open('/tmp/fu09res-1.png', 'rb') as f:
    fu09_bytes = io.BytesIO(f.read())
with open('/tmp/fu10res-1.png', 'rb') as f:
    fu10_bytes = io.BytesIO(f.read())

slide3.shapes.add_picture(fu09_bytes, Inches(0.3), Inches(1.5), Inches(6.2), Inches(5.7))
slide3.shapes.add_picture(fu10_bytes, Inches(6.8), Inches(1.5), Inches(6.2), Inches(5.7))

# ── Slide 4: S-BRAIN改善分析 ──
slide4 = prs.slides[2]  # template slide 3
# Replace sample image
for shape in list(slide4.shapes):
    if shape.shape_type == 13:  # PICTURE
        sp = shape._element; sp.getparent().remove(sp)
    elif shape.shape_type == 1 and 'サンプル' in (shape.text or ''):
        sp = shape._element; sp.getparent().remove(sp)

print('Generating bar charts...')
bar_bytes = make_bar_chart()
slide4.shapes.add_picture(bar_bytes, Inches(0.3), Inches(0.5), Inches(12.7), Inches(6.8))

# Title
txb_title = slide4.shapes.add_textbox(Inches(0), Inches(0.0), Inches(13.33), Inches(0.55))
txb_title.text_frame.text = 'Ａ様　S-BRAIN改善分析（棒グラフ）'
txb_title.text_frame.paragraphs[0].font.size = Pt(14)
txb_title.text_frame.paragraphs[0].font.bold = True
txb_title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x1F,0x38,0x64)
txb_title.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
add_footer(slide4)

# ── Slide 5: 分析データ（スケール表）──
slide5 = prs.slides[3]  # template slide 4
for shape in list(slide5.shapes):
    if shape.shape_type in [13, 1]:
        if shape.shape_type == 1 and hasattr(shape, 'text') and shape.text not in ['（C）2026.（一社）篠浦塾']:
            sp = shape._element; sp.getparent().remove(sp)
        elif shape.shape_type == 13:
            sp = shape._element; sp.getparent().remove(sp)

print('Generating scale table...')
scale_bytes = make_scale_table()
slide5.shapes.add_picture(scale_bytes, Inches(0.1), Inches(0.1), Inches(13.1), Inches(7.3))

# ── Slide 6: 本人観察者 分析シート（新シート）──
slide6 = prs.slides[4]  # template slide 5
for shape in list(slide6.shapes):
    if shape.shape_type in [13, 1]:
        if shape.shape_type == 1 and hasattr(shape, 'text') and 'サンプル' in (shape.text or ''):
            sp = shape._element; sp.getparent().remove(sp)
        elif shape.shape_type == 13:
            sp = shape._element; sp.getparent().remove(sp)

print('Generating analysis sheet...')
analysis_bytes = make_analysis_sheet()
slide6.shapes.add_picture(analysis_bytes, Inches(0.0), Inches(0.1), Inches(13.33), Inches(7.2))

# ── Slides 7-9: 200問回答データ ──
slide7 = prs.slides[5]   # template slide 6
slide8 = prs.slides[6]   # template slide 7

for sl in [slide7, slide8]:
    for shape in list(sl.shapes):
        if shape.shape_type in [13, 1]:
            if shape.shape_type == 1 and hasattr(shape, 'text') and 'サンプル' in (shape.text or ''):
                sp = shape._element; sp.getparent().remove(sp)
            elif shape.shape_type == 13:
                sp = shape._element; sp.getparent().remove(sp)

print('Generating 200Q page 1 (左脳3次元 + 右脳3次元)...')
q_page1 = make_200q_page(
    [('左脳３次元 (Q001〜Q020)', list(range(1,21))),
     ('右脳３次元 (Q041〜Q060)', list(range(41,61)))],
    '① 左脳３次元 / 右脳３次元'
)
slide7.shapes.add_picture(q_page1, Inches(0.0), Inches(0.1), Inches(13.33), Inches(7.3))

print('Generating 200Q page 2 (左脳2次元 + 右脳2次元)...')
q_page2 = make_200q_page(
    [('左脳２次元 (Q021〜Q040)', list(range(21,41))),
     ('右脳２次元 (Q061〜Q080)', list(range(61,81)))],
    '② 左脳２次元 / 右脳２次元'
)
slide8.shapes.add_picture(q_page2, Inches(0.0), Inches(0.1), Inches(13.33), Inches(7.3))

# Add more 200Q slides (new slides)
print('Generating 200Q page 3 (受動脳 + 能動脳)...')
slide_q3 = add_blank_slide()
q_page3 = make_200q_page(
    [('受動脳 (Q081〜Q100)', list(range(81,101))),
     ('動物脳活性度 (Q101〜Q120)', list(range(101,121)))],
    '③ 受動脳 / 動物脳活性度'
)
slide_q3.shapes.add_picture(q_page3, Inches(0.0), Inches(0.1), Inches(13.33), Inches(7.3))
add_footer(slide_q3)

print('Generating 200Q page 4 (動物脳コントロール力 + 脳活用度)...')
slide_q4 = add_blank_slide()
q_page4 = make_200q_page(
    [('動物脳コントロール力 (Q121〜Q140)', list(range(121,141))),
     ('脳活用度 (Q141〜Q160)', list(range(141,161)))],
    '④ 動物脳コントロール力 / 脳活用度'
)
slide_q4.shapes.add_picture(q_page4, Inches(0.0), Inches(0.1), Inches(13.33), Inches(7.3))
add_footer(slide_q4)

print('Generating 200Q page 5 (ストレス度 + ストレス耐性)...')
slide_q5 = add_blank_slide()
q_page5 = make_200q_page(
    [('ストレス度 (Q161〜Q180)', list(range(161,181))),
     ('ストレス耐性・日本精神 (Q181〜Q200)', list(range(181,201)))],
    '⑤ ストレス度 / ストレス耐性・日本精神'
)
slide_q5.shapes.add_picture(q_page5, Inches(0.0), Inches(0.1), Inches(13.33), Inches(7.3))
add_footer(slide_q5)

# ── Slide: その他の特徴 (template slide 8 = optional) ──
slide_opt = prs.slides[7]  # template slide 8
for shape in list(slide_opt.shapes):
    if shape.shape_type in [13, 1]:
        if shape.shape_type == 1 and hasattr(shape, 'text') and 'サンプル' in (shape.text or ''):
            sp = shape._element; sp.getparent().remove(sp)
        elif shape.shape_type == 13:
            sp = shape._element; sp.getparent().remove(sp)

print('Generating special features slide...')
special_bytes = make_special_features()
slide_opt.shapes.add_picture(special_bytes, Inches(0.0), Inches(0.1), Inches(13.33), Inches(7.3))

# Remove the "セミナー発表で..." text box note
for shape in list(slide_opt.shapes):
    if shape.shape_type == 17 and 'セミナー' in (shape.text or ''):
        sp = shape._element; sp.getparent().remove(sp)

# ── Slide 9 (Summary / まとめ) ──
slide9 = prs.slides[8]  # template slide 9

def fill_shape_text(slide, shape_name, text, font_size=10, color=None, bold=False):
    for shape in slide.shapes:
        if shape.name == shape_name and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = text
            p.font.size = Pt(font_size)
            if color: p.font.color.rgb = color
            if bold: p.font.bold = True
            return

# Brain type box
s_3d = subject['left3_pt']+subject['right3_pt']
s_2d = subject['left2_pt']+subject['right2_pt']
o_3d = observer['left3_pt']+observer['right3_pt']
o_2d = observer['left2_pt']+observer['right2_pt']

brain_type_text = (
    f'本人\n'
    f'４の数  右3(14) ＞ 左2(7) ＞ 左3(5) ＝ 右2(5)\n'
    f'４＋３の数  右3(17) ＞ 左3(14) ＞ 右2(11) ＞ 左2(10)\n\n'
    f'観察者\n'
    f'４の数  右3(10) ＞ 左3(7) ＞ 左2(6) ＞ 右2(2)\n'
    f'４＋３の数  右3(18) ＞ 左3(15) ＞ 左2(9) ＞ 右2(4)'
)

brain_use_text = (
    f'本人: {subject["brain_use"]}（{get_rank_brain_use(subject["brain_use"])}）\n'
    f'観察者: {observer["brain_use"]}（{get_rank_brain_use(observer["brain_use"])}）'
)

nodo_judo_text = (
    f'受動脳  本人: {subject["judo_pt"]}（{get_rank_judo(subject["judo_pt"])}）  '
    f'観察者: {observer["judo_pt"]}（{get_rank_judo(observer["judo_pt"])}）\n'
    f'能動脳  本人: {subject["nodo_pt"]}（{get_rank_nodo(subject["nodo_pt"])}）  '
    f'観察者: {observer["nodo_pt"]}（{get_rank_nodo(observer["nodo_pt"])}）'
)

animal_text = (
    f'動物脳コントロール力\n'
    f'  本人: {subject["animal_ctrl"]}（{get_rank_animal_ctrl(subject["animal_ctrl"])}）  '
    f'観察者: {observer["animal_ctrl"]}（{get_rank_animal_ctrl(observer["animal_ctrl"])}）\n'
    f'動物脳活性度（最適値42）\n'
    f'  本人: {subject["animal_act"]}（{get_rank_animal_act(subject["animal_act"])}）  '
    f'観察者: {observer["animal_act"]}（{get_rank_animal_act(observer["animal_act"])}）'
)

stress_text = (
    f'ストレス度  本人: {subject["stress"]}（{get_rank_stress(subject["stress"])}）  '
    f'観察者: {observer["stress"]}（{get_rank_stress(observer["stress"])}）\n'
    f'ストレス耐性  本人: {subject["stress_tol"]}（{get_rank_stress_tol(subject["stress_tol"])}）  '
    f'観察者: {observer["stress_tol"]}（{get_rank_stress_tol(observer["stress_tol"])}）'
)

advice_text = (
    '右脳３次元優位スタイル。直感・感性・大局観が強みで、行動力も高い。\n'
    '受動脳83（高）と能動脳52（平均）のギャップが、情報は多く収集するが\n'
    '判断・調整面での課題につながっている可能性。\n'
    '動物脳活性度61（高）により強いこだわりや固執が生まれやすい。\n'
    'コントロール力84（高）を活かして感情の浄化・昇華を意識的に行うこと。\n'
    '自分の強みをさらに伸ばしながら、部下・周囲との関係改善のために\n'
    '「受け入れる姿勢」と「手放す練習」（マインドフルネス等）を取り入れると良い。\n'
    'IQ132の知性を日本精神・社会貢献方向へ向けることが最大の開花となる。'
)

# Fill in the summary boxes using shape names from template
name_map = {
    '正方形/長方形 6': brain_type_text,
    '正方形/長方形 12': brain_use_text,
    '正方形/長方形 14': nodo_judo_text,
    '正方形/長方形 16': animal_text,
    '正方形/長方形 18': stress_text,
    '正方形/長方形 20': advice_text,
}

for shape in slide9.shapes:
    if shape.name in name_map and shape.has_text_frame:
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        lines = name_map[shape.name].split('\n')
        for i, line in enumerate(lines):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(9)
            p.font.color.rgb = RGBColor(0x1A,0x1A,0x1A)

# Fill header boxes on slide 9
for shape in slide9.shapes:
    if shape.has_text_frame:
        t = shape.text
        if t == '脳のタイプ':
            shape.text_frame.paragraphs[0].font.size = Pt(11)
            shape.text_frame.paragraphs[0].font.bold = True
        elif t == 'NO':
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = 'Ａ様　まとめ'
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)

# Save
output_path = '/tmp/sbrain_analysis_A.pptx'
prs.save(output_path)
print(f'\n✓ PowerPoint saved to: {output_path}')
print(f'  Total slides: {len(prs.slides)}')
PYEOF