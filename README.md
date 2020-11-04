# BMKeyLogger
配信中とかに鍵盤の入力を表示するやつ

## 使い方
同梱の`config.json`に使用するキーまたはボタンを記述します。
キーボードの場合はVirtual key codesを16進の文字列で、ジョイパッドの場合はボタンの番号を整数で記述します。ただしX軸Y軸を割り当てる場合は、X軸マイナス方向なら`-x`、プラス方向なら`+x`のように文字列で記述してください。
デフォルトでは1Pが`qwerty`とLSHIFTで2Pが`,l.;/:\`とRSHIFT、SPACE、PS2専コンの割り当てになっています。カンマ区切りで複数のjoypadやボタンを割り当てることができます。

### Virtual key codes参考
https://docs.microsoft.com/ja-jp/windows/win32/inputdev/virtual-key-codes

