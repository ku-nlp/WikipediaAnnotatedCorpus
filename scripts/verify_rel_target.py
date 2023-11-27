from enum import Enum
from pathlib import Path

from rhoknp import Document
from rhoknp.cohesion import RelTag

KNP_DIR = Path("knp")


class ErrorType(Enum):
    REL_TARGET_MISMATCH = "rel_target_mismatch"
    REL_WITH_UNKNOWN_SID = "rel_with_unknown_sid"
    INDEX_OUT_OF_RANGE = "index_out_of_range"


def search_target_base_phrase(self, rel_tag: RelTag) -> ErrorType | None:
    sentences = self.document.sentences if self.sentence.has_document() else [self.sentence]
    sentences = [sent for sent in sentences if sent.sid == rel_tag.sid]
    if not sentences:
        return ErrorType.REL_WITH_UNKNOWN_SID
    sentence = sentences[0]
    assert rel_tag.base_phrase_index is not None
    if rel_tag.base_phrase_index >= len(sentence.base_phrases):
        return ErrorType.INDEX_OUT_OF_RANGE
    target_base_phrase = sentence.base_phrases[rel_tag.base_phrase_index]
    if not (set(rel_tag.target) & set(target_base_phrase.text)):
        return ErrorType.REL_TARGET_MISMATCH
    return None


def main():
    error_type_to_data: dict[ErrorType, list] = {error_type: [] for error_type in ErrorType}
    for path in sorted(KNP_DIR.glob("**/*.knp")):
        document = Document.from_knp(path.read_text())
        doc_id = document.doc_id
        for base_phrase in document.base_phrases:
            sent_id = base_phrase.sentence.sent_id
            for rel_tag in base_phrase.rel_tags:
                if rel_tag.sid is None:
                    continue
                items = [doc_id, sent_id, base_phrase.text, rel_tag.type]
                error_type = search_target_base_phrase(base_phrase, rel_tag)
                match error_type:
                    case ErrorType.REL_TARGET_MISMATCH:
                        error_type_to_data[error_type].append([*items, rel_tag.target])
                    case ErrorType.REL_WITH_UNKNOWN_SID:
                        error_type_to_data[error_type].append([*items, rel_tag.sid])
                    case ErrorType.INDEX_OUT_OF_RANGE:
                        error_type_to_data[error_type].append([*items, rel_tag.base_phrase_index])
                    case None:
                        continue
    for error_type, data in error_type_to_data.items():
        # write error to csv files
        with open(f"{error_type.value}.csv", "w") as f:
            f.write("文書ID,文ID,基本句,格,ターゲット\n")
            for row in data:
                f.write(",".join(str(item) for item in row) + "\n")


if __name__ == "__main__":
    main()
