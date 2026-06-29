#!/usr/bin/env python3
"""
篠浦塾 S-BRAIN分析発表資料 v2
テンプレート: /tmp/template2.pptx
参考資料: 2026前期FU第3回 PDF
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
_jp_font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(_jp_font_path)
_jp_font = fm.FontProperties(fname=_jp_font_path)
_jp_font_name = _jp_font.get_name()
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = [_jp_font_name, 'DejaVu Sans']

import matplotlib.patches as mpatches
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import io, os

# ─── データ ──────────────────────────────────────────────────────
subject = {
    'name': 'Ａ様',
    'brain_type': '右脳３次元優位スタイル',
    'left_pct': 46, 'right_pct': 54,
    'left3_pt': 24, 'right3_pt': 33,
    'left2_pt': 22, 'right2_pt': 21,
    'left3_pts': 51, 'right3_pts': 70,
    'left2_pts': 47, 'right2_pts': 46,
    'brain_use': 75,
    'judo_pt': 83,
    'nodo_pt': 52,
    'animal_ctrl': 84,
    'animal_act': 61,
    'stress': 26,
    'stress_tol': 64,
    'diag_date': '2026-05-29',
    'account': 'USR46027',
    'answers': [
        3,0,2,4,0,4,3,4,0,3,3,3,3,3,0,4,4,3,2,3,
        4,4,1,4,1,4,3,4,1,4,3,1,1,1,3,4,2,2,0,0,
        4,3,4,4,4,4,1,4,4,4,3,3,4,4,2,2,4,4,4,4,
        1,1,4,1,4,4,0,4,3,4,3,2,0,3,3,1,2,3,0,3,
        3,4,4,4,3,3,3,4,4,1,4,0,3,0,4,4,4,4,1,2,
        0,4,4,4,2,2,2,4,2,3,0,1,0,3,3,4,4,2,1,4,
        4,2,2,4,4,3,3,3,4,3,1,4,4,3,4,4,4,4,4,3,
        2,4,4,4,4,4,4,3,4,2,2,3,1,3,2,4,3,4,1,2,
        0,4,2,2,3,0,0,1,0,1,3,0,3,0,3,1,0,0,0,0,
        3,1,2,4,4,4,3,4,1,0,2,3,4,4,3,0,3,2,0,4,
    ]
}

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
        4,4,3,2,1,3,3,4,2,4,3,4,3,3,2,4,4,3,1,3,
        3,4,2,4,2,4,2,4,1,4,3,0,2,2,1,0,3,4,0,2,
        4,4,4,4,2,4,4,4,4,4,3,3,4,3,3,2,3,3,3,3,
        0,1,1,1,4,2,0,2,2,4,2,0,1,2,1,0,3,2,2,3,
        3,4,4,4,2,2,4,2,4,0,4,1,2,1,4,4,2,2,2,4,
        2,2,3,3,2,0,3,2,3,4,1,0,2,2,3,3,3,2,1,3,
        3,3,1,3,4,4,3,2,4,4,3,4,4,3,4,3,1,3,3,4,
        2,3,2,3,4,3,3,3,3,0,2,1,1,4,2,3,4,4,2,2,
        3,3,3,3,3,0,1,1,0,0,3,2,3,1,3,3,0,0,2,0,
        4,4,4,4,3,4,3,3,2,2,3,3,3,3,3,0,3,4,2,3,
    ]
}

star_qs = {83,84,87,89,92,94,98,99,130,132,133,135,140,150,151,159,162,167,169,
           182,185,186,187,188,189,190,192,194,195,198}

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

# ─── ランク判定 ──────────────────────────────────────────────
def get_rank_brain_use(v):
    if v<=5: return '全くない'
    if v<=24: return 'かなり低い'
    if v<=39: return '低い'
    if v<=53: return 'やや低い'
    if v<=62: return '平均'
    if v<=75: return 'やや高い'
    if v<=90: return '高い'
    return 'かなり高い'

def get_rank_judo(v):
    if v<=5: return '全くない'
    if v<=26: return 'かなり低い'
    if v<=41: return '低い'
    if v<=65: return 'やや低い'
    if v<=72: return '平均'
    if v<=80: return 'やや高い'
    if v<=90: return '高い'
    return 'かなり高い'

def get_rank_nodo(v):
    if v<=5: return '全くない'
    if v<=24: return 'かなり低い'
    if v<=34: return '低い'
    if v<=46: return 'やや低い'
    if v<=55: return '平均'
    if v<=70: return 'やや高い'
    if v<=80: return '高い'
    return 'かなり高い'

def get_rank_animal_ctrl(v):
    if v<=5: return '全くない'
    if v<=34: return 'かなり低い'
    if v<=44: return '低い'
    if v<=58: return 'やや低い'
    if v<=65: return '平均'
    if v<=74: return 'やや高い'
    if v<=85: return '高い'
    return 'かなり高い'

def get_rank_animal_act(v):
    if v<=5: return '全くない'
    if v<=18: return 'かなり低い'
    if v<=29: return '低い'
    if v<=39: return 'やや低い'
    if v<=44: return '最適'
    if v<=55: return 'やや高い'
    if v<=80: return '高い'
    return 'かなり高い'

def get_rank_stress(v):
    if v<=5: return '全くない'
    if v<=15: return 'かなり低い'
    if v<=25: return '低い'
    if v<=30: return 'やや低い'
    if v<=39: return '平均'
    if v<=50: return 'やや高い'
    if v<=60: return '高い'
    return 'かなり高い'

def get_rank_stress_tol(v):
    if v<=5: return '全くない'
    if v<=24: return 'かなり低い'
    if v<=34: return '低い'
    if v<=45: return 'やや低い'
    if v<=52: return '平均'
    if v<=60: return 'やや高い'
    if v<=70: return '高い'
    return 'かなり高い'

# ─── ユーティリティ ──────────────────────────────────────────────
C_BLUE = '#0070C0'
C_RED = '#C00000'
C_DARK = '#1F3864'
C_HEADER = '#2E4F8A'
C_SUBJ_BG = '#FFE0D0'
C_OBS_BG = '#D0E8FF'
C_DIFF_BG = '#FFF0B0'

def fig_to_bytes(fig, dpi=150):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    return buf

def remove_samples(slide):
    for shape in list(slide.shapes):
        if shape.shape_type == 13:  # PICTURE
            shape._element.getparent().remove(shape._element)
        elif shape.shape_type == 1 and hasattr(shape, 'text') and shape.text in ['サンプル', 'テスト結果貼り付け']:
            shape._element.getparent().remove(shape._element)

def get_picture_pos(slide):
    for sh in slide.shapes:
        if sh.shape_type == 13:
            return sh.left, sh.top, sh.width, sh.height
    return None

# ─── Slide 3: S-BRAIN改善分析（棒グラフ）────────────────────────────
def make_bar_chart():
    fig = plt.figure(figsize=(17, 7), facecolor='white')

    # Title bar
    title_ax = fig.add_axes([0, 0.93, 1, 0.07])
    title_ax.set_xlim(0, 1); title_ax.set_ylim(0, 1); title_ax.axis('off')
    title_ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=C_DARK))
    title_ax.text(0.5, 0.5, 'Ａ様　S-BRAIN改善分析', ha='center', va='center',
                  fontsize=16, fontweight='bold', color='white')

    # 3 bar charts side by side
    ax1 = fig.add_axes([0.03, 0.42, 0.29, 0.48])
    ax2 = fig.add_axes([0.36, 0.42, 0.29, 0.48])
    ax3 = fig.add_axes([0.69, 0.42, 0.29, 0.48])

    S_COL = '#2563A8'
    O_COL = '#C0392B'
    W = 0.32

    # Chart 1: 左脳/右脳
    labels1 = ['左脳', '右脳']
    sv1 = [subject['left_pct'], subject['right_pct']]
    ov1 = [observer['left_pct'], observer['right_pct']]
    x1 = np.arange(2)
    b1 = ax1.bar(x1 - W/2, sv1, W, color=S_COL, label='本人')
    b2 = ax1.bar(x1 + W/2, ov1, W, color=O_COL, label='観察者')
    ax1.set_title('左脳・右脳バランス', fontsize=11, fontweight='bold', pad=4)
    ax1.set_ylim(0, 70); ax1.set_xticks(x1); ax1.set_xticklabels(labels1, fontsize=10)
    ax1.legend(fontsize=8, loc='upper right'); ax1.yaxis.grid(True, alpha=0.3)
    ax1.set_ylabel('%', fontsize=9)
    for b in list(b1)+list(b2):
        h = b.get_height()
        ax1.text(b.get_x()+b.get_width()/2, h+0.5, f'{h}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Chart 2: 4タイプ
    labels2 = ['左3', '左2', '右3', '右2']
    sv2 = [subject['left3_pt'], subject['left2_pt'], subject['right3_pt'], subject['right2_pt']]
    ov2 = [observer['left3_pt'], observer['left2_pt'], observer['right3_pt'], observer['right2_pt']]
    x2 = np.arange(4)
    b3 = ax2.bar(x2 - W/2, sv2, W, color=S_COL, label='本人')
    b4 = ax2.bar(x2 + W/2, ov2, W, color=O_COL, label='観察者')
    ax2.set_title('脳の４タイプ', fontsize=11, fontweight='bold', pad=4)
    ax2.set_ylim(0, 42); ax2.set_xticks(x2); ax2.set_xticklabels(labels2, fontsize=10)
    ax2.legend(fontsize=8, loc='upper right'); ax2.yaxis.grid(True, alpha=0.3)
    ax2.set_ylabel('%', fontsize=9)
    for b in list(b3)+list(b4):
        h = b.get_height()
        ax2.text(b.get_x()+b.get_width()/2, h+0.3, f'{h}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Chart 3: 3次元/2次元
    labels3 = ['３次元', '２次元']
    sv3 = [subject['left3_pt']+subject['right3_pt'], subject['left2_pt']+subject['right2_pt']]
    ov3 = [observer['left3_pt']+observer['right3_pt'], observer['left2_pt']+observer['right2_pt']]
    x3 = np.arange(2)
    b5 = ax3.bar(x3 - W/2, sv3, W, color=S_COL, label='本人')
    b6 = ax3.bar(x3 + W/2, ov3, W, color=O_COL, label='観察者')
    ax3.set_title('３次元・２次元', fontsize=11, fontweight='bold', pad=4)
    ax3.set_ylim(0, 70); ax3.set_xticks(x3); ax3.set_xticklabels(labels3, fontsize=10)
    ax3.legend(fontsize=8, loc='upper right'); ax3.yaxis.grid(True, alpha=0.3)
    ax3.set_ylabel('%', fontsize=9)
    for b in list(b5)+list(b6):
        h = b.get_height()
        ax3.text(b.get_x()+b.get_width()/2, h+0.5, f'{h}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Data table below charts
    table_ax = fig.add_axes([0.01, 0.0, 0.98, 0.40])
    table_ax.set_xlim(0, 17); table_ax.set_ylim(0, 4.0); table_ax.axis('off')

    col_labels = ['', '左脳\n３次元', '左脳\n２次元', '右脳\n３次元', '右脳\n２次元',
                  '３次元\n合計', '２次元\n合計', '左脳\n合計', '右脳\n合計']
    col_x = [0.1, 2.1, 4.1, 6.1, 8.1, 10.1, 12.1, 14.1, 15.7]
    col_w = 1.9

    # Header row
    table_ax.add_patch(plt.Rectangle((0.05, 3.1), 16.9, 0.8, color=C_DARK, ec='none'))
    table_ax.text(1.0, 3.5, 'データ表', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    for i, (cx, cl) in enumerate(zip(col_x[1:], col_labels[1:]), 1):
        table_ax.add_patch(plt.Rectangle((cx, 3.1), col_w-0.1, 0.8, color='#3A5FBB', ec='white', lw=0.5))
        table_ax.text(cx+col_w/2-0.05, 3.5, cl, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    # 本人 row
    s_vals_row = [subject['left3_pts'], subject['left2_pts'], subject['right3_pts'], subject['right2_pts'],
                  subject['left3_pts']+subject['right3_pts'], subject['left2_pts']+subject['right2_pts'],
                  subject['left3_pts']+subject['left2_pts'], subject['right3_pts']+subject['right2_pts']]
    table_ax.add_patch(plt.Rectangle((0.05, 1.85), 16.9, 1.2, color='#FFF0E8', ec='gray', lw=0.3))
    table_ax.text(1.0, 2.45, f'本人\n{subject["name"]}', ha='center', va='center', fontsize=9, fontweight='bold', color=C_RED)
    for i, (cx, v) in enumerate(zip(col_x[1:], s_vals_row)):
        table_ax.add_patch(plt.Rectangle((cx, 1.9), col_w-0.1, 1.1, color='#FFE4D8', ec='gray', lw=0.3))
        table_ax.text(cx+col_w/2-0.05, 2.45, str(v), ha='center', va='center', fontsize=12, fontweight='bold', color=C_RED)

    # 観察者 row
    o_vals_row = [observer['left3_pts'], observer['left2_pts'], observer['right3_pts'], observer['right2_pts'],
                  observer['left3_pts']+observer['right3_pts'], observer['left2_pts']+observer['right2_pts'],
                  observer['left3_pts']+observer['left2_pts'], observer['right3_pts']+observer['right2_pts']]
    table_ax.add_patch(plt.Rectangle((0.05, 0.55), 16.9, 1.2, color='#E8F4FF', ec='gray', lw=0.3))
    table_ax.text(1.0, 1.15, f'観察者\n大坪可奈', ha='center', va='center', fontsize=9, fontweight='bold', color=C_BLUE)
    for i, (cx, v) in enumerate(zip(col_x[1:], o_vals_row)):
        table_ax.add_patch(plt.Rectangle((cx, 0.6), col_w-0.1, 1.1, color='#D8EDFF', ec='gray', lw=0.3))
        table_ax.text(cx+col_w/2-0.05, 1.15, str(v), ha='center', va='center', fontsize=12, fontweight='bold', color=C_BLUE)

    # 脳タイプ label
    table_ax.text(0.1, 0.25, f'本人 脳タイプ: {subject["brain_type"]}　　観察者 脳タイプ: {observer["brain_type"]}',
                  va='center', fontsize=9, color='#333333')

    return fig_to_bytes(fig)


# ─── Slide 4: スケール表 ─────────────────────────────────────────
def make_scale_table():
    fig, ax = plt.subplots(figsize=(17, 6.5), facecolor='white')
    ax.set_xlim(0, 17); ax.set_ylim(0, 10); ax.axis('off')

    metrics = [
        # (label, s_val, o_val, rank_fn, ranges, optimal_note)
        ('脳活用度\n(平均58)', subject['brain_use'], observer['brain_use'],
         get_rank_brain_use,
         [5, 24, 39, 53, 62, 75, 90, 100],
         ['全くない', 'かなり低い', '低い', 'やや低い', '平均', 'やや高い', '高い', 'かなり高い'],
         None),
        ('受動脳\n(平均69)', subject['judo_pt'], observer['judo_pt'],
         get_rank_judo,
         [5, 26, 41, 65, 72, 80, 90, 100],
         ['全くない', 'かなり低い', '低い', 'やや低い', '平均', 'やや高い', '高い', 'かなり高い'],
         None),
        ('能動脳\n(平均51)', subject['nodo_pt'], observer['nodo_pt'],
         get_rank_nodo,
         [5, 24, 34, 46, 55, 70, 80, 100],
         ['全くない', 'かなり低い', '低い', 'やや低い', '平均', 'やや高い', '高い', 'かなり高い'],
         None),
        ('動物脳\nコントロール\n(平均62)', subject['animal_ctrl'], observer['animal_ctrl'],
         get_rank_animal_ctrl,
         [5, 34, 44, 58, 65, 74, 85, 100],
         ['全くない', 'かなり低い', '低い', 'やや低い', '平均', 'やや高い', '高い', 'かなり高い'],
         None),
        ('動物脳\n活性度\n(最適42)', subject['animal_act'], observer['animal_act'],
         get_rank_animal_act,
         [5, 18, 29, 39, 44, 55, 80, 100],
         ['全くない', 'かなり低い', '低い', 'やや低い', '最適', 'やや高い', '高い', 'かなり高い'],
         '最適42'),
        ('ストレス度\n(平均36)', subject['stress'], observer['stress'],
         get_rank_stress,
         [5, 15, 25, 30, 39, 50, 60, 100],
         ['全くない', 'かなり低い', '低い', 'やや低い', '平均', 'やや高い', '高い', 'かなり高い'],
         None),
        ('ストレス耐性\n(平均49)', subject['stress_tol'], observer['stress_tol'],
         get_rank_stress_tol,
         [5, 24, 34, 45, 52, 60, 70, 100],
         ['全くない', 'かなり低い', '低い', 'やや低い', '平均', 'やや高い', '高い', 'かなり高い'],
         None),
    ]

    # Title
    ax.add_patch(plt.Rectangle((0, 9.3), 17, 0.7, color=C_DARK))
    ax.text(8.5, 9.65, 'スケール評価表', ha='center', va='center', fontsize=14, fontweight='bold', color='white')

    n = len(metrics)
    row_h = 8.8 / n
    bar_colors = ['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800', '#FF5722', '#F44336', '#B71C1C']

    for i, (label, sv, ov, rank_fn, ranges, rlabels, note) in enumerate(metrics):
        y_top = 9.2 - i * row_h
        y_bot = y_top - row_h
        y_mid = (y_top + y_bot) / 2

        # Label column
        ax.add_patch(plt.Rectangle((0, y_bot+0.05), 1.8, row_h-0.1, color='#EEF2FF', ec='#AAAACC', lw=0.5))
        ax.text(0.9, y_mid, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_DARK)

        # Scale bar area (0-100)
        bar_x0, bar_x1 = 1.9, 14.0
        bar_w = bar_x1 - bar_x0

        # Draw gradient scale
        prev = 0
        for j, (rend, rlabel) in enumerate(zip(ranges, rlabels)):
            seg_x = bar_x0 + prev / 100 * bar_w
            seg_w = (rend - prev) / 100 * bar_w
            ax.add_patch(plt.Rectangle((seg_x, y_bot+0.3), seg_w, row_h-0.6, color=bar_colors[j], ec='white', lw=0.5, alpha=0.7))
            ax.text(seg_x + seg_w/2, y_bot+0.15, rlabel, ha='center', va='center', fontsize=5.5, color='#333333')
            # Tick at boundary
            if j < len(ranges)-1:
                ax.text(seg_x + seg_w, y_bot+0.3 + (row_h-0.6)*0.5, '', ha='center', va='center', fontsize=6)
            prev = rend

        # Subject marker (●)
        sx = bar_x0 + sv / 100 * bar_w
        ax.plot(sx, y_mid, 'v', color=C_RED, markersize=9, zorder=5)
        ax.text(sx, y_bot+0.32, f'●', ha='center', va='bottom', fontsize=10, color=C_RED, zorder=5)

        # Observer marker (▲)
        ox = bar_x0 + ov / 100 * bar_w
        ax.plot(ox, y_mid, '^', color=C_BLUE, markersize=9, zorder=5)
        ax.text(ox, y_top-0.35, f'▲', ha='center', va='top', fontsize=10, color=C_BLUE, zorder=5)

        # Value labels on right
        ax.add_patch(plt.Rectangle((14.1, y_bot+0.05), 1.3, row_h-0.1, color='#FFF0E8', ec='#DDBBAA', lw=0.5))
        ax.text(14.75, y_mid+0.15, f'本人: {sv}', ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_RED)
        ax.text(14.75, y_mid-0.25, f'({rank_fn(sv)})', ha='center', va='center', fontsize=7, color=C_RED)

        ax.add_patch(plt.Rectangle((15.5, y_bot+0.05), 1.4, row_h-0.1, color='#E8F4FF', ec='#AABBDD', lw=0.5))
        ax.text(16.2, y_mid+0.15, f'観: {ov}', ha='center', va='center', fontsize=8.5, fontweight='bold', color=C_BLUE)
        ax.text(16.2, y_mid-0.25, f'({rank_fn(ov)})', ha='center', va='center', fontsize=7, color=C_BLUE)

    # Legend
    ax.plot([], [], 'v', color=C_RED, markersize=8, label=f'本人（{subject["name"]}）')
    ax.plot([], [], '^', color=C_BLUE, markersize=8, label='観察者（大坪可奈）')
    ax.legend(loc='lower right', fontsize=8, framealpha=0.9)

    plt.tight_layout()
    return fig_to_bytes(fig)


# ─── Slide 5: 新シート（本人観察者S-BRAIN脳活診断結果）──────────────
def make_analysis_sheet():
    fig, ax = plt.subplots(figsize=(17, 10), facecolor='white')
    ax.set_xlim(0, 17); ax.set_ylim(0, 10); ax.axis('off')

    # Title
    ax.add_patch(plt.Rectangle((0, 9.3), 17, 0.7, color=C_DARK))
    ax.text(8.5, 9.65, '本人観察者　S-BRAIN脳活診断結果', ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')

    def section_header(title, x, y, w, h=0.45, color=C_HEADER):
        ax.add_patch(plt.Rectangle((x, y), w, h, color=color, ec='none'))
        ax.text(x+0.1, y+h/2, title, va='center', fontsize=9, fontweight='bold', color='white')

    def cell(x, y, w, h, text, bg='white', fc='black', fs=9, bold=False, halign='left'):
        ax.add_patch(plt.Rectangle((x, y), w, h, color=bg, ec='#888888', lw=0.4))
        ha_x = x + 0.1 if halign == 'left' else x + w/2
        ax.text(ha_x, y+h/2, text, va='center', ha=halign, fontsize=fs, fontweight='bold' if bold else 'normal', color=fc, wrap=True)

    # Section 1: 脳のタイプ
    section_header('① 脳のタイプ', 0.1, 8.75, 16.8)
    cell(0.1, 8.3, 8.3, 0.4, f'本人: {subject["brain_type"]}', bg='#FFF0E8', fc=C_RED, fs=9, bold=True, halign='left')
    cell(8.5, 8.3, 8.4, 0.4, f'観察者: {observer["brain_type"]}', bg='#E8F4FF', fc=C_BLUE, fs=9, bold=True, halign='left')

    # Section 2: 4の数 / 4+3の数
    section_header('② ４の数・４＋３の数ランキング', 0.1, 7.75, 16.8)
    cell(0.1, 7.3, 8.3, 0.4,
         '本人　４の数: 右3(14) ＞ 左2(7) ＞ 右2(5) ＝ 左3(5)',
         bg='#FFF0E8', fc=C_RED, fs=8.5)
    cell(8.5, 7.3, 8.4, 0.4,
         '観察者　４の数: 右3(10) ＞ 左3(7) ＞ 左2(6) ＞ 右2(2)',
         bg='#E8F4FF', fc=C_BLUE, fs=8.5)
    cell(0.1, 6.85, 8.3, 0.4,
         '本人　４＋３: 右3(17) ＞ 左3(14) ＞ 右2(11) ＞ 左2(10)',
         bg='#FFF8F5', fc=C_RED, fs=8.5)
    cell(8.5, 6.85, 8.4, 0.4,
         '観察者　４＋３: 右3(18) ＞ 左3(15) ＞ 左2(9) ＞ 右2(4)',
         bg='#F5FAFF', fc=C_BLUE, fs=8.5)

    # Section 3: 脳活用度
    section_header('③ 脳活用度・受動脳・能動脳', 0.1, 6.35, 16.8)
    metrics3 = [
        ('脳活用度\n(平均58)', subject['brain_use'], observer['brain_use'], get_rank_brain_use),
        ('受動脳\n(平均69)', subject['judo_pt'], observer['judo_pt'], get_rank_judo),
        ('能動脳\n(平均51)', subject['nodo_pt'], observer['nodo_pt'], get_rank_nodo),
    ]
    for j, (lbl, sv, ov, fn) in enumerate(metrics3):
        x = 0.1 + j * 5.6
        cell(x, 5.45, 2.0, 0.85, lbl, bg='#E8E8F0', fc=C_DARK, fs=8, halign='center')
        cell(x+2.0, 5.45, 1.7, 0.85, f'{sv}\n({fn(sv)})', bg='#FFF0E8', fc=C_RED, fs=8.5, bold=True, halign='center')
        cell(x+3.7, 5.45, 1.8, 0.85, f'{ov}\n({fn(ov)})', bg='#E8F4FF', fc=C_BLUE, fs=8.5, bold=True, halign='center')

    # Section 4: 動物脳
    section_header('④ 動物脳コントロール力・動物脳活性度', 0.1, 5.35, 16.8)
    metrics4 = [
        ('動物脳\nコントロール力\n(平均62)', subject['animal_ctrl'], observer['animal_ctrl'], get_rank_animal_ctrl),
        ('動物脳活性度\n(最適42)', subject['animal_act'], observer['animal_act'], get_rank_animal_act),
    ]
    for j, (lbl, sv, ov, fn) in enumerate(metrics4):
        x = 0.1 + j * 8.4
        cell(x, 4.45, 3.2, 0.85, lbl, bg='#E8E8F0', fc=C_DARK, fs=8, halign='center')
        cell(x+3.2, 4.45, 2.5, 0.85, f'{sv}　({fn(sv)})', bg='#FFF0E8', fc=C_RED, fs=9, bold=True, halign='center')
        cell(x+5.7, 4.45, 2.6, 0.85, f'{ov}　({fn(ov)})', bg='#E8F4FF', fc=C_BLUE, fs=9, bold=True, halign='center')

    # Section 5: ストレス
    section_header('⑤ ストレス度・ストレス耐性', 0.1, 4.35, 16.8)
    metrics5 = [
        ('ストレス度\n(平均36)', subject['stress'], observer['stress'], get_rank_stress),
        ('ストレス耐性\n(平均49)', subject['stress_tol'], observer['stress_tol'], get_rank_stress_tol),
    ]
    for j, (lbl, sv, ov, fn) in enumerate(metrics5):
        x = 0.1 + j * 8.4
        cell(x, 3.45, 3.2, 0.85, lbl, bg='#E8E8F0', fc=C_DARK, fs=8, halign='center')
        cell(x+3.2, 3.45, 2.5, 0.85, f'{sv}　({fn(sv)})', bg='#FFF0E8', fc=C_RED, fs=9, bold=True, halign='center')
        cell(x+5.7, 3.45, 2.6, 0.85, f'{ov}　({fn(ov)})', bg='#E8F4FF', fc=C_BLUE, fs=9, bold=True, halign='center')

    # Section 6: 設問乖離 (top 比較)
    section_header('⑥ 本人・観察者で認識差が大きい設問（抜粋）', 0.1, 3.35, 16.8)
    big_diff_qs = []
    for qno in range(1, 201):
        sa = subject['answers'][qno-1]
        oa = observer['answers'][qno-1]
        diff = sa - oa
        big_diff_qs.append((abs(diff), qno, sa, oa, diff))
    big_diff_qs.sort(reverse=True)

    header_y = 2.85
    ax.add_patch(plt.Rectangle((0.1, header_y), 6.0, 0.45, color='#D0D8F0', ec='gray', lw=0.3))
    ax.text(0.3, header_y+0.22, '設問番号・内容', va='center', fontsize=8, fontweight='bold')
    ax.add_patch(plt.Rectangle((6.2, header_y), 1.8, 0.45, color='#FFD8C8', ec='gray', lw=0.3))
    ax.text(7.1, header_y+0.22, '本人', ha='center', va='center', fontsize=8, fontweight='bold', color=C_RED)
    ax.add_patch(plt.Rectangle((8.1, header_y), 1.8, 0.45, color='#C8E0FF', ec='gray', lw=0.3))
    ax.text(9.0, header_y+0.22, '観察者', ha='center', va='center', fontsize=8, fontweight='bold', color=C_BLUE)
    ax.add_patch(plt.Rectangle((10.0, header_y), 1.5, 0.45, color='#FFFFD0', ec='gray', lw=0.3))
    ax.text(10.75, header_y+0.22, '差', ha='center', va='center', fontsize=8, fontweight='bold')

    shown = 0
    for (absd, qno, sa, oa, diff) in big_diff_qs:
        if shown >= 6: break
        if absd < 2: break
        y = header_y - (shown+1) * 0.4
        if y < 0.6: break
        bg = '#FFF8F0' if shown % 2 == 0 else 'white'
        is_star = qno in star_qs
        qtxt = q_texts.get(qno, '')[:28] + ('★' if is_star else '')
        ax.add_patch(plt.Rectangle((0.1, y-0.35), 6.0, 0.4, color=bg, ec='#DDDDDD', lw=0.2))
        ax.text(0.2, y-0.15, f'Q{qno:03d} {qtxt}', va='center', fontsize=7,
                color=C_RED if is_star else 'black')
        ax.add_patch(plt.Rectangle((6.2, y-0.35), 1.8, 0.4, color='#FFE8DC', ec='gray', lw=0.2))
        ax.text(7.1, y-0.15, str(sa), ha='center', va='center', fontsize=9, fontweight='bold', color=C_RED)
        ax.add_patch(plt.Rectangle((8.1, y-0.35), 1.8, 0.4, color='#DCE8FF', ec='gray', lw=0.2))
        ax.text(9.0, y-0.15, str(oa), ha='center', va='center', fontsize=9, fontweight='bold', color=C_BLUE)
        dc = C_RED if diff > 0 else C_BLUE
        ax.add_patch(plt.Rectangle((10.0, y-0.35), 1.5, 0.4, color='#FFFFD0', ec='gray', lw=0.2))
        ax.text(10.75, y-0.15, f'{diff:+d}', ha='center', va='center', fontsize=9, fontweight='bold', color=dc)
        shown += 1

    # Section 7: 脳タイプ解説
    section_header('⑦ 脳タイプ特性メモ', 11.7, 2.85, 5.2)
    type_note = (
        '本人: 右脳３次元優位\n'
        '→大局把握・直感・感性が強み\n'
        '→行動力・情熱・こだわり強め\n\n'
        '観察者: 左右脳バランス型\n'
        '→論理＋感性のバランス\n'
        '→多角的視点で分析可能'
    )
    ax.add_patch(plt.Rectangle((11.7, 0.5), 5.2, 2.3, color='#F8F9FF', ec='#8888CC', lw=0.5))
    ax.text(11.85, 2.6, type_note, va='top', fontsize=8, color=C_DARK, linespacing=1.6)

    plt.tight_layout()
    return fig_to_bytes(fig)


# ─── 200問テーブル ──────────────────────────────────────────────

def make_200q_section(ax, x0, y0, w, title, q_range, bg_title='#1F3864'):
    """Draw one Q section table in the given axes at given position."""
    row_h = 0.42
    th = 0.5  # title height
    sh = 0.38  # subheader height
    n = len(q_range)
    total_h = th + sh + n * row_h

    # Title bar
    ax.add_patch(plt.Rectangle((x0, y0 - th), w, th, color=bg_title, ec='none'))
    ax.text(x0 + w/2, y0 - th/2, title, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='white')

    # Sub-header
    col_defs = [
        (0.0, 0.06, 'No', 'center', '#D0D8F0'),
        (0.06, 0.44, '設問内容', 'left', '#D8D8E8'),
        (0.50, 0.155, '本人', 'center', '#FFD0C0'),
        (0.655, 0.165, '観察者', 'center', '#C0D8FF'),
        (0.82, 0.18, '差', 'center', '#FFFFC0'),
    ]
    y_sh = y0 - th - sh
    for (cx_frac, cw_frac, ch, halign, bg) in col_defs:
        cx = x0 + cx_frac * w
        cw = cw_frac * w
        ax.add_patch(plt.Rectangle((cx, y_sh), cw, sh, color=bg, ec='#999999', lw=0.3))
        ax.text(cx + cw/2 if halign == 'center' else cx + 0.05,
                y_sh + sh/2, ch,
                ha=halign, va='center', fontsize=7, fontweight='bold', color='#1A1A1A')

    # Data rows
    for ri, qno in enumerate(q_range):
        sa = subject['answers'][qno-1]
        oa = observer['answers'][qno-1]
        diff = sa - oa
        is_star = qno in star_qs
        yr = y_sh - (ri + 1) * row_h
        row_bg = '#FFF8F2' if ri % 2 == 0 else 'white'
        if abs(diff) >= 3:
            row_bg = '#FFDDDD'
        elif abs(diff) >= 2:
            row_bg = '#FFF8CC'

        ax.add_patch(plt.Rectangle((x0, yr), w, row_h, color=row_bg, ec='#DDDDDD', lw=0.2))

        # No column
        ax.text(x0 + 0.03*w, yr + row_h/2, f'Q{qno}', ha='left', va='center',
                fontsize=6, color='#555555')

        # Text column
        qtxt = q_texts.get(qno, '')
        max_chars = int(w * 5.5)
        if is_star:
            disp = qtxt[:max_chars-1] + ('…' if len(qtxt) > max_chars else '') + '★'
            tcol = C_RED
        else:
            disp = qtxt[:max_chars] + ('…' if len(qtxt) > max_chars else '')
            tcol = '#1A1A1A'
        ax.text(x0 + 0.065*w, yr + row_h/2, disp, va='center', fontsize=6.5, color=tcol)

        # Scores
        ax.text(x0 + 0.575*w, yr + row_h/2, str(sa), ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=C_RED)
        ax.text(x0 + 0.74*w, yr + row_h/2, str(oa), ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=C_BLUE)

        # Diff
        dc = C_RED if diff > 0 else (C_BLUE if diff < 0 else '#666666')
        ax.text(x0 + 0.91*w, yr + row_h/2, f'{diff:+d}' if diff != 0 else '0',
                ha='center', va='center', fontsize=8, fontweight='bold', color=dc)

    # Bottom border
    ax.axhline(y_sh - n * row_h, xmin=x0/ax.get_xlim()[1], xmax=(x0+w)/ax.get_xlim()[1],
               color='#888888', lw=0.8)


def make_200q_page1():
    """Q001-Q080: 左脳系 (左3, 左2) and 右脳系 (右3, 右2) — 2 columns × 2 groups"""
    fig, ax = plt.subplots(figsize=(17, 12), facecolor='white')
    ax.set_xlim(0, 17); ax.set_ylim(-10, 1); ax.axis('off')

    # Page title
    ax.add_patch(plt.Rectangle((0, 0.0), 17, 1.0, color=C_DARK))
    ax.text(8.5, 0.5, '200問回答データ　Ｐ１　（Q001〜Q080  左脳・右脳系）', ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')

    row_h = 0.42
    left_w = 8.2
    right_w = 8.2

    # Left column: 左脳３次元 (Q1-20) then 左脳２次元 (Q21-40)
    y_start_left = -0.1
    make_200q_section(ax, 0.1, y_start_left, left_w,
                      '左脳３次元（Q001〜Q020）', list(range(1, 21)), bg_title='#1A4B8C')
    y_left2 = y_start_left - 0.5 - 0.38 - 20 * row_h - 0.3
    make_200q_section(ax, 0.1, y_left2, left_w,
                      '左脳２次元（Q021〜Q040）', list(range(21, 41)), bg_title='#1A4B8C')

    # Right column: 右脳３次元 (Q41-60) then 右脳２次元 (Q61-80)
    y_start_right = -0.1
    make_200q_section(ax, 8.7, y_start_right, right_w,
                      '右脳３次元（Q041〜Q060）', list(range(41, 61)), bg_title='#8B1A1A')
    y_right2 = y_start_right - 0.5 - 0.38 - 20 * row_h - 0.3
    make_200q_section(ax, 8.7, y_right2, right_w,
                      '右脳２次元（Q061〜Q080）', list(range(61, 81)), bg_title='#8B1A1A')

    # Legend
    ax.text(0.2, -9.7, '■ 差±3以上: 赤背景  ■ 差±2: 黄背景  ★: 逆転質問', fontsize=7, color='#555555')
    ax.text(8.0, -9.7, f'■ 本人(赤): {subject["name"]}　■ 観察者(青): 大坪可奈', fontsize=7, color='#555555')

    return fig_to_bytes(fig, dpi=130)


def make_200q_page2():
    """Q081-Q200: 受動脳系 and 能動脳系 and ストレス系 — 2 columns × 3 groups"""
    fig, ax = plt.subplots(figsize=(17, 14), facecolor='white')
    ax.set_xlim(0, 17); ax.set_ylim(-13, 1); ax.axis('off')

    ax.add_patch(plt.Rectangle((0, 0.0), 17, 1.0, color=C_DARK))
    ax.text(8.5, 0.5, '200問回答データ　Ｐ２　（Q081〜Q200  受動脳・能動脳・ストレス系）', ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')

    row_h = 0.42
    left_w = 8.2
    right_w = 8.2

    # Left column: 受動脳(Q81-100), 能動脳(Q121-140), ストレス度(Q161-180)
    y = -0.1
    make_200q_section(ax, 0.1, y, left_w, '受動脳（Q081〜Q100）', list(range(81, 101)), bg_title='#1A6B3C')
    y -= 0.5 + 0.38 + 20 * row_h + 0.3
    make_200q_section(ax, 0.1, y, left_w, '能動脳（Q121〜Q140）', list(range(121, 141)), bg_title='#6B5A1A')
    y -= 0.5 + 0.38 + 20 * row_h + 0.3
    make_200q_section(ax, 0.1, y, left_w, 'ストレス度（Q161〜Q180）', list(range(161, 181)), bg_title='#6B1A3C')

    # Right column: 動物脳活性度(Q101-120), 動物脳コントロール(Q141-160), ストレス耐性(Q181-200)
    y = -0.1
    make_200q_section(ax, 8.7, y, right_w, '動物脳活性度（Q101〜Q120）', list(range(101, 121)), bg_title='#1A5B6B')
    y -= 0.5 + 0.38 + 20 * row_h + 0.3
    make_200q_section(ax, 8.7, y, right_w, '動物脳コントロール力（Q141〜Q160）', list(range(141, 161)), bg_title='#3A3A8B')
    y -= 0.5 + 0.38 + 20 * row_h + 0.3
    make_200q_section(ax, 8.7, y, right_w, 'ストレス耐性・日本精神（Q181〜Q200）', list(range(181, 201)), bg_title='#5B1A8B')

    ax.text(0.2, -12.7, '■ 差±3以上: 赤背景  ■ 差±2: 黄背景  ★: 逆転質問', fontsize=7, color='#555555')

    return fig_to_bytes(fig, dpi=120)


# ─── Slide 8: その他の特徴 ────────────────────────────────────────
def make_special_features():
    fig, ax = plt.subplots(figsize=(17, 6.5), facecolor='white')
    ax.set_xlim(0, 17); ax.set_ylim(0, 7); ax.axis('off')

    ax.add_patch(plt.Rectangle((0, 6.3), 17, 0.7, color=C_DARK))
    ax.text(8.5, 6.65, 'その他の特徴（特性・メンタル傾向・注目設問）', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    noted_qs = [
        (33, '自分の考えを他人にあてはめて責めてしまうことがある'),
        (4,  '前置きの長い話や意図の見えない話にイライラする'),
        (24, '待ち合わせや締め切りを守れない人は許せない'),
        (10, '理屈のあわない行動をする人は苦手だ'),
        (46, '決断が速く、せっかちだと言われる'),
        (116,'プレッシャーがあると逆に活力がでる'),
        (107,'何かと戦っている時が一番充実感がある'),
        (99, '自分の信じていることであれば何回失敗してもやり方を変えない★'),
        (117,'負けたくやしさはずっと覚えている'),
        (175,'他の人を責めてしまうことがよくある'),
        (130,'失敗すると人のせいにしがちだ★'),
        (120,'自分が好きなことばかりやると周囲によくいわれる'),
    ]

    comments = {
        33: '職場でも指摘あり',
        4:  '会議・報告で顕著に観察',
        24: '完璧主義の現れ',
        10: '論理矛盾に強く反応',
        46: '会議での素早い判断傾向',
        116:'プレッシャー下で攻撃的に',
        107:'競争場面での集中力が高い',
        99: '一度決めたら変えない',
        117:'ネガティブ感情の保持が長い',
        175:'部下への厳しさとして現れる',
        130:'責任転嫁の自覚が薄い',
        120:'過集中の傾向か',
    }

    # Header
    hdr_y = 5.85
    for (x, w, t, bg, fc) in [
        (0.1, 1.0, 'Q番号', '#D0D8F0', '#1A1A1A'),
        (1.2, 6.5, '設問内容', '#D8D8E8', '#1A1A1A'),
        (7.8, 1.5, '本人', '#FFD0C0', C_RED),
        (9.4, 1.5, '観察者', '#C0D8FF', C_BLUE),
        (11.0, 1.2, '差', '#FFFFC0', '#1A1A1A'),
        (12.3, 4.6, '観察者コメント', '#E8E8E8', '#1A1A1A'),
    ]:
        ax.add_patch(plt.Rectangle((x, hdr_y), w, 0.45, color=bg, ec='gray', lw=0.4))
        ax.text(x + w/2, hdr_y + 0.22, t, ha='center', va='center', fontsize=8, fontweight='bold', color=fc)

    for ri, (qno, qtext) in enumerate(noted_qs):
        sa = subject['answers'][qno-1]
        oa = observer['answers'][qno-1]
        diff = sa - oa
        y = hdr_y - (ri + 1) * 0.47
        bg = '#FFF8F0' if ri % 2 == 0 else 'white'
        if abs(diff) >= 3: bg = '#FFDDDD'
        elif abs(diff) >= 2: bg = '#FFF8CC'

        ax.add_patch(plt.Rectangle((0.1, y-0.38), 16.8, 0.42, color=bg, ec='#DDDDDD', lw=0.2))

        is_star = qno in star_qs
        ax.text(0.6, y-0.17, f'Q{qno:03d}', ha='center', va='center', fontsize=7)
        disp = qtext[:35] + ('…' if len(qtext)>35 else '') + ('★' if is_star else '')
        ax.text(1.25, y-0.17, disp, va='center', fontsize=7.5, color=C_RED if is_star else 'black')
        ax.text(8.55, y-0.17, str(sa), ha='center', va='center', fontsize=9, fontweight='bold', color=C_RED)
        ax.text(10.15, y-0.17, str(oa), ha='center', va='center', fontsize=9, fontweight='bold', color=C_BLUE)
        dc = C_RED if diff > 0 else C_BLUE
        ax.text(11.6, y-0.17, f'{diff:+d}' if diff != 0 else '0', ha='center', va='center',
                fontsize=9, fontweight='bold', color=dc)
        ax.text(12.4, y-0.17, comments.get(qno, ''), va='center', fontsize=7.5, color='#555555')

    # Summary box
    ax.add_patch(plt.Rectangle((0.1, 0.05), 16.8, 0.85, color='#FFF9C4', ec='#CCAA00', lw=1.0))
    summary = ('IQ132（メンサ）＋発達障害診断。右脳3次元優位で大局観・直感・行動力が強み。'
               '動物脳活性度61（高）による強いこだわりと固執。受動脳83（高）vs 能動脳52（平均）のギャップあり。'
               'ストレス耐性64（やや高い）だが周囲への影響（攻撃性・巻き込み）は本人自覚より強く観察されている。')
    ax.text(0.3, 0.72, '■ 特性まとめ:', fontsize=8.5, fontweight='bold', color='#7B3F00', va='top')
    ax.text(0.3, 0.52, summary, va='top', fontsize=7.5, color='#1A1A1A', wrap=True)

    plt.tight_layout()
    return fig_to_bytes(fig)


# ─── PPTX作成 ──────────────────────────────────────────────────

print('Loading template...')
prs = Presentation('/tmp/template2.pptx')

def set_multiline_text(shape, lines, font_size=9, color=None):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        if color:
            p.font.color.rgb = color

def replace_picture(slide, img_bytes, fallback_pos=None):
    pos = get_picture_pos(slide)
    remove_samples(slide)
    if pos:
        L, T, W, H = pos
    elif fallback_pos:
        L, T, W, H = fallback_pos
    else:
        L, T, W, H = Inches(0), Inches(1), Inches(13), Inches(6)
    img_bytes.seek(0)
    slide.shapes.add_picture(img_bytes, L, T, W, H)


# ── Slide 1: タイトル ──
slide1 = prs.slides[0]
for sh in slide1.shapes:
    if sh.has_text_frame and '○○' in sh.text:
        tf = sh.text_frame
        tf.clear()
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = 'Ａ様の例題'
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

# ── Slide 2: S-BRAIN結果（本人・観察者）──
slide2 = prs.slides[1]
# Remove placeholder ovals
for sh in list(slide2.shapes):
    if sh.shape_type == 1 and hasattr(sh, 'text') and 'テスト結果' in (sh.text or ''):
        sh._element.getparent().remove(sh._element)

# Place the two S-BRAIN result images in oval positions
# Positions from template: left oval left=886302 top=1914499 w=4735772 h=4438887
#                          right oval left=6812508 top=1914498 w=4735772 h=4438887
with open('/tmp/fu09hires.png', 'rb') as f:
    fu09_b = io.BytesIO(f.read())
with open('/tmp/fu10hires.png', 'rb') as f:
    fu10_b = io.BytesIO(f.read())

slide2.shapes.add_picture(fu09_b, 886302, 1914499, 4735772, 4438887)
slide2.shapes.add_picture(fu10_b, 6812508, 1914498, 4735772, 4438887)

# ── Slide 3: 棒グラフ ──
print('Generating bar chart...')
slide3 = prs.slides[2]
bar_bytes = make_bar_chart()
replace_picture(slide3, bar_bytes)

# ── Slide 4: スケール表 ──
print('Generating scale table...')
slide4 = prs.slides[3]
scale_bytes = make_scale_table()
replace_picture(slide4, scale_bytes)

# ── Slide 5: 新シート ──
print('Generating analysis sheet...')
slide5 = prs.slides[4]
sheet_bytes = make_analysis_sheet()
replace_picture(slide5, sheet_bytes)

# ── Slide 6: 200問 P1 ──
print('Generating 200Q page 1...')
slide6 = prs.slides[5]
q1_bytes = make_200q_page1()
replace_picture(slide6, q1_bytes)

# ── Slide 7: 200問 P2 ──
print('Generating 200Q page 2...')
slide7 = prs.slides[6]
q2_bytes = make_200q_page2()
replace_picture(slide7, q2_bytes)

# ── Slide 8: その他の特徴 ──
print('Generating special features...')
slide8 = prs.slides[7]
# Remove the note text box
for sh in list(slide8.shapes):
    if sh.shape_type == 17 and 'セミナー' in (sh.text or ''):
        sh._element.getparent().remove(sh._element)
sf_bytes = make_special_features()
replace_picture(slide8, sf_bytes)

# ── Slide 9: まとめ ──
slide9 = prs.slides[8]

brain_type_text = (
    '【本人】\n'
    '４の数ランキング: 右3(14) ＞ 左2(7) ＞ 右2(5) ＝ 左3(5)\n'
    '４＋３の数: 右3(17) ＞ 左3(14) ＞ 右2(11) ＞ 左2(10)\n'
    '脳タイプ: 右脳３次元優位スタイル\n\n'
    '【観察者】\n'
    '４の数ランキング: 右3(10) ＞ 左3(7) ＞ 左2(6) ＞ 右2(2)\n'
    '４＋３の数: 右3(18) ＞ 左3(15) ＞ 左2(9) ＞ 右2(4)\n'
    '脳タイプ: 左脳・右脳３次元優位スタイル'
)

brain_use_text = (
    f'本人: {subject["brain_use"]}点（{get_rank_brain_use(subject["brain_use"])}）\n'
    f'観察者: {observer["brain_use"]}点（{get_rank_brain_use(observer["brain_use"])}）'
)

nodo_judo_text = (
    f'受動脳  本人: {subject["judo_pt"]}（{get_rank_judo(subject["judo_pt"])}）'
    f' ／ 観察者: {observer["judo_pt"]}（{get_rank_judo(observer["judo_pt"])}）\n'
    f'能動脳  本人: {subject["nodo_pt"]}（{get_rank_nodo(subject["nodo_pt"])}）'
    f' ／ 観察者: {observer["nodo_pt"]}（{get_rank_nodo(observer["nodo_pt"])}）'
)

animal_text = (
    f'動物脳コントロール力\n'
    f'  本人: {subject["animal_ctrl"]}（{get_rank_animal_ctrl(subject["animal_ctrl"])}）'
    f' ／ 観察者: {observer["animal_ctrl"]}（{get_rank_animal_ctrl(observer["animal_ctrl"])}）\n'
    f'動物脳活性度（最適値42）\n'
    f'  本人: {subject["animal_act"]}（{get_rank_animal_act(subject["animal_act"])}）'
    f' ／ 観察者: {observer["animal_act"]}（{get_rank_animal_act(observer["animal_act"])}）'
)

stress_text = (
    f'ストレス度  本人: {subject["stress"]}（{get_rank_stress(subject["stress"])}）'
    f' ／ 観察者: {observer["stress"]}（{get_rank_stress(observer["stress"])}）\n'
    f'ストレス耐性  本人: {subject["stress_tol"]}（{get_rank_stress_tol(subject["stress_tol"])}）'
    f' ／ 観察者: {observer["stress_tol"]}（{get_rank_stress_tol(observer["stress_tol"])}）'
)

advice_text = (
    '右脳３次元優位スタイル。直感・感性・大局観が強みで行動力も高い。\n'
    '受動脳83（高）と能動脳52（平均）のギャップが、情報収集は得意だが\n'
    '判断・調整面の課題につながっている可能性がある。\n'
    '動物脳活性度61（高）により強いこだわりや固執が生まれやすい。\n'
    'コントロール力84（高）を活かして感情の浄化・昇華を意識的に行うこと。\n'
    '自分の強みをさらに伸ばしながら、部下・周囲との関係改善のために\n'
    '「受け入れる姿勢」と「手放す練習」を取り入れると良い。\n'
    'IQ132の知性を社会貢献方向へ向けることが最大の開花となる。'
)

name_map = {
    '正方形/長方形 6': brain_type_text,
    '正方形/長方形 12': brain_use_text,
    '正方形/長方形 14': nodo_judo_text,
    '正方形/長方形 16': animal_text,
    '正方形/長方形 18': stress_text,
    '正方形/長方形 20': advice_text,
}

for sh in slide9.shapes:
    if sh.name in name_map and sh.has_text_frame:
        lines = name_map[sh.name].split('\n')
        set_multiline_text(sh, lines, font_size=9)

# Fill header NO box → "Ａ様　まとめ"
for sh in slide9.shapes:
    if sh.has_text_frame and sh.text.strip() == 'NO':
        tf = sh.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = 'Ａ様　まとめ'
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

# Save
out = '/tmp/sbrain_analysis_B.pptx'
prs.save(out)
print(f'\n✓ 保存完了: {out}')
print(f'  スライド数: {len(prs.slides)}')
