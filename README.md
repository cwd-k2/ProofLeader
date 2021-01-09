# ProofLeader

指定したファイル, またはディレクトリより深い位置にある.md ファイルの句読点や整数表記を修正します。

(変換例)

- `、`は`、`に変換されます。
- `。`は`。`に変換されます。
- `100111000`は`100,111,000`に変換されます。
- `abc, def`は変換されません。
- `aは123です`は`a は 123 です`に変換されます。

## インストール方法

以下の環境を前提とします.

- python3 (>= 3.2 多分)
- pip
- setuptools

### pip を利用する場合

```sh
python3 -m pip install git+https://github.com/cwd-k2/ProofLeader
```

### npm などを利用する場合

別途 node や npm 等のインストールが必要となります.

```sh
# npm を利用する場合
$ npm install --save-dev git+https://github.com/cwd-k2/ProofLeader.git
# yarn を利用する場合
$ yarn add -D git+https://github.com/cwd-k2/ProofLeader.git
```

## 使用方法

- 起動コマンド

```sh
$ python3 -m proof_leader # pip でインストールした場合
$ npx proof_leader        # npm などを利用した場合
$ proof_leader            # パスの通ったところにインストールした場合
```

- コマンドラインオプション

```
usage: proof_leader [-h] [-v] [-i] [file ...]

positional arguments:
  file           ファイル/フォルダを指定して実行 (無い場合はカレントディレクトリが指定される)

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show version and exit
  -i, --inplace  inplace edit file[s]
```

## 機能

### In-Place な校正

デフォルトでは校正の情報を出力します.

```sh
# 様々な情報が出力される
$ proof_leader
```

`-i|--inplace` オプションを利用することで, 校正を即座にファイルに反映させることができます.

```sh
# 変更点があれば即座にファイルに反映される
$ proof_leader -i
```

### 文章表現の警告機能(ver 1.4 で書式が変更になりました)

ターゲットとなるファイルと同じ階層か, それより上の階層に `word_list.csv` ファイルを作り、以下のように記述します。

<pre>
After1,Before1
After2,Before2_1,Before2_2,Before2_3
After3,Before3_1,Before3_2
</pre>

Before が文章に入っていた場合 After にした方がいいと警告します。

また Before は OR 指定ができます。

```
A,(B|C)
```

B または C のとき警告します。

### 指定文字列の探索

ターゲットとなるファイルと同じ階層か, それより上の階層に `find_list.csv` ファイルを作り、以下のように記述します。

<pre>
Detect
Some
Expressions
</pre>

これにより, 特定の単語が使用されているファイルを見つけ出すことができます.

### 補足

`<pre></pre>` またはバックティック (\`) で囲われている内側の文字に関して、**変換はされません**。

(例)

```
<pre>
123456 // 123,456 にはならない
</pre>
`11111` // 11,111にはならない
```

```
<pre>
致します // WARNINGが表示されます。
</pre>
`致します` // WARNINGが表示されます。
```

## 除外ファイルの設定

本プログラムは指定されたディレクトリ以下の全ての Markdown ファイルを探索します.

指定するファイルと同じ階層か, それより上の階層に `exclusion_list.csv` ファイルを作り、以下のように記述することで校閲対象から除外することができます。

```
.*/node_modules/.*
```

パス名の文字列に対する正規表現のマッチを行います.

## URL

[original](https://github.com/xryuseix/ProofLeader)

[this version](https://github.com/cwd-k2/ProofLeader)
