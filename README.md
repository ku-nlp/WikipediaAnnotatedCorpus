# Wikipedia Annotated Corpus

## Overview

This is a Japanese text corpus that consists of Wikipedia articles with various linguistic annotations.

The linguistic annotations consist of annotations of morphology, named entities, dependencies, predicate-argument
structures including zero anaphora, and coreferences.
For the annotation guidelines, see the manuals in the `doc` directory of
the [ku-nlp/KWDLC](https://github.com/ku-nlp/KWDLC) repository.

## Distributed files

- [`knp/`](./knp): the corpus annotated with morphology, named entities, dependencies, predicate-argument structures, and
  coreferences
- [`org/`](./org): the raw corpus
- [`id/`](./id): document id files providing train/dev/test split

## Statistics

|       | # of documents | # of sentences | # of morphemes | # of named entities | # of predicates | # of coreferring mentions |
|-------|---------------:|---------------:|---------------:|--------------------:|----------------:|--------------------------:|
| train |          1,144 |          4,532 |         65,300 |               4,231 |          17,474 |                    14,479 |
| dev   |            100 |            443 |          6,353 |                 423 |           1,701 |                     1,437 |
| test  |            200 |            775 |         11,123 |                 800 |           2,872 |                     2,534 |
| total |          1,444 |          5,750 |         82,776 |               5,454 |          22,047 |                    18,450 |

## Format of the annotation

Annotations of this corpus are given in the following format (a.k.a. the KNP format).

```text
# S-ID:wiki000010000-1
* 2D
+ 3D
太郎 たろう 太郎 名詞 6 人名 5 * 0 * 0
は は は 助詞 9 副助詞 2 * 0 * 0
* 2D
+ 2D
京都 きょうと 京都 名詞 6 地名 4 * 0 * 0
+ 3D <NE:ORGANIZATION:京都大学>
大学 だいがく 大学 名詞 6 普通名詞 1 * 0 * 0
に に に 助詞 9 格助詞 1 * 0 * 0
* -1D
+ -1D <rel type="ガ" target="太郎" sid="w201106-0000010001-1" id="0"/><rel type="ニ" target="大学" sid="w201106-0000010001-1" id="2"/>
行った いった 行く 動詞 2 * 0 子音動詞カ行促音便形 3 タ形 10
EOS
```

A description of this format can be found in [the documentation of KWDLC](https://github.com/ku-nlp/KWDLC#format-of-the-corpus-annotated-with-annotations-of-morphology-named-entities-dependencies-predicate-argument-structures-and-coreferences).

Note: You can use [rhoknp](https://github.com/ku-nlp/rhoknp) to intuitively access annotations from Python without understanding the syntax of this format.

```python
from rhoknp import Document

with open("knp/wiki0010/wiki00100176.knp") as f:
    document = Document.from_knp(f.read())
for morpheme in document.morphemes:
    ...
```

## References

- 萩行正嗣, 河原大輔, 黒橋禎夫. 多様な文書の書き始めに対する意味関係タグ付きコーパスの構築とその分析, 自然言語処理,
  Vol.21, No.2, pp.213-248, 2014. <https://doi.org/10.5715/jnlp.21.213>

## Contact

If you have any questions or problems with this corpus, please send an email to nl-resource at nlp.ist.i.kyoto-u.ac.jp.

## License

The license for this corpus is subject to CC BY-SA 4.0.
<https://creativecommons.org/licenses/by-sa/4.0/>
