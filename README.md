# tetrisPysta

> 2020/01/27 作成


## とりあえずガワをつくる

1) ゲームのview
1) 操作のview

レイアウトフレームは作っておいて、ゲームロジックはその後に


### todo & memo: ゲームのview
- 20x10 の格子
- スコアとかは、度外視
	- 次にくるblock もいまのところなし



### todo & memo: 操作のview
- ボタンつける
	- 各ボタンの反応確認
- とりあえず、丸とか四角でいいかな
	- label どうだったけか？


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
