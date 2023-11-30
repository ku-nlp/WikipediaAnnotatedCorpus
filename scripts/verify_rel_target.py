import argparse
import dataclasses
import sys
from collections.abc import Iterator
from enum import Enum
from pathlib import Path

from rhoknp import BasePhrase, Document
from rhoknp.cohesion import RelTag


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
    for path in sorted(list_paths(args.paths)):
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


def list_paths(paths: list[str]) -> Iterator[Path]:
    for path_str in paths:
        path = Path(path_str)
        if path.exists() is False:
            print(f"{path} not found and skipped", file=sys.stderr)
            continue
        if path.is_dir():
            yield from path.glob("**/*.knp")
        else:
            yield path


def search_target_base_phrase(base_phrase: BasePhrase, rel_tag: RelTag, do_modify: bool = False) -> ErrorType | RelTag:
    sentences = base_phrase.document.sentences
    sentences = [sent for sent in sentences if sent.sid == rel_tag.sid]
    if not sentences:
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
    if not (set(rel_tag.target) & set(target_base_phrase.text)):
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
        if morpheme.pos in ("助詞", "特殊", "判定詞"):
            start_index += 1
        else:
            break
    end_index = len(morphemes)
    for morpheme in reversed(morphemes):
        if morpheme.pos in ("助詞", "特殊", "判定詞"):
            end_index -= 1
        else:
            break
    ret = "".join(m.text for m in morphemes[start_index:end_index])
    if not ret:
        start_index = 0
        end_index = len(morphemes)
    return "".join(m.text for m in morphemes[start_index:end_index])


if __name__ == "__main__":
    main()
