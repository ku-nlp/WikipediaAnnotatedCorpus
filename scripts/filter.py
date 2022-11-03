from pathlib import Path
import textwrap

from rhoknp import Document


def filter_tags(document: Document) -> Document:
    for phrase in document.phrases:
        phrase.features.clear()
    for base_phrase in document.base_phrases:
        ne_feature = base_phrase.features.get("NE")
        base_phrase.features.clear()
        if ne_feature is not None:
            base_phrase.features["NE"] = ne_feature
    for morpheme in document.morphemes:
        ne_feature = morpheme.features.get("NE")
        morpheme.features.clear()
        if ne_feature is not None:
            morpheme.features["NE"] = ne_feature
        morpheme.semantics.clear()
        morpheme.semantics.is_nil = False
    return document


def main():
    doc_path = Path("knp/wiki0200/wiki02001132.knp")
    filtered_document = filter_tags(Document.from_knp(doc_path.read_text()))
    print(filtered_document.to_knp())


if __name__ == "__main__":
    main()


def test_filter():
    knp_text = textwrap.dedent(
        """\
        # S-ID:wiki00100134-00 KNP:5.0-6a1f607d DATE:2022/04/11 SCORE:0.00000
        * 3D <文頭><ハ><読点><助詞><受けNONE><係:NONE>
        + 3D <文頭><ハ><読点><助詞><受けNONE><係:NONE>
        は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><文頭><付属><タグ単位始><文節始>
        、 、 、 特殊 1 読点 2 * 0 * 0 NIL <英記号><記号><述語区切><付属>
        * 2D <SM-場所><BGH:日本/にほん><地名><助詞><連体修飾><体言><係:ノ格><区切:0-4><正規化代表表記:日本/にほん><主辞代表表記:日本/にほん>
        + 2D <SM-場所><BGH:日本/にほん><地名><助詞><連体修飾><体言><係:ノ格><区切:0-4><名詞項候補><先行詞候補><係チ:非用言格解析||用言&&文節内:Ｔ解析格-ヲ><正規化代表表記:日本/にほん><主辞代表表記:日本/にほん><memo text="メモ1"/><NE:LOCATION:日本>
        日本 にっぽん 日本 名詞 6 地名 4 * 0 * 0 "代表表記:日本/にほん 地名:国" <代表表記:日本/にほん><地名:国><正規化代表表記:日本/にほん><判定詞化名詞:2-2><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><固有キー><文節主辞><NE:LOCATION:single>
        の の の 助詞 9 接続助詞 3 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D <BGH:元号/げんごう><助詞><連体修飾><体言><係:ノ格><区切:0-4><正規化代表表記:元号/げんごう><主辞代表表記:元号/げんごう>
        + 3D <BGH:元号/げんごう><助詞><連体修飾><体言><係:ノ格><区切:0-4><名詞項候補><先行詞候補><係チ:非用言格解析||用言&&文節内:Ｔ解析格-ヲ><正規化代表表記:元号/げんごう><主辞代表表記:元号/げんごう>
        元号 げんごう 元号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:元号/げんごう ドメイン:政治 カテゴリ:抽象物" <代表表記:元号/げんごう><ドメイン:政治><カテゴリ:抽象物><正規化代表表記:元号/げんごう><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        の の の 助詞 9 接続助詞 3 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:つ/つ><文末><カウンタ:つ><数量><句点><体言><用言:判><体言止><一文字漢字><レベル:C><区切:5-5><ID:（文末）><裸名詞><並キ:名:&ST:3.0><並列タイプ:AND><係:文末><提題受:30><主節><格要素><連用要素><状態述語><正規化代表表記:一/いち+つ/つ><主辞代表表記:一/いち+つ/つ><並列類似度:-100.000>
        + -1D <rel type="ガ" target="は、" sid="wiki00100134-00" id="0"/><rel type="ノ" target="元号" sid="wiki00100134-00" id="2"/><rel type="=" target="は、" sid="wiki00100134-00" id="0"/><BGH:つ/つ><文末><カウンタ:つ><数量><句点><体言><用言:判><体言止><一文字漢字><レベル:C><区切:5-5><ID:（文末）><裸名詞><並キ:名:&ST:3.0><並列タイプ:AND><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><正規化代表表記:一/いち+つ/つ><主辞代表表記:一/いち+つ/つ><用言代表表記:つ/つ><節-区切><節-主辞><時制:非過去><述語項構造:dummy:dummy:ガ/N/は、/0/0/5;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ガ２/U/-/-/-/-;ノ/C/元号/0/2/1>
        一 いち 一 名詞 6 数詞 7 * 0 * 0 "カテゴリ:数量 疑似代表表記 代表表記:一/いち" <カテゴリ:数量><疑似代表表記><代表表記:一/いち><正規化代表表記:一/いち><漢字><かな漢字><数字><名詞相当語><自立><種別同格><内容語><タグ単位始><文節始>
        つ つ つ 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0 "代表表記:つ/つ 準内容語 連語由来" <代表表記:つ/つ><準内容語><連語由来><正規化代表表記:つ/つ><カウンタ><かな漢字><ひらがな><表現文末><付属><種別同格><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        # S-ID:wiki00100134-01 KNP:5.0-6a1f607d DATE:2022/04/11 SCORE:-2.00000
        * 1D <文頭><助詞><連体修飾><体言><係:ノ格><区切:0-4><正規化代表表記:安元/あんげん><主辞代表表記:安元/あんげん>
        + 1D <文頭><助詞><連体修飾><体言><係:ノ格><区切:0-4><名詞項候補><先行詞候補><係チ:非用言格解析||用言&&文節内:Ｔ解析格-ヲ><正規化代表表記:安元/あんげん><主辞代表表記:安元/あんげん><Wikipedia上位語:元号/げんごう>
        安元 あんげん 安元 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipedia上位語:元号/げんごう 疑似代表表記 代表表記:安元/あんげん" <自動獲得:Wikipedia><Wikipedia上位語:元号/げんごう><疑似代表表記><代表表記:安元/あんげん><正規化代表表記:安元/あんげん><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        の の の 助詞 9 接続助詞 3 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D <BGH:後/あと><相対名詞><形副名詞><時間><外の関係><読点><体言><一文字漢字><係:連用><修飾><レベル:B><並キ:名:&ST:4.0&&&自立語一致><区切:0-4><ID:（副詞的名詞）><連用要素><連用節><正規化代表表記:後/あと><主辞代表表記:後/あと><並列類似度:-100.000>
        + 3D <rel type="ノ" target="安元" sid="wiki00100134-01" id="0"/><BGH:後/あと><相対名詞><形副名詞><時間><外の関係><読点><体言><一文字漢字><係:連用><修飾><レベル:B><並キ:名:&ST:4.0&&&自立語一致><区切:0-4><ID:（副詞的名詞）><連用要素><連用節><名詞項候補><省略解析なし><正規化代表表記:後/あと><主辞代表表記:後/あと><クエリ削除語><述語項構造:dummy:dummy:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ガ２/U/-/-/-/-;ノ/C/安元/0/0/3>
        後 あと 後 名詞 6 副詞的名詞 9 * 0 * 0 "代表表記:後/あと" <代表表記:後/あと><正規化代表表記:後/あと><相対名詞><漢字><かな漢字><名詞相当語><形副名詞><自立><内容語><タグ単位始><文節始><文節主辞>
        、 、 、 特殊 1 読点 2 * 0 * 0 NIL <英記号><記号><述語区切><付属>
        * 3D <助詞><連体修飾><体言><係:ノ格><区切:0-4><正規化代表表記:養和/ようわ><主辞代表表記:養和/ようわ>
        + 3D <助詞><連体修飾><体言><係:ノ格><区切:0-4><名詞項候補><先行詞候補><係チ:非用言格解析||用言&&文節内:Ｔ解析格-ヲ><正規化代表表記:養和/ようわ><主辞代表表記:養和/ようわ><Wikipedia上位語:元号/げんごう><memo text="メモ2"/>
        養和 ようわ 養和 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipedia上位語:元号/げんごう 疑似代表表記 代表表記:養和/ようわ" <自動獲得:Wikipedia><Wikipedia上位語:元号/げんごう><疑似代表表記><代表表記:養和/ようわ><正規化代表表記:養和/ようわ><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        の の の 助詞 9 接続助詞 3 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:前/まえ><文末><相対名詞><形副名詞><外の関係><句点><体言><用言:判><体言止><一文字漢字><レベル:C><区切:5-5><ID:（文末）><裸名詞><係:文末><提題受:30><主節><格要素><連用要素><状態述語><正規化代表表記:前/まえ><主辞代表表記:前/まえ>
        + -1D <rel type="ガ" target="は、" sid="wiki00100134-00" id="0"/><rel type="ノ" target="養和" sid="wiki00100134-01" id="2"/><rel type="=" target="一つ" sid="wiki00100134-00" id="3"/><BGH:前/まえ><文末><相対名詞><形副名詞><外の関係><句点><体言><用言:判><体言止><一文字漢字><レベル:C><区切:5-5><ID:（文末）><裸名詞><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><名詞項候補><省略解析なし><正規化代表表記:前/まえ><主辞代表表記:前/まえ><用言代表表記:前/まえ><節-区切><節-主辞><時制:非過去><クエリ削除語><述語項構造:dummy:dummy:ガ/O/は、/1/0/5;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ガ２/U/-/-/-/-;ノ/C/養和/0/2/4>
        前 まえ 前 名詞 6 副詞的名詞 9 * 0 * 0 "代表表記:前/まえ" <代表表記:前/まえ><正規化代表表記:前/まえ><相対名詞><漢字><かな漢字><名詞相当語><形副名詞><表現文末><自立><内容語><タグ単位始><文節始><固有修飾><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    filtered_knp_text = textwrap.dedent(
        """\
        # S-ID:wiki00100134-00 KNP:5.0-6a1f607d DATE:2022/04/11 SCORE:0.00000
        * 3D
        + 3D
        は は は 助詞 9 副助詞 2 * 0 * 0
        、 、 、 特殊 1 読点 2 * 0 * 0
        * 2D
        + 2D <memo text="メモ1"/><NE:LOCATION:日本>
        日本 にっぽん 日本 名詞 6 地名 4 * 0 * 0 <NE:LOCATION:single>
        の の の 助詞 9 接続助詞 3 * 0 * 0
        * 3D
        + 3D
        元号 げんごう 元号 名詞 6 普通名詞 1 * 0 * 0
        の の の 助詞 9 接続助詞 3 * 0 * 0
        * -1D
        + -1D <rel type="ガ" target="は、" sid="wiki00100134-00" id="0"/><rel type="ノ" target="元号" sid="wiki00100134-00" id="2"/><rel type="=" target="は、" sid="wiki00100134-00" id="0"/>
        一 いち 一 名詞 6 数詞 7 * 0 * 0
        つ つ つ 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        # S-ID:wiki00100134-01 KNP:5.0-6a1f607d DATE:2022/04/11 SCORE:-2.00000
        * 1D
        + 1D
        安元 あんげん 安元 名詞 6 普通名詞 1 * 0 * 0
        の の の 助詞 9 接続助詞 3 * 0 * 0
        * 3D
        + 3D <rel type="ノ" target="安元" sid="wiki00100134-01" id="0"/>
        後 あと 後 名詞 6 副詞的名詞 9 * 0 * 0
        、 、 、 特殊 1 読点 2 * 0 * 0
        * 3D
        + 3D <memo text="メモ2"/>
        養和 ようわ 養和 名詞 6 普通名詞 1 * 0 * 0
        の の の 助詞 9 接続助詞 3 * 0 * 0
        * -1D
        + -1D <rel type="ガ" target="は、" sid="wiki00100134-00" id="0"/><rel type="ノ" target="養和" sid="wiki00100134-01" id="2"/><rel type="=" target="一つ" sid="wiki00100134-00" id="3"/>
        前 まえ 前 名詞 6 副詞的名詞 9 * 0 * 0
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    filtered_document = filter_tags(document)
    assert filtered_document.to_knp() == filtered_knp_text
