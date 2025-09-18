# kohya-ss GUI Simple
[kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts/tree/main) の、ローカルで動作するシンプルな webview GUI。UI は [index.html](https://dskjal.github.io/kohya-ss-GUI-Simple/index.html) から確認できる（ボタンなどは機能しない）。

## インストール
シェルから以下のコマンドを実行。
> python -m pip install webview

## 起動
run.py を実行。

## 設定
デフォルト設定は省 VRAM 設定で、４つのフォルダを設定すれば、VRAM 8 GB の GPU で学習できる。

## 機能
- コード行数 500 行以下で理解しやすく変更しやすい。AI のコンテキストサイズが不足しないので、AI 任せの変更も容易
- デザインの変更とレイアウトの変更がすぐにできる
- 数値やチェックボックスの引数の追加のようなシンプルな変更ならオプションの追加も容易
