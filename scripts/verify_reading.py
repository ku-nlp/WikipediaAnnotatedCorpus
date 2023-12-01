import re
from pathlib import Path

from rhoknp import Document, Morpheme

KNP_DIR = Path("knp")
HIRAGANA = r"\u3041-\u3096"
HIRAGANA_PTN = re.compile(rf"[ー{HIRAGANA}]+")
MULTIPLE_READING_PTN = re.compile(r"^[^/\s]+(/[^/\s]+)+$")
LATIN_PTN = re.compile(r"[-0-9a-zA-Z'ʏ\u0080-\u00FF\u0100-\u024F]+")
HANGEUL_PTN = re.compile(r"[\uAC00-\uD7AF]+")
ARABIC_PTN = re.compile(r"[\u0600-\u06FF]+")


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
    if (
        LATIN_PTN.fullmatch(morpheme.text) is not None
        or HANGEUL_PTN.fullmatch(morpheme.text) is not None
        or ARABIC_PTN.fullmatch(morpheme.text) is not None
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


def main():
    for path in KNP_DIR.glob("**/*.knp"):
        document = Document.from_knp(path.read_text())
        for morpheme in document.morphemes:
            if MULTIPLE_READING_PTN.fullmatch(morpheme.reading) is not None:
                for reading in morpheme.reading.split("/"):
                    verify_morpheme_reading(morpheme, reading)
            else:
                verify_morpheme_reading(morpheme, morpheme.reading)


if __name__ == "__main__":
    main()
