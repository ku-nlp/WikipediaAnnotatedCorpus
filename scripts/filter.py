import sys
from pathlib import Path

from rhoknp import Document


def filter_tags(document: Document) -> Document:
    for phrase in document.phrases:
        phrase.features.clear()
    for morpheme in document.morphemes:
        ne_feature = morpheme.features.get("NE")
        is_base_phrase_head = morpheme.features.get("基本句-主辞") is True
        morpheme.features.clear()
        if is_base_phrase_head:
            morpheme.features["基本句-主辞"] = True
        if ne_feature is not None:
            morpheme.features["NE"] = ne_feature
        morpheme.semantics.clear()
        morpheme.semantics.nil = True
    return document


def main():
    for path_str in sys.argv[1:]:
        path = Path(path_str)
        if path.exists() is False:
            print(f"{path} not found and skipped", file=sys.stderr)
            continue
        for doc_path in path.glob("**/*.knp") if path.is_dir() else [path]:
            print(f"filtering {doc_path}", file=sys.stderr)
            filtered_document = filter_tags(Document.from_knp(doc_path.read_text()))
            doc_path.write_text(filtered_document.to_knp())


if __name__ == "__main__":
    main()
