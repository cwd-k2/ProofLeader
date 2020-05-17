# Proofreader
カレントディレクトリより深い位置にある.mdファイルの句読点や整数表記を修正します。

(変換例)
* `，`は`、`に変換されます。
* `．`は`。`に変換されます。
* ` 100,111,000 `は` 100,111,000 `に変換されます。
* `abc, def`は変換されません。
* `aは 123 です`は`a は 123 です`に変換されます。

何がどう変換されるのか、厳密なことはそのうち記述します。

## 使用方法

* 起動コマンド

<pre>
sh Proofreader/proofreader.sh
or
sh Proofreader/proofreader.sh TARGET_DIR/
</pre>

* 期待される出力例

<pre>
folder_a/folder_b/README.md : OK
folder_c/README.md : OK
converter : ALL OK
CHECK!! -> https://competent-morse-3888be.netlify.app/
</pre>

* 文章表現の警告機能
同じディレクトリに`word_list.csv`ファイルを作り、以下のように記述します。

<pre>
Before1,After1
Before2,After2
Before3,After3
</pre>

すると以下のようにBeforeが文章に入っていた場合Afterにした方がいいと警告します。

<pre>
WARNING: ファイル名:行数:何文字: (致します) => (いたします)
</pre>

~Before,Afterは正規表現で記述してください。~
正規表現で書きたいのですが、現在`(|)`の 3 文字くらいしか使えません。ごめんなさい><

* 補足
`<pre></pre>`で囲われている内側の文字に関して、**変換はされません**．ですが、警告は出します。

(例)
```
<pre>
123456 // 123,456にはならない
</pre>
```

```
<pre>
致します // WARNINGが表示されます。
</pre>
```

## ディレクトリの配置方法

現在`folder_a/`にいて、`folder_b/`内のREADME.mdを修正したいとします。
そのとき、以下のように配置し、**`folder_a/`で [使用方法の起動コマンド](#使用方法)を使用してください。**

<pre>
folder_a/ -- folder_b/
          |- Rroofreader/
</pre>

## 必要なライブラリ及びパッケージ

* Python 3 ( 3 . 6 . 4 以上)
* pathlib
* sys
* scv
* os
* re