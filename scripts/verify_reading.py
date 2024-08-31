import re
import sys

from rhoknp import Document, Morpheme

from utils import list_files

HIRAGANA = r"\u3041-\u3096"
HIRAGANA_PTN = re.compile(rf"[ー{HIRAGANA}]+")
MULTIPLE_READING_PTN = re.compile(r"^[^/\s]+(/[^/\s]+)+$")
ACRONYM_PTN = re.compile(r"^[A-ZＡ-Ｚ]+$")
LATIN_1_SUPPLEMENT = r"\u0080-\u00FF"
LATIN_EXTENDED_A = r"\u0100-\u017F"
LATIN_EXTENDED_B = r"\u0180-\u024F"
LATIN_EXTENDED_ADDITIONAL = r"\u1E00-\u1EFF"
IPA_EXTENSIONS = r"\u0250-\u02AF"
LATIN_PTN = re.compile(
    rf"[-0-9a-zA-Z'{LATIN_1_SUPPLEMENT}{LATIN_EXTENDED_A}{LATIN_EXTENDED_B}{LATIN_EXTENDED_ADDITIONAL}{IPA_EXTENSIONS}]+"
)
CYRILLIC_PTN = re.compile(r"[\u0400-\u04FF]+")
HANGEUL_PTN = re.compile(r"[\uAC00-\uD7AF]+")
ARABIC_PTN = re.compile(r"[\u0600-\u06FF]+")
SYRIAC_PTN = re.compile(r"[\u0700-\u074F]+")


def verify_morpheme_reading(morpheme: Morpheme, reading: str) -> None:
    # 熟字訓の2単語目以降
    if morpheme.reading in ("　", " ") and morpheme.text not in ("　", " "):
        return
    if morpheme.pos == "特殊":
        # if morpheme.subpos == "句点":
        #     assert morpheme.reading in ("。", ".", "．"), f"{morpheme.reading} ({morpheme.sentence.sid})"
        #     return
        if morpheme.subpos == "読点":
            assert reading in ("、", ",", "，"), f"{reading} ({morpheme.sentence.sid})"
            return
        if reading != morpheme.text:
            assert HIRAGANA_PTN.fullmatch(reading) is not None, f"{reading} ({morpheme.sentence.sid})"
            return
        return

    # 「NHK」などは読みを機械的に推定できるため表層表記がそのままアノテーションされている
    if ACRONYM_PTN.fullmatch(morpheme.text) is not None and morpheme.text == reading:
        return

    if (
        LATIN_PTN.fullmatch(morpheme.text) is not None
        or CYRILLIC_PTN.fullmatch(morpheme.text) is not None
        or HANGEUL_PTN.fullmatch(morpheme.text) is not None
        or ARABIC_PTN.fullmatch(morpheme.text) is not None
        or SYRIAC_PTN.fullmatch(morpheme.text) is not None
    ):
        if morpheme.text == reading:
            return

    if morpheme.pos == "名詞" and morpheme.subpos == "数詞":
        if morpheme.text == reading:
            return

    # 例外
    if morpheme.sentence.sid in ("wiki00183525-02", "wiki00166822-02"):
        return

    if HIRAGANA_PTN.fullmatch(reading) is None:
        print(f"{reading} ({morpheme.sentence.sid})")


def main() -> None:
    for path in sorted(list_files(sys.argv[1:])):
        document = Document.from_knp(path.read_text())
        for morpheme in document.morphemes:
            if MULTIPLE_READING_PTN.fullmatch(morpheme.reading) is not None:
                for reading in morpheme.reading.split("/"):
                    verify_morpheme_reading(morpheme, reading)
            else:
                verify_morpheme_reading(morpheme, morpheme.reading)


if __name__ == "__main__":
    main()
