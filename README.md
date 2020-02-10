# tetrisPysta

> 2020/01/27 作成


📝 2020/02/10



# 仕様のつらつらとしたメモ


- 動いてるブロック
- 止まったブロック
	- 止まったブロックは、停止判断に使う
	- 停止判断は、ブロックが止まるごとに増える
		- 停止判断は、増減あり
			- 一列並びになれば、止まったブロックがきえる
			- 上のブロックが降りてくる
				- 上のブロックのステータスが継承


## status

block ごとに`status` が判明すればいい？


- status の最低条件は？
	- wall
	- fixed




---

📝 2020/02/09

# フラグ管理


もう少し統一させる必要ありそう


マージ切るのが面倒(Pythonista だと) だから、別ファイルつくる



---

📝 2020/02/07

# mino の移動時の`x += 1` 挙動について


マイナス時には、

- 今のブロック -> 移動後ブロック

のカラーのパス


- 今のブロック

default の色


プラス時に、何故か、default 色範囲がデカくなっちゃう



## ダメ 🙅‍♂️

``` py
for b in self.put_minos:
  x, y = b
  y -= 1
  self.take_minos += [x, y],

for t, p in product(self.take_minos, self.tm.fixed_line):
  if t == p:
    self.tm.fixed_line += self.put_minos
    self.put_minos = self.tm.drop_minos()
    break
else:
  for take, put in zip(self.take_minos,self.put_minos):
    tx, ty = take
    px, py = put
    take_block = self.tm.block[tx][ty]
    put_block = self.tm.block[px][py]
    set_color = put_block.fill_color
    take_block.fill_color = set_color
    put_block.fill_color = self.tm.default_color
  self.put_minos = self.take_minos
```




## きた 🙆‍♂️

変えるblockと、動いているblockを一括でlist ぶち込んで


index 指定で、block色とdefault色をつけていくで解決


``` py
minos_len = len(put_minos)
set_minos = put_minos + take_minos
set_color = self.tm.block[put_minos[0][0]][put_minos[0][1]].fill_color
for take, fix in product(take_minos, self.tm.fixed_line):
  if take == fix:
    self.put_minos = put_minos
    break
else:
  for n, i in enumerate(set_minos):
    if n < minos_len:
      self.tm.block[i[0]][i[1]].fill_color = self.tm.default_color
    else:
      self.tm.block[i[0]][i[1]].fill_color = set_color
  self.put_minos = take_minos
return self.put_minos
```


# 関数のスコープ

`self` ものを 関数内の変数にさせて、汚染を回避


`block[x][y]` の、リストだけで管理してるので、メモリはあまり使ってないと思われる(shape オブジェクトを格納させないようにしてる)


---


📝 2020/02/06

# 落下 and 当たり判定

`itertools.product()` で、止まってるminos と、移動minos 総当たり


止まるのが確定したら、移動していたminos のindex を止まってるindex のlist に追加



初めて`itertools` を使った

## `itertools`

しゅ、しゅごい、、、


ということ、しか理解してない





# どこに関数を生やすか？

最終的な、`class MainScene(scene.Scene):` にぶち込めばなんとかなりそうだけど


- 呼び出しが長くなる
	- コードが長い
- 他関数や、変数名参照に時間がかかる
	- 見に行く、スクロールが多くて編集行を見失う


と、人間側のコスト中心だけども


## 変数名

大改装して、一応見通しを良くしたいと思って、やってみたけど



## 関数の引数

引数無しで、呼び出しまくってるけどいいものなのか、、、？


`self.hoge` で、なんとかなるやん！と、思ってるけど


スコープとか理解あやしくて、取り敢えず動いていればヨシ！となっとる、、、

---

📝 2020/02/05


# とりま

ボタン押して落下まではいけた


止めたり、なんだりするのが次かな


# メモ
# Tetrimino

```
mino_I cyan
▪︎▪︎▪︎▪︎

00,01,02,03,04

mino_O yellow
▪︎▪︎
▪︎▪︎
10,11
00,01

mino_S green
 ▪︎▪
︎▪︎▪︎
   11,12
00,01

mino_Z red
▪︎▪︎
 ▪︎▪︎
10,11
   01,02

mino_J blue
▪︎
▪︎▪︎▪︎
10
00,01,02

mino_L orange
  ▪︎
▪︎▪︎▪︎
      12
00,01,02

mino_T purple
 ▪︎
▪︎▪︎▪︎
   11
00,01,02
```


📝 2020/02/04

# 格子の考え方違うやん

```
(0,2)|(1,2)|(2,2)
-----------------
(0,1)|(1,1)|(2,1)
-----------------
(0,0)|(0,1)|(0,2)
```

で、なくて

```
[
 [0,1,2]
 [0,1,2]
 [0,1,2]
]
```

これだけで、成立するのでは ?🤔


ほぼ、同じだが、ワイの考え方が違ってた

---

📝 2020/02/03

# Node を格子状に ?


つまるところ、MVC なのか ?


Node の子が

  - 列で並ぶのではなく
  - x,y 位置で配置される


# Node
```
(0,2)|(1,2)|(2,2)
-----------------
(0,1)|(1,1)|(2,1)
-----------------
(0,0)|(0,1)|(0,2)
```
 
# 格納

ex: `Node.add(x,y) = child`
  - x : 横
  - y : 縦

事前に箱を用意しておく必要あり


# 呼び出し方
ex: `Node.get(x,y)`


Node の中の子を呼ぶイメージ


## get(x,y)

直接使うのではなく



他アクションの親的な使い方

- `active`: 操作できる -> `minos` の種類により
- `fixed`: 着地している -> `active` だった色を継続
- `wall`: 壁 -> 色固定
- `null`: その他 -> 背景(非`active`)


# 色

`minos` の種類により
色の分岐をさせる

- 0: mino_i: 'cyan'
- 1: mino_o: 'yellow'
- 2: mino_s: 'green'
- 3: mino_z: 'red'
- 4: mino_j: 'blue'
- 5: mino_l: 'orange'
- 6: mino_t: 'purple'




---

📝 2020/02/02

並んだら消すフラグ管理が死にそうなので、色々と書き換える

- 壁block
- block を正方形に



一旦

- 落ちるアクション止める
- 自由に動かしてみる
	- 回転も試す



---

📝 2020/02/01

一つのミノを、落下 and 停止までいけた

[ここ](./blockFall.py)


## block 管理

現在は、一次元管理してるのだけども、本来は多分 x,y の二次元管理なんやろうな

- 左右移動
- block の重なり

とかの場面になると、アウチになるんやろなぁ


## 解説

現在までの、解説とかやってみたいけど、書く方が優先になっちゃってるY 🤗

## つぎ

ランダムで、出現block を出せるようにするか

- 関数？
- class ？
- 色は、単色でいくか


---
📝 2020/01/31

# TetrisMino

touch 面倒なので、見た目作った

## 進める手順 🤔
- 落ちる処理？
	- 初動位置の指定
- ランダム表示？
	- どんな分岐方が



---

📝 2020/01/30

# touch関係

1日かけてやっと解決、、、

# class 設計

``` python

class Parent(obj):
  def __init__(self):
    self.hoge = hoge
    # 処理
    
class Child(Parent):
  def __init__(self):
```

的に、書きたいけど、脳が追いついてない

css の時もそうだけど、手段目的になってしまってる（だって、同じこと書いているもの、、、）


📝 2020/01/29
# 親子関係

子のtouch 判断をなにで取得するか？

- `if touch.location in (self.frame):` だと、一つ上の親のframe 座標基準になってしまう
- 階層を減らせばいけそう
	- 今後の必要性を鑑みると取得できるようにしたい


---

📝 2020/01/28

# class 調査

すべて、`MainScene` にブチ込んでいたのでclass で分けたい


## `super(SubNode, self).__init__(parent=main_cls)`

- 継承元(`scene.ShapeNode`)の`parent` 指定を使っている ?
	- ?: 継承だから、そもそも使えるのでは ?
	- `__init__(self, hoge):` の呼び出しではできなかった
- 動いてるから、よし！状態 🤗

## 作ったclass 先のTouch Event

馬鹿正直に、`scene.Scene` 

- `touch_began(self,touch):`
- `touch_moved(self,touch):`
- `touch_ended(self,touch):`

でなくても、良さそう


`touch` も、呼び出し先と、関連してればよし！感


しかし、混乱はしそうなので、統一してやる予定

- 毎回同じのを書き換える
- 同じ呼び出しになる
- 変化を追加class 側でやる


とかなってきたら、変えることも検討

### 個別判定

`if touch.location in (self.frame):` で判別さすと、四角形で取得してる

- 円形は、誤差に
	- 現状は、そこまで細かくしてなくてもいいか
- 後の親も判断する
	- いまのところ問題なし夫で進む


### 分割構成

上からいくか？下からいくか？みたいな状況になってしまっておる、、、



- `MainScene`
	- `ControllerView`
	- `GameView`
		- 今度
			- ロジックも考えなきゃ
			- `ControllerView` で知見を蓄える






# オブジェクト指向プログラミング

なんとなく書いて考えて、

- 親子
- 兄弟

の関係性を意識して、ネスト・レイヤー分けをする。みたいな認識でやってみている

`self` に繋げて`self.hoge` としていいのか？ 🤔


みたいに、なんとなくムカデにならないように。的な


---
📝 2020/01/27

# とりあえずガワをつくる

1) ゲームのview
1) 操作のview

レイアウトフレームは作っておいて、ゲームロジックはその後に


## todo & memo: ゲームのview
- 20x10 の格子
- スコアとかは、度外視
	- 次にくるblock もいまのところなし



## todo & memo: 操作のview
- ボタンつける
	- 各ボタンの反応確認
	- 以前は `class` に`Node` やらつけたた
- とりあえず、丸とか四角でいいかな
	- label どうだったけか？


# まーで、コードひどい

- 繰り返し書いている感の部分は、共通化
- `self` つけるタイミングは？
- `class` 定義の際理解もしる

---
# かき捨てメモ

# field
```
縦20行 × 横10列
main.bounds
(0.00, 0.00, 375.00, 812.00)
man.size
(375.00, 812.00)
```


# blocks

```
I-テトリミノ（水色）
  4列消し「テトリス」を決めることのできる唯一のテトリミノ。
O-テトリミノ（黄色）
  回転させても形の変わらないテトリミノ。
S-テトリミノ（緑）
Z-テトリミノ（赤）
J-テトリミノ（青）
L-テトリミノ（オレンジ）
T-テトリミノ（紫）
  ガイドライン制定後の作品ではT-Spin（後述）が可能。
```


# layer

```
- main(safe_area)
  - view
  - controller
    - arrow
      - `↓`
      - `→`
      - `←`
        - ※ `↑` 変換もあり？
    - enter
```
