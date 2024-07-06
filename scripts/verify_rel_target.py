import argparse
import dataclasses
from enum import Enum

from rhoknp import BasePhrase, Document, Morpheme
from rhoknp.cohesion import RelTag

from utils import list_files


class ErrorType(Enum):
    REL_TARGET_MISMATCH = "rel_target_mismatch"
    REL_WITH_UNKNOWN_SID = "rel_with_unknown_sid"
    INDEX_OUT_OF_RANGE = "index_out_of_range"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+", help="paths to knp files or directories")
    parser.add_argument("--modify", action="store_true", help="modify rel tag errors")
    args = parser.parse_args()

    error_type_to_data: dict[ErrorType, list] = {error_type: [] for error_type in ErrorType}
    for path in sorted(list_files(args.paths)):
        document = Document.from_knp(path.read_text())
        doc_id = document.doc_id
        for base_phrase in document.base_phrases:
            sent_id = base_phrase.sentence.sent_id
            for idx, rel_tag in enumerate(base_phrase.rel_tags):
                if rel_tag.sid is None:
                    continue
                items = [doc_id, sent_id, base_phrase.text, rel_tag.type]
                error_type_or_new_rel = search_target_base_phrase(base_phrase, rel_tag, do_modify=args.modify)
                match error_type_or_new_rel:
                    case ErrorType.REL_TARGET_MISMATCH:
                        error_type_to_data[error_type_or_new_rel].append([*items, rel_tag.target])
                    case ErrorType.REL_WITH_UNKNOWN_SID:
                        error_type_to_data[error_type_or_new_rel].append([*items, rel_tag.sid])
                    case ErrorType.INDEX_OUT_OF_RANGE:
                        error_type_to_data[error_type_or_new_rel].append([*items, rel_tag.base_phrase_index])
                    case RelTag() as new_rel:
                        base_phrase.rel_tags[idx] = new_rel
        if args.modify:
            path.write_text(document.to_knp())
    for error_type, data in error_type_to_data.items():
        # write error to csv files
        with open(f"{error_type.value}.csv", "w") as f:
            f.write("文書ID,文ID,基本句,格,ターゲット\n")
            for row in data:
                f.write(",".join(str(item) for item in row) + "\n")


def search_target_base_phrase(base_phrase: BasePhrase, rel_tag: RelTag, do_modify: bool = False) -> ErrorType | RelTag:
    sentences = base_phrase.document.sentences
    sentences = [sent for sent in sentences if sent.sid == rel_tag.sid]
    if not sentences:
        if do_modify:
            rel_tag = dataclasses.replace(rel_tag, sid=base_phrase.sentence.sid)
            ret = search_target_base_phrase(base_phrase, rel_tag, do_modify=False)
            if isinstance(ret, ErrorType):
                return ErrorType.REL_WITH_UNKNOWN_SID
            sentences = [base_phrase.sentence]
        else:
            return ErrorType.REL_WITH_UNKNOWN_SID
    sentence = sentences[0]
    assert rel_tag.base_phrase_index is not None
    if rel_tag.base_phrase_index >= len(sentence.base_phrases):
        if do_modify:
            matched_base_phrases = [bp for bp in sentence.base_phrases if rel_tag.target == get_core_text(bp)]
            if len(matched_base_phrases) == 1:
                return dataclasses.replace(rel_tag, base_phrase_index=matched_base_phrases[0].index)
        return ErrorType.INDEX_OUT_OF_RANGE
    target_base_phrase = sentence.base_phrases[rel_tag.base_phrase_index]
    if rel_tag.target not in target_base_phrase.text:
        if do_modify:
            matched_base_phrases = [bp for bp in sentence.base_phrases if rel_tag.target == get_core_text(bp)]
            if len(matched_base_phrases) == 1:
                return dataclasses.replace(rel_tag, base_phrase_index=matched_base_phrases[0].index)
        return ErrorType.REL_TARGET_MISMATCH
    return rel_tag


def get_core_text(base_phrase: BasePhrase) -> str:
    """Get the core text without ancillary words."""
    morphemes = base_phrase.morphemes
    start_index = 0
    for morpheme in morphemes:
        if morpheme.pos == "特殊" and (morpheme.subpos != "記号" or morpheme.text == "・"):
            start_index += 1
        else:
            break
    end_index = len(morphemes)
    for morpheme in reversed(morphemes):
        if to_rstrip(morpheme) is True:
            end_index -= 1
        else:
            break
    ret = "".join(m.text for m in morphemes[start_index:end_index])
    if not ret:
        start_index = 0
        end_index = len(morphemes)
    return "".join(m.text for m in morphemes[start_index:end_index])


def to_rstrip(morpheme: Morpheme) -> bool:
    return (morpheme.pos in ("特殊", "助詞", "助動詞", "判定詞") or is_weak_suffix(morpheme)) and (
        morpheme.pos == "特殊" and morpheme.subpos == "記号" and morpheme.text != "・"
    ) is False


def is_weak_suffix(morpheme: Morpheme) -> bool:
    # https://github.com/ku-nlp/KyotoCorpusAnnotationTool/blob/main/js/setting.js
    strong_suffixes: set[str] = set(
        "率|通り|どおり|方|がた|かた|型|形|用|製|家|者|数|費|入り|いり|あけ|上|じょう|作り|づくり|ずみ|無し|なし|増|減|的だ|化|さ|都|道|府|県|郡|市|村|町|区|州".split(
            "|"
        )
    )
    if morpheme.pos != "接尾辞":
        return False
    return (
        morpheme.text not in strong_suffixes
        and morpheme.subpos != "名詞性名詞助数辞"
        and morpheme.subpos != "形容詞性述語接尾辞"
        and morpheme.subpos != "動詞性接尾辞"
    )


if __name__ == "__main__":
    main()
