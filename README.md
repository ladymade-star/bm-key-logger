# BMKeyLogger
配信中とかに鍵盤の入力を表示するやつ

## 使い方
同梱の`config.json`に使用するキーまたはボタンを記述します。

キーボードの場合はVirtual key codesを16進の文字列で、ジョイパッドの場合はボタンの番号を整数で記述します。ただしx軸y軸を割り当てる場合は、x軸マイナス方向なら`-x`、プラス方向なら`+x`のように文字列で記述してください。

デフォルトでは1Pが`qwerty`、LSHIFT、PS2専コン1つ目で、2Pが`,l.;/:\`、RSHIFT、PS2専コン2つ目の割り当てになっています。カンマ区切りで複数のjoypadやボタンを割り当てることができます。

鍵盤の順番は1Pが0～8番目に`皿皿1234567`で2Pが9～17番目に`1234567皿皿`です。

`threshold`にはx軸y軸の閾値を記述します。デフォルトは0.9です。

### Virtual key codes参考
https://docs.microsoft.com/ja-jp/windows/win32/inputdev/virtual-key-codes